const fs = require('fs').promises;
const path = require('path');
const { app } = require('electron');

class BackupManager {
  constructor() {
    this.backupDir = path.join(app.getPath('userData'), 'backups');
    this.maxBackups = 7; // Keep last 7 days
    this.initialized = false;
  }

  async initialize() {
    try {
      // Create backups directory if it doesn't exist
      await fs.mkdir(this.backupDir, { recursive: true });
      this.initialized = true;
      console.log('Backup manager initialized:', this.backupDir);
    } catch (error) {
      console.error('Failed to initialize backup manager:', error);
    }
  }

  async createBackup() {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];
      const backupName = `backup-${timestamp}`;
      const backupPath = path.join(this.backupDir, backupName);

      // Create backup directory
      await fs.mkdir(backupPath, { recursive: true });

      // Files to backup
      const userDataPath = app.getPath('userData');
      const filesToBackup = [
        'config.json',
        'chats.json',
        'agents.json',
        'conversations.json',
        'encryption.key'
      ];

      let backedUpFiles = 0;
      for (const file of filesToBackup) {
        const sourcePath = path.join(userDataPath, file);
        const destPath = path.join(backupPath, file);

        try {
          await fs.access(sourcePath);
          await fs.copyFile(sourcePath, destPath);
          backedUpFiles++;
        } catch (err) {
          // File doesn't exist, skip it
          console.log(`Skipping ${file} (doesn't exist)`);
        }
      }

      console.log(`Backup created: ${backupName} (${backedUpFiles} files)`);

      // Clean up old backups
      await this.cleanOldBackups();

      return { success: true, path: backupPath, files: backedUpFiles };
    } catch (error) {
      console.error('Backup failed:', error);
      return { success: false, error: error.message };
    }
  }

  async cleanOldBackups() {
    try {
      const backups = await fs.readdir(this.backupDir);

      // Filter to only backup directories
      const backupDirs = backups.filter(name => name.startsWith('backup-'));

      // Sort by name (which includes timestamp) descending
      backupDirs.sort().reverse();

      // Delete old backups beyond maxBackups
      if (backupDirs.length > this.maxBackups) {
        const toDelete = backupDirs.slice(this.maxBackups);

        for (const backup of toDelete) {
          const backupPath = path.join(this.backupDir, backup);
          await fs.rm(backupPath, { recursive: true, force: true });
          console.log(`Deleted old backup: ${backup}`);
        }
      }
    } catch (error) {
      console.error('Failed to clean old backups:', error);
    }
  }

  async listBackups() {
    if (!this.initialized) {
      await this.initialize();
    }

    try {
      const backups = await fs.readdir(this.backupDir);
      const backupDirs = backups.filter(name => name.startsWith('backup-'));

      const backupInfo = [];
      for (const backup of backupDirs) {
        const backupPath = path.join(this.backupDir, backup);
        const stats = await fs.stat(backupPath);

        backupInfo.push({
          name: backup,
          path: backupPath,
          created: stats.birthtime,
          size: stats.size
        });
      }

      // Sort by creation date descending
      backupInfo.sort((a, b) => b.created - a.created);

      return { success: true, backups: backupInfo };
    } catch (error) {
      console.error('Failed to list backups:', error);
      return { success: false, error: error.message };
    }
  }

  async restoreBackup(backupName) {
    try {
      const backupPath = path.join(this.backupDir, backupName);

      // Verify backup exists
      await fs.access(backupPath);

      const userDataPath = app.getPath('userData');
      const backupFiles = await fs.readdir(backupPath);

      let restoredFiles = 0;
      for (const file of backupFiles) {
        const sourcePath = path.join(backupPath, file);
        const destPath = path.join(userDataPath, file);

        await fs.copyFile(sourcePath, destPath);
        restoredFiles++;
      }

      console.log(`Restored ${restoredFiles} files from ${backupName}`);

      return {
        success: true,
        message: `Restored ${restoredFiles} files. Please restart the app.`,
        files: restoredFiles
      };
    } catch (error) {
      console.error('Restore failed:', error);
      return { success: false, error: error.message };
    }
  }

  async deleteBackup(backupName) {
    try {
      const backupPath = path.join(this.backupDir, backupName);
      await fs.rm(backupPath, { recursive: true, force: true });

      console.log(`Deleted backup: ${backupName}`);
      return { success: true };
    } catch (error) {
      console.error('Failed to delete backup:', error);
      return { success: false, error: error.message };
    }
  }

  async getBackupSize() {
    try {
      const backups = await this.listBackups();
      if (!backups.success) return 0;

      const totalSize = backups.backups.reduce((sum, b) => sum + b.size, 0);
      return totalSize;
    } catch (error) {
      return 0;
    }
  }
}

module.exports = BackupManager;
