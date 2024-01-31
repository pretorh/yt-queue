import math
import re

def filter_videos(data, filters):
    videos = data['videos']

    if 'status' in filters:
        videos = _filter_by_status(videos, filters['status'])
    if 'title' in filters:
        videos = _filter_by_title(videos, filters['title'])
    if 'min-duration' in filters:
        videos = _filter_by_duration(videos, filters['min-duration'], math.inf)
    if 'max-duration' in filters:
        videos = _filter_by_duration(videos, 0, filters['max-duration'])
    if 'custom' in filters:
        videos = _filter_by_custom(videos, filters['custom'])

    return list(videos)

def _filter_by_status(videos, status):
    for video in videos:
        if 'status' in video and video['status'] == status:
            yield video
        if 'status' not in video and status is None:
            yield video

def _filter_by_title(videos, title_pattern):
    title_re = re.compile(title_pattern)

    for video in videos:
        if 'title' in video and title_re.search(video['title']):
            yield video

def _filter_by_duration(videos, min_duration, max_duration):
    for video in videos:
        if 'duration' in video and video['duration'] is not None:
            if video['duration'] >= min_duration and video['duration'] <= max_duration:
                yield video

def _filter_by_custom(videos, fn):
    for video in videos:
        if fn(video):
            yield video
