#!/usr/bin/env bash
set -e

while IFS= read -r file; do py+=("$file"); done < <(git ls-files '*.py')
echo "${#py[@]} py files:" "${py[@]}"
python "$(which pylint)" "${py[@]}"

while IFS= read -r file; do sh+=("$file"); done < <(git ls-files 'yt-queue' '*.sh')
echo "${#sh[@]} sh files:" "${sh[@]}"
shellcheck "${sh[@]}"
