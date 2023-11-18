import filecmp
import os

from backup_syncer.modules.backup_syncer_config import BackupSyncerConfig


def check_if_identical(fp1: str, fp2: str) -> bool:
    """
    Checks if two files are identical or not.
    :param fp1: First file path
    :param fp2: Second file path
    :return: True if they are identical, False if not
    """
    if fp1 == fp2:
        return True
    type_f1 = os.path.splitext(fp1)[-1].lower()
    type_f2 = os.path.splitext(fp2)[-1].lower()

    if type_f1 != type_f2:
        return False
    return filecmp.cmp(fp1, fp2)


def get_item_type(item_path: str) -> str:
    if os.path.isdir(item_path):
        return "directory"
    else:
        return "file"
