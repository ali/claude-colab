---
name: Optimize CI Docker
overview: Reduce CI minutes by ~50% through job consolidation, aggressive caching (uv + Docker layers), and slimming down the test Docker image.
todos:
  - id: consolidate-jobs
    content: Merge lint-and-format + build jobs into single build job in ci.yml
    status: in_progress
  - id: uv-caching
    content: "Enable built-in uv caching via enable-cache: true in both workflows"
    status: pending
  - id: docker-caching
    content: Add Docker layer caching using docker/build-push-action with GHA cache
    status: pending
  - id: slim-dockerfile
    content: "Optimize Dockerfile: --no-install-recommends, nbconvert only, single RUN layer"
    status: pending
  - id: dockerignore
    content: Create tests/.dockerignore to minimize build context
    status: pending
  - id: artifact-passing
    content: Pass built notebook artifact from build to test-execution job
    status: pending
---

# Optimize Docker Container and GitHub Actions

## Current State Analysis

**CI Workflow Issues:**

- 3 separate jobs each doing full setup (checkout, uv install, Python setup, deps install)
- Docker image rebuilt from scratch on every run (no layer caching)
- No uv dependency caching
- `test-execution` rebuilds notebook that `build` already built

**Dockerfile Issues:**

- Installs full `jupyter` when only `nbconvert` is needed
- No `.dockerignore` - sends entire repo as build context
- Separate apt/pip layers when they could be combined

**Estimated Savings:**

- Job consolidation: ~2-3 min saved per run
- uv caching: ~30-60s saved per job
- Docker layer caching: ~2-3 min saved when image unchanged
- Slim Docker image: ~1 min faster build, less storage

---

## Changes

### 1. Consolidate `lint-and-format` + `build` into Single Job

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) - Merge these jobs since lint is fast and blocking on failure is fine:

```yaml
jobs:
  build:
    name: Build Notebook
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: astral-sh/setup-uv@v7
        with:
          version: "latest"
          enable-cache: true  # Built-in uv caching
      - uses: actions/setup-python@v6
        with:
          python-version: "3.11"
      - run: uv sync --extra dev
      - run: uv run ruff format --check .
      - run: uv run ruff check .
      - run: uv run python build.py
      # ... rest of build steps
      - uses: actions/upload-artifact@v6
        with:
          name: notebook
          path: claude_code_colab_bootstrap.ipynb
          retention-days: 1
```

### 2. Add Docker Layer Caching to `test-execution`

Use GitHub Actions cache with Docker buildx:

```yaml
test-execution:
  needs: build  # Wait for build, download artifact
  steps:
    - uses: actions/checkout@v6
    - uses: actions/download-artifact@v6
      with:
        name: notebook
    - uses: docker/setup-buildx-action@v3
    - uses: docker/build-push-action@v6
      with:
        context: ./tests
        file: ./tests/Dockerfile.test
        tags: claude-colab-test:latest
        load: true
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### 3. Slim Down Dockerfile

[`tests/Dockerfile.test`](tests/Dockerfile.test):

```dockerfile
FROM python:3.11-slim

# Single layer: system deps + Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    socat bubblewrap git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir nbconvert ipykernel \
    && rm -rf /root/.cache

WORKDIR /workspace
CMD ["python", "--version"]
```

**Key changes:**

- `--no-install-recommends` reduces apt packages
- `nbconvert ipykernel` instead of full `jupyter` (~50MB smaller)
- Combined into single RUN for smaller layer

### 4. Add `.dockerignore`

Create [`tests/.dockerignore`](tests/.dockerignore):

```
# Only copy what's needed for the Docker build
*
!Dockerfile.test
```

This reduces build context from ~1MB to ~1KB since the Dockerfile doesn't COPY anything.

### 5. Apply uv Caching to Release Workflow

[`.github/workflows/release.yml`](.github/workflows/release.yml):

```yaml
- uses: astral-sh/setup-uv@v7
  with:
    version: "latest"
    enable-cache: true
```

Also remove `fetch-depth: 0` since we get the tag from `$GITHUB_REF` or input.

### 6. Conditional Docker Tests (Optional)

Skip expensive Docker tests on PRs that only change docs:

```yaml
test-execution:
  if: |
    github.ref == 'refs/heads/main' || 
    contains(github.event.pull_request.labels.*.name, 'test-docker')
```

---

## Summary of Expected Savings

| Optimization | Minutes Saved |

|-----|---|

| Job consolidation | ~2 min |

| uv caching | ~1 min |

| Docker layer caching | ~3 min (when cached) |

| Slim Docker image | ~1 min |

| **Total per run** | **~4-7 min** |

Space savings: ~50MB smaller Docker image, reduced cache storage.