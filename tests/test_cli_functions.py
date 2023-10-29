from pathlib import Path
import yt_queue

def test_can_create(tmp_path):
    info = Path(tmp_path, 'info.json')

    assert not info.exists()
    yt_queue.create(info, 'https://example.com/playlist/1')
    assert info.is_file()
