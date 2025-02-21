# Import necessary modules
from pathlib import Path

from tools.editor import get_file_contents, list_directory_contents, write_content_to_file


# Test list_directory_contents
def test_list_directory_contents():
    """Test list_directory_contents function"""
    # Create a temporary directory and some files
    temp_dir = Path('temp_test_dir')
    if temp_dir.exists():
        for file in temp_dir.iterdir():
            file.unlink()
        temp_dir.rmdir()
    temp_dir.mkdir()
    (temp_dir / 'test_file1.txt').touch()
    (temp_dir / 'test_file2.txt').touch()

    # Check if the function lists the correct contents
    assert sorted(list_directory_contents(str(temp_dir))) == ['test_file1.txt', 'test_file2.txt']

    # Clean up
    for file in temp_dir.iterdir():
        file.unlink()
    temp_dir.rmdir()


# Test get_file_contents
def test_get_file_contents():
    """Test get_file_contents function"""
    # Create a temporary file with some content
    temp_file = Path('temp_test_file.txt')
    temp_file.write_text('Test content')

    # Check if the function reads the correct content
    assert get_file_contents(str(temp_file)) == 'Test content'

    # Clean up
    temp_file.unlink()


# Test write_content_to_file
def test_write_content_to_file():
    """Test write_content_to_file function"""
    # Create a temporary file
    temp_file = Path('temp_test_file.txt')

    # Write content to the file
    write_content_to_file(str(temp_file), 'Test content')

    # Check if the file contains the correct content
    assert temp_file.read_text() == 'Test content'

    # Clean up
    temp_file.unlink()
