# claude-colab

Turn Google Colab into a Claude Code-powered dev box.

`claude-colab` is a **Claude Code plugin marketplace** that ships a self-bootstrapping Colab notebook. It installs Claude Code and configures the `claude-colab` plugin with skills, agents, hooks, and commands.

## Quick Start

1. **Download the notebook** from the [latest release](https://github.com/ali/claude-colab/releases/latest)
2. Open in Google Colab
3. Get a long-lived OAuth token: `claude setup-token` (on your local machine)
4. Add the token to Colab Secrets as `CLAUDE_CODE_OAUTH_TOKEN`
5. Run all cells
6. Open terminal: `source ~/.bashrc && cd /content/claude-workspaces/my-project && claude`

## Plugin Features

The **claude-colab** plugin provides:

| Type | Name | Description |
|------|------|-------------|
| **Command** | `/claude-colab:colab-status` | Check GPU, Drive, workspace status |
| **Command** | `/claude-colab:checkpoint` | Save workspace to Google Drive |
| **Command** | `/claude-colab:colab-update` | Check for plugin updates |
| **Skill** | claude-expert | Claude Code reference and best practices |
| **Skill** | ipynb | Jupyter notebook manipulation |
| **Skill** | customize | Environment customization |
| **Skill** | docs-updater | Documentation management |
| **Skill** | skill-builder | Create new skills |
| **Agent** | colab | Colab environment expert |
| **Agent** | notebook-doctor | Diagnose and fix issues |
| **Hook** | SessionStart | Auto-check for updates |
| **Hook** | PreToolUse | Safety check for dangerous commands |

## Safety Features

The plugin includes a safety hook that blocks dangerous commands:
- `rm -rf /` or `rm -rf ~` - Prevents deleting root/home
- `rm -rf /content/drive` - Protects Google Drive mount
- Fork bombs and system killers
- Direct disk writes

## Storage Modes

- **Ephemeral (default)**: Workspace at `/content/claude-workspaces/` - resets each session
- **Persistent**: Enable Google Drive to save workspace between sessions

## Common Workflows

- **Edit uploaded repos**: Upload a zip, unzip it, `cd` into it, run `claude`
- **Edit notebooks**: Use the `ipynb` skill to create/edit `.ipynb` files
- **Check status**: Run `/claude-colab:colab-status` for environment info
- **Save work**: Run `/claude-colab:checkpoint` to save to Drive

## Architecture

This repository serves dual purposes:

1. **Plugin Marketplace** - Claude Code can fetch the plugin directly from this GitHub repo
2. **Bootstrap Notebook** - Downloads configure the marketplace and enable the plugin

```
.claude-plugin/
  marketplace.json     # Marketplace manifest
src/plugin/
  .claude-plugin/
    plugin.json        # Plugin manifest
  skills/              # 5 skills
  agents/              # 2 agents
  commands/            # 3 commands
  hooks/               # SessionStart, PreToolUse, PostToolUse
  scripts/             # Hook implementations
```

## Development

### Setup

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

### Building

```bash
uv run python build.py
# Generates dist/claude-colab.ipynb
```

### Testing

```bash
uv run python -m pytest tests/ -v
```

## Issue Tracking

This project uses [beads](https://github.com/steveyegge/beads) for issue tracking. Issues are stored in the `beads-sync` branch.

```bash
bd list          # List issues
bd ready         # Find unblocked work
bd create "..."  # Create issue
```
