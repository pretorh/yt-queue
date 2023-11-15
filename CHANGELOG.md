# Changelog

## unreleased

### Added

- Api: `filter_videos` function to filter by rules given (currently 'status', 'custom' function)

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
