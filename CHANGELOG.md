# Changelog

## [1.0.0] - 2026-05-05

### Added
- Initial release
- Smart clipboard monitoring
- Automatic session grouping (2-minute inactivity threshold)
- GUI interface with session browsing
- Local SQLite database storage
- Multi-threaded clipboard monitoring

### Fixed
- SQLite threading issues with `check_same_thread=False`
- Duplicate clip prevention within 5 seconds