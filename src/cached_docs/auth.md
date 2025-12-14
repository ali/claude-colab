# Claude Code Authentication

## Authentication Methods

Claude Code supports multiple authentication methods:

### OAuth Token (Recommended for Interactive Use)

Claude Code uses OAuth tokens for authentication. You can obtain a token using:

```bash
claude login --print-token
```

This will:
1. Open a browser for OAuth authentication
2. Print the token to stdout
3. Save the token to `~/.claude.json` for future use

### API Key (For Headless/CI Use)

For non-interactive environments, you can use an API key:

```bash
export ANTHROPIC_API_KEY=your-api-key
claude
```

Or set it in `settings.json`:

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "your-api-key"
  }
}
```

### Token Storage

OAuth tokens are stored in:
- `~/.claude.json` - Contains OAuth session and preferences
- `~/.claude/.credentials.json` - Legacy location (may be used in some setups)

### Environment Variables

- `ANTHROPIC_API_KEY` - API key for Claude API
- `ANTHROPIC_AUTH_TOKEN` - Custom Authorization header value
- `CLAUDE_CODE_OAUTH_TOKEN` - OAuth token (can be set from Colab Secrets)

### Colab-Specific Setup

In Google Colab, you can:

1. Get token from your local machine:
   ```bash
   claude login --print-token
   ```

2. Save to Colab Secrets:
   - Click the key icon in Colab sidebar
   - Add secret: `CLAUDE_CODE_TOKEN` (or `CLAUDE_CODE_OAUTH_TOKEN`)
   - Paste the token value

3. The notebook will read the secret and configure authentication automatically.

### Token Format

OAuth tokens are typically long strings that look like:
```
claude_oauth_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Troubleshooting

- **Token expired**: Re-run `claude login --print-token` to get a new token
- **Token not found**: Check `~/.claude.json` or re-authenticate
- **Colab authentication fails**: Verify the secret name matches what the notebook expects
