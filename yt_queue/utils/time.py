from datetime import datetime, timedelta
import re

def is_stale(last_refreshed, only_if_older):
    since_last_refresh = timedelta(seconds = datetime.now().timestamp() - last_refreshed)

    def get_timedelta():
        match = re.compile(r'(\d+)(min|hour|day)s?').match(only_if_older)
        if match:
            if match.group(2) == 'min':
                return timedelta(minutes=int(match.group(1)))
            if match.group(2) == 'hour':
                return timedelta(hours=int(match.group(1)))
            if match.group(2) == 'day':
                return timedelta(days=int(match.group(1)))
        return None

    delta = get_timedelta()
    if since_last_refresh < delta:
        return False

    return True
