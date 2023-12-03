def map_entry_to_video(entry):
    if entry is None:
        return None
    if 'url' not in entry:
        return None

    return {
            'id': entry['id'],
            'url': entry['url'],
            'title': entry['title'],
            'duration': entry['duration'],
    }

def map_and_merge(entry, videos):
    video = map_entry_to_video(entry)
    if video is None:
        return

    existing = [x for x in videos if x['id'] == entry['id']]
    if any(existing):
        existing[0].update(video)
    else:
        videos.append(video)
