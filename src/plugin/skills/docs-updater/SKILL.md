# Documentation Updater Skill

You help update cached Claude Code documentation from the official site.

## When to Use

- User asks to update documentation
- User wants to check for latest docs
- Debugging issues that might be fixed in newer docs
- Setting up a fresh Colab environment

## How It Works

Documentation is cached in `cached_docs/` (or `{workspace}/cached_docs/` in Colab).

### The Docs Manifest

The `docs_manifest.json` file is the source of truth for all documentation. It contains:
- `base_url`: Base URL for all documentation (https://code.claude.com/docs/en)
- `sitemap_url`: URL to the sitemap listing all available docs (https://code.claude.com/docs/llms.txt)
- `last_updated`: ISO timestamp of last update
- `docs`: Array of documentation entries

Each doc entry has:
- `filename`: Name of the cached file (e.g., "overview.md")
- `url`: Full URL to download from, or "local" for local-only docs
- `title`: Human-readable title
- `description`: Brief description of the doc

**Manifest Structure:**
```json
{
  "base_url": "https://code.claude.com/docs/en",
  "sitemap_url": "https://code.claude.com/docs/llms.txt",
  "last_updated": "2025-12-14T17:45:44.334247",
  "docs": [
    {
      "filename": "overview.md",
      "url": "https://code.claude.com/docs/en/overview.md",
      "title": "Claude Code Overview",
      "description": "Getting started guide and overview of Claude Code"
    }
  ]
}
```

### Update Process

1. **Check manifest**: Read `docs_manifest.json`
   - Verify it's valid JSON
   - Check `last_updated` timestamp
   - Review `docs` array for completeness

2. **Run update script**: Execute `update_docs.py`
   ```bash
   python3 update_docs.py        # Normal update
   python3 update_docs.py --force # Force re-download all
   ```

   Or in Colab, use the "Update Documentation" cell in the bootstrap notebook.

3. **Verify**: Check that files in `cached_docs/` have metadata headers

## Documentation Sources

All docs come from: https://code.claude.com/docs/en/

- `overview.md` - Getting started
- `settings.md` - Configuration reference
- `hooks.md` - Hooks system
- `statusline.md` - Status line config
- `plugins-reference.md` - Plugin system technical reference
- `cli-reference.md` - CLI command reference
- `slash-commands.md` - Slash commands reference
- `auth.md` - Local documentation (not downloaded)

## Metadata Headers

Each cached doc has a header like:
```html
<!--
Documentation Source: https://code.claude.com/docs/en/overview.md
Title: Claude Code Overview
Description: Getting started guide and overview of Claude Code
Downloaded: 2025-12-14T17:22:27.516901
Last Updated: 2025-12-14T17:22:27.516901
Check for updates: https://code.claude.com/docs/en/overview.md
Sitemap: https://code.claude.com/docs/llms.txt
-->
```

## Workflow: Adding New Documentation

When user requests to add new docs:

1. **Check sitemap** for available docs:
   ```bash
   curl -s https://code.claude.com/docs/llms.txt | grep -i "keyword"
   ```

2. **Add entry** to manifest's `docs` array

3. **Run update script** to download

4. **Update config files** that reference docs

## Troubleshooting

- **Download fails**: Check network, try `--force` flag, verify URL is correct
- **Missing manifest**: Create `docs_manifest.json` with proper structure
- **Invalid JSON**: Validate with `python3 -m json.tool docs_manifest.json`
- **Old docs**: Check timestamps in metadata headers, run update script
