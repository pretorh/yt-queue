import sys
from datetime import datetime
from . import file
from .cli import argument_parser
from .internal import mapper, yt_dlp_wrapper
from .filters import filter_videos
from .utils.loggers import StdLogger
from .utils.time import is_stale

VERSION = '0.11.2'
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

def show_info(info, logger=_log):
    data = read(info)
    logger.info(f"URL: {data['url']}")

    local_time_last_refresh = datetime.fromtimestamp(data['refreshed']).astimezone().isoformat()
    logger.output(f"Last refreshed: {local_time_last_refresh}")

    logger.output(f"{len(data['videos'])} videos")

    no_status = 0
    status_counts = {}
    for video in data['videos']:
        if 'status' in video:
            status = video['status']
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1
        else:
            no_status += 1

    logger.output(f"{len(status_counts.keys())} distinct status:")
    for status, count in status_counts.items():
        logger.output(f"{count} with {status}")
    logger.output(f"{no_status} with no status")

def refresh(info, logger=_log, only_if_older=None):
    data = read(info)
    url = data['url']

    if only_if_older is not None:
        last_refreshed = data['refreshed']
        local_time_last_refresh = datetime.fromtimestamp(last_refreshed).astimezone().isoformat()
        if not is_stale(last_refreshed, only_if_older):
            logger.info(f'{info} was refreshed at {local_time_last_refresh}, ' +
                        f'which is still within the {only_if_older} range')
            return None

    logger.info(f'Refreshing {info} ({url})')
    yt_info = yt_dlp_wrapper.extract_info(url, yt_dlp_wrapper.ProgressLogger(logger))

    for entry in yt_info['entries']:
        mapper.map_and_merge(entry, data['videos'])

    data['refreshed'] = datetime.now().timestamp()
    write(info, data)
    return data['refreshed']

def list_filtered_ids(info, options, logger=_log):
    _log.formatted_output = True
    data = read(info)

    found = filter_videos(data, options)
    logger.info(f'Found {len(found)} matching videos')
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

def _filter_options_from_arg_parse(args):
    options = {}
    if args.status:
        options['status'] = args.status
    elif args.no_status:
        options['status'] = None
    if args.max_duration:
        options['max-duration'] = args.max_duration
    if args.min_duration:
        options['min-duration'] = args.min_duration
    if args.title:
        options['title'] = args.title

    return options

def cli(argv=sys.argv[1:]):
    parser = argument_parser()
    args = parser.parse_args(argv)

    if args.sub_command == 'version':
        _log.output(_fullname)
    elif args.sub_command == 'create':
        create(args.file, args.url)
    elif args.sub_command == 'info':
        show_info(args.file)
    elif args.sub_command == 'refresh':
        refresh(args.file, only_if_older=args.only_if_older)
    elif args.sub_command == 'filter':
        list_filtered_ids(args.file, _filter_options_from_arg_parse(args))
    elif args.sub_command == 'set-status':
        set_status(args.file, args.video_id, args.status)
    elif args.sub_command == 'read-field':
        read_field(args.file, args.video_id, args.field_name)
    else:
        _log.info(_fullname)
        _log.warning(f'Cli argument parsing failed {sys.argv} {args}')
        sys.exit(1)
