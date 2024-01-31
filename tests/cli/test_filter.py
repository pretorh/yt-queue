from pathlib import Path
import json
import pytest
from yt_queue import cli
from ..mocks import data_dict

@pytest.fixture(name='file_with_some_data')
def create_info_file(tmp_path):
    file = Path(tmp_path, 'info.json')
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data_dict(), f)
    return file

def test_filter_without_args_returns_all(file_with_some_data, capsys):
    cli(f"filter {file_with_some_data}".split())
    captured = capsys.readouterr()
    assert captured.out == "idA\nidB\nidC\n"

def test_filter_status(file_with_some_data, capsys):
    cli(f"filter {file_with_some_data} --status test".split())
    captured = capsys.readouterr()
    assert captured.out == "idB\nidC\n"

def test_filter_no_status(file_with_some_data, capsys):
    cli(f"filter {file_with_some_data} --no-status".split())
    captured = capsys.readouterr()
    assert captured.out == "idA\n"

def test_filter_min_duration(file_with_some_data, capsys):
    cli(f"filter {file_with_some_data} --min-duration 60".split())
    captured = capsys.readouterr()
    assert captured.out.find("idB") == -1

def test_filter_max_duration(file_with_some_data, capsys):
    cli(f"filter {file_with_some_data} --max-duration 60".split())
    captured = capsys.readouterr()
    assert captured.out.find("idB") != -1

def test_filter_title(file_with_some_data, capsys):
    regex = '[BC]$'
    cli(f"filter {file_with_some_data} --title {regex}".split())
    captured = capsys.readouterr()
    assert captured.out == "idB\nidC\n"

def test_filter_mutex_status_no_status(file_with_some_data):
    with pytest.raises(SystemExit):
        cli(f"filter {file_with_some_data} --no-status --status test".split())

def test_filter_all(file_with_some_data, capsys):
    regex = '[BC]$'
    cli([
        "filter",
        f"{file_with_some_data}",
        "--title",          f"{regex}",
        "--min-duration",   "60",
        "--max-duration",   "1800",
        "--status",         "test",
    ])
    captured = capsys.readouterr()
    assert captured.out == "idC\n"
