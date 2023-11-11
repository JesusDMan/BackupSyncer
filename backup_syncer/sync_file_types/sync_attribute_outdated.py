from BackupSyncer.file_syncer.sync_file_types.sync_attribute_replace import (
    SyncAttributeReplace,
)


class SyncAttributeOutdated(SyncAttributeReplace):
    def __init__(self, original_file_path: str, backup_file_path: str):
        super().__init__(original_file_path, backup_file_path)
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
            self.backup_file_path = self.original_file_path
            self.original_file_path = new_source

    def action(self):
        if self.replace_anyway:
            super().action()

    def __str__(self):
        if self.replace_anyway:
            return super().__str__()
        else:
            return (
                f"{f'Older ({self.file_type}) ':-<{self.length_for_printing}} {self.backup_file_path}\n"
                f"{f'Newer ({self.file_type}) ':-<{self.length_for_printing}} {self.original_file_path}\n"
            )
