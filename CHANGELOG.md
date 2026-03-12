# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-12

### Added

- **Garbage Cleaner**: Remove scripts, styles, garbage attributes, and HTML entities from HTML
  - Removes all `<script>` and `<style>` tags
  - Filters attributes to keep only `class` and `href` on anchors
  - Handles HTML entities properly with entity mapping
  - Removes `&nbsp;` entities with counting
  - Returns cleaning statistics (size reduction %, scripts removed, etc.)

- **Space Cleaner**: Remove unnecessary whitespace between tags
  - Removes newlines between HTML tags
  - Preserves spacing around inline elements (`<a>`, `<span>`, `<strong>`, etc.)
  - Optimizes HTML size without changing content

- **HREF Analyzer**: Interactively review and fix broken href attributes
  - Identifies incomplete href references (missing .htm/.html extensions)
  - Interactive prompt for user confirmation on each link
  - Supports special href types (anchors, emails, phones, JavaScript)

### Features

- **Interactive CLI**: Multi-line HTML input with clipboard integration
- **Professional UI**: Rich formatting with panels, tables, and color output
- **Multiple Tools**: Three specialized cleaners in one orchestrated menu
- **Windows Clipboard**: Automatic clipboard output on Windows via PowerShell
- **Comprehensive Testing**: 5/5 validation tests with edge case coverage
- **Clean Architecture**: Modular design following SOLID principles
- **Complete Documentation**: README, QUICKSTART, and agent instructions

### Technical

- Python 3.10+ support
- Pure functions with no side effects
- Dataclass-based result tracking
- HTML parsing with BeautifulSoup4 and stdlib HTMLParser
- Windows clipboard integration via subprocess
