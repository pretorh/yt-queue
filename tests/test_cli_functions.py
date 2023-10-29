from pathlib import Path
import yt_queue
from .mocks import mock_yt_dlp, response_extract_info

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
