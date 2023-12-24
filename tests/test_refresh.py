import pytest
import yt_queue
from .mocks import mock_yt_dlp, response_extract_info, append_to_response

@pytest.fixture(name='path_to_created_file')
def create_simple_file(tmp_path):
    file = tmp_path / 'info.json'
    with open(file, 'w', encoding='utf-8') as f:
        f.write('{ "url": "https://example.com/playlist/1" }')
    return file

def test_refresh_skips_none_videos(path_to_created_file, monkeypatch):
    file = path_to_created_file

    response = response_extract_info(video_count=3)
    append_to_response(response, None)
    mock_yt_dlp(monkeypatch, extract_info=response)

    yt_queue.refresh(file)
    data = yt_queue.read(file)
    assert len(data['videos']) == 3

def test_saves_timestamp(path_to_created_file, monkeypatch):
    file = path_to_created_file

    mock_yt_dlp(monkeypatch, extract_info=response_extract_info())

    yt_queue.refresh(file)
    data = yt_queue.read(file)
    assert data['refreshed'] > 0

def test_only_if_stale(path_to_created_file, monkeypatch):
    # when recently refreshed
    file = path_to_created_file
    mock_yt_dlp(monkeypatch, extract_info=response_extract_info())
    yt_queue.refresh(file)
    data = yt_queue.read(file)
    original_refreshed_timestamp = data['refreshed']

    # and refreshing again
    refresh_result = yt_queue.refresh(file, only_if_older='1hour')
    assert refresh_result is None
    data = yt_queue.read(file)
    assert data['refreshed'] == original_refreshed_timestamp
