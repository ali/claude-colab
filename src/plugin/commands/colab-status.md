---
description: Check Colab environment status, GPU info, and Drive mount
allowed-tools: Bash, Read
---

Check the Colab environment status:

1. **GPU Status**
   ```bash
   python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}'); print(f'Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB' if torch.cuda.is_available() else '')"
   ```

2. **Drive Mount**
   ```bash
   ls -la /content/drive/ 2>/dev/null || echo "Drive not mounted"
   ```

3. **Workspace**
   ```bash
   ls -la /content/claude-workspaces/ 2>/dev/null
   cat /content/claude-workspaces/*/ENVIRONMENT.json 2>/dev/null | head -50
   ```

4. **Claude Code**
   ```bash
   which claude && claude --version
   ```

5. **Plugin Status**
   ```bash
   cat ~/.claude/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('Plugins:', d.get('enabledPlugins', []))"
   ```

Summarize the status in a clear report.
