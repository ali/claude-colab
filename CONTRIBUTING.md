# Contributing to Claude Code Colab Bootstrap

This project uses a **source-based build system** where content is maintained in `src/` and compiled into the final notebook.

## Project Structure

```
.
├── src/
│   ├── skills/          # Individual skill files (.md)
│   ├── agents/          # Individual agent files (.md)
│   ├── docs/            # Cached Claude Code documentation
│   ├── hooks/           # Hook scripts (.py)
│   ├── guide.md         # User guide content
│   └── bootstrap_template.ipynb  # Notebook template with placeholders
├── build.py             # Build script
├── claude_code_colab_bootstrap.ipynb  # Generated (do not edit directly)
└── claude_code_colab_DEBUG.ipynb      # Debug variant
```

## Development Workflow

### 1. Edit Source Files

**Skills**: Edit files in `src/skills/*.md`
- Each skill is a separate markdown file
- Use `@src/docs/...` references to link to documentation
- Example: `@src/docs/settings.md` in skill content

**Agents**: Edit files in `src/agents/*.md`
- Same format as skills
- Use YAML frontmatter for agent metadata

**Guide**: Edit `src/guide.md`
- This becomes `CLAUDE_CODE_COLAB_GUIDE.md` in the workspace

**Hooks**: Edit Python scripts in `src/hooks/*.py`
- `markdown_formatter.py` - Auto-formats markdown files
- `statusline.py` - Custom status line display

**Template**: Edit `src/bootstrap_template.ipynb`
- Contains placeholders: `{{GUIDE_CONTENT}}`, `{{SKILLS_DICT}}`, etc.
- These are replaced during build

### 2. Build the Notebook

After making changes, rebuild the notebook:

```bash
uv run python build.py
# or if uv is not available:
python3 build.py
```

This will:
- Read all source files from `src/`
- Inject content into the template
- Generate `claude_code_colab_bootstrap.ipynb`

### 3. Test

1. Upload the generated notebook to Colab
2. Run all cells
3. Verify skills, agents, and hooks are installed correctly
4. Test authentication flow

## Adding a New Skill

1. Create `src/skills/my-skill.md`:

```markdown
# My Skill

Description of what this skill does.

## When to Use
- Trigger condition 1
- Trigger condition 2

## Capabilities
What the skill enables Claude to do.

Reference docs: @src/cached_docs/settings.md
```

2. Rebuild: `python3 build.py`
3. The skill will be automatically included in the notebook

## Adding a New Agent

1. Create `src/agents/my-agent.md`:

```markdown
---
name: my-agent
description: What this agent does
tools: Bash, Read, Write
model: sonnet
---

# My Agent

Agent description and capabilities.
```

2. Rebuild: `python3 build.py`

## Updating Documentation

Documentation is cached in `src/cached_docs/`:

- `overview.md` - Claude Code overview
- `settings.md` - Settings reference
- `hooks.md` - Hooks documentation
- `statusline.md` - Status line configuration
- `plugins-reference.md` - Plugin system technical reference
- `cli-reference.md` - CLI command reference
- `slash-commands.md` - Slash commands reference
- `auth.md` - Authentication guide

To update docs, use the update script:

```bash
uv run update-docs
# or
uv run python update_docs.py
# or if uv is not available:
python3 update_docs.py
```

This will:
- Download latest docs from https://code.claude.com/docs/en/
- Add metadata headers showing source URL and timestamp
- Update `src/docs_manifest.json` with last update time

The manifest (`src/docs_manifest.json`) contains:
- URLs for all documentation files
- Sitemap URL: https://code.claude.com/docs/llms.txt
- Metadata about each doc

Docs are kept as-is from the source (with metadata headers added).

## Using @ References

Skills and agents can reference documentation files using `@` syntax:

```markdown
For details on hooks, see @src/docs/hooks.md
For settings, see @src/docs/settings.md
```

This allows Claude to load documentation on-demand rather than embedding everything.

## Build Script Details

The `build.py` script:

1. Reads `src/bootstrap_template.ipynb`
2. Loads all skills from `src/skills/*.md`
3. Loads all agents from `src/agents/*.md`
4. Loads guide from `src/guide.md`
5. Loads hooks from `src/hooks/*.py`
6. Replaces placeholders in template:
   - `{{GUIDE_CONTENT}}` → guide content
   - `{{SKILLS_DICT}}` → Python dict of skills
   - `{{AGENTS_DICT}}` → Python dict of agents
   - `{{MARKDOWN_FORMATTER_HOOK}}` → markdown formatter script
   - `{{STATUSLINE_HOOK}}` → statusline script
7. Writes `claude_code_colab_bootstrap.ipynb`

## Important Notes

- **Never edit `claude_code_colab_bootstrap.ipynb` directly** - it's generated
- Always edit source files in `src/` and rebuild
- The template uses placeholders that must match exactly (case-sensitive)
- String escaping is handled automatically by the build script

## Debugging Build Issues

If the build fails:

1. Check that all source files exist
2. Verify placeholder names match exactly (including `{{` and `}}`)
3. Check for syntax errors in Python dict generation
4. Run with verbose output: `python3 -u build.py`

## Testing Changes

Before committing:

1. Run `python3 build.py`
2. Verify the generated notebook is valid JSON
3. Test in Colab to ensure everything works
4. Check that skills/agents are installed correctly
