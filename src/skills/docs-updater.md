# Documentation Updater Skill

You help update cached Claude Code documentation from the official site.

## When to Use

- User asks to update documentation
- User wants to check for latest docs
- Debugging issues that might be fixed in newer docs
- Setting up a fresh Colab environment

## How It Works

Documentation is cached in `src/cached_docs/` (or `{workspace}/cached_docs/` in Colab).

### Update Process

1. **Check manifest**: Read `src/docs_manifest.json` or `{workspace}/docs_manifest.json`
   - Contains URLs for all docs
   - Has sitemap URL: https://code.claude.com/docs/llms.txt
   - Shows last update timestamp

2. **Run update script**: Execute `update_docs.py`
   ```bash
   python3 update_docs.py
   ```
   
   Or in Colab, use the "Update Documentation" cell in the bootstrap notebook.

3. **Verify**: Check that files in `cached_docs/` have metadata headers showing:
   - Source URL
   - Download timestamp
   - Sitemap link

## Documentation Sources

All docs come from: https://code.claude.com/docs/en/

- `overview.md` - Getting started
- `settings.md` - Configuration reference
- `hooks.md` - Hooks system
- `statusline.md` - Status line config
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

## In Colab Environment

If the update script isn't available:

1. Download `update_docs.py` from the repo
2. Download `src/docs_manifest.json` 
3. Create `cached_docs/` directory in workspace
4. Run the update script

Or use the notebook cell that's included in the bootstrap.

## Troubleshooting

- **Download fails**: Check network, try `--force` flag
- **Missing manifest**: Create `docs_manifest.json` with doc URLs
- **Old docs**: Check timestamps in metadata headers
- **Sitemap**: Fetch https://code.claude.com/docs/llms.txt to see all available docs
