def filter_by_status(data, status):
    return list(_filter_by_status(data['videos'], status))

def _filter_by_status(videos, status):
    for video in videos:
        if 'status' in video and video['status'] == status:
            yield video
        if 'status' not in video and status is None:
            yield video
