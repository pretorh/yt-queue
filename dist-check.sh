#!/usr/bin/env sh
set -e

venv=.dist-env
dist=${1?'pass the path to the dist file to install'}

rm -rf $venv
python3 -m venv $venv
# shellcheck source=/dev/null
. $venv/bin/activate
pip install "$dist"

if [ "$(which yt-queue)" = "$VIRTUAL_ENV/bin/yt-queue" ] ; then
  echo "yt-queue cli is available in VIRTUAL_ENV path"
else
  echo "yt-queue cli is not available in VIRTUAL_ENV" >&2
  exit 1
fi
YT_QUEUE=yt-queue tests/cli.sh

YT_QUEUE=yt-queue tests/doc.sh

deactivate
