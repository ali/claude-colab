# claude-collab

Claude Code for Google Colab

Self-bootstrapping notebook that installs Claude Code in Google Colab and sets up a complete development environment with skills, agents, hooks, and status line.

## Quick Start

1. Open `claude_code_colab_bootstrap.ipynb` in Google Colab
2. Get your auth token: `claude login --print-token` (on your local machine)
3. Add token to Colab Secrets as `CLAUDE_CODE_TOKEN`
4. Run all cells
5. Open terminal and run `claude`

## Development

This project uses `uv` for Python package management and a source-based build system. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync project dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # or: uv run <command>
```

### Building

- Edit source files in `src/`
- Run `uv run python build.py` to generate the notebook
- Never edit `claude_code_colab_bootstrap.ipynb` directly

### Updating Documentation

```bash
uv run update-docs
# or
uv run python update_docs.py
```

## Issue Tracking with Beads

This project uses [beads (bd)](https://github.com/steveyegge/beads) for dependency-aware issue tracking. All issues are stored in the `beads-sync` branch to keep the main branch clean.

### Setup

Beads is already initialized in this repository. The `.beads/` directory contains:
- `beads.db` - SQLite database (not committed)
- `issues.jsonl` - Git-synced issue storage (committed to `beads-sync` branch)

### Working with the Sync Branch

The `beads-sync` branch contains all beads metadata. To work with issues:

```bash
# Switch to sync branch to view/update issues
git checkout beads-sync

# Work with issues
bd list
bd create "New issue"
bd ready  # Find unblocked work

# Commit issue changes
git add .beads/issues.jsonl
git commit -m "Update issues"
git push origin beads-sync

# Switch back to main branch
git checkout main
```

### Auto-Sync

Beads automatically syncs between the database and JSONL:
- Changes are exported to `issues.jsonl` after 5 seconds
- Pulling the `beads-sync` branch imports newer issues automatically
- Git hooks ensure consistency

### For AI Agents

See [AGENTS.md](AGENTS.md) for detailed instructions on using beads with AI assistants.
