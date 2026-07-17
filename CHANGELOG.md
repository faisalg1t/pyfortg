# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-15

### Added
- Initial release of PyForTG
- **Core Features:**
  - Async-first TelegramClient with webhook and polling support
  - Full Telegram Bot API implementation (TelegramClient methods)
  - Comprehensive message, callback, and command handlers
  - Decorator-based routing system (@bot.on_message, @bot.on_callback, etc.)
  - Advanced filter system for selective message processing
  - Middleware system for request/response processing
  - Inline keyboard and reply keyboard builders
  - File upload and download support

- **Storage Support:**
  - Redis backend for session and caching management
  - PostgreSQL backend for persistent user data storage
  - Abstract Storage interface for custom implementations

- **Developer Experience:**
  - Type hints throughout the codebase
  - Comprehensive error handling with custom exceptions
  - Utility functions for validation and text formatting
  - Extensive documentation with 6 example bots
  - Unit tests for core components

- **Distribution:**
  - Published to PyPI as `pyfortg`
  - GitHub repository with CI/CD workflows
  - Automated testing on Python 3.9+
  - Automated publishing on releases

### Documentation
- Complete README with quick start guide
- API reference documentation
- Installation and setup guides
- Storage backend configuration guides
- Example bots demonstrating various features

## [1.0.1] - Unreleased

### Planned Features
- WebSocket support for alternative update handling
- Stub method system for batch API calls
- Advanced state machine for conversation flows
- Built-in rate limiting middleware
- Database migrations helper
- CLI tool for bot scaffolding
