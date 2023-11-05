import yt_dlp

def extract_info(url):
    opts = { 'extract_flat': 'in_playlist' }
    with yt_dlp.YoutubeDL(opts) as ydl:
        yt_info = ydl.extract_info(url)
        yt_info = ydl.sanitize_info(yt_info)
    return yt_info
