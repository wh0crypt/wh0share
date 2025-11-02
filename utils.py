import os
import sys
from typing import Tuple


def check_env(env_vars: Tuple[str]) -> None:
    """
    Checks if the specified environment variables are set.

    This function takes a tuple of environment variable names and checks
    if each one is set (not None). If any variable is not set, it prints
    an error message and terminates the program with an exit code of 1.

    Args:
        env_vars (Tuple[str]): A tuple of environment variable names to check.
    """

    error = False

    for env_var in env_vars:
        if env_var is None:
            print(f"{env_var} not set in .env file")
            error = True

    if error:
        sys.exit(1)


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Checks if the uploaded file is allowed based on its extension.

    Args:
        filename (str): The name of the uploaded file.
        allowed_extensions (set): A set of allowed file extensions.

    Returns:
        bool: True if the file is allowed, False otherwise.
    """

    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def get_folder_size(folder: str) -> int:
    """
    Get the total size of all files in a folder.

    Args:
        folder (str): The path to the folder.

    Returns:
        int: The total size of all files in bytes.
    """

    total = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)

    return total


def check_available_storage(
    upload_folder: str, max_storage_bytes: int
) -> Tuple[bool, int]:
    """
    Check if there is enough available storage for the upload folder.

    Args:
        upload_folder (str): The path to the upload folder.
        max_storage_bytes (int): The maximum allowed storage in bytes.

    Returns:
        Tuple[bool, int]: A tuple containing a boolean indicating if there is enough storage
        and the amount of free disk space available.
    """

    stat = os.statvfs(upload_folder)
    disk_free_bytes = stat.f_bavail * stat.f_frsize
    security_margin_bytes = 10240**3
    available_bytes = max(disk_free_bytes - security_margin_bytes, 0)

    return available_bytes >= max_storage_bytes, available_bytes
