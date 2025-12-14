# Skill Builder Skill

You create high-quality Claude Code skills. Skills are markdown files that give Claude specialized knowledge and capabilities.

## Skill Anatomy

A skill lives in `.claude/skills/skill-name/` and contains:

```
.claude/skills/my-skill/
├── SKILL.md          # Required: Main skill definition
├── examples/         # Optional: Example files
├── templates/        # Optional: Templates to use
└── resources/        # Optional: Reference docs, data
```

## SKILL.md Structure

```markdown
# Skill Name

Brief description of what this skill does and when to use it.

## Capabilities
What the skill enables Claude to do.

## Knowledge
Domain-specific information Claude needs.

## Patterns
Common patterns, templates, or approaches.

## Examples
Concrete examples of skill in action.

## Gotchas
Common mistakes to avoid.
```

## Skill Design Principles

### 1. Trigger Clarity
Make it obvious when to use the skill:
- "When user asks about X..."
- "For tasks involving Y..."
- "Use this skill for Z..."

### 2. Actionable Knowledge
Don't just describe - provide:
- Copy-paste code templates
- Step-by-step procedures
- Decision trees for common choices

### 3. Context Awareness
Include environment-specific details:
- File paths that matter
- Commands to run
- Tools available

### 4. Error Handling
Document common failures:
- What errors look like
- How to diagnose
- How to fix

### 5. Composability
Skills should work together:
- Reference other skills when relevant
- Don't duplicate - delegate
- Use consistent conventions

## Skill Types

### Knowledge Skills
Provide domain expertise:
```markdown
# React Best Practices Skill

## Component Patterns
- Prefer functional components with hooks
- Use custom hooks for reusable logic
...
```

### Workflow Skills
Guide multi-step processes:
```markdown
# Deploy to Production Skill

## Pre-Deploy Checklist
1. Run tests: `pytest`
2. Check types: `mypy .`
3. Build: `npm run build`
...
```

### Tool Skills
Wrap complex tools:
```markdown
# Docker Skill

## Common Commands
| Task | Command |
|------|---------|
| Build | `docker build -t name .` |
...
```

### Meta Skills
Help with Claude Code itself:
```markdown
# Debug Skill

## When Claude is stuck
1. Check /status
2. Run /clear if context polluted
3. Break task into smaller steps
...
```

## Creating a Skill

### Step 1: Identify the Need
Ask:
- What task is repetitive or error-prone?
- What knowledge does Claude need to access repeatedly?
- What would make a workflow smoother?

### Step 2: Gather Knowledge
- Collect examples of good outputs
- Document common mistakes
- Note environment requirements

### Step 3: Structure the Skill
- Start with clear trigger conditions
- Add actionable content (not just descriptions)
- Include examples
- Add gotchas section

### Step 4: Test the Skill
- Try invoking it with various prompts
- Check if Claude uses it correctly
- Refine based on failures

### Step 5: Iterate
- Add missing knowledge as gaps appear
- Remove unhelpful sections
- Keep it focused and useful

## Anti-Patterns

❌ **Too Vague**
```markdown
## How to Code
Write good code that works.
```

✅ **Specific and Actionable**
```markdown
## Error Handling Pattern
Always wrap external calls:
\`\`\`python
try:
    result = api.call()
except ApiError as e:
    logger.error(f"API failed: {e}")
    raise
\`\`\`
```

❌ **Information Dump**
```markdown
## Everything About Docker
[5000 words of Docker documentation]
```

✅ **Curated and Contextual**
```markdown
## Docker for This Project
We use multi-stage builds. Key commands:
- Dev: `docker-compose up`
- Prod: `docker build -f Dockerfile.prod .`
```

## Skill Template

```markdown
# [Skill Name]

[One-line description]

## When to Use
- [Trigger condition 1]
- [Trigger condition 2]

## Quick Reference
| Task | How |
|------|-----|
| ... | ... |

## Detailed Knowledge

### [Topic 1]
[Content]

### [Topic 2]
[Content]

## Examples

### Example: [Scenario]
[Input/output example]

## Common Issues

### [Issue 1]
**Symptom:** ...
**Cause:** ...
**Fix:** ...
```
