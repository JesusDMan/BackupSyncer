import os
from datetime import datetime

from backup_syncer.modules.sync_file_types.sync_attribute_replace import (
    SyncAttributeReplace,
)


class SyncAttributeOutdated(SyncAttributeReplace):
    def __init__(self, index: int, original_item_path: str, backup_item_path: str):
        super().__init__(
            index=index,
            original_item_path=original_item_path,
            backup_item_path=backup_item_path,
        )
        self.replace_anyway = False

    def change(self):
        if self.replace_anyway:
            super().change()

        elif self.is_canceled:
            print("Ineffective anyway...")

        elif input("Do you want to replace anyway? (y/[n]): ") == "y":
            self.replace_anyway = True

        elif input("Do you want to replace the other way? (y/[n]): ") == "y":
            self.replace_anyway = True
            new_source = self.backup_file_path
            self.backup_file_path = self.source_file_path
            self.source_file_path = new_source

    def action(self):
        if self.replace_anyway:
            super().action()

    def __present__(self):
        if self.replace_anyway:
            return super().__present__()
        else:
            return (
                f"{self.index} {f'Older ({self.item_type}) ':-<{self.length_for_printing}} {self.source_file_path} "
                f"({datetime.utcfromtimestamp(os.stat(self.source_file_path).st_mtime)})\n"
                f"{self.index} {f'Newer ({self.item_type}) ':-<{self.length_for_printing}} {self.backup_file_path}"
                f" ({datetime.utcfromtimestamp(os.stat(self.backup_file_path).st_mtime)})"
            )
