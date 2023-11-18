import os
import shutil

from backup_syncer.modules.printing_utils import copy_file

from backup_syncer.modules.sync_file_types.sync_attribute import SyncAttribute


class SyncAttributeReplace(SyncAttribute):
    def change(self):
        if self.is_canceled:
            print("Already canceled...")

        elif input("Do you want to avoid replacing? (y/[n]): ") == "y":
            self.remove()

        elif input("Do you want to replace the other way? (y/[n]): ") == "y":
            new_source = self.backup_file_path
            self.backup_file_path = self.source_file_path
            self.source_file_path = new_source

    def action(self):
        if self.is_canceled:
            return

        os.remove(self.backup_file_path)
        copy_file(src_fp=self.source_file_path, backup_fp=self.backup_file_path)

    def __present__(self):
        return (
            f"{self.index} {f'Replace ({self.item_type}) ':-<{self.length_for_printing}} {self.backup_file_path}\n"
            f"{self.index} {f'With ({self.item_type}) ':-<{self.length_for_printing}} {self.source_file_path}"
        )
