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
