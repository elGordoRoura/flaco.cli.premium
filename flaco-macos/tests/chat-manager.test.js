/**
 * Basic unit tests for ChatManager class
 * Run with: node tests/chat-manager.test.js
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const testDataDir = path.join(__dirname, '../test-data');

process.env.FLACO_STORE_DIR = testDataDir;
process.env.XDG_CONFIG_HOME = testDataDir;
process.env.XDG_DATA_HOME = testDataDir;

fs.rmSync(testDataDir, { recursive: true, force: true });
fs.mkdirSync(testDataDir, { recursive: true });

// Reset cached settings to ensure fresh base path per test run
delete require.cache[require.resolve('../settings')];

const ChatManager = require('../chat-manager');

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

console.log('\n🧪 Running ChatManager Tests\n');

// Create test instance
const chatManager = new ChatManager();

// Test 1: ChatManager initialization
test('ChatManager should initialize', () => {
  assert.ok(chatManager, 'ChatManager should be defined');
  const chats = chatManager.getAllChats();
  assert.ok(Array.isArray(chats), 'Should have chats array');
});

// Test 2: Create new chat
test('Should create new chat', () => {
  const chat = chatManager.createChat('Test Chat');

  assert.ok(chat, 'Should return chat object');
  assert.ok(chat.id, 'Chat should have id');
  assert.strictEqual(chat.name, 'Test Chat');
  assert.ok(Array.isArray(chat.messages), 'Chat should have messages array');
  assert.ok(chat.createdAt, 'Chat should have createdAt');
  assert.ok(chat.updatedAt, 'Chat should have updatedAt');
});

// Test 3: Get all chats
test('Should get all chats', () => {
  const chats = chatManager.getAllChats();

  assert.ok(Array.isArray(chats), 'Should return array');
  assert.ok(chats.length > 0, 'Should have at least one chat');
});

// Test 4: Get chat by ID
test('Should get chat by ID', () => {
  const chats = chatManager.getAllChats();
  const chatId = chats[0].id;

  const chat = chats.find(c => c.id === chatId);

  assert.ok(chat, 'Should return chat');
  assert.strictEqual(chat.id, chatId);
});

// Test 5: Rename chat
test('Should rename chat', () => {
  const chats = chatManager.getAllChats();
  const chatId = chats[0].id;

  const renamed = chatManager.renameChat(chatId, 'Renamed Chat');

  assert.ok(renamed, 'Should return renamed chat');
  assert.strictEqual(renamed.name, 'Renamed Chat');

  const updatedChats = chatManager.getAllChats();
  const chat = updatedChats.find(c => c.id === chatId);
  assert.strictEqual(chat.name, 'Renamed Chat');
});

// Test 6: Toggle star
test('Should toggle star on chat', () => {
  const chats = chatManager.getAllChats();
  const chatId = chats[0].id;

  // Ensure clean state
  chatManager.store.set('chats', chats.map(c => c.id === chatId ? { ...c, starred: false } : c));

  // Star it (undefined becomes true)
  let starred = chatManager.toggleStar(chatId);
  assert.strictEqual(starred.starred, true, 'First toggle should star');

  // Unstar it
  starred = chatManager.toggleStar(chatId);
  assert.strictEqual(starred.starred, false, 'Second toggle should unstar');

  // Star it again
  starred = chatManager.toggleStar(chatId);
  assert.strictEqual(starred.starred, true, 'Third toggle should star again');
});

// Test 7: Add message to chat
test('Should add message to chat', () => {
  const chats = chatManager.getAllChats();
  const chatId = chats[0].id;

  const message = chatManager.addMessage('user', 'Hello!', chatId);

  assert.ok(message, 'Should return message');
  assert.ok(message.id, 'Message should have id');
  assert.strictEqual(message.role, 'user');
  assert.strictEqual(message.content, 'Hello!');
  assert.ok(message.timestamp, 'Message should have timestamp');
});

// Test 8: Get messages from chat
test('Should get messages from chat', () => {
  const chats = chatManager.getAllChats();
  const chatId = chats[0].id;

  const messages = chatManager.getMessages(chatId);

  assert.ok(Array.isArray(messages), 'Should return array');
  assert.ok(messages.length > 0, 'Should have at least one message');

  const msg = messages[0];
  assert.ok(msg.id, 'Message should have id');
  assert.ok(msg.role, 'Message should have role');
  assert.ok(msg.content, 'Message should have content');
});

// Test 9: Add assistant response
test('Should add assistant response', () => {
  const chats = chatManager.getAllChats();
  const chatId = chats[0].id;

  const message = chatManager.addMessage('assistant', 'Hi there!', chatId);

  assert.strictEqual(message.role, 'assistant');
  assert.strictEqual(message.content, 'Hi there!');

  const messages = chatManager.getMessages(chatId);
  assert.ok(messages.length >= 2, 'Should have multiple messages');
});

// Test 10: Clear messages
test('Should clear messages from chat', () => {
  const chats = chatManager.getAllChats();
  const chatId = chats[0].id;

  const success = chatManager.clearMessages(chatId);

  assert.strictEqual(success, true);

  const messages = chatManager.getMessages(chatId);
  assert.strictEqual(messages.length, 0, 'Should have no messages');
});

// Test 11: Delete chat
test('Should delete chat', () => {
  const chats = chatManager.getAllChats();
  const initialCount = chats.length;
  const chatId = chats[0].id;

  const result = chatManager.deleteChat(chatId);

  assert.ok(result.success, 'Should return success');

  const newChats = chatManager.getAllChats();
  assert.strictEqual(newChats.length, initialCount - 1);

  const deletedChat = newChats.find(c => c.id === chatId);
  assert.strictEqual(deletedChat, undefined, 'Chat should be deleted');
});

// Test 12: Create multiple chats
test('Should create multiple chats', () => {
  const chat1 = chatManager.createChat('Chat 1');
  const chat2 = chatManager.createChat('Chat 2');
  const chat3 = chatManager.createChat('Chat 3');

  assert.ok(chat1.id !== chat2.id, 'Chats should have unique IDs');
  assert.ok(chat2.id !== chat3.id, 'Chats should have unique IDs');

  const chats = chatManager.getAllChats();
  assert.ok(chats.length >= 3, 'Should have at least 3 chats');
});

// Test 13: Get starred chats
test('Should filter starred chats', () => {
  const chats = chatManager.getAllChats();

  // Reset starred state
  chatManager.store.set('chats', chats.map(c => ({ ...c, starred: false })));
  const refreshed = chatManager.getAllChats();

  // Star two more chats (use different chats from test 6)
  if (refreshed.length >= 3) {
    chatManager.toggleStar(refreshed[1].id);
    chatManager.toggleStar(refreshed[2].id);

    const starred = chatManager.getAllChats().filter(c => c.starred);
    assert.ok(starred.length >= 2, 'Should have more starred chats');
  }
});

// Print results
console.log('\n' + '='.repeat(50));
console.log(`✅ Passed: ${passed}`);
console.log(`❌ Failed: ${failed}`);
console.log(`📊 Total: ${passed + failed}`);
console.log('='.repeat(50) + '\n');

// Exit with appropriate code
process.exit(failed > 0 ? 1 : 0);
