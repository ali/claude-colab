# Notebook Tests

This directory contains tests for the built notebook.

## Test Structure

- **`test_notebook.py`**: Fast validation tests that check:
  - Notebook JSON structure validity
  - All placeholders were replaced
  - Required content exists (skills, agents, guide, hooks)
  - Content is not empty

- **`test_notebook_execution.py`**: Docker-based execution tests that:
  - Execute the notebook in an isolated Docker container
  - Verify all cells run without errors
  - Test with and without authentication tokens
  - Check that expected files are created

## Running Tests

### Quick Tests (No Docker Required)

```bash
# Run all fast validation tests
uv run pytest tests/test_notebook.py -v

# Or just pytest if you're in the venv
pytest tests/test_notebook.py -v
```

### Execution Tests (Requires Docker)

```bash
# Run Docker-based execution tests
uv run pytest tests/test_notebook_execution.py -v -m docker

# Test without authentication token (default)
uv run pytest tests/test_notebook_execution.py::test_notebook_execution_without_token -v -m docker

# Test with authentication token (if you have one)
CLAUDE_CODE_OAUTH_TOKEN=your_token_here uv run pytest tests/test_notebook_execution.py::test_notebook_executes_in_docker -v -m docker
```

### All Tests

```bash
# Run all tests (skips Docker tests if Docker unavailable)
uv run pytest tests/ -v

# Run all tests including Docker (fails if Docker unavailable)
uv run pytest tests/ -v -m docker
```

## Docker Test Environment

The Docker tests use `tests/Dockerfile.test` which creates a Colab-like environment:
- Python 3.11
- System dependencies (socat, bubblewrap, git)
- Jupyter and nbconvert for executing notebooks

The Docker image is built automatically on first run and cached for subsequent tests.

## Authentication

**Authentication is optional for tests.** The notebook is designed to work without a token:
- Without token: Notebook runs successfully, but authentication is not configured
- With token: Set `CLAUDE_CODE_OAUTH_TOKEN` environment variable to test with authentication

The tests verify that the notebook handles both cases gracefully.

## CI Integration

- **Fast tests** (`test_notebook.py`) run in every CI build
- **Execution tests** (`test_notebook_execution.py`) run on main branch and PRs, but don't fail the build if Docker is unavailable

## Troubleshooting

### Docker tests fail with "Docker not found"
- Install Docker: https://docs.docker.com/get-docker/
- Ensure Docker daemon is running: `docker ps`

### Notebook execution times out
- Increase timeout in `test_notebook_execution.py` (default: 900 seconds)
- Check network connectivity (notebook installs packages from PyPI)

### Tests fail with "nbconvert not available"
- Install dev dependencies: `uv sync --extra dev`
- Or install manually: `pip install jupyter nbconvert`
