#!/usr/bin/env python3
"""
SessionStart hook for Claude Code Colab plugin.
Runs at the beginning of each Claude Code session.

Features:
- Checks for plugin updates from GitHub releases
- Displays welcome message with environment info
- Sets up environment variables if needed
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# GitHub repo for update checks
GITHUB_REPO = "ali/claude-colab"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


# Current version (read from plugin.json or fallback)
def get_current_version():
    """Get current plugin version from plugin.json."""
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if plugin_root:
        plugin_json = Path(plugin_root) / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            try:
                with open(plugin_json) as f:
                    data = json.load(f)
                    return data.get("version", "0.0.0")
            except Exception:
                pass
    return "0.0.0"


def check_for_updates():
    """Check GitHub releases for newer version."""
    try:
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={
                "User-Agent": "claude-colab-plugin",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            latest_version = data.get("tag_name", "").lstrip("v")
            release_url = data.get("html_url", "")
            return latest_version, release_url
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, TimeoutError):
        # Silently fail - don't block session start
        return None, None


def compare_versions(current, latest):
    """Compare semantic versions. Returns True if latest > current."""
    if not current or not latest:
        return False
    try:
        current_parts = [int(x) for x in current.split(".")]
        latest_parts = [int(x) for x in latest.split(".")]
        # Pad to same length
        while len(current_parts) < 3:
            current_parts.append(0)
        while len(latest_parts) < 3:
            latest_parts.append(0)
        return latest_parts > current_parts
    except ValueError:
        return False


def get_environment_info():
    """Gather environment information for display."""
    info = {}

    # Check if in Colab
    info["in_colab"] = os.path.exists("/content") and os.environ.get("COLAB_RELEASE_TAG")

    # Check GPU
    try:
        import torch

        info["gpu"] = torch.cuda.is_available()
        if info["gpu"]:
            info["gpu_name"] = torch.cuda.get_device_name(0)
    except ImportError:
        info["gpu"] = None

    # Check Drive
    info["drive_mounted"] = os.path.exists("/content/drive/My Drive") or os.path.exists(
        "/content/drive/MyDrive"
    )

    return info


def main():
    """Main session start hook."""
    current_version = get_current_version()

    # Check for updates (non-blocking)
    latest_version, release_url = check_for_updates()

    # Build output
    output_lines = []

    # Update notification (if available)
    if latest_version and compare_versions(current_version, latest_version):
        output_lines.append(
            f"\033[33m✨ colab-toolkit update available: v{current_version} → v{latest_version}\033[0m"
        )
        output_lines.append("\033[33m   Run: /plugin update colab-toolkit\033[0m")
        if release_url:
            output_lines.append(f"\033[33m   Release: {release_url}\033[0m")

    # Environment info (for Colab)
    env_info = get_environment_info()
    if env_info.get("in_colab"):
        status_parts = []
        if env_info.get("gpu"):
            status_parts.append(f"GPU: {env_info.get('gpu_name', 'Yes')}")
        else:
            status_parts.append("GPU: No")
        if env_info.get("drive_mounted"):
            status_parts.append("Drive: Mounted")
        if status_parts:
            output_lines.append(f"\033[36mColab: {' | '.join(status_parts)}\033[0m")

    # Print output if any
    if output_lines:
        print("\n".join(output_lines))

    return 0


if __name__ == "__main__":
    sys.exit(main())
