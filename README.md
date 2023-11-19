# yt-queue
CLI to keep track of videos in Youtube playlists

## cli

tl;dr:

```sh
yt-queue create <name.ytq.json> <url>
yt-queue refresh <name.ytq.json>
yt-queue get-no-status <name.ytq.json>
yt-queue read-field <name.ytq.json> <video-id> <url>
yt-queue set-status <name.ytq.json> <video-id> <status>
```

See `yt-queue -h` or `yt-queue <subcommand> -h` for details.

### output

Most cli subcommands' output (`stdout`) is parsable. `stderr` is used for logging:

- `get-no-status` and `get-status` returns the video ids, 1 per line
- `read-field` returns the value of the field for the given video id

Other subcommands output should not be parsed - they contain either progress or verbose logging (including
from `yt-dlp`)

## development

```shell
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
# or
pip install --editable .
pip install '.[dev]'
```

other dependencies: `shellcheck`

tests: `./check.sh`

test the built packages: `./dist-check.sh dist/...`
