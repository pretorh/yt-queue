import yt_queue
from .mocks import data_dict

def test_filter_by_specific_status():
    data = data_dict()

    filtered = yt_queue.filters.filter_by_status(data, 'test')
    assert len(filtered) == 2
    assert filtered[0]['id'] == 'idB'
    assert filtered[1]['id'] == 'idC'

def test_filter_by_no_status():
    data = data_dict()

    filtered = yt_queue.filters.filter_by_status(data, None)
    assert len(filtered) == 1
    assert filtered[0]['id'] == 'idA'
