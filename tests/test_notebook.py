"""
Tests for the built notebook.

Validates structure, content, and plugin marketplace configuration.

The new architecture uses the plugin system - skills, agents, hooks, and
commands are provided by the colab-toolkit plugin from this repo's marketplace.
"""

import json
import re
from pathlib import Path

import pytest

# Placeholders that should be replaced during build
EXPECTED_PLACEHOLDERS = [
    "{{BOOTSTRAP_VERSION}}",
    "{{GITHUB_REPO}}",
]

# Required content patterns for the new plugin-based architecture
REQUIRED_CONTENT_PATTERNS = [
    (r"BOOTSTRAP_VERSION\s*=\s*\"[\d.]+\"", "Bootstrap version"),
    (r"extraKnownMarketplaces", "Marketplace configuration"),
    (r"enabledPlugins", "Enabled plugins"),
    (r"colab-toolkit@claude-colab", "Plugin reference"),
]


@pytest.fixture
def notebook_path():
    """Path to the built notebook."""
    return Path(__file__).parent.parent / "dist" / "claude-colab.ipynb"


@pytest.fixture
def notebook(notebook_path):
    """Load and return the notebook JSON."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        return json.load(f)


class TestNotebookStructure:
    """Test notebook JSON structure and basic validity."""

    def test_notebook_exists(self, notebook_path):
        """Test that the notebook file exists."""
        assert notebook_path.exists(), f"Notebook not found at {notebook_path}"

    def test_notebook_is_valid_json(self, notebook_path):
        """Test that the notebook is valid JSON."""
        with open(notebook_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict), "Notebook should be a JSON object"

    def test_notebook_has_required_keys(self, notebook):
        """Test that notebook has required top-level keys."""
        required_keys = ["cells", "metadata", "nbformat", "nbformat_minor"]
        for key in required_keys:
            assert key in notebook, f"Notebook missing required key: {key}"

    def test_notebook_has_cells(self, notebook):
        """Test that notebook has cells."""
        assert "cells" in notebook
        assert isinstance(notebook["cells"], list)
        assert len(notebook["cells"]) > 0, "Notebook should have at least one cell"

    def test_cells_have_required_fields(self, notebook):
        """Test that all cells have required fields."""
        for i, cell in enumerate(notebook["cells"]):
            assert "cell_type" in cell, f"Cell {i} missing cell_type"
            assert "source" in cell, f"Cell {i} missing source"
            assert cell["cell_type"] in ["markdown", "code", "raw"], (
                f"Cell {i} has invalid cell_type: {cell['cell_type']}"
            )


class TestNotebookContent:
    """Test notebook content for completeness and correctness."""

    def test_no_placeholders_remain(self, notebook):
        """Test that all placeholders have been replaced."""
        notebook_text = json.dumps(notebook, ensure_ascii=False)
        for placeholder in EXPECTED_PLACEHOLDERS:
            assert placeholder not in notebook_text, (
                f"Placeholder {placeholder} was not replaced in built notebook"
            )

    def test_required_content_exists(self, notebook):
        """Test that required content patterns exist in the notebook."""
        # Get all code cell sources
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        for pattern, description in REQUIRED_CONTENT_PATTERNS:
            assert re.search(pattern, all_code), (
                f"Required content not found: {description} (pattern: {pattern})"
            )

    def test_marketplace_configuration(self, notebook):
        """Test that marketplace is properly configured."""
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        # Check marketplace config structure
        assert "extraKnownMarketplaces" in all_code, "extraKnownMarketplaces not found"
        assert "claude-colab" in all_code, "claude-colab marketplace not found"
        assert "github" in all_code, "GitHub source type not found"

    def test_plugin_enabled(self, notebook):
        """Test that colab-toolkit plugin is enabled."""
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        assert "enabledPlugins" in all_code, "enabledPlugins not found"
        assert "colab-toolkit@claude-colab" in all_code, "Plugin not enabled"

    def test_version_is_valid(self, notebook):
        """Test that version number is valid semver."""
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        # Find version pattern
        version_match = re.search(r'BOOTSTRAP_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', all_code)
        assert version_match, "BOOTSTRAP_VERSION not found or invalid"

        version = version_match.group(1)
        parts = version.split(".")
        assert len(parts) == 3, "Version should be semver (X.Y.Z)"
        for part in parts:
            assert part.isdigit(), "Version parts should be numeric"

    def test_github_repo_is_valid(self, notebook):
        """Test that GitHub repo is valid."""
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        # Check for owner/repo pattern
        repo_match = re.search(r'"repo":\s*"([^/]+/[^"]+)"', all_code)
        assert repo_match, "GitHub repo not found in proper format (owner/repo)"

        repo = repo_match.group(1)
        assert "/" in repo, "Repo should be in owner/repo format"


class TestPluginStructure:
    """Test that the plugin structure exists and is valid."""

    def test_plugin_json_exists(self):
        """Test that plugin.json exists."""
        plugin_path = Path(__file__).parent.parent / "src" / "plugin" / ".claude-plugin" / "plugin.json"
        assert plugin_path.exists(), f"Plugin manifest not found at {plugin_path}"

    def test_plugin_json_is_valid(self):
        """Test that plugin.json is valid JSON with required fields."""
        plugin_path = Path(__file__).parent.parent / "src" / "plugin" / ".claude-plugin" / "plugin.json"
        with open(plugin_path, "r") as f:
            plugin = json.load(f)

        assert "name" in plugin, "Plugin missing 'name' field"
        assert "version" in plugin, "Plugin missing 'version' field"
        assert plugin["name"] == "colab-toolkit", "Plugin name should be 'colab-toolkit'"

    def test_marketplace_json_exists(self):
        """Test that marketplace.json exists."""
        marketplace_path = Path(__file__).parent.parent / ".claude-plugin" / "marketplace.json"
        assert marketplace_path.exists(), f"Marketplace manifest not found at {marketplace_path}"

    def test_marketplace_json_is_valid(self):
        """Test that marketplace.json is valid JSON with required fields."""
        marketplace_path = Path(__file__).parent.parent / ".claude-plugin" / "marketplace.json"
        with open(marketplace_path, "r") as f:
            marketplace = json.load(f)

        assert "name" in marketplace, "Marketplace missing 'name' field"
        assert "plugins" in marketplace, "Marketplace missing 'plugins' field"
        assert len(marketplace["plugins"]) > 0, "Marketplace should have at least one plugin"

    def test_skills_exist(self):
        """Test that skills directory has content."""
        skills_dir = Path(__file__).parent.parent / "src" / "plugin" / "skills"
        assert skills_dir.exists(), "Skills directory not found"
        skills = list(skills_dir.glob("*/SKILL.md"))
        assert len(skills) > 0, "No skills found in plugin"

    def test_agents_exist(self):
        """Test that agents directory has content."""
        agents_dir = Path(__file__).parent.parent / "src" / "plugin" / "agents"
        assert agents_dir.exists(), "Agents directory not found"
        agents = list(agents_dir.glob("*.md"))
        assert len(agents) > 0, "No agents found in plugin"

    def test_commands_exist(self):
        """Test that commands directory has content."""
        commands_dir = Path(__file__).parent.parent / "src" / "plugin" / "commands"
        assert commands_dir.exists(), "Commands directory not found"
        commands = list(commands_dir.glob("*.md"))
        assert len(commands) > 0, "No commands found in plugin"

    def test_hooks_json_exists(self):
        """Test that hooks.json exists and is valid."""
        hooks_path = Path(__file__).parent.parent / "src" / "plugin" / "hooks" / "hooks.json"
        assert hooks_path.exists(), "hooks.json not found"
        with open(hooks_path, "r") as f:
            hooks = json.load(f)
        assert "hooks" in hooks, "hooks.json missing 'hooks' key"
