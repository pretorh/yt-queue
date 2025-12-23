# Changelog

## unreleased

### Changed

- Updated `yt-dlp` to `2025.12.08`. See yt-dlp [requirement changes](https://github.com/yt-dlp/yt-dlp/issues/15012) since `2025.11.12`

## 0.12.0

### Removed

- Python 3.9 support (minimum is now `3.10`)

### Updated

- (Technical) build for Python `3.13` and `3.14`

## 0.11.20

### Changed

- Updated `yt-dlp` to `2025.10.14`

## 0.11.18

### Changed

- Updated `yt-dlp` to `2025.09.26`

## 0.11.17

### Changed

- Updated `yt-dlp` to `2025.09.23`
- dev: update build tools

## 0.11.16

### Changed

- Updated `yt-dlp` to `2025.09.05`
- dev: update helper scripts (version bump, add `yt-dlp` update helper)

## 0.11.15

### Changed

- Updated `yt-dlp` to `2025.08.20`

## 0.11.14

### Changed

- Updated `yt-dlp` to `2025.08.11`

## 0.11.13

### Changed

- Updated `yt-dlp` to `2025.06.30`

## 0.11.12

### Changed

- Updated `yt-dlp` to `2025.06.09`

## 0.11.11

### Changed

- Updated `yt-dlp` to `2025.05.22`
- dev: update build tools

## 0.11.10

### Changed

- Updated `yt-dlp` to `2025.03.31`
- dev: update build tools

## 0.11.9

### Changed

- Updated `yt-dlp` to `2025.02.19`

## 0.11.8

### Changed

- Updated `yt-dlp` to `2025.01.26`

## 0.11.7

### Changed

- Updated `yt-dlp` to `2025.01.15`

### Fixed

- Dev: example video used in tests

## 0.11.6

### Changed

- Updated `yt-dlp` to `2024.12.03`

## 0.11.5

### Changed

- Updated `yt-dlp` to `2024.11.04`

### Removed

- Python 3.8 support (minimum is now `3.9`)

## 0.11.3

### Changed

- Updated `yt-dlp` to `2024.10.22`

## 0.11.2

### Changed

- Updated `yt-dlp` to `2024.09.27`

## 0.11.1

### Fixed

- Remove removed cli functions from help output

## 0.11.0

### Removed

- Deprecated `get-no-status`, `get-status` CLI functions and `get_no_status`, `get_status` api functions

## 0.10.4

### Changed

- Updated `yt-dlp` to `2024.8.01`

## 0.10.3

### Changed

- Updated `yt-dlp` to `2024.07.25`

## 0.10.2

### Changed

- Updated `yt-dlp` to `2024.07.16`

## 0.10.1

### Changed

- Updated `yt-dlp` to `2024.07.02`

## 0.9.1

### Fixed

- Updated `yt-dlp` to `2024.4.9`
- dev: version bump script
- dev: dist check ci action

## 0.8.0

### Changed

- Updated `yt-dlp` to `2024.03.10`
- Update documentation and examples

## 0.7.1

### Fixed

- Crash when filtering videos that have no duration

## 0.7.0

### Added

- CLI: `filter --title <regular expression>` to only return videos that matches the regular expression
- CLI: `filter --min-duration <seconds>` to only return videos with a duration greater or equal the value
- CLI: `filter --max-duration <seconds>` to only return videos with a duration less or equal the value
- api: `title` option for `filter_videos`
- api: `min-duration` option for `filter_videos`
- api: `max-duration` option for `filter_videos`

## 0.6.0

### Deprecated

- CLI: `get-no-status`: use `filter --no-status` instead
- CLI: `get-status`: use `filter ... --status=...` instead
- api: `get_no_status`: use `list_filtered_ids(..., {'status': None})` instead
- api: `get_status`: use `list_filtered_ids(..., {'status': ...})` instead

## 0.5.0

### Added

- CLI: add `--only-if-older=<time>` to `refresh` sub command to skip if recently refreshed
- api: `only_if_older` option to refresh to skip refreshing if recently refreshed

## 0.4.0

### Added

- CLI: `info` command to show info and statistics
- Saving last successful `refreshed` timestamp

## 0.3.1

### Fixed

- Ignore video entries without urls (crash fix)

## 0.3.0

### Added

- CLI: `--help` options and subcommand descriptions
- Api: `filter_videos` function to filter by rules given (currently 'status', 'custom' function)
- Api: `cli.argument_parser` to parse `sys.argv` using `argparse`

### Fixed

- Updated `yt-dlp` dependency

## 0.2.0

### Added

- Add loggers to control output

### Changed

- Less verbose output in CLI
- Less verbose `yt_dlp` output

### Removed

- Python 3.7 support (minimum is now `3.8`)

## 0.1.1

### Fixed

- Version number in CLI output

## 0.1.0

### Added

- Save `title` and `duration` for each video

## 0.0.1

### Added

- exposing CLI functions with parameters

## 0.0.0

### Added

- Ability to create new info file
- Refresh playlist to save video ids
- Ability to get videos with no or specific "status" field
- Ability to set "status" fields for videos
- Ability to read specific fields for videos from loaded json
- `yt-dlp` dependency
- `yt_queue` module setup
