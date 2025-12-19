# Settings Migration System

This guide explains how to safely evolve Flaco AI's settings schema without breaking existing installations.

## Why Migrations?

As Flaco AI evolves, you'll need to change the settings schema:
- Rename fields for better clarity
- Add new required fields
- Change data structures
- Remove deprecated settings
- Transform data formats

Without migrations, users would:
- Lose their settings on updates
- Experience crashes from missing fields
- Need to manually reconfigure everything

**Migrations solve this** by automatically transforming old settings to match the new schema.

---

## How It Works

### Schema Version Tracking

`settings.js` tracks the current schema version:

```javascript
const CURRENT_SCHEMA_VERSION = 1; // Increment when adding migrations

const schema = {
  schemaVersion: {
    type: 'number',
    default: CURRENT_SCHEMA_VERSION
  },
  // ... other fields
};
```

### Migration Array

Migrations are defined in the `MIGRATIONS` array:

```javascript
const MIGRATIONS = [
  {
    version: 2,
    migrate: (store) => {
      // Transform settings from v1 to v2
    }
  },
  {
    version: 3,
    migrate: (store) => {
      // Transform settings from v2 to v3
    }
  }
];
```

### Automatic Execution

On app startup, `runMigrations()` automatically:
1. Checks current settings version
2. Applies any pending migrations in order
3. Updates version to latest
4. Logs all migrations for debugging

---

## Adding a Migration

### Step 1: Increment Schema Version

In `settings.js`:

```javascript
const CURRENT_SCHEMA_VERSION = 2; // Was 1, now 2
```

### Step 2: Add Migration to Array

```javascript
const MIGRATIONS = [
  {
    version: 2,
    migrate: (store) => {
      // Your migration code here
    }
  }
];
```

### Step 3: Update Schema

Add/modify the schema definition:

```javascript
const schema = {
  schemaVersion: {
    type: 'number',
    default: CURRENT_SCHEMA_VERSION
  },
  // Add new field or modify existing
  newField: {
    type: 'string',
    default: 'default-value'
  }
};
```

### Step 4: Test Migration

1. Install previous version
2. Configure settings
3. Update to new version
4. Verify settings migrated correctly
5. Check console logs for migration messages

---

## Migration Examples

### Example 1: Rename a Field

**Scenario:** Rename `selectedModel` to `currentModel`

```javascript
{
  version: 2,
  migrate: (store) => {
    const oldValue = store.get('selectedModel');
    if (oldValue !== undefined) {
      store.set('currentModel', oldValue);
      store.delete('selectedModel');
    }
  }
}
```

**Then update schema:**

```javascript
const schema = {
  // Remove selectedModel
  currentModel: {  // New name
    type: 'string',
    default: 'claude-sonnet-4'
  }
};
```

### Example 2: Add Required Field with Default

**Scenario:** Add `theme` field (light/dark mode)

```javascript
{
  version: 2,
  migrate: (store) => {
    // Set default theme for existing users
    if (store.get('theme') === undefined) {
      store.set('theme', 'dark');
    }
  }
}
```

**Then update schema:**

```javascript
const schema = {
  theme: {
    type: 'string',
    enum: ['light', 'dark'],
    default: 'dark'
  }
};
```

### Example 3: Transform Data Structure

**Scenario:** Convert API keys from individual fields to an object

**Before:**
```javascript
{
  anthropicApiKey: 'sk-ant-...',
  openaiApiKey: 'sk-...'
}
```

**After:**
```javascript
{
  apiKeys: {
    anthropic: 'sk-ant-...',
    openai: 'sk-...'
  }
}
```

**Migration:**
```javascript
{
  version: 2,
  migrate: (store) => {
    const anthropicKey = store.get('anthropicApiKey', '');
    const openaiKey = store.get('openaiApiKey', '');

    store.set('apiKeys', {
      anthropic: anthropicKey,
      openai: openaiKey
    });

    store.delete('anthropicApiKey');
    store.delete('openaiApiKey');
  }
}
```

**Update schema:**
```javascript
const schema = {
  apiKeys: {
    type: 'object',
    default: {
      anthropic: '',
      openai: ''
    }
  }
};
```

**Update getters/setters:**
```javascript
getAnthropicKey() {
  return this.store.get('apiKeys.anthropic', '');
}

setAnthropicKey(key) {
  const keys = this.store.get('apiKeys', {});
  keys.anthropic = key;
  this.store.set('apiKeys', keys);
}
```

### Example 4: Remove Deprecated Field

**Scenario:** Remove unused `firstRun` field

```javascript
{
  version: 2,
  migrate: (store) => {
    // No data transformation needed, just cleanup
    store.delete('firstRun');
  }
}
```

**Then remove from schema:**
```javascript
const schema = {
  // firstRun removed
};
```

### Example 5: Add Field Based on Existing Data

**Scenario:** Add `modelProvider` based on current `selectedModel`

```javascript
{
  version: 2,
  migrate: (store) => {
    const model = store.get('selectedModel', '');
    let provider = 'anthropic'; // default

    if (model.includes('gpt')) {
      provider = 'openai';
    } else if (model.includes('llama')) {
      provider = 'local';
    }

    store.set('modelProvider', provider);
  }
}
```

### Example 6: Migrate Array Structure

**Scenario:** Add `type` field to all agents

```javascript
{
  version: 2,
  migrate: (store) => {
    const agents = store.get('customAgents', []);

    const migratedAgents = agents.map(agent => ({
      ...agent,
      type: 'custom' // Add default type
    }));

    store.set('customAgents', migratedAgents);
  }
}
```

---

## Best Practices

### 1. Always Check for Existing Values

```javascript
// Good
const value = store.get('oldField');
if (value !== undefined) {
  store.set('newField', value);
}

// Bad (might overwrite with undefined)
store.set('newField', store.get('oldField'));
```

### 2. Provide Safe Defaults

```javascript
// Good
const agents = store.get('customAgents', []);
agents.forEach(agent => {
  agent.priority = agent.priority || 0;
});
store.set('customAgents', agents);
```

### 3. Test Edge Cases

- Fresh install (no existing settings)
- Partial settings (some fields missing)
- Corrupted settings
- Very old versions (multiple migrations to apply)

### 4. Log Everything

```javascript
migrate: (store) => {
  console.log('[Migration v2] Starting...');
  const oldValue = store.get('oldField');
  console.log('[Migration v2] Old value:', oldValue);

  store.set('newField', transformedValue);
  console.log('[Migration v2] New value:', transformedValue);

  console.log('[Migration v2] Complete');
}
```

### 5. Handle Errors Gracefully

```javascript
migrate: (store) => {
  try {
    // Migration logic
  } catch (error) {
    console.error('[Migration v2] Failed:', error);
    // Provide fallback or throw with helpful message
    throw new Error(`Migration v2 failed: ${error.message}`);
  }
}
```

### 6. Never Skip Versions

```javascript
// Good - Sequential versions
const MIGRATIONS = [
  { version: 2, migrate: ... },
  { version: 3, migrate: ... },
  { version: 4, migrate: ... }
];

// Bad - Skipped version 3
const MIGRATIONS = [
  { version: 2, migrate: ... },
  { version: 4, migrate: ... }  // Where's version 3?
];
```

### 7. Document Breaking Changes

```javascript
{
  version: 2,
  // Breaking change: selectedModel renamed to currentModel
  // Reason: Better naming consistency across codebase
  // Impact: All instances of getModel() now use 'currentModel' key
  migrate: (store) => {
    const oldValue = store.get('selectedModel');
    store.set('currentModel', oldValue);
    store.delete('selectedModel');
  }
}
```

---

## Testing Migrations

### Manual Testing

1. **Test Fresh Install:**
   ```bash
   rm -rf ~/Library/Application\ Support/flaco-desktop/
   npm start
   ```
   - Should create settings with latest version
   - No migrations should run

2. **Test Migration from Previous Version:**
   - Install old version
   - Configure settings
   - Close app
   - Update to new version
   - Open app
   - Check console for migration logs
   - Verify settings intact

3. **Test Multiple Version Jumps:**
   - Install v1
   - Configure settings
   - Update directly to v4 (skipping v2, v3)
   - Verify all migrations run in order

### Automated Testing

Create test in `settings.test.js`:

```javascript
const Settings = require('./settings');

describe('Settings Migrations', () => {
  it('should migrate from v1 to v2', () => {
    // Mock store with v1 data
    const mockStore = {
      get: jest.fn(),
      set: jest.fn(),
      delete: jest.fn()
    };

    mockStore.get.mockReturnValueOnce(1); // schemaVersion

    // Run migration
    const settings = new Settings();
    settings.runMigrations();

    // Verify transformations
    expect(mockStore.set).toHaveBeenCalledWith('newField', expectedValue);
  });
});
```

---

## Troubleshooting

### Migration Fails on Startup

**Symptom:** App crashes with "Settings migration failed"

**Fix:**
1. Check console logs for specific error
2. Verify migration logic handles all edge cases
3. Add try-catch with better error messages

### Settings Lost After Update

**Symptom:** Users report blank settings after update

**Cause:** Migration deleted data without preserving it

**Fix:**
1. Always read before delete:
   ```javascript
   const value = store.get('oldField');
   store.set('newField', value);
   store.delete('oldField'); // Only delete after copy
   ```

### Incorrect Migration Order

**Symptom:** Settings partially migrated or corrupted

**Cause:** Migrations not applied in order

**Fix:** Ensure `MIGRATIONS` array is sorted by version:
```javascript
MIGRATIONS.sort((a, b) => a.version - b.version);
```

---

## Version History

### v1 (Current)

**Schema:**
- `aiProvider`: string (anthropic/openai/local)
- `anthropicApiKey`: string
- `openaiApiKey`: string
- `selectedModel`: string
- `firstRun`: boolean
- `localModelEndpoint`: string
- `customAgents`: array
- `currentAgent`: string

**No migrations yet** - this is the baseline version.

---

## Future Migration Ideas

When implementing these features, add migrations:

1. **Add theme support:**
   - Add `theme` field (light/dark/auto)
   - Default to 'dark' for existing users

2. **Restructure API keys:**
   - Move to `apiKeys` object
   - Add support for multiple keys per provider

3. **Add user preferences:**
   - `autoSave`: boolean
   - `showToolCalls`: boolean
   - `maxTokens`: number

4. **Agent enhancements:**
   - Add `agent.type` (built-in vs custom)
   - Add `agent.tags` array for categorization

5. **Conversation settings:**
   - `maxHistoryLength`: number
   - `contextWindow`: number

---

## Key Takeaways

1. **Always increment `CURRENT_SCHEMA_VERSION`** when adding migrations
2. **Test migrations thoroughly** before releasing
3. **Never modify old migrations** once released
4. **Provide safe defaults** for all new fields
5. **Log everything** for debugging
6. **Handle errors gracefully** to prevent data loss

---

**Remember:** Migrations are critical for production apps. Take time to get them right!
