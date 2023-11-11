import abc
import os
import shutil

from BackupSyncer.backup_syncer.utils import attribute_type


class SyncAttribute(abc.ABC):
    length_for_printing = 40

    def __init__(self, original_file_path: str, backup_file_path: str):
        self.original_file_path = original_file_path
        self.backup_file_path = backup_file_path
        self.file_type = attribute_type(self.original_file_path)
        self.is_canceled = False

    def remove(self):
        self.original_file_path = "<Canceled>"
        self.backup_file_path = "<Canceled>"
        self.is_canceled = True

    @abc.abstractmethod
    def change(self):
        ...

    @abc.abstractmethod
    def action(self):
        ...

    @abc.abstractmethod
    def __str__(self):
        ...
