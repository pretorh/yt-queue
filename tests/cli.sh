#!/usr/bin/env bash
set -eE

cli=./yt_queue.py
log=tests/run.log

fail() {
  echo "failed: ${FUNCNAME[1]}"
  echo "cli output:"
  tail $log
  exit 1
}
ok() {
  echo "ok: ${FUNCNAME[1]}"
}
trap fail ERR

test_cli_is_executable() {
  $cli >$log 2>&1
  ok
}

test_cli_is_executable
