# Changelog

All notable changes to claude-colab will be documented in this file.

## [0.2.0] - 2024-12-15

### Added
- **Plugin marketplace architecture** - this repo is now a Claude Code plugin marketplace
- **Safety hook** - PreToolUse hook blocks dangerous commands (`rm -rf /`, fork bombs, etc.)
- **Auto-update check** - SessionStart hook checks GitHub releases for updates
- **Plugin commands** (use `claude-colab:` prefix):
  - `/claude-colab:colab-status` - Check Colab environment status
  - `/claude-colab:checkpoint` - Save workspace to Google Drive
  - `/claude-colab:colab-update` - Check for plugin updates
- **5 skills**: claude-expert, ipynb, customize, docs-updater, skill-builder
- **2 agents**: colab, notebook-doctor

### Changed
- Bootstrap notebook now uses plugin system instead of embedded content
- Simplified bootstrap - just configures marketplace and enables plugin
- Commands require `claude-colab:` namespace prefix for clarity

### Removed
- Embedded skills/agents/hooks from notebook (now provided by plugin)
- Self-modifying notebook approach (replaced by plugin updates)

### Fixed
- `enabledPlugins` setting now uses object format (not array)
- Removed redundant `hooks` field from plugin.json (auto-discovered)

## [0.1.2] - 2024-12-14

### Fixed
- Documentation updates
- Minor bug fixes

## [0.1.1] - 2024-12-13

### Added
- Initial plugin structure
- Basic Colab integration

## [0.1.0] - 2024-12-12

### Added
- Initial release
- Self-bootstrapping Colab notebook
- Claude Code installation automation
- Basic skills and agents
