# Import necessary modules
from pathlib import Path
from typing import List, Union

# Tool to list directory contents
def list_directory_contents(directory: str) -> List[str]:
    """Tool that lists the contents of a directory.
    Args:
        directory (str): The path to the directory to list contents.
    Returns:
        List[str]: A list of file and directory names in the specified directory.
    """
    path = Path(directory)
    if not path.exists():
        raise ValueError(f"Directory {directory} does not exist.")
    return [str(item.name) for item in path.iterdir()]

# Tool to get file contents
def get_file_contents(file_path: str) -> str:
    """Tool that gets the contents of a file.
    Args:
        file_path (str): The path to the file.
    Returns:
        str: The contents of the file.
    """
    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"File {file_path} does not exist.")
    return path.read_text()

# Tool to write content to a file
def write_content_to_file(file_path: str, content: str) -> None:
    """Tool that writes content to a file.
    Args:
        file_path (str): The path to the file.
        content (str): The content to write to the file.
    """
    path = Path(file_path)
    path.write_text(content)
