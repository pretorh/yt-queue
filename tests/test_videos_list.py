from yt_queue.internal.mapper import map_entry_to_video, map_and_merge
from .mocks import response_video_playlist_info

def test_appends_new():
    entry = response_video_playlist_info(vid='id1')
    videos = []

    map_and_merge(entry, videos)

    assert len(videos) == 1
    assert videos[0]['id'] == 'id1'

def test_does_not_append_existing():
    entry = response_video_playlist_info(vid='id1')
    videos = [{ 'id': 'id1' }]

    map_and_merge(entry, videos)

    assert len(videos) == 1

def test_does_not_overwrite_status():
    entry = response_video_playlist_info(vid='id1')
    videos = [{ 'id': 'id1', 'status': "something" }]

    map_and_merge(entry, videos)

    assert videos[0]['status'] == "something"

def test_merges_all_fields_into_existing():
    entry = response_video_playlist_info(vid='id1')
    videos = [{ 'id': 'id1' }]

    map_and_merge(entry, videos)

    assert videos == [ map_entry_to_video(entry) ]
