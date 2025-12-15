---
description: Check for and display available plugin updates
allowed-tools: Bash, Read
---

Check for updates to the colab-toolkit plugin:

1. **Get current version**
   ```bash
   # From plugin.json if available
   cat ~/.claude/plugins/*/colab-toolkit/.claude-plugin/plugin.json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('version', 'unknown'))" || echo "unknown"
   ```

2. **Check GitHub for latest release**
   ```bash
   curl -s "https://api.github.com/repos/ali/claude-colab/releases/latest" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Latest: {d.get(\"tag_name\", \"unknown\")}'); print(f'URL: {d.get(\"html_url\", \"\")}')"
   ```

3. **Compare and report**
   - If update available, show: `/plugin update colab-toolkit`
   - If up to date, confirm current version
   - Show release notes URL if available

4. **Optional: Check notebook version**
   - If `_bootstrap_source.ipynb` exists, check its version
   - Recommend re-downloading bootstrap notebook if outdated
