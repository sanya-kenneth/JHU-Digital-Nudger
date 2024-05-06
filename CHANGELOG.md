# Change Log
All notable changes to this project will be documented in this file.

The format is based on Semantic Versioning 2.0.0 - https://semver.org/

## Increment Format
Given a version number `MAJOR.MINOR.PATCH`, increment the:

1. `MAJOR` version when you make incompatible API changes,
2. `MINOR` version when you add functionality in a backwards-compatible manner
3. `PATCH` version when you make backwards-compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

Date format: `YYYY-MM-DD`

## Valid SubGroup Changes for a release
- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for once-stable features removed in upcoming releases.
- `Removed` for deprecated features removed in this release.
- `Fixed` for any bug fixes.
- `Security` to invite users to upgrade in case of vulnerabilities.

e.g.
## [0.0.1-beta] 2018-10-09
### Added
- Auto generation of changelog

### Changed
- Update date format to yyyy-mm-dd

### Security
- Harden centos image used

### Fixed
- Wrong timestamp format for `registration_date` field

## Version
N.B. - The version has to be of this format `__version__= '1.0.1'`

__version__= '1.0.0'
