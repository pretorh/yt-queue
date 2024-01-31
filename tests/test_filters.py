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

def test_filter_title():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, { 'title': 'Video A' })
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idA'

def test_filter_title_excludes_untitled():
    data = data_dict()
    data_dict_append(data, 'idD', None)

    filtered = yt_queue.filters.filter_videos(data, { 'title': 'Video A' })
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idA'

def test_filter_title_regex():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, { 'title': '^E.*B$' })
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idB'

    filtered = yt_queue.filters.filter_videos(data, { 'title': '^[^E]' })
    assert len(filtered) == 2
    assert filtered[0]['id'] == 'idA'
    assert filtered[1]['id'] == 'idC'

def test_filter_title_simple_matches_as_regex():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, { 'title': 'A' })
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idA'
    filtered = yt_queue.filters.filter_videos(data, { 'title': 'Video' })
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idA'
    filtered = yt_queue.filters.filter_videos(data, { 'title': 'deo' })
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idA'

def test_filter_min_duration():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, { 'min-duration': 90 })
    assert len(filtered) == 2
    assert filtered[0]['id'] == 'idA'
    assert filtered[1]['id'] == 'idC'

def test_filter_max_duration():
    data = data_dict()

    filtered = yt_queue.filters.filter_videos(data, { 'max-duration': 120 })
    assert len(filtered) == 2
    assert filtered[0]['id'] == 'idA'
    assert filtered[1]['id'] == 'idB'

def test_filter_duration_excludes_missing_and_none_durations():
    data = data_dict()
    data_dict_append(data, 'idD', None)
    # no duration for idD
    data_dict_append(data, 'idE', None)
    data['videos'][-1]['duration'] = None

    filtered = yt_queue.filters.filter_videos(data, { 'min-duration': 90 })
    assert len(filtered) == 2
    filtered = yt_queue.filters.filter_videos(data, { 'max-duration': 120 })
    assert len(filtered) == 2

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
