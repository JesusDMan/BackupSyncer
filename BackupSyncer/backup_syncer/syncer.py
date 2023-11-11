# Sync folders
import os
from typing import List, Callable, Any, Dict

from BackupSyncer.backup_syncer import setup_file_utils
from BackupSyncer.backup_syncer.sync_file_types import (
    sync_attribute_create,
    sync_attribute_delete,
    sync_attribute_replace,
    sync_attribute_outdated,
)
from BackupSyncer.backup_syncer.utils import check_if_identical


class Syncer:
    CHANGE_MENU = (
        "Changing menu:\n"
        "-> n for new\n"
        "-> d for delete\n"
        "-> r for replace\n"
        "-> o for outdated source\n"
        "-> m for menu\n"
        "-> c for cancel\n"
        "For example, 'r 1' - replace 1."
    )

    length_for_printing = 40

    display_header_seperator: Callable[[Any], None] = lambda self: print("=" * 107)
    display_seperator: Callable[[Any], None] = lambda self: print("~" * 40)

    def __init__(self, setup_fp: str):
        self.setup_directories: List[
            Dict[str, str]
        ] = setup_file_utils.get_setup_dirs_from_user(setup_fp)

        self.files_to_create: List[sync_attribute_create.SyncAttributeCreate] = []
        # Files that are on the source but not on the destination
        self.files_to_delete: List[sync_attribute_delete.SyncAttributeDelete] = []
        # Files that are on the destination but not on the source, and the source is newer
        self.files_to_replace: List[sync_attribute_replace.SyncAttributeReplace] = []
        # Files that are not updated in the destination, and will be recreated from the source
        self.outdated_files: List[sync_attribute_outdated.SyncAttributeOutdated] = []
        # Files that are newer on the destination than on the source, and won't be replaced

        self.printing_titles = {
            "Going to be created:": self.files_to_create,
            "Going to be updated:": self.files_to_replace,
            "Going to be deleted:": self.files_to_delete,
            "Outdated source (the destination is newer, won't be replaced):": self.outdated_files,
        }

    def print_sync(self) -> None:
        self.display_header_seperator()
        for title, files_list in self.printing_titles.items():
            if files_list:
                print(title)
                for i, item in enumerate(files_list):
                    print(f"{i}\n{item}")
                self.display_seperator()

    # ======================================================================================================================
    # SIDE FUNCTIONS:

    def search_trash(self, src_dp, dst_dp) -> None:
        """
        Searches for file which are in the destination but not on the source, and adds them to the self.will_be_deleted list.
        :param src_dp: Source directory path
        :param dst_dp: Destination directory path
        :return: None
        """
        src_dir = os.listdir(src_dp)
        dst_dir = os.listdir(dst_dp)
        for something in dst_dir:
            if something not in src_dir:
                item_to_delete = sync_attribute_delete.SyncAttributeDelete(
                    backup_file_path=os.path.join(dst_dp, something)
                )
                self.files_to_delete.append(item_to_delete)

    def make_change_in_action(self) -> None:
        """
         Gives the user an opportunity to change something before anything is done.
        :return: None
        """
        options = {
            "n": self.files_to_create,
            "d": self.files_to_delete,
            "r": self.files_to_replace,
            "o": self.outdated_files,
            "m": lambda *args: print(self.CHANGE_MENU),
        }
        change = (
            self.files_to_create
            or self.files_to_delete
            or self.files_to_replace
            or self.outdated_files
        ) and input("Do you want to change something? ([y]/n): ") != "n"
        if not change:
            return
        print(self.CHANGE_MENU)
        while change is not False:
            change = input(
                "Enter n/d/r/o/m/c (number) according to what you want to change: "
            )
            if change == "m":
                print(self.CHANGE_MENU)
                continue
            if change == "c":
                return
            try:
                action_char, attribute_index = change.split(" ")
                attribute_index = int(attribute_index)
                options[action_char][attribute_index].change()
                print("worked?")
                self.print_sync()
            except Exception as e:
                print(f"'{change}' isn't a valid request.")
            else:
                change = input("Do you want to change something else? ([y]/n): ") != "n"

    def sync_file(self, src_fp: str, src_fn: str, dst_dp: str) -> None:
        """
        Adding file to "self.will_be_replaced", "self.will_be_deleted" or "self.will_be_created"
        :param src_fp: Source file path
        :param src_fn: Source file name
        :param dst_dp: Destination directory path
        :return: None
        """
        dst_dir = os.listdir(dst_dp)
        dst_fn = src_fn
        if src_fn in dst_dir:
            dst_fp = os.path.join(dst_dp, dst_fn)
            if not check_if_identical(src_fp, dst_fp):
                if os.stat(dst_fp).st_mtime > os.stat(src_fp).st_mtime:
                    outdated_item = sync_attribute_outdated.SyncAttributeOutdated(
                        original_file_path=src_fp, backup_file_path=dst_fp
                    )
                    self.outdated_files.append(outdated_item)
                else:
                    to_replace_item = sync_attribute_replace.SyncAttributeReplace(
                        original_file_path=src_fp, backup_file_path=dst_fp
                    )
                    self.files_to_replace.append(to_replace_item)
        else:
            to_create_item = sync_attribute_create.SyncAttributeCreate(
                original_file_path=src_fp, backup_file_path=os.path.join(dst_dp, src_fn)
            )
            self.files_to_create.append(to_create_item)

    # ======================================================================================================================
    # MAIN SHIT:

    def sync_directory(self, src_dp: str, dst_dp: str) -> None:
        """
        Goes over every file in the destination tree, creates it if it doesn't exist and syncs it if in does.
        :param src_dp: source directory path
        :param dst_dp: destination directory path
        :return: None
        """

        self.search_trash(src_dp, dst_dp)

        dst_directories = os.listdir(dst_dp)
        for src_dir in os.listdir(src_dp):
            if os.path.isdir(os.path.join(src_dp, src_dir)):
                if (
                    src_dir not in dst_directories
                ):  # If the directory isn't in the dst_dir
                    to_create_item = sync_attribute_create.SyncAttributeCreate(
                        original_file_path=os.path.join(src_dp, src_dir),
                        backup_file_path=os.path.join(dst_dp, src_dir),
                    )
                    self.files_to_create.append(to_create_item)

                else:
                    sub_src_dir = os.path.join(src_dp, src_dir)
                    sub_dst_dir = os.path.join(dst_dp, src_dir)
                    self.sync_directory(sub_src_dir, sub_dst_dir)
            else:
                src_fp = os.path.join(src_dp, src_dir)
                self.sync_file(src_fp, src_dir, dst_dp)

    def finale_sync(self) -> None:
        """
        Deleting/replacing files according to the global "trash", "replace" and "newer_in_dst" lists
        :return: None
        """

        for item in (
            self.files_to_create
            + self.files_to_replace
            + self.files_to_delete
            + self.outdated_files
        ):
            if not item.is_canceled:
                print(item)
                item.action()

    def use_setup(self) -> None:
        """
        Syncing directories according to the sync setup file (located in the setup_fp path)
        :return: None
        """
        for line in self.setup_directories:
            self.sync_directory(src_dp=line["src"], dst_dp=line["dst"])
