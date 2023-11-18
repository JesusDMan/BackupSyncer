import os
from typing import List, Dict


class BackupSyncerConfig:
    note_marker = "#"
    src_and_backup_seperator = " | "

    def __init__(self, config_fp: str):
        self.config_fp = config_fp
        self.sync_config_dirs: List[Dict[str, str]] = []
        self.update_sync_config_dirs()

    def update_sync_config_dirs(self) -> None:
        """
        Update the sync_config_dirs attribute by the config file and update the config file, until the user is happy.
        :return: None
        """
        if not os.path.exists(self.config_fp):
            self.update_config_file()

        self.sync_config_dirs = self.get_sync_config_dirs_from_configuration()
        self.display()

        while input("Fine? ([y]/n): ") == "n":
            self.update_config_file()
            self.sync_config_dirs = self.get_sync_config_dirs_from_configuration()
            self.display()

        self.create_missing_backup_directories()

    def get_sync_config_dirs_from_configuration(self) -> List[Dict[str, str]]:
        """
        Get the source and backup directories from the config file.
        :return: A list of source and backup directories.
        """
        configuration = []
        with open(self.config_fp, "r", encoding="UTF-8") as config_file:
            dir_paths = config_file.read().split("\n")
            for line in dir_paths:
                if self.validate_config_file_attribute(line):
                    line = line.split(self.src_and_backup_seperator)
                    configuration.append({"src": line[0], "backup": line[1]})
        return configuration

    def update_config_file(self) -> None:
        """
        Create the config file if it doesn't exist and open it with notepad for editing.
        :return: None
        """
        if not os.path.exists(os.path.dirname(self.config_fp)):
            os.mkdir(os.path.dirname(self.config_fp))
        os.system(f"notepad {self.config_fp}")

    def create_missing_backup_directories(self):
        """
        Create backup directories that doesn't exist.
        :return:
        """
        for sync_config_attribute in self.sync_config_dirs:
            backup_dir_path = sync_config_attribute["backup"]
            if not os.path.exists(backup_dir_path):
                print(f"{backup_dir_path} doesn't exists, creating...")
                os.makedirs(backup_dir_path)

    def validate_config_file_attribute(self, attribute: str) -> bool:
        """
        Validates a config attribute.
        :param attribute: A config-file attribute.
        :return: If the attribute is valid.
        """
        return self.config_file_attribute_string_validation(
            attribute
        ) and self.config_file_attribute_src_and_backup_validation(attribute)

    def config_file_attribute_string_validation(self, attribute: str):
        """
        Validates a config-file attribute -> If this attribute is a source-backup format attribute.
        :param attribute: A line from the config file.
        :return: If the attribute's format is valid.
        """
        if not attribute or attribute[0] == self.note_marker:
            return False
        if self.src_and_backup_seperator not in attribute:
            print(
                f"Invalid: '{attribute}' doesn't contain {self.src_and_backup_seperator}, skipping..."
            )
            return False
        if attribute.count(self.src_and_backup_seperator) != 1:
            print(
                f"Invalid: '{attribute}' can't contain {self.src_and_backup_seperator} more than once, skipping..."
            )
            return False
        return True

    def config_file_attribute_src_and_backup_validation(self, attribute: str) -> bool:
        """
        Validates the source and backup directories of an attribute.
        :param attribute: A config-file attribute.
        :return: If the attribute's directories are valid (exists, etc.)
        """
        src_dir_path, backup_dir_path = attribute.split(self.src_and_backup_seperator)

        if not os.path.exists(src_dir_path):
            print(f"{src_dir_path} doesn't exist, skipping...")
        elif not os.path.isdir(src_dir_path):
            print(f"{src_dir_path} exists but not a directory, skipping...")
        elif os.path.exists(backup_dir_path) and not os.path.isdir(backup_dir_path):
            print(f"{backup_dir_path} exists but not a directory, skipping...")
        else:
            return True
        return False

    def display(self) -> None:
        print(f"{'~' * 40}\nSetup is:\n{self}")

    def __str__(self) -> str:
        string_repr = ""
        for sync_config_attribute in self.sync_config_dirs:
            string_repr += (
                f"src: ~~~~~~~~~ {sync_config_attribute['src']} "
                f"backup : ~~~~~~~~~ {sync_config_attribute['backup']}"
                f"\n"
            )
        return string_repr
