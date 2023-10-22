#!/usr/bin/env python
import json
import sys

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
