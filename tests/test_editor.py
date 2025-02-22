import pathlib

import pytest

from tools.editor import get_file_contents, list_directory_contents, write_content_to_file


@pytest.fixture()
def test_directory(tmp_path: pathlib.Path) -> pathlib.Path:
    test_dir = tmp_path / 'test_dir'
    test_dir.mkdir()
    (test_dir / 'file1.txt').write_text('This is file 1')
    (test_dir / 'file2.txt').write_text('This is file 2')

    typeshed = test_dir / 'typeshed'
    typeshed.mkdir()
    (typeshed / 'file3.txt').write_text('This is file 3')

    return test_dir


def test_list_directory_contents(test_directory: pathlib.Path) -> None:
    contents = list_directory_contents(str(test_directory))
    expected_contents = ['file1.txt', 'file2.txt', 'typeshed']
    assert sorted(contents) == sorted(expected_contents)


def test_list_directory_contents_empty_directory(tmp_path: pathlib.Path) -> None:
    empty_dir = tmp_path / 'empty_dir'
    empty_dir.mkdir()
    contents = list_directory_contents(str(empty_dir))
    assert contents == []


def test_get_file_contents(test_directory: pathlib.Path) -> None:
    file_path = test_directory / 'file1.txt'
    content = get_file_contents(str(file_path))
    assert content == 'This is file 1'


def test_get_file_contents_nonexistent_file(test_directory: pathlib.Path) -> None:
    file_path = test_directory / 'nonexistent_file.txt'
    with pytest.raises(FileNotFoundError):
        get_file_contents(str(file_path))


def test_write_content_to_file(test_directory: pathlib.Path) -> None:
    new_file_path = test_directory / 'new_file.txt'
    write_content_to_file(str(new_file_path), 'This is a new file')
    content = get_file_contents(str(new_file_path))
    assert content == 'This is a new file'


def test_write_content_to_file_existing_file(test_directory: pathlib.Path) -> None:
    file_path = test_directory / 'file1.txt'
    write_content_to_file(str(file_path), 'Overwritten content')
    content = get_file_contents(str(file_path))
    assert content == 'Overwritten content'


def test_write_content_to_file_nonexistent_directory(tmp_path: pathlib.Path) -> None:
    nonexistent_dir = tmp_path / 'nonexistent_dir'
    file_path = nonexistent_dir / 'new_file.txt'
    with pytest.raises(FileNotFoundError):
        write_content_to_file(str(file_path), 'This is a new file')
