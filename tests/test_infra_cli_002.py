from pathlib import Path

DOCKERFILE = Path(__file__).parent.parent / "Dockerfile"


def test_cli_infra_002_1_s1_dockerfile_declares_buildable_image():
    # GIVEN - a Dockerfile exists at the project root using a Python base image

    assert DOCKERFILE.exists(), "Dockerfile not found"
    content = DOCKERFILE.read_text()

    # WHEN / THEN - it declares a valid buildable image
    assert "FROM python" in content
    assert "WORKDIR /app" in content
    assert "PYTHONPATH=/app" in content
    assert "COPY minesweeper/" in content
    assert "COPY tests/" in content
    assert "pytest" in content


def test_cli_infra_002_2_s1_dockerfile_installs_pytest():
    # GIVEN - the Docker image has been built successfully

    content = DOCKERFILE.read_text()

    # WHEN / THEN - pytest is installed via pip inside the container
    assert "pip install" in content
    assert "pytest" in content


def test_cli_infra_002_3_s1_cli_module_is_importable():
    # GIVEN - the project is available inside the container

    cli_path = Path(__file__).parent.parent / "minesweeper" / "cli.py"
    assert cli_path.exists(), "minesweeper/cli.py not found"

    import importlib.util

    # WHEN / THEN - cli.py loads without ImportError
    spec = importlib.util.spec_from_file_location("minesweeper.cli", cli_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
