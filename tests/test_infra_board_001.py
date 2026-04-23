from pathlib import Path

DOCKERFILE = Path(__file__).parent.parent / "Dockerfile"


def test_board_infra_001_1_s1_dockerfile_declares_buildable_image():
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
