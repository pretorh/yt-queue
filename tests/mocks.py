import yt_dlp

class MockYoutubeDL:
    def __init__(self, builder):
        self.builder = builder

    def extract_info(self, _url):
        return self.builder.extract_info

    @staticmethod
    def sanitize_info(raw):
        return raw

class MockYtDlpContextManager:
    def __init__(self, extract_info=None):
        self.extract_info = extract_info

    def __enter__(self):
        # with yt_dlp.YoutubeDL
        return MockYoutubeDL(self)

    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):
        pass

def mock_yt_dlp(monkeypatch, extract_info=None):
    def create_mock(_opts):
        return MockYtDlpContextManager(
            extract_info=extract_info,
        )

    monkeypatch.setattr(yt_dlp, "YoutubeDL", create_mock)

def response_extract_info(video_count=1):
    " returns a simplified version of playlist data for extract_info "
    video_responses=[]
    for i in range(0, video_count):
        video_responses.append(response_video_playlist_info(i))

    return {
        'id': 'PL-id1',
        'entries': video_responses,
    }

def response_video_playlist_info(vid):
    " returns a simplified response for a video in a playlist for extract_info "
    return {
        'id': f'{vid}',
        'url': f'https://example.com/video/v{vid}',
    }
