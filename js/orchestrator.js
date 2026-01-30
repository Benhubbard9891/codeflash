/**
 * LLM Orchestrator - Chain and DAG execution engine
 */

const providerRegistry = new Map();

/**
 * Register a provider for use in orchestration
 */
export function registerProvider(name, provider) {
  providerRegistry.set(name, provider);
}

/**
 * Execute a linear chain of roles
 */
export async function executeChain(roles, initialPayload, options = {}) {
  const providerName = options.provider || 'default';
  const provider = providerRegistry.get(providerName);
  
  if (!provider) {
    throw new Error(`Provider not registered: ${providerName}`);
  }

  const trace = [];
  let currentPayload = initialPayload;

  for (const role of roles) {
    const prompt = JSON.stringify(currentPayload);
    const startTime = Date.now();
    
    try {
      const result = await provider.call(prompt, role, options);
      const duration = Date.now() - startTime;
      
      trace.push({
        role,
        success: true,
        result,
        duration,
        timestamp: new Date().toISOString()
      });
      
      // Chain output becomes next input
      currentPayload = result.data;
    } catch (error) {
      trace.push({
        role,
        success: false,
        error: error.message,
        duration: Date.now() - startTime,
        timestamp: new Date().toISOString()
      });
      
      throw new Error(`Chain failed at role ${role}: ${error.message}`);
    }
  }

  return {
    success: true,
    finalOutput: currentPayload,
    trace
  };
}

/**
 * Execute multiple roles in parallel
 */
export async function executeParallel(roles, payload, options = {}) {
  const providerName = options.provider || 'default';
  const provider = providerRegistry.get(providerName);
  
  if (!provider) {
    throw new Error(`Provider not registered: ${providerName}`);
  }

  const prompt = JSON.stringify(payload);
  const results = await Promise.allSettled(
    roles.map(async (role) => {
      const startTime = Date.now();
      const result = await provider.call(prompt, role, options);
      return {
        role,
        success: true,
        result,
        duration: Date.now() - startTime,
        timestamp: new Date().toISOString()
      };
    })
  );

  const trace = results.map((r, i) => {
    if (r.status === 'fulfilled') {
      return r.value;
    } else {
      return {
        role: roles[i],
        success: false,
        error: r.reason.message,
        timestamp: new Date().toISOString()
      };
    }
  });

  return {
    success: trace.every(t => t.success),
    outputs: trace.map(t => t.result?.data),
    trace
  };
}

/**
 * Compile a DAG graph definition into an executable graph
 */
export function compileGraph(definition) {
  const nodes = definition.nodes || {};
  const edges = definition.edges || [];

  return {
    definition,
    async execute(initialPayload, options = {}) {
      const providerName = options.provider || 'default';
      const provider = providerRegistry.get(providerName);
      
      if (!provider) {
        throw new Error(`Provider not registered: ${providerName}`);
      }

      const trace = [];
      const nodeOutputs = new Map();
      const visited = new Set();

      // Topological sort to determine execution order
      const executionOrder = topologicalSort(nodes, edges);

      for (const nodeId of executionOrder) {
        const node = nodes[nodeId];
        if (!node) continue;

        // Gather inputs from dependencies
        const inputs = edges
          .filter(e => e.to === nodeId)
          .map(e => nodeOutputs.get(e.from))
          .filter(Boolean);

        const payload = inputs.length > 0 ? inputs[inputs.length - 1] : initialPayload;
        const prompt = JSON.stringify(payload);
        const startTime = Date.now();

        try {
          const result = await provider.call(prompt, node.role, options);
          const duration = Date.now() - startTime;

          trace.push({
            role: node.role,
            nodeId,
            success: true,
            result,
            duration,
            timestamp: new Date().toISOString()
          });

          nodeOutputs.set(nodeId, result.data);
          visited.add(nodeId);
        } catch (error) {
          trace.push({
            role: node.role,
            nodeId,
            success: false,
            error: error.message,
            duration: Date.now() - startTime,
            timestamp: new Date().toISOString()
          });

          throw new Error(`DAG execution failed at node ${nodeId}: ${error.message}`);
        }
      }

      // Find output nodes (nodes with no outgoing edges)
      const outputNodes = Object.keys(nodes).filter(
        nodeId => !edges.some(e => e.from === nodeId)
      );
      
      const finalOutputs = outputNodes.map(nodeId => nodeOutputs.get(nodeId));

      return {
        success: true,
        outputs: finalOutputs,
        trace
      };
    }
  };
}

/**
 * Topological sort for DAG execution order
 */
function topologicalSort(nodes, edges) {
  const nodeIds = Object.keys(nodes);
  const inDegree = new Map(nodeIds.map(id => [id, 0]));
  const adjList = new Map(nodeIds.map(id => [id, []]));

  // Build adjacency list and calculate in-degrees
  for (const edge of edges) {
    adjList.get(edge.from).push(edge.to);
    inDegree.set(edge.to, (inDegree.get(edge.to) || 0) + 1);
  }

  // Find nodes with no dependencies
  const queue = nodeIds.filter(id => inDegree.get(id) === 0);
  const result = [];

  while (queue.length > 0) {
    const current = queue.shift();
    result.push(current);

    for (const neighbor of adjList.get(current) || []) {
      inDegree.set(neighbor, inDegree.get(neighbor) - 1);
      if (inDegree.get(neighbor) === 0) {
        queue.push(neighbor);
      }
    }
  }

  // Check for cycles
  if (result.length !== nodeIds.length) {
    throw new Error('DAG contains cycles');
  }

  return result;
}
