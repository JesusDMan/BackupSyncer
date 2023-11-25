import os
import shutil

from backup_syncer.modules.utils import copy_dir, copy_file
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

        if self.item_type == "directory":
            os.mkdir(self.backup_file_path)
            copy_dir(src_dp=self.source_file_path, backup_dp=self.backup_file_path)

        else:
            copy_file(src_fp=self.source_file_path, backup_fp=self.backup_file_path)

    def __present__(self):
        return (
            f"{self.index} {f'New ({self.item_type}) ':-<{self.length_for_printing}} {self.backup_file_path}\n"
            f"{self.index} {f'From ({self.item_type}) ':-<{self.length_for_printing}} {self.source_file_path}"
        )
