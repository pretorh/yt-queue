from yt_queue.internal.mapper import map_entry_to_video
from .mocks import response_video_playlist_info

def test_map_id_fields():
    entry = response_video_playlist_info(vid='id1')
    video = map_entry_to_video(entry)
    assert video['id'] == 'id1'
    assert video['url'] == 'https://example.com/video/vid1'

def test_ignore_none_entries():
    entry = None
    video = map_entry_to_video(entry)
    assert video is None

def test_ignore_no_url():
    entry = response_video_playlist_info(vid='id1')
    del entry['url']
    video = map_entry_to_video(entry)
    assert video is None

def test_map_duration():
    entry = response_video_playlist_info(vid='id1')
    video = map_entry_to_video(entry)
    assert video['duration'] == 10

def test_map_title():
    entry = response_video_playlist_info(vid='id1')
    video = map_entry_to_video(entry)
    assert video['title'] == "video id1"
