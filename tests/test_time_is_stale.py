from datetime import datetime
from yt_queue.utils.time import is_stale

def test_is_stale():
    assert is_stale(0, '1hour')

def test_hours():
    now = datetime.now().timestamp()
    assert not is_stale(now, '1hour')
    assert not is_stale(now, '2hours')
    assert not is_stale(now, '100hours')
    assert not is_stale(now + 1800, '1hour')
    assert is_stale(now - 3600, '1hour')
    assert is_stale(now - 7200, '2hours')
    assert is_stale(now - 360000, '100hours')

def test_days():
    now = datetime.now().timestamp()
    assert not is_stale(now, '1day')
    assert not is_stale(now, '2days')
    assert not is_stale(now, '100days')
    assert not is_stale(now - (0.5 * 86400), '1day')
    assert is_stale(now - (1 * 86400), '1day')
    assert is_stale(now - (2 * 86400), '2days')
    assert is_stale(now - (100 * 86400), '100days')

def test_minutes():
    now = datetime.now().timestamp()
    assert not is_stale(now, '1min')
    assert not is_stale(now, '2mins')
    assert not is_stale(now, '100mins')
    assert not is_stale(now + 30, '1min')
    assert is_stale(now - 60, '1min')
    assert is_stale(now - 120, '2mins')
    assert is_stale(now - 6000, '100mins')
