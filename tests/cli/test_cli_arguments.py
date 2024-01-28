from pathlib import Path
import json
import pytest
from yt_queue import cli, VERSION
from ..mocks import data_dict

@pytest.fixture(name='file_with_some_data')
def create_info_file(tmp_path):
    file = Path(tmp_path, 'info.json')
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data_dict(), f)
    return file

def test_version(capsys):
    cli("version".split())
    captured = capsys.readouterr()
    assert captured.out.find(f"yt-queue {VERSION}") != -1

def test_create(tmp_path):
    info = Path(tmp_path, 'info.json')

    assert not info.exists()
    cli(f"create {info} https://example.com/playlist/1".split())
    assert info.is_file()

def test_info(file_with_some_data, capsys):
    cli(f"info {file_with_some_data}".split())

    captured = capsys.readouterr()
    # see `test_can_output_info` for more detailed output
    assert captured.out.find("1 distinct status:") != -1

def test_read_field(file_with_some_data, capsys):
    cli(f"read-field {file_with_some_data} idA url".split())
    captured = capsys.readouterr()
    assert captured.out == "https://example.com/videos/a\n"

def test_set_status(file_with_some_data, capsys):
    def assert_on_status(expected):
        cli(f"filter {file_with_some_data} --status new-status".split())
        captured = capsys.readouterr()
        if expected is None:
            assert captured.out == ""
        else:
            assert captured.out == f"{expected}\n"

    assert_on_status(expected = None)
    cli(f"set-status {file_with_some_data} idB new-status".split())
    assert_on_status("idB")
