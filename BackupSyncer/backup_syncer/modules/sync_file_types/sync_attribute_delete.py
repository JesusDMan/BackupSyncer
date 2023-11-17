import os
import shutil

from backup_syncer.modules.sync_file_types.sync_attribute import SyncAttribute


class SyncAttributeDelete(SyncAttribute):
    def __init__(self, backup_file_path: str):
        super().__init__(original_file_path="", backup_file_path=backup_file_path)

    def change(self):
        if self.is_canceled:
            print("Already canceled...")
            return
        self.remove()

    def action(self):
        if self.is_canceled:
            return

        if self.file_type == "directory":
            shutil.rmtree(self.backup_file_path)
        else:
            os.remove(self.backup_file_path)

    def __str__(self):
        return f"{f'Delete ({self.file_type}) ':-<{self.length_for_printing}} {self.backup_file_path}\n"
