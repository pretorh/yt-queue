import yt_queue
from .mocks import mock_yt_dlp, response_extract_info, append_to_response

def test_refresh_skips_none_videos(tmp_path, monkeypatch):
    file = tmp_path / 'info.json'
    with open(file, 'w', encoding='utf-8') as f:
        f.write('{ "url": "https://example.com/playlist/1" }')

    response = response_extract_info(video_count=3)
    append_to_response(response, None)
    mock_yt_dlp(monkeypatch, extract_info=response)

    yt_queue.refresh(file)
    data = yt_queue.read(file)
    assert len(data['videos']) == 3
