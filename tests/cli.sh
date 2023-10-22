#!/usr/bin/env bash
set -eE

cli=./yt_queue.py
playlist="https://www.youtube.com/playlist?list=PL0pg4HdU1lNMtRzycn3wbKyfQO5vQZja9"
info=tests/info.json
log=tests/run.log

# utils

fail() {
  echo "failed: ${FUNCNAME[1]}"
  if [ -n "$1" ] ; then
    echo "$@"
  fi
  echo "cli output:"
  tail $log
  exit 1
}
ok() {
  echo "ok: ${FUNCNAME[1]}"
}
print_json_field() {
  field=$1
  python < "$info" -c \
    'import sys,json; d=json.load(sys.stdin); print('"$field"')'
}
assert() {
  test "$1" = "$2" || fail "$1 != $2"
}
trap fail ERR

# tests

test_cli_is_executable() {
  $cli >$log 2>&1
  ok
}

test_can_create_info() {
  rm -f "$info"
  $cli create "$info" "$playlist" >$log 2>&1
  test -f "$info" || fail "json file not created"
  assert "$(print_json_field 'd["url"]')" "$playlist"
  ok
}

test_cli_is_executable
test_can_create_info
