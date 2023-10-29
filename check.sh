#!/usr/bin/env sh
set -e

pytest
tests/cli.sh

python "$(which pylint)" ./**/*.py
shellcheck yt-queue ./**/*.sh
