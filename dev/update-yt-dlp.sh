#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"/..

ytdlp_version=$1
echo yt-dlp=="$ytdlp_version" > requirements.txt
(
  echo "# Changelog"
  echo ""
  echo "## unreleased"
  echo ""
  echo "### Changed"
  echo ""
  echo "- Updated \`yt-dlp\` to \`$ytdlp_version\`"
  tail -n+2 CHANGELOG.md
) > CHANGELOG.md.new
mv CHANGELOG.md{.new,}

git add --patch requirements.txt
git add --patch CHANGELOG.md

dev/init.sh
# shellcheck source=/dev/null
source .env/bin/activate
./check.sh

MESSAGE_SUFFIX=" for yt-dlp update" dev/version-bump.sh patch
