#!/usr/bin/env sh
set -e

example_playlist="https://www.youtube.com/playlist?list=PL0pg4HdU1lNMtRzycn3wbKyfQO5vQZja9"
example_video_id=BaW_jenozKc

if [ "$1" = "doc" ] ; then
  grep -E "^(yt-queue|# )" < "$0" | \
    sed 's#readme-example.ytq.json#example.ytq.json#g' | \
    sed 's#".example_playlist"#"'"$example_playlist"'"#g' | \
    sed 's#".example_video_id"#"'"$example_video_id"'"#g' | \
    sed 's# |.*##g' | \
    sed 's,^# ,\n# ,g' | \
    tail --lines +2
  exit 0
else
  export PATH=".:$PATH"
fi

echo "Testing that example works as expected"
rm -f readme-example.ytq.json

# create a new file
yt-queue create readme-example.ytq.json "$example_playlist"
test -f readme-example.ytq.json

# refresh a file, only if it wasnt recently updated
yt-queue refresh readme-example.ytq.json --only-if-older=1day

# get the "new" items
yt-queue filter --no-status readme-example.ytq.json | \
  grep "$example_video_id"

# read the values of a video from the file
yt-queue read-field readme-example.ytq.json "$example_video_id" url | \
  grep -E "youtube.com/.*$example_video_id"
yt-queue read-field readme-example.ytq.json "$example_video_id" title | \
  grep -E "test video"

# set the status
yt-queue set-status readme-example.ytq.json "$example_video_id" some-text-status
yt-queue filter --status=some-text-status readme-example.ytq.json | \
  grep "$example_video_id"

# more filter options
yt-queue filter --title "test video" readme-example.ytq.json | \
  grep "$example_video_id"
yt-queue filter --min-duration 3 readme-example.ytq.json | \
  grep "$example_video_id"
yt-queue filter --max-duration 11 readme-example.ytq.json | \
  grep "$example_video_id"
echo ""

echo "Testing markdown example"
$0 doc > readme-example.sh
bash -xe readme-example.sh
echo ""

echo "Markdown example:"
echo '```sh'
cat readme-example.sh
echo '```'

rm readme-example.sh
