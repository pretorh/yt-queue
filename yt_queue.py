#!/usr/bin/env python
import json
import sys
import yt_dlp

print('yt-queue 0.0.0', file=sys.stderr)

# utils

def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        playlist_data = json.load(file)
    if not 'videos' in playlist_data:
        playlist_data['videos'] = []
    return playlist_data

def write(filename, playlist_data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(playlist_data, file, indent=4)

# cli

def _create():
    info = sys.argv[2]
    url = sys.argv[3]
    print(f'creating {info} for {url}')

    data = {
        'url': url,
    }
    write(info, data)

def _refresh():
    info = sys.argv[2]
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
    data = read(info)

    print(f'list videos with no status from {info}', file=sys.stderr)
    found = [video for video in data['videos'] if 'status' not in video]
    print(f'found {len(found)} videos', file=sys.stderr)
    for video in found:
        print(video['id'])

def _get_status():
    [info, status] = sys.argv[2:4]
    data = read(info)

    print(f'list videos with status {status} from {info}', file=sys.stderr)
    found = [video for video in data['videos'] if 'status' in video and video['status'] == status]
    print(f'found {len(found)} videos', file=sys.stderr)
    for video in found:
        print(video['id'])

def _set_status():
    [info, video_id, new_status] = sys.argv[2:5]
    data = read(info)

    print(f'set videos[{video_id}] to status {new_status} in {info}')

    found = [video for video in data['videos'] if video['id'] == video_id]
    for video in found:
        video['status'] = new_status
    print(f'updating {info} (found {len(found)} videos)')
    write(info, data)

def _read_field():
    [info, video_id, field] = sys.argv[2:5]
    data = read(info)
    print(f'get videos[{video_id}][{field}] from {info}', file=sys.stderr)

    found = [video for video in data['videos'] if video['id'] == video_id]
    if any(found) and field in found[0]:
        print(found[0][field])

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
