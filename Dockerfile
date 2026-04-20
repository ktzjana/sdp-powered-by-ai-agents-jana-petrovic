FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir pytest

COPY tests/ tests/

CMD ["pytest", "tests/", "-v", "--tb=short"]
