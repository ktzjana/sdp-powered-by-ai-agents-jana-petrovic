from pathlib import Path

DOCKERFILE = Path(__file__).parent.parent / "Dockerfile"


def test_cli_infra_001_1_s1_dockerfile_declares_buildable_image():
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


def test_cli_infra_001_2_s1_dockerfile_installs_pytest():
    # GIVEN - the Docker image has been built successfully

    content = DOCKERFILE.read_text()

    # WHEN / THEN - pytest is installed via pip inside the container
    assert "pip install" in content
    assert "pytest" in content


def test_cli_infra_001_3_s1_cli_module_is_importable():
    # GIVEN - the project is available inside the container

    cli_path = Path(__file__).parent.parent / "minesweeper" / "cli.py"
    assert cli_path.exists(), "minesweeper/cli.py not found"

    import importlib.util

    # WHEN / THEN - cli.py loads without ImportError
    spec = importlib.util.spec_from_file_location("minesweeper.cli", cli_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_cli_infra_001_4_s1_input_parser_test_module_is_discoverable():
    # GIVEN - the tests/ directory exists in the project

    # WHEN / THEN - an input parsing test file exists for pytest to discover
    assert (
        Path(__file__).parent / "test_input_parser.py"
    ).exists(), "tests/test_input_parser.py not found"


def test_cli_infra_001_4_s2_repository_supports_pytest_discovery_inside_docker():
    # GIVEN - the repository root and tests/ directory
    tests_dir = Path(__file__).parent
    content = DOCKERFILE.read_text()

    # WHEN / THEN - structure required for pytest discovery inside Docker is present
    assert tests_dir.exists()
    assert (tests_dir / "test_infra_cli_001.py").exists()
    assert (tests_dir / "test_input_parser.py").exists()
    assert "COPY tests/" in content
    assert "pytest" in content
    assert "tests/" in content
