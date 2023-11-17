import os
import shutil

from backup_syncer.modules.sync_file_types.sync_attribute import SyncAttribute


class SyncAttributeReplace(SyncAttribute):
    def change(self):
        if self.is_canceled:
            print("Already canceled...")

        elif input("Do you want to avoid replacing? (y/[n]): ") == "y":
            self.remove()

        elif input("Do you want to replace the other way? (y/[n]): ") == "y":
            new_source = self.backup_file_path
            self.backup_file_path = self.original_file_path
            self.original_file_path = new_source

    def action(self):
        if self.is_canceled:
            return

        os.remove(self.backup_file_path)
        shutil.copy(src=self.original_file_path, dst=self.backup_file_path)

    def __str__(self):
        return (
            f"{f'Replace ({self.file_type}) ':-<{self.length_for_printing}} {self.backup_file_path}\n"
            f"{f'With ({self.file_type}) ':-<{self.length_for_printing}} {self.original_file_path}\n"
        )
