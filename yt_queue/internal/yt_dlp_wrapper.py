import yt_dlp

def extract_info(url, yt_dlp_logger):
    opts = {
        'extract_flat': 'in_playlist',
        'logger': yt_dlp_logger,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        yt_info = ydl.extract_info(url)
        yt_info = ydl.sanitize_info(yt_info)
    return yt_info

class Logger:
    def __init__(self, logger):
        self.logger = logger

    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        self.logger.info(f"yt_dlp: {msg}")

    def warning(self, msg):
        self.logger.warning(f"yt_dlp warning: {msg}")

    def error(self, msg):
        self.logger.error(f"yt_dlp error: {msg}")

class ProgressLogger(Logger):
    def info(self, msg):
        if msg.startswith('[download] '):
            super().info(msg)
