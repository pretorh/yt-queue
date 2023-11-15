import yt_queue
from .mocks import data_dict

def test_filter_all_videos_when_no_filters_given():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, {})
    assert len(filtered) == 3

def test_filter_by_specific_status():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, { 'status': 'test' })
    assert len(filtered) == 2
    assert filtered[0]['id'] == 'idB'
    assert filtered[1]['id'] == 'idC'

def test_filter_by_no_status():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, { 'status': None })
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idA'
