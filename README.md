# claude-colab

Claude Code for Google Colab — bootstrap a notebook, bring your own repo/notebook, and let Claude maintain the environment (and the notebook) as it runs.

`claude-colab` ships a self-bootstrapping Colab notebook that installs Claude Code and sets up a complete development environment with skills, agents, hooks, and a status line. It’s built for a few high-value workflows:

- **Bootstrap fast**: turn a fresh Colab runtime into a working `claude` terminal in minutes.
- **Edit real projects**: upload a repo/notebook (or `git clone`) and have Claude edit files and run commands directly in Colab.
- **Self-improve**: the notebook copies its own source into the workspace and includes customization skills plus a cached Claude Code docs bundle, so Claude can customize and maintain the setup while it’s running.

## Quick Start

1. **Download the notebook** from the [latest release](https://github.com/ali/claude-colab/releases/latest)
2. Open the downloaded notebook in Google Colab
3. Get your auth token: `claude login --print-token` (anywhere you have Claude Code installed)
4. Add the token to Colab Secrets as `CLAUDE_CODE_TOKEN` (recommended; don’t paste it into a cell)
5. Run all cells
6. Open terminal and run `claude`

## Common Workflows

- **Use ephemeral or persistent workspaces**: run in ephemeral mode by default, or enable Google Drive mode in the notebook to keep your workspace between sessions.
- **Edit a repo you upload**: upload a zip in Colab, unzip it in the workspace, `cd` into it, then run `claude` and ask it to run tests/fix bugs/refactor.
- **Edit notebooks**: keep notebooks in the workspace and use the built-in `ipynb` skill to create/edit `.ipynb` files safely.
- **Customize/self-maintain the notebook**: Claude can edit `bootstrap_config.json` and `_bootstrap_source.ipynb` in your workspace; re-run the notebook to apply changes.
- **Use cached docs as context**: run the “Update Documentation” cell to populate `src/cached_docs/` used by the `claude-expert` skill.

### Included Skills & Agents

- Skills: `customize`, `ipynb`, `skill-builder`, `claude-expert`
- Agents: `notebook-doctor`, `colab`

For more details, see `src/guide.md`.

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

**For project contributors:**
- Edit source files in `src/`
- Run `uv run python build.py` to generate the notebook in `dist/`
- The built notebook is only committed during releases (see `.github/workflows/release.yml`)
- Contributors should edit source files, not the generated notebook

**For end users:**
- Feel free to edit the downloaded notebook however you want!
- You can modify it manually or have Claude edit it while running inside the notebook
- The notebook is designed to be self-modifying and interactive

### Updating Documentation

```bash
uv run python update_docs.py
# or
uv run ./update_docs.py
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
