# yt-queue
CLI to keep track of videos in Youtube playlists

## cli

See `yt-queue -h` and `yt-queue <subcommand> -h` for details.

Examples:

```sh
# create a new file
yt-queue create example.ytq.json "https://www.youtube.com/playlist?list=PL0pg4HdU1lNMtRzycn3wbKyfQO5vQZja9"

# refresh a file, only if it wasnt recently updated
yt-queue refresh example.ytq.json --only-if-older=1day

# get the "new" items
yt-queue filter --no-status example.ytq.json

# read the values of a video from the file
yt-queue read-field example.ytq.json "BaW_jenozKc" url
yt-queue read-field example.ytq.json "BaW_jenozKc" title

# set the status
yt-queue set-status example.ytq.json "BaW_jenozKc" some-text-status
yt-queue filter --status=some-text-status example.ytq.json

# more filter options
yt-queue filter --title "test video" example.ytq.json
yt-queue filter --min-duration 3 example.ytq.json
yt-queue filter --max-duration 11 example.ytq.json
```

### output

Most cli subcommands' output (`stdout`) is parsable. `stderr` is used for logging:

- `filter` returns the matching video ids, 1 per line
- `read-field` returns the value of the field for the given video id

Other subcommands output should not be parsed - they contain either progress or verbose logging (including
from `yt-dlp`)

## development

setup (or recreate) environment with `source dev/init.sh`

or manually:

```shell
python3 -m venv .env
source .env/bin/activate
pip install --editable .
pip install '.[dev]'
```

other dependencies: `shellcheck`

tests: `./check.sh`

test the built packages: `./dist-check.sh dist/...`
