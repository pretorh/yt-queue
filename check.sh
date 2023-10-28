#!/usr/bin/env sh
set -e

tests/cli.sh

python "$(which pylint)" ./**/*.py
shellcheck yt-queue ./**/*.sh
