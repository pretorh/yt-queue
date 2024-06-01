#!/usr/bin/env sh
set -e

cd "$(dirname "$0")/.."
if [ -n "$VIRTUAL_ENV" ] ; then
  echo "deactivating first"
  deactivate
fi

rm -rf .env
python3 -m venv .env
# shellcheck source=/dev/null
. .env/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
