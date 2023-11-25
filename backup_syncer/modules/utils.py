import filecmp
import os
from typing import Tuple, List

from tqdm import tqdm


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


def copy_file(src_fp: str, backup_fp: str) -> None:
    with tqdm(
        total=os.path.getsize(src_fp),
        unit="B",
        unit_scale=True,
        desc=f"Copying {src_fp} to {backup_fp}",
        miniters=0.1,
    ) as pbar:
        copy_file_with_progress(src_fp, backup_fp, pbar)


def copy_file_with_progress(src_fp: str, dst_fp: str, pbar: tqdm) -> None:
    chunk_size = 4096
    source_f = open(src_fp, "rb")
    backup_f = open(dst_fp, "wb", buffering=chunk_size * 1000)

    while True:
        chunk = source_f.read(chunk_size)
        if not chunk:
            break
        backup_f.write(chunk)
        pbar.update(len(chunk))

    source_f.close()
    backup_f.close()


def get_files_count(dir_path: str) -> int:
    number_of_files = 0
    if os.path.isdir(dir_path):
        for path, dirs, filenames in os.walk(dir_path):
            number_of_files += len(filenames)
    return number_of_files


def get_dir_size_and_files(dir_path: str) -> Tuple[int, List[str]]:
    files_size_sum = 0
    files = []
    if os.path.isdir(dir_path):
        for path, dirs, filenames in os.walk(dir_path):
            for filename in filenames:
                files_size_sum += os.path.getsize(os.path.join(path, filename))
                files.append(os.path.join(path, filename))
    return files_size_sum, files


def copy_dir(src_dp: str, backup_dp: str) -> None:
    dir_size, files = get_dir_size_and_files(src_dp)

    with tqdm(
        total=dir_size,
        unit="B",
        unit_scale=True,
        desc=f"Copying {src_dp} to {backup_dp}",
        miniters=0.1,
    ) as pbar:
        for file in files:
            dir_name = os.path.dirname(file)
            backup_dir_name = dir_name.replace(src_dp, backup_dp)
            if not os.path.exists(backup_dir_name):
                os.makedirs(backup_dir_name)
            backup_file_path = file.replace(src_dp, backup_dp)

            copy_file_with_progress(file, backup_file_path, pbar)
