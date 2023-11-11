import sys
from . import file
from .internal import mapper, yt_dlp_wrapper
from .utils.loggers import StdLogger

VERSION = '0.1.1'
_fullname = f"yt-queue {VERSION}"

# utils

def read(filename):
    return file.read(filename)

def write(filename, playlist_data):
    return file.write(filename, playlist_data)

# cli

_log = StdLogger()

def _create():
    info = sys.argv[2]
    url = sys.argv[3]
    create(info, url)

def create(info, url, logger=_log):
    data = {
        'url': url,
    }
    write(info, data)
    logger.info(f'{info} created')

def _refresh():
    info = sys.argv[2]
    refresh(info)

def refresh(info, logger=_log):
    data = read(info)
    url = data['url']
    logger.info(f'Refreshing {info} ({url})')
    yt_info = yt_dlp_wrapper.extract_info(url, yt_dlp_wrapper.ProgressLogger(logger))

    for entry in yt_info['entries']:
        mapper.map_and_merge(entry, data['videos'])

    write(info, data)

def _get_no_status():
    info = sys.argv[2]
    get_no_status(info)

def get_no_status(info, logger=_log):
    _log.formatted_output = True
    data = read(info)

    found = [video for video in data['videos'] if 'status' not in video]
    logger.info(f'Found {len(found)} videos with no status in {info}')
    for video in found:
        logger.output(video['id'])

def _get_status():
    [info, status] = sys.argv[2:4]
    get_status(info, status)

def get_status(info, status, logger=_log):
    _log.formatted_output = True
    data = read(info)

    found = [video for video in data['videos'] if 'status' in video and video['status'] == status]
    logger.info(f'Found {len(found)} videos with status {status} in {info}')
    for video in found:
        logger.output(video['id'])

def _set_status():
    [info, video_id, new_status] = sys.argv[2:5]
    set_status(info, video_id, new_status)

def set_status(info, video_id, new_status):
    data = read(info)

    found = [video for video in data['videos'] if video['id'] == video_id]
    for video in found:
        video['status'] = new_status
    write(info, data)

def _read_field():
    [info, video_id, field] = sys.argv[2:5]
    read_field(info, video_id, field)

def read_field(info, video_id, field, logger=_log):
    _log.formatted_output = True
    data = read(info)

    found = [video for video in data['videos'] if video['id'] == video_id]
    if any(found) and field in found[0]:
        logger.output(found[0][field])

def cli():
    if len(sys.argv) == 2 and sys.argv[1] == 'version':
        _log.output(_fullname)
    elif len(sys.argv) == 4 and sys.argv[1] == 'create':
        _create()
    elif len(sys.argv) == 3 and sys.argv[1] == 'refresh':
        _refresh()
    elif len(sys.argv) == 3 and sys.argv[1] == 'get-no-status':
        _get_no_status()
    elif len(sys.argv) == 4 and sys.argv[1] == 'get-status':
        _get_status()
    elif len(sys.argv) == 5 and sys.argv[1] == 'set-status':
        _set_status()
    elif len(sys.argv) == 5 and sys.argv[1] == 'read-field':
        _read_field()
    else:
        _log.info(_fullname)
        _log.warning(f'unknown cli arguments {sys.argv}')
        sys.exit(1)
