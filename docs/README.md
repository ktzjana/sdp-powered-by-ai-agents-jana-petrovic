# Minesweeper Kata

A terminal-based Minesweeper kata implemented as the final end-to-end project
for the Software Development Processes Powered by AI Agents course. The project
demonstrates AI-assisted requirements analysis, architecture design, TDD/BDD
implementation, CI/CD validation, and Sphinx-based documentation.

## What The Kata Solves

This kata implements the core Minesweeper gameplay loop:

- generate a board with random mine placement
- reveal cells and flood-fill empty regions
- flag and unflag suspected mines
- detect win and loss conditions
- render the game clearly in the terminal

## Tech Stack And Architecture Overview

- Python 3.12
- Pytest for automated testing
- Docker for reproducible local build and test execution
- GitHub Actions for CI and documentation deployment
- Sphinx + MyST for project documentation
- arc42 and C4/sequence diagrams for architecture documentation

Architecture is organized into three main layers:

- `BOARD` domain: board state, mine placement, adjacent counts, reveal logic
- `GAME` controller: gameplay orchestration, win/loss transitions
- `CLI` presentation: command parsing and terminal rendering

## Build And Run Locally

Run the game directly:

```bash
python3 minesweeper/cli.py
```

Run with a fixed seed for deterministic behavior:

```bash
python3 minesweeper/cli.py --seed 42
```

Build and run tests with Docker:

```bash
docker build -t minesweeper .
docker run --rm minesweeper
```

Run the game from the Docker image:

```bash
docker run --rm -it minesweeper python minesweeper/cli.py --seed 42
```

Gameplay commands:

- `r <row> <col>` reveals a cell, for example `r 0 0`
- `f <row> <col>` toggles a flag on a cell, for example `f 1 3`
- `q` quits the game

## Run Tests

Run the full local test suite:

```bash
python3 -m pytest -v
```

The Docker image is also configured to run the full test suite by default:

```bash
docker run --rm minesweeper
```

## Documentation Site

Live Sphinx documentation:

https://ktzjana.github.io/sdp-powered-by-ai-agents-jana-petrovic/

## Project Structure

```text
.
├── .github/workflows/       # CI and docs deployment workflows
├── docs/                    # Sphinx site, architecture docs, user stories
│   ├── architecture/        # arc42 chapters and diagrams
│   └── user-stories/        # story inventory and story bundles
├── minesweeper/             # application source code
├── tests/                   # pytest test suite
├── Dockerfile               # containerized test/runtime setup
└── README.md                # project overview
```

## Author

Jana Petrovic
