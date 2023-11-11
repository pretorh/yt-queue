#!/usr/bin/env bash
set -e

mapfile -t py < <(git ls-files '*.py')
echo "py files:" "${py[@]}"
python "$(which pylint)" "${py[@]}"

mapfile -t sh < <(git ls-files 'yt-queue' '*.sh')
echo "sh files:" "${sh[@]}"
shellcheck "${sh[@]}"
