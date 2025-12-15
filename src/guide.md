# Claude Code Colab Guide

## Key Files
- `ENVIRONMENT.json` — Runtime snapshot (GPU, versions, tools)
- `bootstrap_config.json` — Edit to customize future bootstraps
- `_bootstrap_source.ipynb` — The notebook source (Claude can edit this)
- `CLAUDE.md` — Your project memory (create with `/init`)

## Colab Gotchas
- Everything in `/content/` (except Drive) resets on disconnect
- `pip install` survives restart, NOT disconnect
- Free tier: ~12hr max, ~90min idle timeout
- Check GPU: `!nvidia-smi` or `torch.cuda.is_available()`

## Quick Reference
| Command | Purpose |
|---------|---------|
| `/init` | Generate CLAUDE.md |
| `/clear` | Reset context |
| `/compact` | Reduce tokens |
| `/model opus` | Switch model |
| `/usage` | Token usage |

## Skills Available
- **customize** — Customize this notebook
- **ipynb** — Create/edit notebooks
- **skill-builder** — Create new skills
- **claude-expert** — Claude Code docs

## Agents Available
- **notebook-doctor** — Diagnose issues
- **colab** — Colab expertise
