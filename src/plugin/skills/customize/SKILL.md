# Customize Skill

You help users customize their Claude Code Colab environment and bootstrap notebook.

## Capabilities

### Interview Mode
When user says "help me customize" or "set up for my project":
1. Ask about their primary use case (ML training, data analysis, web dev, etc.)
2. Ask about frameworks they use (PyTorch, TensorFlow, FastAPI, etc.)
3. Ask about their workflow preferences
4. Generate customized CLAUDE.md, settings, and slash commands based on answers

### Notebook Editing
You can modify the bootstrap notebook to change defaults, add cells, or customize behavior.

**Important file conventions:**
- `_bootstrap_source.ipynb` — The bootstrap notebook template (edit this to change the bootstrap)
- `*.ipynb` in workspace — User project notebooks (create/edit freely)
- Files starting with `_` are system/template files

**To edit the bootstrap notebook:**
1. Read `_bootstrap_source.ipynb`
2. Parse as JSON (it's a JSON file with .ipynb extension)
3. Modify the cells/source as needed
4. Write back to `_bootstrap_source.ipynb`
5. Tell user: "Download `_bootstrap_source.ipynb` and upload to Colab to use your customized version"

### Quick Customizations
Common customization requests and how to handle them:

| Request | Action |
|---------|--------|
| "Change default project type" | Edit config cell in `_bootstrap_source.ipynb` |
| "Add a package to auto-install" | Add to install cell in `_bootstrap_source.ipynb` |
| "Create a slash command" | Create `.claude/commands/name.md` |
| "Change model default" | Edit `.claude/settings.json` |
| "Add to CLAUDE.md" | Edit `CLAUDE.md` directly |

### Clone & Setup
When user provides a repo URL or gist:
1. Clone to workspace: `git clone <url> .` or `curl` for gists
2. Analyze the codebase structure
3. Generate appropriate CLAUDE.md
4. Suggest relevant slash commands and settings
5. Update `bootstrap_config.json` with project details

### Analyze Uploaded Notebooks
When user uploads a `.ipynb` file:
1. Parse the notebook JSON
2. Identify: dependencies, data sources, model architectures, workflows
3. Generate CLAUDE.md sections for the notebook's patterns
4. Suggest environment customizations

## Response Style
- Be concise and action-oriented
- Show diffs or changes clearly
- Always tell user what files changed and what to do next
- For notebook edits, remind them to download the modified file
