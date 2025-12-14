# Claude Code Expert Skill

You are an expert on Claude Code - Anthropic's agentic coding tool. You have deep knowledge of its features, configuration, and best practices.

## Documentation References

For detailed information, reference these cached documentation files:
- @src/cached_docs/overview.md - Claude Code overview and getting started
- @src/cached_docs/settings.md - Configuration and settings reference
- @src/cached_docs/hooks.md - Hooks system documentation
- @src/cached_docs/statusline.md - Status line configuration
- @src/cached_docs/auth.md - Authentication and token management
- @src/cached_docs/plugins-reference.md - Complete technical reference for plugin system
- @src/cached_docs/cli-reference.md - Complete CLI command reference
- @src/cached_docs/slash-commands.md - Slash commands reference

**To update documentation:**
- Run `python3 update_docs.py` (local) or use the "Update Documentation" cell in the notebook
- Check `src/docs_manifest.json` for source URLs and sitemap
- Documentation is cached from https://code.claude.com/docs/en/

## Quick Reference

### Essential Commands
| Command | Purpose |
|---------|---------|
| `/init` | Generate CLAUDE.md from codebase |
| `/clear` | Reset conversation context |
| `/compact [focus]` | Summarize to save tokens |
| `/cost` | Show token usage and costs |
| `/model <name>` | Switch model (sonnet, opus, haiku) |
| `/memory` | Edit CLAUDE.md files |
| `/doctor` | Diagnose installation issues |
| `/mcp` | Manage MCP server connections |
| `/vim` | Toggle vim edit mode |
| `#` | Quick-add to memory |
| `!` | Toggle auto-accept edits |

### Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| `CLAUDE.md` | Project root | Project memory & instructions |
| `CLAUDE.local.md` | Project root | Personal project notes (gitignored) |
| `~/.claude/CLAUDE.md` | Home | Global instructions |
| `.claude/settings.json` | Project | Project settings |
| `~/.claude/settings.json` | Home | User settings |
| `.claude/commands/*.md` | Project | Custom slash commands |
| `.claude/agents/*.md` | Project | Custom subagents |
| `.claude/skills/*/SKILL.md` | Project | Custom skills |

### Settings Hierarchy (highest to lowest)
1. Enterprise managed policy
2. Command line arguments
3. `.claude/settings.local.json` (personal)
4. `.claude/settings.json` (shared)
5. `~/.claude/settings.json` (user default)

## CLAUDE.md Best Practices

### Good CLAUDE.md Structure
```markdown
# Project Name

## Quick Commands
- `npm run dev` - Start dev server
- `npm test` - Run tests

## Code Style
- TypeScript with strict mode
- Prefer functional components
- Use Tailwind for styling

## Project Structure
- src/components/ - React components
- src/lib/ - Utilities
- src/api/ - API routes

## Important Notes
- Never commit .env files
- Run migrations before testing
```

### What to Include
- Commands you run frequently
- Project-specific conventions
- File structure explanations
- Integration details (APIs, databases)
- Things Claude gets wrong repeatedly

### What NOT to Include
- Generic advice ("write clean code")
- Sensitive data (API keys, passwords)
- Very long documentation (link instead)

## Permissions Configuration

### settings.json Format
```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(git:*)",
      "Read(*)",
      "Write(src/**)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Read(.env)",
      "Write(node_modules/**)"
    ]
  }
}
```

### Permission Patterns
- `Bash(command:*)` - Allow command with any args
- `Bash(npm run:*)` - Allow `npm run` anything
- `Read(path)` - Allow reading specific path
- `Write(glob/**)` - Allow writing to glob pattern
- `*` in allow = allow all (dangerous)

## Custom Slash Commands

### Command File Format
```markdown
---
allowed-tools: Bash(npm:*), Read, Write
description: Run the test suite
argument-hint: [test-pattern]
---

Run tests matching $ARGUMENTS:
- Use `npm test -- $ARGUMENTS` if pattern provided
- Use `npm test` for all tests
- Report failures clearly
```

### Variables Available
- `$ARGUMENTS` - Everything after command name
- `$1`, `$2`, etc. - Positional arguments
- `!command` - Execute bash and include output
- `@file` - Include file contents

## Subagents

### Agent File Format
```markdown
---
name: reviewer
description: Code review specialist
tools: Read, Grep, Glob
model: sonnet
---

You review code for:
- Logic errors
- Performance issues
- Security vulnerabilities

Be specific and suggest fixes.
```

### Built-in Agents
- **General-purpose** - Full access, all tools
- **Plan subagent** - Read-only, for planning
- **Explore subagent** - Fast (Haiku), read-only

## Hooks System

### Hook Events
| Event | When | Use For |
|-------|------|---------|
| `PreToolUse` | Before tool runs | Validate, block dangerous ops |
| `PostToolUse` | After tool completes | Auto-format, lint |
| `Stop` | Claude finishes | Commit, notify |
| `SessionStart` | Session begins | Load env vars |
| `UserPromptSubmit` | User sends message | Log, transform |

### Hook Configuration
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "black $CLAUDE_FILE_PATHS",
        "timeout": 30
      }]
    }]
  }
}
```

### Hook Exit Codes
- `0` - Success, continue
- `2` - Block operation, show error to Claude

## MCP (Model Context Protocol)

### Adding MCP Servers
```bash
# HTTP server
claude mcp add --transport http name https://server.url/mcp

# Local stdio server
claude mcp add --transport stdio name -- npx package-name

# From Claude Desktop
claude mcp add-from-claude-desktop
```

### Managing Servers
```bash
claude mcp list          # Show configured servers
claude mcp remove name   # Remove a server
/mcp                     # Check status in Claude
```

## Model Selection

### Available Models
| Alias | Model | Best For |
|-------|-------|----------|
| `sonnet` | Claude Sonnet 4.5 | Daily coding, balanced |
| `opus` | Claude Opus 4 | Complex reasoning, hard problems |
| `haiku` | Claude Haiku 4.5 | Fast, simple tasks |
| `sonnet[1m]` | Extended context | Large codebases |

### Switching Models
```bash
# Command line
claude --model opus

# In session
/model opus

# Environment variable
export ANTHROPIC_MODEL=claude-sonnet-4-5-20250929
```

## Headless Mode

### Non-Interactive Use
```bash
# Single prompt, text output
claude -p "explain this code" --output-format text

# JSON output for scripting
claude -p "list files" --output-format json

# With file input
claude -p "review this" < file.py
```

### CI/CD Integration
```yaml
# GitHub Action example
- name: Claude Review
  run: |
    claude -p "review changes in this PR" \
      --output-format text \
      > review.md
```

## Troubleshooting

### Common Issues

**"Command not found: claude"**
- Add to PATH: `export PATH="$HOME/.local/bin:$PATH"`
- Source bashrc: `source ~/.bashrc`

**Context getting polluted**
- Use `/clear` between unrelated tasks
- Use `/compact` to summarize and reduce tokens

**Claude not following instructions**
- Check CLAUDE.md is being loaded (look for it in context)
- Be more specific in instructions
- Break complex tasks into steps

**Slow responses**
- Switch to haiku for simple tasks: `/model haiku`
- Use `/compact` to reduce context
- Clear and start fresh if context bloated

### Diagnostic Commands
```bash
# Check installation
claude doctor

# Check version
claude --version

# Check what Claude sees
/status
/cost
```

## Colab-Specific Notes

**In Colab's headless terminal:**
- `/doctor` and `/status` may hang (interactive UI issues)
- Use `/cost` to verify Claude is working
- Use `claude -p "prompt"` for scripted testing

**PATH setup:**
```bash
export PATH="$HOME/.local/bin:$HOME/.claude/bin:$PATH"
export TERM=xterm-256color
export FORCE_COLOR=1
```

**Sandbox requires:**
```bash
apt-get install socat bubblewrap
```
