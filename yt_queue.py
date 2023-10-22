#!/usr/bin/env python
import json
import sys
import yt_dlp

print('yt-queue 0.0.0')

if len(sys.argv) == 4 and sys.argv[1] == 'create':
    INFO = sys.argv[2]
    URL = sys.argv[3]
    print(f'creating {INFO} for {URL}')

    data = {
        'url': URL,
    }
    with open(INFO, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
elif len(sys.argv) == 3 and sys.argv[1] == 'refresh':
    INFO = sys.argv[2]
    with open(INFO, 'r', encoding='utf-8') as f:
        data = json.load(f)
        url = data['url']
    print(f'refreshing {INFO} ({url})')

    opts = { 'extract_flat': 'in_playlist' }
    with yt_dlp.YoutubeDL(opts) as ydl:
        yt_info = ydl.extract_info(url)
        yt_info = ydl.sanitize_info(yt_info)

    print('parsing playlist entries')
    if not 'videos' in data:
        data['videos'] = []
    for entry in yt_info['entries']:
        if entry is not None:
            exists = any(x for x in data['videos'] if x['id'] == entry['id'])
            if not exists:
                data['videos'].append({
                    'id': entry['id'],
                })

    print(f'updating {INFO}')
    with open(INFO, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
elif len(sys.argv) == 3 and sys.argv[1] == 'get-no-status':
    INFO = sys.argv[2]
    with open(INFO, 'r', encoding='utf-8') as f:
        data = json.load(f)
        url = data['url']
    if not 'videos' in data:
        data['videos'] = []
    print(f'list videos with no status from {INFO}')
    found = [video for video in data['videos'] if 'status' not in video]
    print(f'found {len(found)} videos')
    for video in found:
        print(video['id'])
elif len(sys.argv) == 4 and sys.argv[1] == 'get-status':
    [INFO, STATUS] = sys.argv[2:4]
    with open(INFO, 'r', encoding='utf-8') as f:
        data = json.load(f)
        url = data['url']
    if not 'videos' in data:
        data['videos'] = []
    print(f'list videos with status {STATUS} from {INFO}')
    found = [video for video in data['videos'] if 'status' in video and video['status'] == STATUS]
    print(f'found {len(found)} videos')
    for video in found:
        print(video['id'])
elif len(sys.argv) == 5 and sys.argv[1] == 'set-status':
    [INFO, VIDEO_ID, NEW_STATUS] = sys.argv[2:5]
    with open(INFO, 'r', encoding='utf-8') as f:
        data = json.load(f)
        url = data['url']
    if not 'videos' in data:
        data['videos'] = []
    print(f'set videos[{VIDEO_ID}] to status {NEW_STATUS} in {INFO}')

    found = [video for video in data['videos'] if video['id'] == VIDEO_ID]
    for video in found:
        video['status'] = NEW_STATUS
    print(f'updating {INFO} (found {len(found)} videos)')
    with open(INFO, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

elif len(sys.argv) > 1:
    print(f'unknown cli arguments {sys.argv}')
    sys.exit(1)
