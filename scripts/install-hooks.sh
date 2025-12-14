#!/bin/sh
# Install git hooks from scripts/hooks/ to .git/hooks/
#
# This script copies the shared hooks to the local .git/hooks/ directory
# so they are active for this repository.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_SOURCE="$SCRIPT_DIR/hooks"
HOOKS_TARGET="$REPO_ROOT/.git/hooks"

if [ ! -d "$HOOKS_SOURCE" ]; then
    echo "Error: hooks directory not found: $HOOKS_SOURCE" >&2
    exit 1
fi

if [ ! -d "$HOOKS_TARGET" ]; then
    echo "Error: .git/hooks directory not found: $HOOKS_TARGET" >&2
    exit 1
fi

echo "Installing git hooks from $HOOKS_SOURCE to $HOOKS_TARGET..."

for hook in pre-commit pre-push post-merge; do
    if [ -f "$HOOKS_SOURCE/$hook" ]; then
        cp "$HOOKS_SOURCE/$hook" "$HOOKS_TARGET/$hook"
        chmod +x "$HOOKS_TARGET/$hook"
        echo "  ✓ Installed $hook"
    else
        echo "  ⚠ Warning: $hook not found in $HOOKS_SOURCE" >&2
    fi
done

echo ""
echo "✓ Git hooks installed successfully!"
echo ""
echo "The following hooks are now active:"
echo "  - pre-commit: Runs bd sync, ruff format, and ruff check"
echo "  - pre-push: Ensures bd JSONL files are committed"
echo "  - post-merge: Syncs bd database after git pull/merge"
