#!/usr/bin/env sh
set -e

version=$(./dev/get-current-version.sh)

awk "/^## $version/{flag=1;next}/^## /{flag=0}flag" CHANGELOG.md
