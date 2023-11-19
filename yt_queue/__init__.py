import sys
from . import file
from .cli import argument_parser
from .internal import mapper, yt_dlp_wrapper
from .filters import filter_videos
from .utils.loggers import StdLogger

VERSION = '0.3.0'
_fullname = f"yt-queue {VERSION}"

# utils

def read(filename):
    return file.read(filename)

def write(filename, playlist_data):
    return file.write(filename, playlist_data)

# cli

_log = StdLogger()

def create(info, url, logger=_log):
    data = {
        'url': url,
    }
    write(info, data)
    logger.info(f'{info} created')

def refresh(info, logger=_log):
    data = read(info)
    url = data['url']
    logger.info(f'Refreshing {info} ({url})')
    yt_info = yt_dlp_wrapper.extract_info(url, yt_dlp_wrapper.ProgressLogger(logger))

    for entry in yt_info['entries']:
        mapper.map_and_merge(entry, data['videos'])

    write(info, data)

def get_no_status(info, logger=_log):
    _log.formatted_output = True
    data = read(info)

    found = filter_videos(data, { 'status': None })
    logger.info(f'Found {len(found)} videos with no status in {info}')
    for video in found:
        logger.output(video['id'])

def get_status(info, status, logger=_log):
    _log.formatted_output = True
    data = read(info)

    found = filter_videos(data, { 'status': status })
    logger.info(f'Found {len(found)} videos with status {status} in {info}')
    for video in found:
        logger.output(video['id'])

def set_status(info, video_id, new_status):
    data = read(info)

    found = [video for video in data['videos'] if video['id'] == video_id]
    for video in found:
        video['status'] = new_status
    write(info, data)

def read_field(info, video_id, field, logger=_log):
    _log.formatted_output = True
    data = read(info)

    found = [video for video in data['videos'] if video['id'] == video_id]
    if any(found) and field in found[0]:
        logger.output(found[0][field])

def cli():
    parser = argument_parser()
    args = parser.parse_args()

    if args.sub_command == 'version':
        _log.output(_fullname)
    elif args.sub_command == 'create':
        create(args.file, args.url)
    elif args.sub_command == 'refresh':
        refresh(args.file)
    elif args.sub_command == 'get-no-status':
        get_no_status(args.file)
    elif args.sub_command == 'get-status':
        get_status(args.file, args.status)
    elif args.sub_command == 'set-status':
        set_status(args.file, args.video_id, args.status)
    elif args.sub_command == 'read-field':
        read_field(args.file, args.video_id, args.field_name)
    else:
        _log.info(_fullname)
        _log.warning(f'Cli argument parsing failed {sys.argv} {args}')
        sys.exit(1)
