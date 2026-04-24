# Chapter 7: Deployment View

## 7.1 Overview

Minesweeper is a single-process CLI application. There is no server, database, or cloud infrastructure. The project is deployed and validated locally via Docker (localhost container execution), with optional direct local execution via Python.

## 7.2 Deployment Diagram (C4 Level)

![Deployment Diagram](diagrams/deployment.svg)

Diagram source: `docs/architecture/diagrams/deployment.puml`

## 7.3 How to Run

```bash
# From the project root
docker build -t minesweeper .
docker run --rm minesweeper

# Optional interactive run
docker run --rm -it minesweeper python minesweeper/cli.py --seed 42

# Optional direct local run (without Docker)
python3 minesweeper/cli.py --seed 42
```

## 7.4 Runtime Requirements

| Requirement        | Value              |
|--------------------|--------------------|
| Python version     | 3.12+              |
| Container runtime  | Docker             |
| External packages  | None for gameplay runtime (stdlib only) |
| OS                 | Any (Linux, macOS, Windows) |
| Persistent storage | None               |
