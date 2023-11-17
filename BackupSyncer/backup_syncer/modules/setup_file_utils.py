import os
import sys
from typing import List, Dict, Optional


def get_setup_dirs(setup_fp: str) -> List[Dict[str, str]]:
    setup_dirs = []
    with open(setup_fp, "r", encoding="UTF-8") as setup_f:
        dir_paths = setup_f.read().split("\n")
        for line in dir_paths:
            if validate_src_dst(line):
                line = line.split(" | ")
                setup_dirs.append({"src": line[0], "dst": line[1]})
    return setup_dirs


def print_setup(setup_dirs: List[Dict[str, str]]) -> None:
    """
    Prints the setup from the setup file
    :return: None
    """
    print(f"{'~'*40}\n" f"Setup is:")
    for line in setup_dirs:
        print(f"src: ~~~~~~~~~ {line['src']} dst: ~~~~~~~~~ {line['dst']}")


def create_setup(setup_fp: str) -> None:
    """
    Creates the setup (the user enters sources and destinations, which are being saved in the setup file)
    :return: None
    """
    if not os.path.exists(os.path.dirname(setup_fp)):
        os.mkdir(os.path.dirname(setup_fp))
    os.system(f"notepad {setup_fp}")


def creat_missing_destinations(setup_dirs: List[Dict[str, str]]):
    for line in setup_dirs:
        dst_dir_path = line["dst"]
        if not os.path.exists(dst_dir_path):
            print(f"{dst_dir_path} doesn't exists, creating...")
            os.makedirs(dst_dir_path)


def validate_src_dst(attribute: str) -> bool:
    if not attribute or attribute[0] == "#":
        return False
    if " | " not in attribute:
        print(f"Invalid: '{attribute}' doesn't contain ' | ', skipping...")
        return False
    if attribute.count(" | ") != 1:
        print(f"Invalid: '{attribute}' can't contain ' | ' more than once, skipping...")
        return False

    src_dir_path, dst_dir_path = attribute.split(" | ")

    if not os.path.exists(src_dir_path):
        print(f"{src_dir_path} doesn't exist, skipping...")
    elif not os.path.isdir(src_dir_path):
        print(f"{src_dir_path} exists but not a directory, skipping...")
    elif not os.path.isdir(dst_dir_path):
        print(f"{dst_dir_path} exists but not a directory, skipping...")
    else:
        return True
    return False


def get_setup_dirs_from_user(setup_fp: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Makes sure the setup file exists and fine with the user
    """

    if not setup_fp and (
        len(sys.argv) == 2
        and os.path.exists(sys.argv[1])
        and os.path.isfile(sys.argv[1])
    ):
        setup_fp = sys.argv[1]

    if not os.path.exists(setup_fp):
        create_setup(setup_fp)

    setup_dirs = get_setup_dirs(setup_fp)
    print_setup(setup_dirs)

    while input("Fine? ([y]/n): ") == "n":
        create_setup(setup_fp)
        setup_dirs = get_setup_dirs(setup_fp)
        print_setup(setup_dirs)

    creat_missing_destinations(setup_dirs)
    return setup_dirs
