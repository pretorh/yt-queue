#!/usr/bin/env bash
set -eE

cli=${YT_QUEUE-./yt-queue}
playlist="https://www.youtube.com/playlist?list=PL0pg4HdU1lNMtRzycn3wbKyfQO5vQZja9"
example_info=tests/example.info.json
expected_video_id=BaW_jenozKc
info=tests/info.json
log=tests/run.log

echo "# using cli from $cli = $(which "$cli")"

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
    'import sys,json; d=json.load(sys.stdin); print('"$field"')' || echo "<failed to read: $field>"
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

test_cli_fails_for_invalid_params() {
  if $cli invalid-command >$log 2>&1 ; then
    fail "did not fail when invalid command given to cli"
  fi
  ok
}

test_can_create_info() {
  rm -f "$info"
  $cli create "$info" "$playlist" >$log 2>&1
  test -f "$info" || fail "json file not created"
  assert "$(print_json_field 'd["url"]')" "$playlist"
  ok
}

test_can_refresh_info() {
  $cli refresh "$info" >$log 2>&1
  assert "$(print_json_field 'len(d["videos"])')" 1
  assert "$(print_json_field 'd["videos"][0]["id"]')" $expected_video_id
  ok
}

test_refresh_only_adds_new_item_does_not_remove_old_or_readd_existing() {
  cp "$example_info" "$info"

  $cli refresh "$info" >$log 2>&1

  assert "$(print_json_field 'len(d["videos"])')" 2
  assert "$(print_json_field 'd["videos"][0]["id"]')" "invalid-id"
  assert "$(print_json_field 'd["videos"][1]["id"]')" $expected_video_id
  assert "$(print_json_field 'd["videos"][1]["fieldToNotRemove"]')" 1

  # but it may add new fields
  assert "$(print_json_field 'd["videos"][1]["url"]')" "https://www.youtube.com/watch?v=$expected_video_id"

  ok
}

test_can_manage_item_status() {
  cp "$example_info" "$info"
  std_out=tests/out.log

  $cli get-no-status "$info" >$std_out 2>$log
  assert "$(cat $std_out)" \
    "invalid-id
$expected_video_id"

  $cli set-status "$info" "invalid-id" "test-status-123" >$log 2>&1

  $cli get-no-status "$info" >$std_out 2>$log
  assert "$(cat $std_out)" "$expected_video_id"

  $cli get-status "$info" test-status-123 >$std_out 2>$log
  assert "$(cat $std_out)" "invalid-id"

  ok
}

test_can_read_field_in_video() {
  cp "$example_info" "$info"
  std_out=tests/out.log

  $cli read-field "$info" "$expected_video_id" "fieldToNotRemove" >$std_out 2>$log
  assert "$(cat $std_out)" "1"

  # empty string for unknown fields
  $cli read-field "$info" "invalid-id" "fieldToNotRemove" >$std_out 2>$log
  assert "$(cat $std_out)" ""

  ok
}

test_cli_is_executable
test_cli_fails_for_invalid_params
test_can_create_info
test_can_refresh_info
test_refresh_only_adds_new_item_does_not_remove_old_or_readd_existing
test_can_manage_item_status
test_can_read_field_in_video
