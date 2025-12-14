# Documentation Updater Skill

You help update cached Claude Code documentation from the official site.

## When to Use

- User asks to update documentation
- User wants to check for latest docs
- Debugging issues that might be fixed in newer docs
- Setting up a fresh Colab environment

## How It Works

Documentation is cached in `src/cached_docs/` (or `{workspace}/cached_docs/` in Colab).

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

### Using the Manifest

**To read the manifest:**
```python
import json
from pathlib import Path

manifest_path = Path('src/docs_manifest.json')
with open(manifest_path, 'r') as f:
    manifest = json.load(f)

# Access properties
base_url = manifest['base_url']
sitemap_url = manifest['sitemap_url']
last_updated = manifest['last_updated']
docs = manifest['docs']

# Find a specific doc
doc = next((d for d in docs if d['filename'] == 'hooks.md'), None)
```

**To check what docs are available:**
- Read `manifest['docs']` to see all tracked docs
- Check `manifest['last_updated']` to see when docs were last refreshed
- Use `manifest['sitemap_url']` to discover new docs from the official site

### Updating the Manifest

**To add a new documentation file:**

1. **Discover docs from sitemap:**
   ```bash
   curl -s https://code.claude.com/docs/llms.txt
   ```
   This lists all available docs with titles and URLs.

2. **Add entry to manifest:**
   ```python
   import json
   from pathlib import Path
   
   manifest_path = Path('src/docs_manifest.json')
   with open(manifest_path, 'r') as f:
       manifest = json.load(f)
   
   # Add new doc entry
   new_doc = {
       "filename": "new-doc.md",
       "url": "https://code.claude.com/docs/en/new-doc.md",
       "title": "New Documentation",
       "description": "Description of what this doc covers"
   }
   
   manifest['docs'].append(new_doc)
   
   # Write back
   with open(manifest_path, 'w') as f:
       json.dump(manifest, f, indent=2)
   ```

3. **Or edit manually:**
   - Open `src/docs_manifest.json`
   - Add a new entry to the `docs` array
   - Ensure JSON is valid (proper commas, quotes, etc.)

**To update an existing entry:**
- Modify the `url`, `title`, or `description` fields
- The `filename` should remain the same (it's the cache key)

**To remove a doc:**
- Remove the entry from the `docs` array
- Optionally delete the cached file from `src/cached_docs/`

### Update Process

1. **Check manifest**: Read `src/docs_manifest.json` or `{workspace}/docs_manifest.json`
   - Verify it's valid JSON
   - Check `last_updated` timestamp
   - Review `docs` array for completeness

2. **Run update script**: Execute `update_docs.py`
   ```bash
   python3 update_docs.py        # Normal update
   python3 update_docs.py --force # Force re-download all
   ```
   
   The script will:
   - Read the manifest
   - Download each doc from its URL (skip if `url == "local"`)
   - Add metadata headers to cached files
   - Update `last_updated` timestamp in manifest
   
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

## In Colab Environment

If the update script isn't available:

1. Download `update_docs.py` from the repo
2. Download `src/docs_manifest.json` 
3. Create `cached_docs/` directory in workspace
4. Run the update script

Or use the notebook cell that's included in the bootstrap.

## Workflow: Adding New Documentation

When user requests to add new docs (e.g., "add skills.md to cached docs"):

1. **Check sitemap** for available docs:
   ```bash
   curl -s https://code.claude.com/docs/llms.txt | grep -i "skills"
   ```

2. **Read current manifest**:
   ```python
   import json
   manifest = json.load(open('src/docs_manifest.json'))
   ```

3. **Add new entry** to manifest's `docs` array:
   ```python
   new_doc = {
       "filename": "skills.md",
       "url": "https://code.claude.com/docs/en/skills.md",
       "title": "Agent Skills",
       "description": "Create, manage, and share Skills to extend Claude's capabilities"
   }
   manifest['docs'].append(new_doc)
   json.dump(manifest, open('src/docs_manifest.json', 'w'), indent=2)
   ```

4. **Run update script** to download:
   ```bash
   python3 update_docs.py
   ```

5. **Update config files** that reference docs:
   - `src/skills/claude-expert.md` - Add to Documentation References
   - `src/skills/docs-updater.md` - Add to Documentation Sources
   - `CONTRIBUTING.md` - Add to Updating Documentation section

6. **Rebuild notebook** if needed:
   ```bash
   python3 build.py
   ```

## Troubleshooting

- **Download fails**: Check network, try `--force` flag, verify URL is correct
- **Missing manifest**: Create `docs_manifest.json` with proper structure (see above)
- **Invalid JSON**: Validate with `python3 -m json.tool src/docs_manifest.json`
- **Old docs**: Check timestamps in metadata headers, run update script
- **Sitemap**: Fetch https://code.claude.com/docs/llms.txt to see all available docs
- **Manifest not updating**: Ensure `update_docs.py` has write permissions, check file path
- **Local docs**: Set `url: "local"` in manifest to skip download (e.g., auth.md)
