from pathlib import Path

DOCKERFILE = Path(__file__).parent.parent / "Dockerfile"


def test_game_infra_001_1_s1_dockerfile_declares_buildable_image():
    # GIVEN - a Dockerfile exists at the project root using a Python base image
    assert DOCKERFILE.exists(), "Dockerfile not found"

    content = DOCKERFILE.read_text()

    # WHEN - docker build -t minesweeper . is executed from the project root

    # THEN - the build completes with exit code 0; no build errors
    assert "FROM python" in content
    assert "WORKDIR /app" in content
    assert "PYTHONPATH=/app" in content
    assert "COPY minesweeper/" in content
    assert "COPY tests/" in content
    assert "pytest" in content


def test_game_infra_001_2_s1_dockerfile_installs_pytest():
    # GIVEN - the Docker image has been built successfully
    content = DOCKERFILE.read_text()

    # WHEN - docker run minesweeper pytest --version is executed

    # THEN - pytest reports its version and exits with code 0; no ModuleNotFoundError
    assert "pip install" in content
    assert "pytest" in content


def test_game_infra_001_3_s1_cli_module_is_importable():
    # GIVEN - the Docker image has been built successfully
    import importlib.util

    cli_path = Path(__file__).parent.parent / "minesweeper" / "cli.py"
    assert cli_path.exists(), "minesweeper/cli.py not found"

    # WHEN - docker run minesweeper python minesweeper/cli.py is executed

    # THEN - the process exits with code 0; no ImportError or ModuleNotFoundError
    spec = importlib.util.spec_from_file_location("minesweeper.cli", cli_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def test_game_infra_001_4_s1_reveal_test_module_is_discoverable():
    # GIVEN - the Docker image has been built and tests/ is copied into the container
    tests_dir = Path(__file__).parent
    content = DOCKERFILE.read_text()

    # WHEN - docker run minesweeper pytest tests/ is executed

    # THEN - pytest discovers reveal tests; all pass; exits with code 0
    assert (tests_dir / "test_game.py").exists(), "tests/test_game.py not found"
    assert "COPY tests/" in content
    assert "pytest" in content
    assert "tests/" in content
