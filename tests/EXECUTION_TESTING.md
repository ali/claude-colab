# Notebook Execution Testing

This document describes the Docker-based execution testing setup for the built notebook.

## Overview

The execution tests run the notebook in an isolated Docker container to verify:
- All cells execute without errors
- Dependencies install correctly
- Files are created as expected
- The notebook works with and without authentication tokens

## Architecture

### Test Environment

The tests use a Docker container based on `tests/Dockerfile.test` which provides:
- Python 3.11 (matching Colab's Python version)
- System dependencies: `socat`, `bubblewrap`, `git`
- Jupyter and nbconvert for executing notebooks

### Test Flow

1. **Build Docker image** (cached after first run)
2. **Copy notebook** to temporary directory
3. **Execute notebook** using `jupyter nbconvert --execute`
4. **Verify results**:
   - Check execution_count on cells (proves they ran)
   - Check for error outputs
   - Verify expected output was produced

## Authentication Handling

**Authentication is optional.** The notebook is designed to work without a token:

- **Without token**: Notebook runs successfully, authentication cell prints a warning but doesn't fail
- **With token**: Set `CLAUDE_CODE_OAUTH_TOKEN` environment variable to test with authentication

The tests include:
- `test_notebook_executes_in_docker`: General execution test (uses token if provided)
- `test_notebook_execution_without_token`: Explicitly tests without token

## Google Drive Handling

The notebook defaults to `USE_GOOGLE_DRIVE = False` (ephemeral mode), which:
- Doesn't require Google Drive mounting
- Works perfectly in Docker
- Creates files in `/content/claude-workspaces/` instead of Drive

The notebook gracefully handles missing `google.colab` module (catches `ImportError`).

## Running Tests

### Prerequisites

- Docker installed and running
- Dev dependencies: `uv sync --extra dev`

### Basic Usage

```bash
# Run all execution tests
uv run pytest tests/test_notebook_execution.py -v -m docker

# Test without token (default)
uv run pytest tests/test_notebook_execution.py::test_notebook_execution_without_token -v -m docker

# Test with token (if you have one)
CLAUDE_CODE_OAUTH_TOKEN=your_token uv run pytest tests/test_notebook_execution.py::test_notebook_executes_in_docker -v -m docker
```

### CI Integration

The execution tests run in CI on:
- Main branch pushes
- Pull requests

They don't fail the build if Docker is unavailable (graceful degradation).

## Troubleshooting

### "Docker not found"
- Install Docker: https://docs.docker.com/get-docker/
- Ensure Docker daemon is running: `docker ps`

### "Failed to build Docker image"
- Check Dockerfile syntax
- Ensure Docker has sufficient resources
- Try: `docker system prune` to free space

### "Notebook execution timeout"
- Default timeout: 900 seconds (15 minutes)
- Increase in test if needed
- Check network connectivity (installs packages from PyPI)

### "ImportError: google.colab"
- This is expected and handled gracefully
- The notebook catches this and continues

### "No cells were executed"
- Check that nbconvert is installed in Docker image
- Verify notebook JSON is valid
- Check Docker logs: `docker logs <container_id>`

## Test Customization

### Adjusting Timeout

Edit `test_notebook_execution.py`:
```python
timeout=900,  # Change this value (seconds)
```

### Adding Environment Variables

Add to `docker_cmd` in test:
```python
docker_cmd.extend(["-e", "MY_VAR=value"])
```

### Testing Different Python Versions

Edit `tests/Dockerfile.test`:
```dockerfile
FROM python:3.10-slim  # Change version
```

## Future Enhancements

Potential improvements:
- [ ] Test with different Python versions
- [ ] Test with USE_GOOGLE_DRIVE=True (mock Drive API)
- [ ] Verify specific file contents after execution
- [ ] Test notebook in actual Colab environment (integration test)
- [ ] Performance benchmarks (execution time tracking)
