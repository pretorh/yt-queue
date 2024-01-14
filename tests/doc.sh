#!/usr/bin/env sh
set -e

example_playlist="https://www.youtube.com/playlist?list=PL0pg4HdU1lNMtRzycn3wbKyfQO5vQZja9"
example_video_id=BaW_jenozKc

if [ "$1" = "doc" ] ; then
  grep "^yt-queue" < "$0" | \
    sed 's#readme-example.ytq.json#<name.ytq.json>#g' | \
    sed 's#".example_playlist"#<url>#g' | \
    sed 's#".example_video_id"#<video-id>#g' | \
    sed 's#watched#<status>#g' | \
    sed 's#|.*##g'
  exit 0
else
  export PATH=".:$PATH"
fi

# create a new file
yt-queue create readme-example.ytq.json "$example_playlist"

# refresh a file, only if it wasnt recently updated
yt-queue refresh readme-example.ytq.json --only-if-older=1day

# get the "new" items
yt-queue filter --no-status readme-example.ytq.json | \
  grep "$example_video_id"

# read the values of a video from the file
yt-queue read-field readme-example.ytq.json "$example_video_id" url
yt-queue read-field readme-example.ytq.json "$example_video_id" title

# set the status
yt-queue set-status readme-example.ytq.json "$example_video_id" watched
yt-queue filter --status=watched readme-example.ytq.json | \
  grep "$example_video_id"
