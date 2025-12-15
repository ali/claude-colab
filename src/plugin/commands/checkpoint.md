---
description: Save a checkpoint to Google Drive with timestamp
allowed-tools: Bash, Write, Read
argument-hint: [checkpoint-name]
---

Save a checkpoint of the current workspace to Google Drive.

1. **Check Drive is mounted**
   ```bash
   if [ ! -d "/content/drive/My Drive" ]; then
       echo "ERROR: Google Drive not mounted. Run the mount cell in your notebook first."
       exit 1
   fi
   ```

2. **Create checkpoint directory**
   ```bash
   CHECKPOINT_DIR="/content/drive/My Drive/claude-checkpoints"
   mkdir -p "$CHECKPOINT_DIR"
   ```

3. **Save checkpoint**
   - If `$ARGUMENTS` provided, use that as checkpoint name
   - Otherwise use timestamp: `checkpoint_YYYYMMDD_HHMMSS`
   - Copy relevant workspace files (excluding large data files)
   - Save a manifest of what was saved

4. **Confirm to user**
   - Report what was saved
   - Report checkpoint location
   - Report size

Example checkpoint structure:
```
/content/drive/My Drive/claude-checkpoints/
└── my-checkpoint/
    ├── manifest.json
    ├── workspace/
    │   ├── CLAUDE.md
    │   ├── .claude/
    │   └── src/
    └── environment.json
```
