/**
 * User-friendly error messages with actionable solutions
 */

const ERROR_MESSAGES = {
  // Ollama/Local AI errors
  OLLAMA_NOT_RUNNING: {
    title: 'Ollama Not Running',
    message: 'Cannot connect to Ollama. Is it running?',
    details: `Ollama doesn't appear to be running on your machine.

**To fix:**
1. Install Ollama from [ollama.ai](https://ollama.ai) (available for Mac, Windows, Linux)
2. Start Ollama (runs automatically on install, or run \`ollama serve\`)
3. Wait for "Listening on 127.0.0.1:11434"
4. Try sending your message again

**Alternative:** Switch to Anthropic or OpenAI in Settings if you have an API key.`,
    action: 'Open Settings',
    actionCallback: 'openSettings'
  },

  OLLAMA_NO_MODEL: {
    title: 'No Ollama Model Found',
    message: 'No models available in Ollama',
    details: `You haven't pulled any models yet.

**To fix:**
1. Open terminal
2. Run: \`ollama pull llama3.1\` (or any model)
3. Wait for download to complete
4. Refresh models in Settings

**Popular models:**
- llama3.1 (recommended)
- codellama (for coding)
- mistral (fast)`,
    action: 'Open Settings',
    actionCallback: 'openSettings'
  },

  // Anthropic errors
  ANTHROPIC_INVALID_KEY: {
    title: 'Invalid Anthropic API Key',
    message: 'Your Anthropic API key is invalid or expired',
    details: `The API key you provided doesn't work.

**To fix:**
1. Go to console.anthropic.com
2. Sign in to your account
3. Navigate to API Keys
4. Create a new key or copy existing one
5. Paste into Settings → API Key

**Note:** Keys start with "sk-ant-api03-"`,
    action: 'Open Settings',
    actionCallback: 'openSettings'
  },

  ANTHROPIC_QUOTA_EXCEEDED: {
    title: 'Anthropic Quota Exceeded',
    message: 'You\'ve exceeded your Anthropic API quota',
    details: `Your account has run out of credits or hit rate limits.

**To fix:**
1. Check your usage at console.anthropic.com
2. Add credits if needed
3. Wait if you hit rate limits (usually resets in an hour)

**Alternative:** Switch to OpenAI or Local (Ollama) in Settings`,
    action: 'Check Console',
    actionCallback: () => require('electron').shell.openExternal('https://console.anthropic.com')
  },

  // OpenAI errors
  OPENAI_INVALID_KEY: {
    title: 'Invalid OpenAI API Key',
    message: 'Your OpenAI API key is invalid or expired',
    details: `The API key you provided doesn't work.

**To fix:**
1. Go to platform.openai.com/api-keys
2. Sign in to your account
3. Create a new secret key
4. Copy it immediately (you won't see it again!)
5. Paste into Settings → API Key

**Note:** Keys start with "sk-"`,
    action: 'Open Settings',
    actionCallback: 'openSettings'
  },

  OPENAI_QUOTA_EXCEEDED: {
    title: 'OpenAI Quota Exceeded',
    message: 'You\'ve exceeded your OpenAI API quota',
    details: `Your account has run out of credits or hit rate limits.

**To fix:**
1. Check billing at platform.openai.com/account/billing
2. Add payment method if needed
3. Check usage limits

**Alternative:** Switch to Anthropic or Local (Ollama) in Settings`,
    action: 'Check Billing',
    actionCallback: () => require('electron').shell.openExternal('https://platform.openai.com/account/billing')
  },

  // Network errors
  NETWORK_ERROR: {
    title: 'Network Connection Failed',
    message: 'Cannot connect to the internet',
    details: `Flaco AI couldn't reach the API server.

**To fix:**
1. Check your internet connection
2. Try opening a website in your browser
3. Restart your router if needed
4. Check if a VPN is blocking connections
5. Try again in a few seconds

**If using Local AI:** This shouldn't happen with Ollama. Check if Ollama is running.`,
    action: 'Retry',
    actionCallback: 'retry'
  },

  // File operation errors
  FILE_READ_ERROR: {
    title: 'Cannot Read File',
    message: 'Failed to read the selected file',
    details: `The file might be:
- Corrupted
- In use by another program
- Permission protected
- Too large

**To fix:**
1. Check file permissions
2. Close other programs using it
3. Try a different file
4. Check file isn't corrupted`,
    action: 'Try Another File',
    actionCallback: 'importFile'
  },

  FILE_WRITE_ERROR: {
    title: 'Cannot Save File',
    message: 'Failed to save the file',
    details: `This could be because:
- No disk space available
- Permission denied
- Invalid file path
- Disk is read-only

**To fix:**
1. Check available disk space
2. Choose a different save location
3. Check folder permissions
4. Try a different filename`,
    action: 'Try Again',
    actionCallback: 'retry'
  },

  // Backup/restore errors
  BACKUP_FAILED: {
    title: 'Backup Failed',
    message: 'Could not create backup',
    details: `The automatic backup failed.

**This might be because:**
- No disk space
- Permission issues
- Corrupted data files

**Your data is still safe**, but automatic backups aren't working.

**To fix:**
1. Check available disk space
2. Try creating a manual backup
3. Check console logs for details`,
    action: 'Open Logs',
    actionCallback: 'openLogs'
  },

  RESTORE_FAILED: {
    title: 'Restore Failed',
    message: 'Could not restore from backup',
    details: `The backup restoration failed.

**To fix:**
1. Try a different backup
2. Check backup folder exists
3. Verify backup files aren't corrupted
4. Contact support if issue persists

**Warning:** Don't delete current data until restore succeeds!`,
    action: 'View Backups',
    actionCallback: 'viewBackups'
  },

  // Rate limiting
  RATE_LIMIT_EXCEEDED: {
    title: 'Slow Down!',
    message: 'You\'re sending messages too quickly',
    details: `You've sent 20 messages in the last minute.

**This limit prevents:**
- Accidental API spam
- Runaway costs
- Infinite loops

**To continue:**
Wait {waitTime} seconds, or switch windows and come back (resets the counter).

**Normal conversation?** You won't hit this limit.`,
    action: 'Wait',
    actionCallback: null
  },

  // Generic fallback
  UNKNOWN_ERROR: {
    title: 'Something Went Wrong',
    message: 'An unexpected error occurred',
    details: `We're not sure what happened, but here's what you can try:

**Quick fixes:**
1. Try again
2. Restart Flaco AI
3. Check logs for details
4. Report this if it keeps happening

**To prevent data loss:**
Your chats are automatically backed up daily.`,
    action: 'Open Logs',
    actionCallback: 'openLogs'
  }
};

/**
 * Parse error and return user-friendly message
 */
function parseError(error) {
  const errorString = error.message || error.toString();
  const lowerError = errorString.toLowerCase();

  // Ollama errors
  if (lowerError.includes('econnrefused') && lowerError.includes('11434')) {
    return ERROR_MESSAGES.OLLAMA_NOT_RUNNING;
  }
  if (lowerError.includes('no models') || lowerError.includes('model not found')) {
    return ERROR_MESSAGES.OLLAMA_NO_MODEL;
  }

  // Anthropic errors
  if (lowerError.includes('invalid_api_key') || (lowerError.includes('anthropic') && lowerError.includes('401'))) {
    return ERROR_MESSAGES.ANTHROPIC_INVALID_KEY;
  }
  if (lowerError.includes('quota') || lowerError.includes('429')) {
    return ERROR_MESSAGES.ANTHROPIC_QUOTA_EXCEEDED;
  }

  // OpenAI errors
  if (lowerError.includes('invalid api key') || (lowerError.includes('openai') && lowerError.includes('401'))) {
    return ERROR_MESSAGES.OPENAI_INVALID_KEY;
  }
  if (lowerError.includes('insufficient_quota') || lowerError.includes('rate_limit')) {
    return ERROR_MESSAGES.OPENAI_QUOTA_EXCEEDED;
  }

  // Network errors
  if (lowerError.includes('enotfound') || lowerError.includes('network') || lowerError.includes('timeout')) {
    return ERROR_MESSAGES.NETWORK_ERROR;
  }

  // File errors
  if (lowerError.includes('enoent') || lowerError.includes('file not found')) {
    return ERROR_MESSAGES.FILE_READ_ERROR;
  }
  if (lowerError.includes('eacces') || lowerError.includes('permission denied')) {
    return ERROR_MESSAGES.FILE_WRITE_ERROR;
  }

  // Backup errors
  if (lowerError.includes('backup') && lowerError.includes('failed')) {
    return ERROR_MESSAGES.BACKUP_FAILED;
  }
  if (lowerError.includes('restore') && lowerError.includes('failed')) {
    return ERROR_MESSAGES.RESTORE_FAILED;
  }

  // Default
  return ERROR_MESSAGES.UNKNOWN_ERROR;
}

/**
 * Format error for display
 */
function formatErrorMessage(error, context = {}) {
  const errorInfo = parseError(error);

  // Replace placeholders
  let details = errorInfo.details;
  if (context.waitTime) {
    details = details.replace('{waitTime}', context.waitTime);
  }

  return {
    title: errorInfo.title,
    message: errorInfo.message,
    details: details,
    action: errorInfo.action,
    actionCallback: errorInfo.actionCallback,
    rawError: error.message || error.toString()
  };
}

module.exports = {
  ERROR_MESSAGES,
  parseError,
  formatErrorMessage
};
