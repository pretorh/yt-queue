import sys
import yt_dlp
from . import file

# utils

def read(filename):
    return file.read(filename)

def write(filename, playlist_data):
    return file.write(filename, playlist_data)

# cli

def _create():
    info = sys.argv[2]
    url = sys.argv[3]
    create(info, url)

def create(info, url):
    print(f'creating {info} for {url}')

    data = {
        'url': url,
    }
    write(info, data)

def _refresh():
    info = sys.argv[2]
    refresh(info)

def refresh(info):
    data = read(info)
    url = data['url']
    print(f'refreshing {info} ({url})')

    opts = { 'extract_flat': 'in_playlist' }
    with yt_dlp.YoutubeDL(opts) as ydl:
        yt_info = ydl.extract_info(url)
        yt_info = ydl.sanitize_info(yt_info)

    print('parsing playlist entries')
    if not 'videos' in data:
        data['videos'] = []
    for entry in yt_info['entries']:
        if entry is not None:
            existing = [x for x in data['videos'] if x['id'] == entry['id']]
            if any(existing):
                existing[0]['url'] = entry['url']
            else:
                data['videos'].append({
                    'id': entry['id'],
                    'url': entry['url'],
                })

    print(f'updating {info}')
    write(info, data)

def _get_no_status():
    info = sys.argv[2]
    get_no_status(info)

def get_no_status(info):
    data = read(info)

    print(f'list videos with no status from {info}', file=sys.stderr)
    found = [video for video in data['videos'] if 'status' not in video]
    print(f'found {len(found)} videos', file=sys.stderr)
    for video in found:
        print(video['id'])

def _get_status():
    [info, status] = sys.argv[2:4]
    get_status(info, status)

def get_status(info, status):
    data = read(info)

    print(f'list videos with status {status} from {info}', file=sys.stderr)
    found = [video for video in data['videos'] if 'status' in video and video['status'] == status]
    print(f'found {len(found)} videos', file=sys.stderr)
    for video in found:
        print(video['id'])

def _set_status():
    [info, video_id, new_status] = sys.argv[2:5]
    set_status(info, video_id, new_status)

def set_status(info, video_id, new_status):
    data = read(info)

    print(f'set videos[{video_id}] to status {new_status} in {info}')

    found = [video for video in data['videos'] if video['id'] == video_id]
    for video in found:
        video['status'] = new_status
    print(f'updating {info} (found {len(found)} videos)')
    write(info, data)

def _read_field():
    [info, video_id, field] = sys.argv[2:5]
    read_field(info, video_id, field)

def read_field(info, video_id, field):
    data = read(info)
    print(f'get videos[{video_id}][{field}] from {info}', file=sys.stderr)

    found = [video for video in data['videos'] if video['id'] == video_id]
    if any(found) and field in found[0]:
        print(found[0][field])

def cli():
    print('yt-queue 0.0.0', file=sys.stderr)

    if len(sys.argv) == 4 and sys.argv[1] == 'create':
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
    elif len(sys.argv) > 1:
        print(f'unknown cli arguments {sys.argv}', file=sys.stderr)
        sys.exit(1)
