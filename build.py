#!/usr/bin/env python3
"""
Build script to compile the bootstrap notebook from source files.

Reads src/bootstrap_template.ipynb and replaces placeholders with
version info and configuration, then generates dist/claude-colab.ipynb.

The new architecture uses the plugin system - skills, agents, hooks, and
commands are provided by the claude-colab plugin from this repo's marketplace.
"""

import json
import re
import subprocess
from pathlib import Path


def get_version():
    """Get version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if match:
            return match.group(1)
    return "0.0.0"


def get_github_repo():
    """Get GitHub repo from git remote (owner/repo format)."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"], capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        # Handle both HTTPS and SSH URLs
        # https://github.com/owner/repo.git
        # git@github.com:owner/repo.git
        if "github.com" in url:
            if url.startswith("git@"):
                # git@github.com:owner/repo.git
                match = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
            else:
                # https://github.com/owner/repo.git
                match = re.search(r"github\.com/(.+?)(?:\.git)?$", url)
            if match:
                return match.group(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    # Fallback
    return "ali/claude-colab"


def update_plugin_version(version):
    """Update plugin.json with current version."""
    plugin_json_path = Path("src/plugin/.claude-plugin/plugin.json")
    if plugin_json_path.exists():
        with open(plugin_json_path) as f:
            plugin_data = json.load(f)
        plugin_data["version"] = version
        with open(plugin_json_path, "w") as f:
            json.dump(plugin_data, f, indent=2)
        print(f"  ✓ Updated plugin.json version to {version}")


def update_marketplace_version(version):
    """Update marketplace.json with current version."""
    marketplace_json_path = Path(".claude-plugin/marketplace.json")
    if marketplace_json_path.exists():
        with open(marketplace_json_path) as f:
            marketplace_data = json.load(f)
        for plugin in marketplace_data.get("plugins", []):
            if plugin.get("name") == "claude-colab":
                plugin["version"] = version
        with open(marketplace_json_path, "w") as f:
            json.dump(marketplace_data, f, indent=2)
        print(f"  ✓ Updated marketplace.json version to {version}")


def build_notebook():
    """Build the final notebook from template."""
    version = get_version()
    github_repo = get_github_repo()

    print(f"Building claude-colab notebook v{version}")
    print(f"  GitHub repo: {github_repo}")

    # Update version in plugin and marketplace manifests
    update_plugin_version(version)
    update_marketplace_version(version)

    # Read template
    template_path = Path("src/bootstrap_template.ipynb")
    with open(template_path, "r") as f:
        notebook = json.load(f)

    # Replace placeholders in notebook cells
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            # Join source lines
            source = "".join(cell["source"])

            # Replace placeholders
            source = source.replace("{{BOOTSTRAP_VERSION}}", version)
            source = source.replace("{{GITHUB_REPO}}", github_repo)

            # Convert back to list format
            lines = source.split("\n")
            cell["source"] = [
                line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)
            ]
        elif cell["cell_type"] == "markdown":
            # Also replace in markdown cells
            source = "".join(cell["source"])
            source = source.replace("{{BOOTSTRAP_VERSION}}", version)
            source = source.replace("{{GITHUB_REPO}}", github_repo)
            lines = source.split("\n")
            cell["source"] = [
                line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)
            ]

    # Write final notebook
    output_dir = Path("dist")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "claude-colab.ipynb"
    with open(output_path, "w") as f:
        json.dump(notebook, f, indent=2)

    # Count plugin components
    skills_dir = Path("src/plugin/skills")
    agents_dir = Path("src/plugin/agents")
    commands_dir = Path("src/plugin/commands")

    skill_count = len(list(skills_dir.glob("*/SKILL.md"))) if skills_dir.exists() else 0
    agent_count = len(list(agents_dir.glob("*.md"))) if agents_dir.exists() else 0
    command_count = len(list(commands_dir.glob("*.md"))) if commands_dir.exists() else 0

    print(f"\n✓ Built {output_path}")
    print(f"  Plugin: claude-colab v{version}")
    print(f"  - {skill_count} skills")
    print(f"  - {agent_count} agents")
    print(f"  - {command_count} commands")
    print(f"  Marketplace: {github_repo}")


if __name__ == "__main__":
    build_notebook()
