from datetime import datetime, timedelta

def is_stale(last_refreshed, only_if_older):
    since_last_refresh = timedelta(seconds = datetime.now().timestamp() - last_refreshed)

    if only_if_older == '1hour' and since_last_refresh < timedelta(hours=1):
        return False
    return True
