# Supervisor CLI v1.2 - Policy-Enforced LLM Orchestrator

A command-line tool for orchestrating LLM (Large Language Model) calls with built-in policy enforcement.

## Installation

```bash
npm install
```

## Usage

The supervisor CLI provides three main commands:

### 1. Chain Command

Execute a linear chain of role-based LLM calls with policy enforcement.

```bash
node supervisor.js chain <sequence> <payload> [options]
```

**Arguments:**
- `sequence`: Hyphen-separated role sequence (e.g., "analyst-writer-editor")
- `payload`: JSON payload to start the chain

**Options:**
- `--provider <name>`: LLM provider (openai|anthropic|mock) [default: mock]
- `--api-key <key>`: API key for paid providers
- `--policy <policies>`: Comma-separated policy list [default: safety,schema,audit]
- `--output <file>`: Save result to file
- `--strict`: Fail on any policy violation

**Example:**

```bash
node supervisor.js chain analyst-writer '{"topic":"AI safety"}' --policy safety,novelty,audit
```

### 2. DAG Command

Execute a Directed Acyclic Graph (DAG) workflow.

```bash
node supervisor.js dag <def> <payload> [options]
```

**Arguments:**
- `def`: JSON graph definition with nodes and edges
- `payload`: JSON payload for the workflow

**Options:**
- `--provider <name>`: LLM provider [default: mock]
- `--policy <policies>`: Comma-separated policy list [default: safety,schema,audit]

**Example:**

```bash
node supervisor.js dag '{"nodes":{"n1":{"role":"analyst"},"n2":{"role":"writer"}},"edges":[{"from":"n1","to":"n2"}]}' '{"idea":"testing"}'
```

### 3. Audit Command

View audit log statistics.

```bash
node supervisor.js audit
```

## Policy Enforcement

The supervisor enforces the following policies:

### Available Policies

1. **safety**: Detects dangerous, illegal, or violating content in outputs
2. **schema**: Validates output against JSON schemas (requires role registry configuration)
3. **length**: Ensures output size is under 50,000 characters
4. **novelty**: Checks that novelty score is above 0.3
5. **audit**: Logs all executions to `supervisor-audit.jsonl`

### Default Policies

By default, the following policies are active: `safety`, `schema`, `audit`

## Architecture

### Components

1. **supervisor.js**: Main CLI tool with command handling and policy enforcement
2. **js/orchestrator.js**: Core orchestration engine
   - `executeChain()`: Sequential role execution
   - `executeParallel()`: Parallel role execution
   - `compileGraph()`: DAG compilation and execution
   - `registerProvider()`: Provider registration
3. **js/providers.js**: LLM provider implementations
   - Mock provider (for testing)
   - OpenAI provider (placeholder)
   - Anthropic provider (placeholder)

### Audit Logging

All executions are logged to `supervisor-audit.jsonl` in JSON Lines format with:
- Timestamp
- Trace of role executions
- Applied policies

## Examples

### Basic Chain

```bash
node supervisor.js chain analyst-writer '{"topic":"climate change"}' --provider mock
```

### Chain with Output File

```bash
node supervisor.js chain analyst-reviewer-editor '{"task":"code review"}' --output result.json
```

### Strict Mode

```bash
node supervisor.js chain researcher-writer '{"query":"AI safety"}' --strict --policy safety,novelty
```

### Complex DAG

```bash
node supervisor.js dag '{
  "nodes": {
    "research": {"role": "researcher"},
    "analyze": {"role": "analyst"},
    "write": {"role": "writer"}
  },
  "edges": [
    {"from": "research", "to": "analyze"},
    {"from": "analyze", "to": "write"}
  ]
}' '{"topic":"machine learning"}'
```

## License

MIT
