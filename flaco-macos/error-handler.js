const { app, dialog } = require('electron');
const log = require('electron-log');
const fs = require('fs').promises;
const path = require('path');

class ErrorHandler {
  constructor() {
    this.errorLogPath = path.join(app.getPath('userData'), 'error.log');
    this.setupHandlers();
  }

  setupHandlers() {
    // Main process uncaught exceptions
    process.on('uncaughtException', (error) => {
      this.handleCriticalError('Uncaught Exception', error);
    });

    // Main process unhandled promise rejections
    process.on('unhandledRejection', (reason, promise) => {
      this.handleCriticalError('Unhandled Promise Rejection', reason);
    });

    // Electron app errors
    app.on('render-process-gone', (event, webContents, details) => {
      this.handleRenderProcessGone(details);
    });

    app.on('child-process-gone', (event, details) => {
      this.handleChildProcessGone(details);
    });
  }

  async logError(type, error) {
    const timestamp = new Date().toISOString();
    const errorMessage = error.stack || error.toString();

    const logEntry = `
[${timestamp}] ${type}
${errorMessage}
${'='.repeat(80)}
`;

    try {
      await fs.appendFile(this.errorLogPath, logEntry);
      log.error(`${type}:`, errorMessage);
    } catch (err) {
      console.error('Failed to write error log:', err);
    }
  }

  handleCriticalError(type, error) {
    this.logError(type, error);

    const errorMessage = error.message || error.toString();

    // Show dialog to user
    dialog.showErrorBox(
      'Flaco AI - Critical Error',
      `${type}: ${errorMessage}\n\nThe application will attempt to recover. If the problem persists, please check the error log.`
    );

    // Don't exit - try to recover
    log.error('Critical error handled, continuing execution');
  }

  handleRenderProcessGone(details) {
    const { reason, exitCode } = details;

    this.logError('Render Process Gone', new Error(`Reason: ${reason}, Exit Code: ${exitCode}`));

    if (reason === 'crashed') {
      dialog.showErrorBox(
        'Flaco AI - Renderer Crashed',
        'The application window crashed. Please restart Flaco AI.'
      );

      // Try to reload the window
      try {
        const { BrowserWindow } = require('electron');
        const windows = BrowserWindow.getAllWindows();
        if (windows.length > 0) {
          windows[0].reload();
        }
      } catch (err) {
        log.error('Failed to reload window:', err);
      }
    }
  }

  handleChildProcessGone(details) {
    const { type, reason, exitCode, serviceName } = details;

    this.logError('Child Process Gone', new Error(
      `Type: ${type}, Service: ${serviceName || 'unknown'}, Reason: ${reason}, Exit Code: ${exitCode}`
    ));
  }

  // Renderer-safe error reporting
  static createRendererHandler() {
    return `
      window.addEventListener('error', (event) => {
        console.error('Renderer error:', event.error);
        // Could send to main process via IPC if needed
      });

      window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled promise rejection:', event.reason);
        // Could send to main process via IPC if needed
      });
    `;
  }
}

module.exports = ErrorHandler;
