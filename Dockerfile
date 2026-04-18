FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir pytest

COPY . .

CMD ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]
