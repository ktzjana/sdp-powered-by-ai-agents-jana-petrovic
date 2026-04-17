# GAME Domain Stories — Reveal a Cell

## GAME-STORY-001

**AS A** player
**I WANT** to reveal a cell by entering its coordinates
**SO THAT** I can uncover the board and progress toward winning

**Architecture Reference:** Chapter 1 Introduction and Goals — FR-2, FR-4, FR-6; Chapter 6 Runtime View — 6.1 Scenario: Reveal a Cell

---

### GAME-STORY-001-S1: Reveal a numbered cell (has adjacent mines)

**GIVEN**
- the board is initialised with a fixed seed
- cell (2, 3) is a safe cell with `adjacent_count > 0`

**WHEN**
- the player enters `r 2 3`

**THEN**
- cell (2, 3) is marked as revealed
- the board is re-rendered showing the adjacent mine count at (2, 3)
- the game continues (no win/loss)

---

### GAME-STORY-001-S2: Reveal a mine ends the game as a loss

**GIVEN**
- the board is initialised with a fixed seed
- cell (1, 1) contains a mine

**WHEN**
- the player enters `r 1 1`

**THEN**
- `Board.reveal()` returns `MINE_HIT`
- the game transitions to loss state
- the CLI prints `"BOOM! You hit a mine."`
- the game loop exits

---

### GAME-STORY-001-S3: Reveal an empty cell triggers flood-fill

**GIVEN**
- the board is initialised with a fixed seed
- cell (0, 0) is empty (`adjacent_count == 0`, no mine)

**WHEN**
- the player enters `r 0 0`

**THEN**
- cell (0, 0) and all connected empty cells are revealed
- numbered border cells adjacent to the empty region are also revealed
- no mine cell is revealed during flood-fill

---

### GAME-STORY-001-S4: E2E — player reveals cells until a mine is hit

**GIVEN**
- the game is started with `python minesweeper/cli.py --seed 42`
- the board is a 5 × 5 grid with 3 mines

**WHEN**
- the player types `r 0 0` (safe cell)
- then types `r 1 1` (mine cell, known from seed)

**THEN**
- after `r 0 0` the board renders with at least one cell revealed
- after `r 1 1` the CLI prints the loss message and the process exits

---

## FE Sub-Stories

### GAME-FE-001.1

**AS A** player
**I WANT** the board to re-render after every reveal command
**SO THAT** I can see the updated state immediately after each action

**Architecture Reference:** Chapter 5 Building Block View — BoardRenderer; Chapter 6 Runtime View — 6.1 Scenario: Reveal a Cell

#### GAME-FE-001.1-S1: Board re-renders after a successful reveal

**GIVEN**
- the game is running and the board is displayed

**WHEN**
- the player enters `r 2 3` and the cell is safe

**THEN**
- the updated board is printed to stdout
- the revealed cell shows its `adjacent_count` (or blank if empty)
- all other cells retain their previous display state

#### GAME-FE-001.1-S2: Loss message is printed on mine reveal

**GIVEN**
- the game is running

**WHEN**
- the player reveals a mine cell

**THEN**
- the CLI prints `"BOOM! You hit a mine."` to stdout
- no further board prompt is shown

---

## BE Sub-Stories

### GAME-BE-001.1

**AS A** developer
**I WANT** `Board.reveal()` to return `MINE_HIT` when a mine cell is revealed
**SO THAT** the Game controller can transition to loss state without inspecting cell internals

**Architecture Reference:** Chapter 5 Building Block View — Board, RevealService; Chapter 6 Runtime View — 6.1 alt: cell is mine

#### GAME-BE-001.1-S1: Revealing a mine returns MINE_HIT

**GIVEN**
- a board where cell (1, 1) is a mine

**WHEN**
- `board.reveal(1, 1)` is called

**THEN**
- the return value equals `MINE_HIT` (or equivalent sentinel)
- the cell is marked revealed

#### GAME-BE-001.1-S2: Revealing a safe cell returns OK

**GIVEN**
- a board where cell (2, 2) is a safe numbered cell

**WHEN**
- `board.reveal(2, 2)` is called

**THEN**
- the return value equals `OK`
- `board.cell(2, 2).revealed == True`

---

### GAME-BE-001.2

**AS A** developer
**I WANT** `RevealService` to recursively reveal all connected empty cells (flood-fill)
**SO THAT** FR-6 is satisfied without the Game controller managing recursion

**Architecture Reference:** Chapter 5 Building Block View — RevealService; Chapter 9 Architecture Decisions — ADR-002

#### GAME-BE-001.2-S1: Flood-fill reveals all connected empty cells

**GIVEN**
- a 3 × 3 board where cells (0,0), (0,1), (1,0), (1,1) are empty and (0,2), (1,2), (2,0), (2,1), (2,2) are numbered or mines

**WHEN**
- `board.reveal(0, 0)` is called

**THEN**
- cells (0,0), (0,1), (1,0), (1,1) are all revealed
- numbered border cells adjacent to the empty region are revealed
- no mine cell is revealed

#### GAME-BE-001.2-S2: Flood-fill does not revisit already-revealed cells

**GIVEN**
- cell (0, 0) has already been revealed

**WHEN**
- `board.reveal(0, 0)` is called again

**THEN**
- the board state is unchanged
- no infinite recursion or error occurs

---

### GAME-BE-001.3

**AS A** developer
**I WANT** `Game.reveal()` to call `check_win()` after every safe reveal
**SO THAT** the win condition is evaluated after each player action

**Architecture Reference:** Chapter 5 Building Block View — Game; Chapter 6 Runtime View — 6.1 alt: cell has adjacent mines / cell is empty

#### GAME-BE-001.3-S1: check_win is called after a safe reveal

**GIVEN**
- a game with one safe cell remaining unrevealed

**WHEN**
- the player reveals that last safe cell

**THEN**
- `Game.check_win()` returns `True`
- the game transitions to win state

#### GAME-BE-001.3-S2: check_win returns False when safe cells remain

**GIVEN**
- a game where multiple safe cells are still unrevealed

**WHEN**
- the player reveals one safe cell

**THEN**
- `Game.check_win()` returns `False`
- the game loop continues

---

## INFRA Sub-Stories

### GAME-INFRA-001.1

**AS A** developer
**I WANT** pytest tests for `RevealService` and `Game.reveal()` to run automatically
**SO THAT** regressions in reveal logic and flood-fill are caught immediately

**Architecture Reference:** Chapter 1 Introduction and Goals — Quality Goal: Testability; Chapter 10 Quality Requirements — QS-1, QS-3

#### GAME-INFRA-001.1-S1: Reveal unit tests run via pytest with no I/O dependencies

**GIVEN**
- unit tests for `Board.reveal()`, `RevealService`, and `Game.reveal()` exist under `tests/`

**WHEN**
- `pytest` is executed from the project root

**THEN**
- all reveal-related tests are discovered and pass
- no stdin/stdout is accessed during the test run

---

### GAME-INFRA-001.2

**AS A** developer
**I WANT** the game to accept a `--seed` argument at the CLI entry point
**SO THAT** reveal scenarios are reproducible in automated tests

**Architecture Reference:** Chapter 9 Architecture Decisions — ADR-004; Chapter 7 Deployment View

#### GAME-INFRA-001.2-S1: Game runs with a fixed seed from the CLI

**GIVEN**
- Python 3.10+ is installed

**WHEN**
- `python minesweeper/cli.py --seed 42` is executed

**THEN**
- the game starts with a deterministic board
- the same mine positions appear on every run with `--seed 42`

---

### GAME-INFRA-001.3

**AS A** developer
**I WANT** invalid reveal coordinates to be caught and reported without crashing
**SO THAT** the game loop remains robust during manual and automated play

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — 8.2 Error Handling; Chapter 10 Quality Requirements — QS-4

#### GAME-INFRA-001.3-S1: Out-of-bounds reveal re-prompts without crashing

**GIVEN**
- the game is running with a 5 × 5 board

**WHEN**
- the player enters `r 99 99`

**THEN**
- the CLI prints a usage hint
- the game re-prompts for input
- the process does not exit or raise an unhandled exception

---

## Traceability Table

| Scenario ID           | Architecture Reference                                              | Parent Story     | Testable Assertion                                                          |
|-----------------------|---------------------------------------------------------------------|------------------|-----------------------------------------------------------------------------|
| GAME-STORY-001-S1     | Chapter 1 FR-2, Chapter 6 Runtime View 6.1 (numbered cell)         | GAME-STORY-001   | cell is revealed; adjacent_count shown; game continues                      |
| GAME-STORY-001-S2     | Chapter 1 FR-4, Chapter 6 Runtime View 6.1 (mine alt)              | GAME-STORY-001   | MINE_HIT returned; loss message printed; game exits                         |
| GAME-STORY-001-S3     | Chapter 1 FR-6, Chapter 9 ADR-002, Chapter 6 Runtime View 6.1      | GAME-STORY-001   | flood-fill reveals all connected empty cells and numbered border cells      |
| GAME-STORY-001-S4     | Chapter 6 Runtime View 6.1, Chapter 9 ADR-004                      | GAME-STORY-001   | E2E: safe reveal renders board; mine reveal prints loss message and exits   |
| GAME-FE-001.1-S1      | Chapter 5 Building Block View — BoardRenderer                       | GAME-FE-001.1    | updated board printed to stdout after safe reveal                           |
| GAME-FE-001.1-S2      | Chapter 6 Runtime View 6.1 (mine alt)                               | GAME-FE-001.1    | loss message printed; no further prompt shown                               |
| GAME-BE-001.1-S1      | Chapter 5 Building Block View — RevealService, Chapter 6 6.1       | GAME-BE-001.1    | board.reveal() returns MINE_HIT for a mine cell                             |
| GAME-BE-001.1-S2      | Chapter 5 Building Block View — RevealService                       | GAME-BE-001.1    | board.reveal() returns OK and sets revealed=True for a safe cell            |
| GAME-BE-001.2-S1      | Chapter 5 Building Block View — RevealService, Chapter 9 ADR-002   | GAME-BE-001.2    | all connected empty cells and numbered border cells revealed by flood-fill  |
| GAME-BE-001.2-S2      | Chapter 9 ADR-002                                                   | GAME-BE-001.2    | re-revealing an already-revealed cell is a no-op; no recursion error        |
| GAME-BE-001.3-S1      | Chapter 5 Building Block View — Game, Chapter 6 Runtime View 6.3   | GAME-BE-001.3    | check_win() returns True when last safe cell is revealed                    |
| GAME-BE-001.3-S2      | Chapter 5 Building Block View — Game                                | GAME-BE-001.3    | check_win() returns False when safe cells remain; loop continues            |
| GAME-INFRA-001.1-S1   | Chapter 1 Quality Goal: Testability, Chapter 10 QS-3               | GAME-INFRA-001.1 | pytest runs all reveal tests with zero I/O dependencies                     |
| GAME-INFRA-001.2-S1   | Chapter 9 ADR-004, Chapter 7 Deployment View                        | GAME-INFRA-001.2 | --seed 42 produces identical board on every run                             |
| GAME-INFRA-001.3-S1   | Chapter 8 Error Handling, Chapter 10 QS-4                           | GAME-INFRA-001.3 | out-of-bounds input re-prompts; process stays alive                         |
