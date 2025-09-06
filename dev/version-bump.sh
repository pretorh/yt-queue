#!/usr/bin/env bash
set -e
git fetch

new_version=${1?'new version number missing'}
old_version=$(grep "VERSION = " yt_queue/__init__.py | awk -F\' '{print $2}')
if [ "$new_version" == "patch" ] ; then
  new_version=$(echo "$old_version" | awk -F. '{print $1"."$2"."$3+1}')
fi

echo "Bump from $old_version -> $new_version"
sed -i.orig "s/^## unreleased$/## $new_version/" CHANGELOG.md
sed -i.orig "s/^VERSION = '.*'$/VERSION = '$new_version'/" yt_queue/__init__.py

git add --patch CHANGELOG.md yt_queue/__init__.py
git commit -m "bump to version $new_version$MESSAGE_SUFFIX"
read -r -p "enter for diff to last release"
git diff --staged "$(git describe --tags --abbrev=0)"

echo "https://github.com/pretorh/yt-queue/releases/new"
echo "tag and release title: v$new_version"
