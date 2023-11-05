def map_and_merge(entry, videos):
    if entry is None:
        return

    existing = [x for x in videos if x['id'] == entry['id']]
    if any(existing):
        existing[0]['url'] = entry['url']
    else:
        videos.append({
            'id': entry['id'],
            'url': entry['url'],
        })
