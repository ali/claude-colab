"""
Tests for the built notebook.

Validates structure, content, and optionally executes the notebook.
"""

import json
import re
from pathlib import Path

import pytest

# Placeholders that should be replaced during build
EXPECTED_PLACEHOLDERS = [
    "{{GUIDE_CONTENT}}",
    "{{MARKDOWN_FORMATTER_HOOK}}",
    "{{STATUSLINE_HOOK}}",
    "{{UPDATE_DOCS_SCRIPT}}",
    "{{DOCS_MANIFEST_JSON}}",
    "{{SKILLS_DICT}}",
    "{{AGENTS_DICT}}",
]

# Required content patterns that should exist in the built notebook
REQUIRED_CONTENT_PATTERNS = [
    (r"GUIDE\s*=\s*'''", "Guide content variable"),
    (r"SKILLS\s*=\s*\{", "Skills dictionary"),
    (r"AGENTS\s*=\s*\{", "Agents dictionary"),
    (r"markdown_formatter\s*=\s*'''", "Markdown formatter hook"),
    (r"statusline_script\s*=\s*'''", "Statusline hook"),
    (r"update_docs_script\s*=\s*'''", "Update docs script"),
    (r"docs_manifest\s*=\s*\{", "Docs manifest"),
]


@pytest.fixture
def notebook_path():
    """Path to the built notebook."""
    return Path(__file__).parent.parent / "claude_code_colab_bootstrap.ipynb"


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

    def test_skills_dict_not_empty(self, notebook):
        """Test that skills dictionary is populated."""
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        # Find SKILLS = {...} pattern
        skills_match = re.search(r"SKILLS\s*=\s*(\{.*?\})", all_code, re.DOTALL)
        assert skills_match, "SKILLS dictionary not found"

        # Try to evaluate it (safely)
        skills_str = skills_match.group(1)
        # Check it's not just an empty dict
        assert skills_str.strip() != "{}", "SKILLS dictionary should not be empty"
        # Check it has content (at least one key-value pair)
        assert ":" in skills_str, "SKILLS dictionary should contain skills"

    def test_agents_dict_not_empty(self, notebook):
        """Test that agents dictionary is populated."""
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        # Find AGENTS = {...} pattern
        agents_match = re.search(r"AGENTS\s*=\s*(\{.*?\})", all_code, re.DOTALL)
        assert agents_match, "AGENTS dictionary not found"

        # Check it's not just an empty dict
        agents_str = agents_match.group(1)
        assert agents_str.strip() != "{}", "AGENTS dictionary should not be empty"
        assert ":" in agents_str, "AGENTS dictionary should contain agents"

    def test_guide_content_not_empty(self, notebook):
        """Test that guide content is populated."""
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        # Find GUIDE = '''...''' pattern
        guide_match = re.search(r"GUIDE\s*=\s*'''(.*?)'''", all_code, re.DOTALL)
        assert guide_match, "GUIDE content not found"
        guide_content = guide_match.group(1)
        assert len(guide_content.strip()) > 0, "GUIDE content should not be empty"

    def test_hooks_are_present(self, notebook):
        """Test that hook scripts are present."""
        code_sources = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"])
                code_sources.append(source)

        all_code = "\n".join(code_sources)

        # Check for markdown formatter
        markdown_match = re.search(r"markdown_formatter\s*=\s*'''(.*?)'''", all_code, re.DOTALL)
        assert markdown_match, "markdown_formatter hook not found"
        assert len(markdown_match.group(1).strip()) > 0, (
            "markdown_formatter hook should not be empty"
        )

        # Check for statusline
        statusline_match = re.search(r"statusline_script\s*=\s*'''(.*?)'''", all_code, re.DOTALL)
        assert statusline_match, "statusline_script hook not found"
        assert len(statusline_match.group(1).strip()) > 0, (
            "statusline_script hook should not be empty"
        )
