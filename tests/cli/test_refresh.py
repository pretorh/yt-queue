from pathlib import Path
from datetime import datetime, timedelta
from yt_queue import cli, read
from ..mocks import mock_yt_dlp, response_extract_info

def test_refresh(tmp_path, monkeypatch):
    file = Path(tmp_path, 'info.json')
    with open(file, 'w', encoding='utf-8') as f:
        f.write('{ "url": "https://example.com/playlist/1" }')

    mock_yt_dlp(monkeypatch, extract_info=response_extract_info(video_count=3))

    cli(f"refresh {file}".split())
    data = read(file)
    assert len(data['videos']) == 3

def test_refresh_only_if_older(tmp_path, monkeypatch):
    file = Path(tmp_path, 'info.json')
    ten_minutes_ago = datetime.now().timestamp() - timedelta(minutes=10).total_seconds()

    with open(file, 'w', encoding='utf-8') as f:
        f.write('{')
        f.write('"url": "https://example.com/playlist/1",')
        f.write(f'"refreshed": {ten_minutes_ago}')
        f.write('}')

    mock_yt_dlp(monkeypatch, extract_info=response_extract_info(video_count=3))

    cli(f"refresh {file} --only-if-older 15mins".split())
    data = read(file)
    assert len(data['videos']) == 0

    cli(f"refresh {file} --only-if-older 5mins".split())
    data = read(file)
    assert len(data['videos']) == 3
