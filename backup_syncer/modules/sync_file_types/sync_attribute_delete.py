import os
import shutil

from backup_syncer.modules.sync_file_types.sync_attribute import SyncAttribute


class SyncAttributeDelete(SyncAttribute):
    def __init__(self, index: int, backup_item_path: str):
        super().__init__(
            index=index, original_item_path="", backup_item_path=backup_item_path
        )

    def change(self):
        if self.is_canceled:
            print("Already canceled...")
            return
        self.remove()

    def action(self):
        if self.is_canceled:
            return

        if self.item_type == "directory":
            shutil.rmtree(self.backup_file_path)
        else:
            os.remove(self.backup_file_path)

    def __present__(self):
        return f"{self.index} {f'Delete ({self.item_type}) ':-<{self.length_for_printing}} {self.backup_file_path}"
