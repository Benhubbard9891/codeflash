/**
 * LLM Provider implementations
 */

// Mock provider for testing
const mockProvider = (apiKey) => ({
  name: 'mock',
  async call(prompt, roleId, options = {}) {
    return {
      data: {
        role: roleId,
        content: `Mock response for role ${roleId}`,
        prompt: prompt.substring(0, 50) + '...',
        novelty_score: 0.5,
        timestamp: new Date().toISOString()
      },
      metadata: {
        provider: 'mock',
        latency: Math.floor(Math.random() * 100) + 50
      }
    };
  }
});

// OpenAI provider (placeholder)
const openaiProvider = (apiKey) => ({
  name: 'openai',
  async call(prompt, roleId, options = {}) {
    if (!apiKey) {
      throw new Error('OpenAI API key required');
    }
    // In a real implementation, this would call OpenAI API
    return {
      data: {
        role: roleId,
        content: `OpenAI response for role ${roleId}`,
        prompt: prompt.substring(0, 50) + '...',
        novelty_score: 0.6,
        timestamp: new Date().toISOString()
      },
      metadata: {
        provider: 'openai',
        latency: Math.floor(Math.random() * 200) + 100
      }
    };
  }
});

// Anthropic provider (placeholder)
const anthropicProvider = (apiKey) => ({
  name: 'anthropic',
  async call(prompt, roleId, options = {}) {
    if (!apiKey) {
      throw new Error('Anthropic API key required');
    }
    // In a real implementation, this would call Anthropic API
    return {
      data: {
        role: roleId,
        content: `Anthropic response for role ${roleId}`,
        prompt: prompt.substring(0, 50) + '...',
        novelty_score: 0.7,
        timestamp: new Date().toISOString()
      },
      metadata: {
        provider: 'anthropic',
        latency: Math.floor(Math.random() * 150) + 80
      }
    };
  }
});

export const providers = {
  mock: mockProvider,
  openai: openaiProvider,
  anthropic: anthropicProvider
};
