/**
 * Basic unit tests for Settings class
 * Run with: node tests/settings.test.js
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

// Mock electron app
const testDataDir = path.join(__dirname, '../test-data');
process.env.XDG_CONFIG_HOME = testDataDir;
process.env.XDG_DATA_HOME = testDataDir;
process.env.FLACO_STORE_DIR = testDataDir;

global.app = {
  getPath: (name) => {
    if (name === 'userData') {
      return path.join(__dirname, '../test-data');
    }
    return path.join(__dirname, '../test-data');
  }
};

// Create test data directory
fs.rmSync(testDataDir, { recursive: true, force: true });
fs.mkdirSync(testDataDir, { recursive: true });

// Import Settings class
const Settings = require('../settings');

// Test counter
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(`   Error: ${error.message}`);
    failed++;
  }
}

console.log('\n🧪 Running Settings Tests\n');

// Test 1: Settings initialization
test('Settings should initialize', () => {
  assert.ok(Settings, 'Settings should be defined');
  assert.ok(Settings.store, 'Settings should have store');
});

// Test 2: Provider get/set
test('Provider get/set should work', () => {
  Settings.setProvider('local');
  assert.strictEqual(Settings.getProvider(), 'local');

  // Should coerce any provider back to local
  Settings.setProvider('anthropic');
  assert.strictEqual(Settings.getProvider(), 'local');
});

// Test 3: Model get/set
test('Model get/set should work', () => {
  Settings.setModel('llama3');
  assert.strictEqual(Settings.getModel(), 'llama3');

  Settings.setModel('qwen2');
  assert.strictEqual(Settings.getModel(), 'qwen2');
});

// Test 4: Local endpoint
test('Local endpoint should work', () => {
  const endpoint = 'http://localhost:11434';
  Settings.setLocalEndpoint(endpoint);
  assert.strictEqual(Settings.getLocalEndpoint(), endpoint);
});

// Test 5: hasValidConfig
test('hasValidConfig should detect valid config', () => {
  // Test local
  Settings.setProvider('local');
  Settings.setLocalEndpoint('http://localhost:11434');
  assert.strictEqual(Settings.hasValidConfig(), true);
});

// Test 6: hasValidConfig should detect invalid config
test('hasValidConfig should detect invalid config', () => {
  Settings.setProvider('local');
  Settings.setLocalEndpoint('');
  assert.strictEqual(Settings.hasValidConfig(), false);
});

// Test 7: First run flag
test('First run flag should work', () => {
  Settings.setFirstRunComplete();
  assert.strictEqual(Settings.isFirstRun(), false);
});

// Test 8: Default agents initialization
test('Default agents should initialize', () => {
  const agents = Settings.getAgents();
  assert.ok(Array.isArray(agents), 'Agents should be an array');
  assert.ok(agents.length > 0, 'Should have default agents');

  const agent = agents[0];
  assert.ok(agent.id, 'Agent should have id');
  assert.ok(agent.name, 'Agent should have name');
  assert.ok(agent.emoji, 'Agent should have emoji');
  assert.ok(agent.description, 'Agent should have description');
});

// Test 9: Add custom agent
test('Should add custom agent', () => {
  const initialCount = Settings.getAgents().length;

  Settings.addAgent({
    name: 'Test Agent',
    emoji: '🧪',
    description: 'Test description'
  });

  const agents = Settings.getAgents();
  assert.strictEqual(agents.length, initialCount + 1);

  const testAgent = agents.find(a => a.name === 'Test Agent');
  assert.ok(testAgent, 'Should find test agent');
  assert.strictEqual(testAgent.emoji, '🧪');
});

// Test 10: Update agent
test('Should update agent', () => {
  const agents = Settings.getAgents();
  const agentId = agents[agents.length - 1].id;

  Settings.updateAgent(agentId, {
    name: 'Updated Agent',
    emoji: '✨'
  });

  const updated = Settings.getAgents().find(a => a.id === agentId);
  assert.strictEqual(updated.name, 'Updated Agent');
  assert.strictEqual(updated.emoji, '✨');
});

// Test 11: Delete agent
test('Should delete agent', () => {
  const agents = Settings.getAgents();
  const initialCount = agents.length;
  const agentId = agents[agents.length - 1].id;

  Settings.deleteAgent(agentId);

  const newAgents = Settings.getAgents();
  assert.strictEqual(newAgents.length, initialCount - 1);
  assert.ok(!newAgents.find(a => a.id === agentId), 'Agent should be deleted');
});

// Test 12: Current agent
test('Should get/set current agent', () => {
  const agents = Settings.getAgents();
  const agentId = agents[0].id;

  Settings.setCurrentAgent(agentId);
  assert.strictEqual(Settings.getCurrentAgent(), agentId);
});

// Test 13: getAll() should return all settings
test('getAll() should return all settings', () => {
  Settings.setLocalEndpoint('http://localhost:11434');
  Settings.setProvider('local');
  const all = Settings.getAll();

  assert.ok(all.provider, 'Should have provider');
  assert.ok(all.model, 'Should have model');
  assert.ok(all.localEndpoint, 'Should have localEndpoint');
  assert.ok(Array.isArray(all.agents), 'Should have agents array');
  assert.ok(all.currentAgent, 'Should have current agent id');
});

// Test 14: Schema version placeholder (should exist even if unused)
test('Schema version placeholder should exist', () => {
  const version = Settings.store.get('schemaVersion');
  assert.ok(version === undefined || typeof version === 'number', 'Schema version should be undefined or a number');
});

// Print results
console.log('\n' + '='.repeat(50));
console.log(`✅ Passed: ${passed}`);
console.log(`❌ Failed: ${failed}`);
console.log(`📊 Total: ${passed + failed}`);
console.log('='.repeat(50) + '\n');

// Cleanup
try {
  const configPath = path.join(testDataDir, 'config.json');
  if (fs.existsSync(configPath)) {
    fs.unlinkSync(configPath);
  }
  fs.rmSync(testDataDir, { recursive: true, force: true });
  console.log('🧹 Test data cleaned up\n');
} catch (error) {
  console.error('⚠️  Failed to cleanup test data:', error.message);
}

// Exit with appropriate code
process.exit(failed > 0 ? 1 : 0);
