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

def test_can_output_info(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.show_info(file)
    captured = capsys.readouterr()
    # the output cannot not be _fully_ parsed, but contains:
    assert "https://example.com/playlist/1" in captured.err
    assert "Last refreshed: " in captured.out
    assert "3 videos" in captured.out
    assert "1 distinct status:" in captured.out
    assert "2 with test" in captured.out
    assert "1 with no status" in captured.out

def test_can_filter_by_status(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.list_filtered_ids(file, {'status': None})
    captured = capsys.readouterr()
    assert captured.out == "idA\n"

    yt_queue.list_filtered_ids(file, {'status': "test"})
    captured = capsys.readouterr()
    assert captured.out == "idB\nidC\n"

def test_can_filter_by_title(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.list_filtered_ids(file, {'title': "^V"})
    captured = capsys.readouterr()
    assert captured.out == "idA\n"

def test_can_filter_by_duration(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.list_filtered_ids(file, {'min-duration': 120})
    captured = capsys.readouterr()
    assert captured.out == "idA\nidC\n"

def test_can_filter_nothing_filtered_by_default(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.list_filtered_ids(file, {})
    captured = capsys.readouterr()
    assert captured.out == "idA\nidB\nidC\n"

def test_can_set_status(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.set_status(file, "idB", "new-status")
    capsys.readouterr()

    yt_queue.list_filtered_ids(file, {'status': "new-status"})
    captured = capsys.readouterr()
    assert captured.out == "idB\n"
    yt_queue.list_filtered_ids(file, {'status': "test"})
    captured = capsys.readouterr()
    assert captured.out == "idC\n"

def test_can_read_field_of_video(file_with_some_data, capsys):
    file = file_with_some_data

    yt_queue.read_field(file, "idA", "url")
    captured = capsys.readouterr()
    assert captured.out == "https://example.com/videos/a\n"
