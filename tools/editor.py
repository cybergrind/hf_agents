from pathlib import Path

from smolagents import tool


@tool
def list_directory_contents(directory: str) -> list[Path]:
    """List the contents of a directory.

    Args:
        directory: The directory path to list contents and files.

    Returns:
        list[Path]: A list of paths representing the contents of the directory.
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise ValueError(f'The provided path {directory} is not a directory.')
    return list(directory.iterdir())


@tool
def get_file_contents(file_path: str) -> str:
    """Get the contents of a file.

    Args:
        file_path: The path to the file.

    Returns:
        str: The contents of the file.
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        raise ValueError(f'The provided path {file_path} is not a file.')
    return file_path.read_text(encoding='utf-8')


@tool
def write_content_to_file(file_path: str, content: str) -> None:
    """Write content to a file.

    Args:
        file_path: The path to the file.
        content: The content to write to the file.
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
