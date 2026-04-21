# BOARD Domain Stories

## BOARD-STORY-001

**AS A** player
**I WANT** the game to generate a grid of configurable size with randomly placed mines
**SO THAT** each game session presents a unique and unpredictable challenge

**Architecture Reference:** Chapter 1 Introduction and Goals — FR-1, Chapter 5 Building Block View — Board, MinePlacer

---

### BOARD-STORY-001-S1: Board is initialised with the correct dimensions

**GIVEN**

* the player starts the game with grid size 5 rows × 5 columns and 3 mines

**WHEN**

* the board is created

**THEN**

* the grid contains exactly 25 cells
* every cell starts in an unrevealed, unflagged state

---

### BOARD-STORY-001-S2: Mines are placed randomly on the board

**GIVEN**

* the board has been initialised with size 5 × 5 and 3 mines

**WHEN**

* mine placement runs

**THEN**

* exactly 3 cells are marked as mines
* mine positions differ between runs with different random seeds (ADR-004)

---

### BOARD-STORY-001-S3: Adjacent mine counts are computed correctly after placement

**GIVEN**

* mines have been placed on the board

**WHEN**

* mine placement completes

**THEN**

* every safe cell holds an `adjacent_count` equal to the number of its neighbouring cells that contain a mine
* mine cells are not assigned an adjacent count

---

### BOARD-STORY-001-S4: End-to-end board initialization

**GIVEN**

* the player starts a new game with grid size 5 × 5 and 3 mines

**WHEN**

* the game initializes completely through the CLI

**THEN**

* the board is created with exactly 25 cells
* exactly 3 mines are placed on the board
* all safe cells have correct `adjacent_count` values
* the initial board is rendered in the terminal with all cells hidden

---

## FE Sub-Stories

> Note: this project has no graphical frontend. The CLI layer (`cli.py`) acts as the presentation layer and is treated as the FE equivalent.

### BOARD-FE-001.1

**AS A** player
**I WANT** the initial board to be displayed in the terminal after the game starts
**SO THAT** I can see the grid before making my first move

**Architecture Reference:** Chapter 5 Building Block View — BoardRenderer, Chapter 6 Runtime View — Reveal a Cell

#### BOARD-FE-001.1-S1: Initial board renders all cells as hidden

**GIVEN**

* the board has been initialised and no cells have been revealed

**WHEN**

* the board renderer prints the current game state

**THEN**

* every cell appears as the hidden symbol (e.g. `.` or `#`)
* the grid dimensions match the configured size

---

## BE Sub-Stories

### BOARD-BE-001.1

**AS A** developer
**I WANT** the Board to be initialised with the specified number of rows, columns, and mines
**SO THAT** the game state is correctly set up before the first player action

**Architecture Reference:** Chapter 5 Building Block View — Board, MinePlacer

#### BOARD-BE-001.1-S1: Board constructor creates a grid of the correct size

**GIVEN**

* rows = 4, cols = 4, mines = 2 are provided as constructor arguments

**WHEN**

* a `Board` instance is created

**THEN**

* `board.rows == 4` and `board.cols == 4`
* the grid contains 16 `Cell` objects
* all cells have `revealed = False` and `flagged = False`

---

### BOARD-BE-001.2

**AS A** developer
**I WANT** `MinePlacer` to distribute exactly the requested number of mines across the grid
**SO THAT** the mine count is always consistent with the game configuration

**Architecture Reference:** Chapter 5 Building Block View — MinePlacer, Chapter 9 Architecture Decisions — ADR-004

#### BOARD-BE-001.2-S1: Exactly N mines are placed on the board

**GIVEN**

* a 5 × 5 board is initialised with 5 mines

**WHEN**

* `MinePlacer` runs

**THEN**

* exactly 5 cells have `is_mine = True`
* no cell is marked as a mine more than once

#### BOARD-BE-001.2-S2: Mine placement is reproducible with a fixed seed

**GIVEN**

* `random.seed(42)` is set before board initialisation (ADR-004)
* a 5 × 5 board is created with 3 mines

**WHEN**

* `MinePlacer` runs twice using the same seed

**THEN**

* the mine positions are identical in both runs

---

### BOARD-BE-001.3

**AS A** developer
**I WANT** each safe cell to have its `adjacent_count` set to the correct value after mine placement
**SO THAT** reveal logic can display accurate neighbour information to the player

**Architecture Reference:** Chapter 5 Building Block View — MinePlacer, Chapter 5 Building Block View — Cell

#### BOARD-BE-001.3-S1: Interior safe cell gets the correct adjacent mine count

**GIVEN**

* a board where a safe cell at position (2, 2) has 2 neighbouring mines

**WHEN**

* `MinePlacer` completes

**THEN**

* `board.cell(2, 2).adjacent_count == 2`

#### BOARD-BE-001.3-S2: Corner safe cell considers only valid neighbours

**GIVEN**

* a board where the safe cell at position (0, 0) has 1 neighbouring mine at (0, 1)

**WHEN**

* `MinePlacer` completes

**THEN**

* `board.cell(0, 0).adjacent_count == 1`
* no out-of-bounds positions are accessed

---

## INFRA Sub-Stories

### BOARD-INFRA-001.1 — Dockerfile Build

**AS A** developer
**I WANT** the project to build successfully inside a Docker container
**SO THAT** the execution environment is reproducible on any machine with Docker installed

**Architecture Reference:** Chapter 7 Deployment View — 7.3 How to Run, 7.4 Runtime Requirements; Chapter 9 Architecture Decisions — ADR-003

#### BOARD-INFRA-001.1-S1: Dockerfile builds without errors

**GIVEN**

* a `Dockerfile` exists at the project root
* the `Dockerfile` uses a `python:3.10` (or later) base image
* the project source is copied into the image

**WHEN**

* `docker build -t minesweeper .` is executed from the project root

**THEN**

* the build completes with exit code 0
* no build errors or missing-file errors are reported

---

### BOARD-INFRA-001.2 — Dependency Installation Inside Container

**AS A** developer
**I WANT** all required dependencies to be installed correctly inside the Docker container
**SO THAT** the application and test suite can run without missing-module errors

**Architecture Reference:** Chapter 7 Deployment View — 7.4 Runtime Requirements; Chapter 2 Architecture Constraints — TC-4

> **Applicability note:** The architecture specifies stdlib-only runtime dependencies (TC-4). The container must still install `pytest` for test execution. No other third-party packages are required.

#### BOARD-INFRA-001.2-S1: pytest is available inside the container after build

**GIVEN**

* the Docker image has been built successfully

**WHEN**

* `docker run minesweeper pytest --version` is executed

**THEN**

* pytest reports its version and exits with code 0
* no `ModuleNotFoundError` is raised

---

### BOARD-INFRA-001.3 — Project Build Inside Container

**AS A** developer
**I WANT** the project to be importable and executable inside the Docker container
**SO THAT** the game can be launched and tested without host-machine Python

**Architecture Reference:** Chapter 5 Building Block View — Board, MinePlacer; Chapter 7 Deployment View — 7.3 How to Run

#### BOARD-INFRA-001.3-S1: Game launches inside the container without import errors

**GIVEN**

* the Docker image has been built successfully

**WHEN**

* `docker run minesweeper python minesweeper/cli.py --help` (or equivalent smoke-run with piped EOF) is executed

**THEN**

* the process exits with code 0
* no `ImportError` or `ModuleNotFoundError` is printed to stdout or stderr

---

### BOARD-INFRA-001.4 — Test Suite Execution via pytest Inside Container

**AS A** developer
**I WANT** the full test suite to run successfully inside the Docker container via pytest
**SO THAT** board initialisation logic is verified in the containerised environment

**Architecture Reference:** Chapter 7 Deployment View — 7.3 How to Run; Chapter 2 Architecture Constraints — OC-2; Chapter 5 Building Block View — Board, MinePlacer

#### BOARD-INFRA-001.4-S1: pytest discovers and runs board tests inside the container

**GIVEN**

* the Docker image has been built successfully
* test files for board initialisation exist under a `tests/` directory at the project root

**WHEN**

* `docker run minesweeper pytest tests/` is executed

**THEN**

* pytest discovers at least the board-related test files
* all discovered tests pass
* pytest exits with code 0

#### BOARD-INFRA-001.4-S2: Repository structure supports pytest discovery inside Docker

**GIVEN**

* the Docker image has been built and the working directory is set to the project root inside the container

**WHEN**

* `docker run minesweeper pytest --collect-only` is executed

**THEN**

* pytest collects test items without "no tests ran" or collection errors
* the collected items include board initialisation tests

---

## Implementation Order

The story is implemented following the backend-first approach:

1. **INFRA** — build container, verify dependencies, confirm project runs, and execute tests inside Docker

   * BOARD-INFRA-001.1 (Dockerfile build)
   * BOARD-INFRA-001.2 (dependency installation)
   * BOARD-INFRA-001.3 (project build / launch inside container)
   * BOARD-INFRA-001.4 (test suite via pytest inside container)

2. **BE** — implement core domain logic and services

   * BOARD-BE-001.1
   * BOARD-BE-001.2
   * BOARD-BE-001.3

3. **FE (CLI)** — render board state to the user

   * BOARD-FE-001.1

4. **E2E Verification** — validate the complete story

   * BOARD-STORY-001 (all scenarios)

---

## Traceability Verification

| Scenario ID          | Architecture Reference                                        | Parent Story      | Testable Assertion                                                    |
| -------------------- | ------------------------------------------------------------- | ----------------- | --------------------------------------------------------------------- |
| BOARD-STORY-001-S1   | Chapter 1 FR-1, Chapter 5 Building Block View — Board         | BOARD-STORY-001   | grid contains exactly rows×cols cells, all unrevealed and unflagged   |
| BOARD-STORY-001-S2   | Chapter 5 Building Block View — MinePlacer, Chapter 9 ADR-004 | BOARD-STORY-001   | exactly N cells are marked as mines; positions vary across seeds      |
| BOARD-STORY-001-S3   | Chapter 5 Building Block View — MinePlacer, Cell              | BOARD-STORY-001   | every safe cell has adjacent_count equal to neighbouring mines        |
| BOARD-STORY-001-S4   | Chapter 5 Building Block View, Chapter 6 Runtime View         | BOARD-STORY-001   | full initialization flow works end-to-end from CLI to board rendering |
| BOARD-FE-001.1-S1    | Chapter 5 Building Block View — BoardRenderer                 | BOARD-FE-001.1    | all cells render as hidden on the initial board display               |
| BOARD-BE-001.1-S1    | Chapter 5 Building Block View — Board, MinePlacer             | BOARD-BE-001.1    | board dimensions and cell count match constructor arguments           |
| BOARD-BE-001.2-S1    | Chapter 5 Building Block View — MinePlacer                    | BOARD-BE-001.2    | exactly N mines placed with no duplicates                             |
| BOARD-BE-001.2-S2    | Chapter 9 ADR-004                                             | BOARD-BE-001.2    | same seed produces identical mine positions                           |
| BOARD-BE-001.3-S1    | Chapter 5 Building Block View — MinePlacer, Cell              | BOARD-BE-001.3    | interior safe cell adjacent_count equals expected value               |
| BOARD-BE-001.3-S2    | Chapter 5 Building Block View — MinePlacer, Cell              | BOARD-BE-001.3    | corner cell uses only valid in-bounds neighbours                      |
| BOARD-INFRA-001.1-S1 | Chapter 7 Deployment View — 7.3, 7.4; Chapter 9 ADR-003        | BOARD-INFRA-001.1 | `docker build` completes with exit code 0; no build errors            |
| BOARD-INFRA-001.2-S1 | Chapter 7 Deployment View — 7.4; Chapter 2 TC-4                | BOARD-INFRA-001.2 | `pytest --version` succeeds inside container; no ModuleNotFoundError  |
| BOARD-INFRA-001.3-S1 | Chapter 5 Building Block View — Board; Chapter 7 — 7.3         | BOARD-INFRA-001.3 | game launches inside container; no ImportError                        |
| BOARD-INFRA-001.4-S1 | Chapter 7 — 7.3; Chapter 2 OC-2; Chapter 5 — Board, MinePlacer | BOARD-INFRA-001.4 | pytest discovers and passes board tests inside container              |
| BOARD-INFRA-001.4-S2 | Chapter 7 — 7.3; Chapter 2 OC-2; Chapter 5 — Board, MinePlacer | BOARD-INFRA-001.4 | `pytest --collect-only` collects board tests without errors           |
