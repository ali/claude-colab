# Git Hooks

This directory contains shared git hooks for the project. These hooks are tracked in git and need to be installed to `.git/hooks/` to be active.

## Installation

Run the install script from the repository root:

```bash
./scripts/install-hooks.sh
```

Or manually copy hooks:

```bash
cp scripts/hooks/* .git/hooks/
chmod +x .git/hooks/*
```

## Available Hooks

### pre-commit

Runs before each commit:

1. **Beads sync**: Flushes pending bd issue changes to JSONL files
2. **Ruff format**: Auto-formats Python files with `ruff format`
3. **Ruff check**: Auto-fixes linting issues with `ruff check --fix`
4. **Auto-staging**: Re-stages files after auto-fixes

**Requirements**: `uv` (preferred) or `ruff` must be available.

### pre-push

Runs before pushing to remote:

- Ensures all bd JSONL files are committed
- Offers to run `bd sync` interactively if changes are detected
- Prevents pushing stale issue tracking data

**Requirements**: `bd` command (optional, warns if missing)

### post-merge

Runs after `git pull` or `git merge`:

- Imports updated bd JSONL files into the local database
- Keeps issue tracking in sync after pulling changes

**Requirements**: `bd` command (optional, warns if missing)

## Updating Hooks

After modifying hooks in this directory, re-run the install script:

```bash
./scripts/install-hooks.sh
```

## Troubleshooting

**Hooks not running?**
- Make sure hooks are installed: `ls -la .git/hooks/`
- Check file permissions: `chmod +x .git/hooks/*`

**Ruff/uv not found?**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Or install ruff directly: `pip install ruff`

**Beads hooks failing?**
- Make sure `bd` is installed and in PATH
- Check `.beads/config.yaml` for sync-branch configuration
