from pathlib import Path
import json
import pytest
import yt_queue
from .mocks import mock_yt_dlp, response_extract_info, data_dict

@pytest.fixture(name='file_with_some_data')
def create_info_file(tmp_path):
    file = tmp_path / 'info.json'
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data_dict(), f)
    return file

def test_can_create(tmp_path):
    info = Path(tmp_path, 'info.json')

    assert not info.exists()
    yt_queue.create(info, 'https://example.com/playlist/1')
    assert info.is_file()

def test_can_refresh(tmp_path, monkeypatch):
    file = tmp_path / 'info.json'
    with open(file, 'w', encoding='utf-8') as f:
        f.write('{ "url": "https://example.com/playlist/1" }')

    mock_yt_dlp(monkeypatch, extract_info=response_extract_info(video_count=3))

    yt_queue.refresh(file)
    data = yt_queue.read(file)
    assert len(data['videos']) == 3

def test_can_filter_by_status(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.get_no_status(file)
    captured = capsys.readouterr()
    assert captured.out == "idA\n"

    yt_queue.get_status(file, "test")
    captured = capsys.readouterr()
    assert captured.out == "idB\nidC\n"

def test_can_set_status(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.set_status(file, "idB", "new-status")
    capsys.readouterr()

    yt_queue.get_status(file, "new-status")
    captured = capsys.readouterr()
    assert captured.out == "idB\n"
    yt_queue.get_status(file, "test")
    captured = capsys.readouterr()
    assert captured.out == "idC\n"

def test_can_read_field_of_video(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.read_field(file, "idA", "url")
    captured = capsys.readouterr()
    assert captured.out == "https://example.com/videos/a\n"
