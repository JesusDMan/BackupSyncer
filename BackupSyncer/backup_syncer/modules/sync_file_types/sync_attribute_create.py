import os
import shutil

from backup_syncer.modules.sync_file_types.sync_attribute import SyncAttribute


class SyncAttributeCreate(SyncAttribute):
    def change(self):
        if self.is_canceled:
            print("Already canceled...")
            return
        self.remove()

    def action(self):
        if self.is_canceled:
            return

        if self.file_type == "directory":
            os.mkdir(self.backup_file_path)
            shutil.copytree(
                self.original_file_path, self.backup_file_path, dirs_exist_ok=True
            )

        else:
            shutil.copy(self.original_file_path, self.backup_file_path)

    def __str__(self):
        return (
            f"{f'New ({self.file_type}) ':-<{self.length_for_printing}} {self.backup_file_path}\n"
            f"{f'From ({self.file_type}) ':-<{self.length_for_printing}} {self.original_file_path}\n"
        )
