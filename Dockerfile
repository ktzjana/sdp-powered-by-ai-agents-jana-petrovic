FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY pyproject.toml .
RUN pip install --no-cache-dir pytest

COPY Dockerfile .
COPY minesweeper/ minesweeper/
COPY tests/ tests/

CMD ["pytest", "tests/", "-v", "--tb=short"]
