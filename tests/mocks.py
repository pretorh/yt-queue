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
    """
    returns a simplified version of playlist data for extract_info
    test using:
        from yt_queue.internal.yt_dlp_wrapper import extract_info
        from pprint import pprint
        pprint({**d, 'entries': []})
    """
    video_responses=[]
    for i in range(0, video_count):
        video_responses.append(response_video_playlist_info(i))

    return {
        'id': 'PL-id1',
        'entries': video_responses,
    }

def append_to_response(response, item):
    response['entries'].append(item)

def response_video_playlist_info(vid):
    """
    returns a simplified response for a video in a playlist for extract_info
    test using:
        ...
        pprint(d['entries'][0])
    """
    return {
        'id': f'{vid}',
        'url': f'https://example.com/video/v{vid}',
        'duration': 10,
        'title': f"video {vid}",
    }

def data_dict():
    return {
        'url': 'https://example.com/playlist/1',
        'videos': [
            {
                'id': 'idA',
                'url': 'https://example.com/videos/a',
                'title': 'Video A',
                'duration': 120,
            },
            {
                'id': 'idB',
                'url': 'https://example.com/videos/b',
                'title': 'Example B',
                'status': 'test',
                'duration': 59,
            },
            {
                'id': 'idC',
                'url': 'https://example.com/videos/c',
                'title': 'Test C',
                'status': 'test',
                'duration': 1398,
            },
        ],
    }

def data_dict_append(data, i, status):
    data['videos'].append({ 'id': i, 'url': f"https://example.com/videos/{i}", 'status': status })
