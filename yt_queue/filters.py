def filter_videos(data, filters):
    videos = data['videos']

    if 'status' in filters:
        videos = _filter_by_status(videos, filters['status'])
    if 'custom' in filters:
        videos = _filter_by_custom(videos, filters['custom'])

    return list(videos)

def _filter_by_status(videos, status):
    for video in videos:
        if 'status' in video and video['status'] == status:
            yield video
        if 'status' not in video and status is None:
            yield video

def _filter_by_custom(videos, fn):
    for video in videos:
        if fn(video):
            yield video
