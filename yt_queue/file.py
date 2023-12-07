import json

def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        playlist_data = json.load(file)
    if not 'refreshed' in playlist_data:
        playlist_data['refreshed'] = 0
    if not 'videos' in playlist_data:
        playlist_data['videos'] = []
    return playlist_data

def write(filename, playlist_data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(playlist_data, file, indent=4)
