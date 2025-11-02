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
