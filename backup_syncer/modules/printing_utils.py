import os

from tqdm import tqdm


def copy_file(src_fp: str, backup_fp: str):
    with tqdm(
        total=os.path.getsize(src_fp),
        unit="B",
        unit_scale=True,
        desc=f"Copying {src_fp} to {backup_fp}",
        miniters=0.1,
    ) as pbar:
        copy_file_with_progress(src_fp, backup_fp, pbar)


def copy_file_with_progress(src_fp: str, dst_fp: str, pbar: tqdm):
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


def get_dir_size(dir_path: str):
    files_size_sum = 0
    files = []
    if os.path.isdir(dir_path):
        for path, dirs, filenames in os.walk(dir_path):
            for filename in filenames:
                files_size_sum += os.path.getsize(os.path.join(path, filename))
                files.append(os.path.join(path, filename))
    return files_size_sum, files


def copy_dir(src_dp: str, backup_dp: str):
    dir_size, files = get_dir_size(src_dp)

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
