"""
This module manages automated backups of expense data before critical actions such as deletion.
"""

from datetime import datetime
import os
import shutil

class BackupManager:
 
    def __init__(self, source_filepath: str = "data/expenses.json", backups_dir: str = "backups"):
 
        self.source_filepath = source_filepath
        self.backups_dir = backups_dir
        os.makedirs(self.backups_dir, exist_ok=True)

    def create_backup(self) -> str:
 
        if not os.path.exists(self.source_filepath):
            raise FileNotFoundError(f"Source file {self.source_filepath} does not exist. Cannot create backup.")

        # Timestamp format: YYYYMMDD_HHMMSS
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"expense_backup_{timestamp}.json"
        backup_filepath = os.path.join(self.backups_dir, backup_filename)

        try:
            shutil.copy2(self.source_filepath, backup_filepath)
            return backup_filepath
        except Exception as e:
            raise IOError(f"Failed to create backup copy: {e}")
