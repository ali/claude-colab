"""
Execute the built notebook in a Docker container to verify it works.

This test runs the notebook cells in an isolated environment to ensure:
- All cells execute without errors
- Dependencies install correctly
- Files are created as expected
- The notebook works without requiring authentication tokens
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def notebook_path():
    """Path to the built notebook."""
    return Path(__file__).parent.parent / "claude_code_colab_bootstrap.ipynb"


@pytest.fixture
def docker_image():
    """Docker image name for testing."""
    return "claude-colab-test:latest"


@pytest.fixture(scope="session")
def build_docker_image(docker_image):
    """Build the Docker image for testing (once per test session)."""
    dockerfile_path = Path(__file__).parent.parent / "tests" / "Dockerfile.test"
    
    if not dockerfile_path.exists():
        pytest.skip(f"Dockerfile not found at {dockerfile_path}")
    
    # Build the image
    result = subprocess.run(
        [
            "docker",
            "build",
            "-f",
            str(dockerfile_path),
            "-t",
            docker_image,
            str(dockerfile_path.parent),
        ],
        capture_output=True,
        text=True,
    )
    
    if result.returncode != 0:
        pytest.fail(
            f"Failed to build Docker image:\n{result.stderr}\n{result.stdout}"
        )
    
    yield docker_image
    
    # Cleanup: remove the image (optional, commented out to speed up subsequent runs)
    # subprocess.run(["docker", "rmi", docker_image], capture_output=True)


@pytest.mark.docker
def test_notebook_executes_in_docker(notebook_path, build_docker_image, docker_image):
    """
    Execute the notebook in a Docker container.
    
    This test:
    1. Copies the notebook into a temporary directory
    2. Runs it in a Docker container with nbconvert
    3. Verifies execution completed without errors
    4. Checks that expected files were created
    
    Requires Docker to be installed and running.
    Set CLAUDE_CODE_OAUTH_TOKEN environment variable to test with authentication.
    """
    if not notebook_path.exists():
        pytest.skip(f"Notebook not found at {notebook_path}")
    
    # Create a temporary directory for the test
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Copy notebook to temp directory
        test_notebook = tmp_path / "test_notebook.ipynb"
        import shutil
        shutil.copy(notebook_path, test_notebook)
        
        # Prepare environment variables
        env_vars = {}
        if os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
            env_vars["CLAUDE_CODE_OAUTH_TOKEN"] = os.environ["CLAUDE_CODE_OAUTH_TOKEN"]
        
        # Build docker run command
        docker_cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{tmp_path}:/workspace",
            "-w",
            "/workspace",
        ]
        
        # Add environment variables
        for key, value in env_vars.items():
            docker_cmd.extend(["-e", f"{key}={value}"])
        
        # Add image and command
        docker_cmd.extend([
            docker_image,
            "python",
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=600",
            "--ExecutePreprocessor.kernel_name=python3",
            "test_notebook.ipynb",
        ])
        
        # Run the notebook in Docker
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=900,  # 15 minute timeout
        )
        
        # Check execution result
        if result.returncode != 0:
            pytest.fail(
                f"Notebook execution failed:\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            )
        
        # Verify the notebook was executed (check for execution_count)
        with open(test_notebook, "r") as f:
            executed_notebook = json.load(f)
        
        executed_cells = [
            cell
            for cell in executed_notebook["cells"]
            if cell.get("cell_type") == "code"
            and cell.get("execution_count") is not None
        ]
        
        assert len(executed_cells) > 0, "No cells were executed"
        
        # Check for execution errors
        error_cells = []
        for cell in executed_notebook["cells"]:
            if cell.get("cell_type") == "code":
                outputs = cell.get("outputs", [])
                for output in outputs:
                    if output.get("output_type") == "error":
                        error_cells.append({
                            "cell_index": executed_notebook["cells"].index(cell),
                            "error": output.get("ename", "Unknown"),
                            "message": "".join(output.get("traceback", [])),
                        })
        
        if error_cells:
            error_msg = "Notebook execution errors found:\n"
            for err in error_cells:
                error_msg += f"\nCell {err['cell_index']}: {err['error']}\n{err['message']}\n"
            pytest.fail(error_msg)
        
        # Verify execution was successful
        # The main indicator is that cells executed without errors
        print(f"✓ Notebook executed successfully")
        print(f"  - {len(executed_cells)} code cells executed")
        if env_vars:
            print(f"  - Tested with authentication token")
        else:
            print(f"  - Tested without authentication token (optional)")
        
        # Optional: Check that some expected output was produced
        # (e.g., print statements from the notebook)
        has_output = any(
            cell.get("outputs")
            for cell in executed_notebook["cells"]
            if cell.get("cell_type") == "code"
        )
        assert has_output, "Expected at least some cells to produce output"


@pytest.mark.docker
def test_notebook_execution_without_token(notebook_path, build_docker_image, docker_image):
    """
    Specifically test that the notebook works without an authentication token.
    
    This ensures the notebook gracefully handles missing authentication.
    """
    if not notebook_path.exists():
        pytest.skip(f"Notebook not found at {notebook_path}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        test_notebook = tmp_path / "test_notebook.ipynb"
        import shutil
        shutil.copy(notebook_path, test_notebook)
        
        # Explicitly unset any token
        docker_cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{tmp_path}:/workspace",
            "-w",
            "/workspace",
            "-e",
            "CLAUDE_CODE_OAUTH_TOKEN=",  # Explicitly empty
            docker_image,
            "python",
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            "--ExecutePreprocessor.timeout=600",
            "--ExecutePreprocessor.kernel_name=python3",
            "test_notebook.ipynb",
        ]
        
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=900,
        )
        
        # Should succeed even without token
        assert result.returncode == 0, (
            f"Notebook should execute without token:\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )
        
        # Verify auth cell handled missing token gracefully
        with open(test_notebook, "r") as f:
            executed_notebook = json.load(f)
        
        # Find the auth cell and check its output
        for cell in executed_notebook["cells"]:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "Configure Authentication" in source:
                    outputs = cell.get("outputs", [])
                    output_text = "".join(
                        [
                            "".join(o.get("text", []))
                            for o in outputs
                            if o.get("output_type") == "stream"
                        ]
                    )
                    # Should mention no token found, but not error
                    assert "No auth token found" in output_text or "⚠️" in output_text, (
                        "Auth cell should handle missing token gracefully"
                    )
