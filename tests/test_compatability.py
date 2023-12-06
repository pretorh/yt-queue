import pytest
import yt_queue

class TestEmptyFile:
    @pytest.fixture(name='data')
    def open_simple_file(self, tmp_path):
        file = tmp_path / 'info.json'
        with open(file, 'w', encoding='utf-8') as f:
            f.write('{ "url": "https://example.com/playlist/1" }')
        return yt_queue.file.read(file)

    def test_url_as_set(self, data):
        assert data['url'] == "https://example.com/playlist/1"
    def test_empty_videos(self, data):
        assert len(data['videos']) == 0
    def test_0_last_refresh(self, data):
        assert data['refreshed'] == 0
