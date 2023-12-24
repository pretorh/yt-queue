from yt_queue.utils.time import is_stale

def test_is_stale():
    assert is_stale(0, '1hour')
