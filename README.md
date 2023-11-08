# yt-queue
CLI to keep track of videos in Youtube playlists

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
