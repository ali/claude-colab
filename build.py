#!/usr/bin/env python3
"""
Build script to compile the bootstrap notebook from source files.

Reads src/ directory and injects content into src/bootstrap_template.ipynb
to generate claude_code_colab_bootstrap.ipynb
"""

import json
from pathlib import Path


def read_file(path):
    """Read a file and return its content."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def escape_for_python_string(content, use_triple_quotes=False):
    """Escape content for use in a Python string literal."""
    if use_triple_quotes:
        # For triple-quoted strings, only escape backslashes and the closing quote sequence
        content = content.replace("\\", "\\\\")
        content = content.replace("'''", "\\'\\'\\'")
        return content
    else:
        # For single-quoted strings, escape backslashes, quotes, and newlines
        content = content.replace("\\", "\\\\")
        content = content.replace("'", "\\'")
        content = content.replace("\n", "\\n")
        return content


def build_notebook():
    """Build the final notebook from template and source files."""

    # Read template
    template_path = Path("src/bootstrap_template.ipynb")
    with open(template_path, "r") as f:
        notebook = json.load(f)

    # Read guide
    guide_content = read_file("src/guide.md")

    # Read hooks
    markdown_formatter = read_file("src/hooks/markdown_formatter.py")
    statusline_script = read_file("src/hooks/statusline.py")

    # Read update_docs script and manifest (for notebook cell)
    update_docs_script = read_file("update_docs.py")
    docs_manifest = json.loads(read_file("src/docs_manifest.json"))

    # Read skills
    skills_dir = Path("src/skills")
    skills = {}
    for skill_file in sorted(skills_dir.glob("*.md")):  # Sort for deterministic order
        skill_name = skill_file.stem
        skills[skill_name] = read_file(skill_file)

    # Read agents
    agents_dir = Path("src/agents")
    agents = {}
    for agent_file in sorted(agents_dir.glob("*.md")):  # Sort for deterministic order
        agent_name = agent_file.stem
        agents[agent_name] = read_file(agent_file)

    # Convert skills and agents to Python dict string format
    def dict_to_python_string(d):
        """Convert a dict to a Python string representation."""
        items = []
        # Sort keys for deterministic output
        for key in sorted(d.keys()):
            value = d[key]
            # Escape the value for Python string
            escaped_value = escape_for_python_string(value)
            items.append(f"'{key}': '{escaped_value}'")
        return "{" + ", ".join(items) + "}"

    skills_dict_str = dict_to_python_string(skills)
    agents_dict_str = dict_to_python_string(agents)

    # Replace placeholders in notebook cells
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            # Join source lines
            source = "".join(cell["source"])

            # Replace all placeholders
            source = source.replace("{{GUIDE_CONTENT}}", escape_for_python_string(guide_content))
            source = source.replace(
                "{{MARKDOWN_FORMATTER_HOOK}}",
                escape_for_python_string(markdown_formatter, use_triple_quotes=True),
            )
            source = source.replace(
                "{{STATUSLINE_HOOK}}",
                escape_for_python_string(statusline_script, use_triple_quotes=True),
            )
            source = source.replace(
                "{{UPDATE_DOCS_SCRIPT}}",
                escape_for_python_string(update_docs_script, use_triple_quotes=True),
            )
            source = source.replace("{{DOCS_MANIFEST_JSON}}", json.dumps(docs_manifest, indent=2))
            source = source.replace("{{SKILLS_DICT}}", skills_dict_str)
            source = source.replace("{{AGENTS_DICT}}", agents_dict_str)

            # Convert back to list format (each line is a string ending with \n except possibly the last)
            lines = source.split("\n")
            cell["source"] = [
                line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)
            ]

    # Write final notebook
    output_dir = Path("dist")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "claude_code_colab_bootstrap.ipynb"
    with open(output_path, "w") as f:
        json.dump(notebook, f, indent=2)

    print(f"✓ Built {output_path}")
    print(f"  - {len(skills)} skills")
    print(f"  - {len(agents)} agents")
    print(f"  - Guide: {len(guide_content)} chars")
    print("  - Hooks: markdown_formatter, statusline")


if __name__ == "__main__":
    build_notebook()
