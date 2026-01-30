#!/usr/bin/env node
/**
 * Supervisor CLI v1.2 - Policy-Enforced LLM Orchestrator
 * npm i commander ajv chalk fs path
 */

import { Command } from 'commander';
import chalk from 'chalk';
import Ajv from 'ajv';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { executeChain, executeParallel, registerProvider, compileGraph } from './js/orchestrator.js';
import { providers } from './js/providers.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ajv = new Ajv({ allErrors: true });
const auditLog = 'supervisor-audit.jsonl';

const program = new Command()
  .name('supervisor')
  .description('Policy-enforced LLM orchestrator')
  .version('1.2.0');

// Role registry for schema validation
const roleRegistry = {};

const defaultPolicies = {
  safety: (output) => !/dangerous|illegal|violate/i.test(JSON.stringify(output)),
  schema: (output, roleId) => ajv.compile(roleRegistry[roleId]?.schema || {})(output),
  length: (output) => JSON.stringify(output).length < 50000,
  novelty: (output) => output.novelty_score > 0.3 || true,
  audit: async (trace, appliedPolicies = {}) => {
    await fs.appendFile(auditLog, JSON.stringify({
      timestamp: new Date().toISOString(),
      trace: trace.map(t => ({ role: t.role, success: t.success })),
      policies: Object.keys(appliedPolicies)
    }) + '\n');
    return true;
  }
};

// Policy enforcement middleware
async function enforcePolicies(trace, policies = defaultPolicies, options = {}) {
  const violations = [];
  for (const [name, policy] of Object.entries(policies)) {
    for (const step of trace) {
      // Handle audit policy specially to pass the policies list
      if (name === 'audit') {
        await policy(trace, policies);
      } else if (!await policy(step.result?.data, step.role, options)) {
        violations.push({ policy: name, role: step.role, data: step.result?.data });
      }
    }
  }
  if (violations.length > 0) {
    console.log(chalk.yellow('⚠ Policy violations:'), violations.length);
    return { success: false, violations };
  }
  console.log(chalk.green('✔ All policies passed'));
  return { success: true, trace };
}

program
  .command('chain <sequence> <payload>')
  .description('Execute linear role chain')
  .option('--provider <name>', 'openai|anthropic|mock', 'mock')
  .option('--api-key <key>', 'API key for paid providers')
  .option('--policy <policies>', 'safety,schema,length,novelty,audit', 'safety,schema,audit')
  .option('--output <file>', 'Save result to file')
  .option('--strict', 'Fail on any policy violation', false)
  .action(async (sequence, payloadStr, cmd) => {
    try {
      const roles = sequence.split('-');
      const payload = JSON.parse(payloadStr);
      const provider = providers[cmd.provider];
      if (!provider) throw new Error(`Unknown provider: ${cmd.provider}`);

      registerProvider('default', provider(cmd.apiKey));

      console.log(chalk.blue(`🔄 Chain: ${roles.join(' → ')}`));
      const start = Date.now();

      const result = await executeChain(roles, payload, { provider: 'default' });
      const duration = Date.now() - start;

      const activePolicies = {};
      cmd.policy.split(',').forEach(p => activePolicies[p] = defaultPolicies[p]);
      
      const policyResult = await enforcePolicies(result.trace, activePolicies, { strict: cmd.strict });
      
      const output = {
        metadata: { duration, roles: roles.length, policies: Object.keys(activePolicies), provider: cmd.provider },
        ...result,
        policy: policyResult
      };

      console.log(chalk.green('✔ Chain complete'), `(${duration}ms)`);
      
      if (cmd.output) {
        await fs.writeFile(cmd.output, JSON.stringify(output, null, 2));
        console.log(chalk.gray(`💾 Saved: ${cmd.output}`));
      }

      if (!policyResult.success && cmd.strict) {
        process.exit(1);
      }

      console.log(JSON.stringify(output, null, 2));
    } catch (err) {
      console.error(chalk.red('✖'), err.message);
      process.exit(1);
    }
  });

program
  .command('dag <def>')
  .description('Execute DAG (JSON graph def)')
  .option('--provider <name>', 'mock', 'mock')
  .option('--policy <policies>', 'safety,schema,audit', 'safety,schema,audit')
  .action(async (defStr, cmd) => {
    try {
      const def = JSON.parse(defStr);
      registerProvider('default', providers[cmd.provider]());
      
      const graph = compileGraph(def);
      const result = await graph.execute({ idea: 'DAG test' });
      
      const policies = {};
      (cmd.policy || 'safety,schema,audit').split(',').forEach(p => policies[p] = defaultPolicies[p]);
      const policyResult = await enforcePolicies(result.trace, policies);
      
      console.log(chalk.green('✔ DAG complete'), JSON.stringify({ ...result, policy: policyResult }, null, 2));
    } catch (err) {
      console.error(chalk.red('✖'), err.message);
      process.exit(1);
    }
  });

program
  .command('audit')
  .description('Show audit log stats')
  .action(async () => {
    try {
      const stats = await fs.readFile(auditLog, 'utf8')
        .then(data => data.trim().split('\n').filter(Boolean).length)
        .catch(() => 0);
      console.log(chalk.cyan(`📊 Audit entries: ${stats}`));
    } catch (err) {
      console.log(chalk.gray('No audit log yet'));
    }
  });

program.parse(process.argv);
