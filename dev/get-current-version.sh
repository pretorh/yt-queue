#!/usr/bin/env sh
set -e

grep "VERSION = " yt_queue/__init__.py | awk -F\' '{print $2}'
