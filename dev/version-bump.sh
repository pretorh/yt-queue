#!/usr/bin/env bash
set -e

new_version=${1?'new version number missing'}

sed -i.orig "s/^## unreleased$/## $new_version/" CHANGELOG.md
sed -i.orig "s/^VERSION = '.*'$/VERSION = '$new_version'/" yt_queue/__init__.py

git add --patch CHANGELOG.md yt_queue/__init__.py
git commit -m "bump to version $new_version"
read -r -p "enter for diff to last release"
git diff --staged "$(git describe --tags --abbrev=0)"

echo "https://github.com/pretorh/yt-queue/releases/new"
echo "tag and release title: v$new_version"
