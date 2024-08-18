import argparse

def argument_parser():
    parser = argparse.ArgumentParser(
        prog='yt-queue',
        description="Keep track of videos in Youtube playlists")

    subparsers = parser.add_subparsers(title="subcommands", dest='sub_command', required=True)

    subparsers.add_parser('version', help="Show the current version and exit")

    _add_create_sub_command(subparsers)
    _add_refresh_sub_command(subparsers)
    _add_info_sub_command(subparsers)
    _add_filter_sub_command(subparsers)
    _add_set_status_sub_command(subparsers)
    _add_read_field_sub_command(subparsers)

    return parser

def _add_create_sub_command(subparsers):
    parser_create = subparsers.add_parser('create',
        help="Create a new file to track a playlist")
    parser_create.add_argument('file')
    parser_create.add_argument('url')

def _add_refresh_sub_command(subparsers):
    parser_refresh = subparsers.add_parser('refresh',
        help="Refresh the playlist, updating the videos in the given file")
    parser_refresh.add_argument('file')
    parser_refresh.add_argument('--only-if-older', dest='only_if_older',
                                metavar='SINCE',
                                help='Skip if refreshed more recently than <x><hours|mins|days>')

def _add_info_sub_command(subparsers):
    parser_info = subparsers.add_parser('info',
        help="Show info and statistics about the file and videos")
    parser_info.add_argument('file')

def _add_filter_sub_command(subparsers):
    parser_filter = subparsers.add_parser('filter',
        help="List video ids that matches the given filter arguments")
    parser_filter.add_argument('file')

    status = parser_filter.add_mutually_exclusive_group()
    status.add_argument('--status')
    status.add_argument('--no-status', action='store_true')

    parser_filter.add_argument('--min-duration', type=int,
                        help="Return only videos with duration >= MIN_DURATION")
    parser_filter.add_argument('--max-duration', type=int,
                        help="Return only videos with duration <= MAX_DURATION")
    parser_filter.add_argument('--title',
                        help="Return only videos with a title matching the regular expression")

def _add_set_status_sub_command(subparsers):
    parser_set_statue = subparsers.add_parser('set-status',
        help="Set a video's 'status' field")
    parser_set_statue.add_argument('file')
    parser_set_statue.add_argument('video_id')
    parser_set_statue.add_argument('status')

def _add_read_field_sub_command(subparsers):
    parser_read_field = subparsers.add_parser('read-field',
        help="Read a field from a video")
    parser_read_field.add_argument('file')
    parser_read_field.add_argument('video_id')
    parser_read_field.add_argument('field_name')
