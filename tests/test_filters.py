import yt_queue
from .mocks import data_dict, data_dict_append

def custom_filter_func(video):
    return not video['id'].endswith('A') and video['id'] != 'idC'

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

def test_filter_by_custom_check():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, { 'custom': custom_filter_func })
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idB'

def test_filter_by_all_checks():
    data = data_dict()
    data_dict_append(data, 'idD', None)
    data_dict_append(data, 'idE', 'test')

    filtered = yt_queue.filters.filter_videos(data, {
      'custom': custom_filter_func, # not A, C
      'status': 'test', # B, C, E
    })
    assert len(filtered) == 2
    assert filtered[0]['id'] == 'idB'
    assert filtered[1]['id'] == 'idE'
