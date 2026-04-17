# GAME Domain Stories — Win / Loss Detection

## GAME-STORY-002

**AS A** player
**I WANT** the game to detect when I have won or lost
**SO THAT** the game ends with clear feedback

**Architecture Reference:** Chapter 1 Introduction and Goals — FR-4, FR-5; Chapter 5 Building Block View — Game; Chapter 6 Runtime View — 6.1 Scenario: Reveal a Cell, 6.3 Scenario: Win Condition

---

### GAME-STORY-002-S1: Loss — revealing a mine ends the game immediately

**GIVEN**
- the board is initialised with a fixed seed
- cell (1, 1) contains a mine

**WHEN**
- the player enters `r 1 1`

**THEN**
- the game transitions to loss state
- the CLI prints `"BOOM! You hit a mine."`
- no further input is accepted

---

### GAME-STORY-002-S2: Win — revealing the last safe cell ends the game

**GIVEN**
- all safe cells except (3, 3) have been revealed
- cell (3, 3) is safe

**WHEN**
- the player enters `r 3 3`

**THEN**
- `Game.check_win()` returns `True`
- the CLI prints `"You win!"`
- the game loop exits

---

### GAME-STORY-002-S3: Game continues when safe cells remain

**GIVEN**
- multiple safe cells are still unrevealed

**WHEN**
- the player reveals one safe cell

**THEN**
- `Game.check_win()` returns `False`
- the CLI re-prompts for the next command
- the game loop does not exit

---

### GAME-STORY-002-S4: E2E — full game from start to win

**GIVEN**
- the game is started with `python minesweeper/cli.py --seed 7`
- the board is a 3 × 3 grid with 1 mine (known position from seed)

**WHEN**
- the player reveals all safe cells in sequence

**THEN**
- after the last safe reveal the CLI prints `"You win!"`
- the process exits cleanly with code 0

---

## FE Sub-Stories

### GAME-FE-002.1

**AS A** player
**I WANT** a clear win or loss message printed to the terminal when the game ends
**SO THAT** I know the outcome without ambiguity

**Architecture Reference:** Chapter 5 Building Block View — BoardRenderer; Chapter 6 Runtime View — 6.1 (mine alt), 6.3 (win)

#### GAME-FE-002.1-S1: Win message is printed on game completion

**GIVEN**
- the last safe cell has just been revealed

**WHEN**
- `Game` signals `game_over(win)` to the CLI

**THEN**
- the CLI prints `"You win!"` to stdout
- no input prompt follows

#### GAME-FE-002.1-S2: Loss message is printed on mine reveal

**GIVEN**
- the player has just revealed a mine

**WHEN**
- `Game` signals `game_over(loss)` to the CLI

**THEN**
- the CLI prints `"BOOM! You hit a mine."` to stdout
- no input prompt follows

---

## BE Sub-Stories

### GAME-BE-002.1

**AS A** developer
**I WANT** `Game.check_win()` to return `True` only when every safe cell is revealed
**SO THAT** the win condition is evaluated correctly after each action

**Architecture Reference:** Chapter 5 Building Block View — Game; Chapter 6 Runtime View — 6.3 Scenario: Win Condition; Chapter 10 Quality Requirements — QS-2

#### GAME-BE-002.1-S1: check_win returns True when all safe cells are revealed

**GIVEN**
- a board with 2 mines and 7 safe cells
- all 7 safe cells have `revealed == True`

**WHEN**
- `game.check_win()` is called

**THEN**
- the return value is `True`

#### GAME-BE-002.1-S2: check_win returns False when any safe cell is unrevealed

**GIVEN**
- a board with 2 mines and 7 safe cells
- 6 safe cells are revealed; 1 remains hidden

**WHEN**
- `game.check_win()` is called

**THEN**
- the return value is `False`

---

### GAME-BE-002.2

**AS A** developer
**I WANT** `Game` to transition to a terminal loss state when `Board.reveal()` returns `MINE_HIT`
**SO THAT** the game loop stops and no further moves are processed

**Architecture Reference:** Chapter 5 Building Block View — Game; Chapter 6 Runtime View — 6.1 alt: cell is mine; Chapter 10 Quality Requirements — QS-1

#### GAME-BE-002.2-S1: Game enters loss state on MINE_HIT

**GIVEN**
- `Board.reveal()` returns `MINE_HIT`

**WHEN**
- `Game.reveal()` processes the result

**THEN**
- `game.state` equals `LOSS` (or equivalent)
- subsequent calls to `game.reveal()` are rejected or no-op

#### GAME-BE-002.2-S2: Game enters win state after check_win passes

**GIVEN**
- `Board.reveal()` returns `OK`
- `game.check_win()` returns `True`

**WHEN**
- `Game.reveal()` processes the result

**THEN**
- `game.state` equals `WIN`
- the game loop exits

---

### GAME-BE-002.3

**AS A** developer
**I WANT** flagged cells to not count as revealed for win detection
**SO THAT** the player must reveal — not just flag — all safe cells to win

**Architecture Reference:** Chapter 5 Building Block View — Game, Cell; Chapter 12 Glossary — Win condition

#### GAME-BE-002.3-S1: Flagged safe cell does not satisfy win condition

**GIVEN**
- all safe cells except (2, 2) are revealed
- cell (2, 2) is flagged but not revealed

**WHEN**
- `game.check_win()` is called

**THEN**
- the return value is `False`

---

## INFRA Sub-Stories

### GAME-INFRA-002.1

**AS A** developer
**I WANT** pytest tests for win/loss detection to run automatically
**SO THAT** regressions in game-ending logic are caught immediately

**Architecture Reference:** Chapter 1 Introduction and Goals — Quality Goal: Testability; Chapter 10 Quality Requirements — QS-1, QS-2

#### GAME-INFRA-002.1-S1: Win/loss unit tests run via pytest with no I/O

**GIVEN**
- unit tests for `Game.check_win()` and loss-state transition exist under `tests/`

**WHEN**
- `pytest` is executed from the project root

**THEN**
- all win/loss tests are discovered and pass
- no stdin/stdout is accessed during the test run

---

### GAME-INFRA-002.2

**AS A** developer
**I WANT** the process to exit with code 0 on win and code 0 on loss (clean exit)
**SO THAT** automated test runners can verify the game completed without errors

**Architecture Reference:** Chapter 7 Deployment View; Chapter 9 Architecture Decisions — ADR-003

#### GAME-INFRA-002.2-S1: Process exits cleanly after win

**GIVEN**
- the game is run with `python minesweeper/cli.py --seed 7`
- the player reveals all safe cells

**WHEN**
- the win condition is triggered

**THEN**
- the process exits with code 0
- `"You win!"` was printed before exit

#### GAME-INFRA-002.2-S2: Process exits cleanly after loss

**GIVEN**
- the game is run with `python minesweeper/cli.py --seed 7`
- the player reveals a mine

**WHEN**
- the loss condition is triggered

**THEN**
- the process exits with code 0
- `"BOOM! You hit a mine."` was printed before exit

---

## Traceability Table

| Scenario ID           | Architecture Reference                                              | Parent Story     | Testable Assertion                                                        |
|-----------------------|---------------------------------------------------------------------|------------------|---------------------------------------------------------------------------|
| GAME-STORY-002-S1     | Chapter 1 FR-4, Chapter 6 Runtime View 6.1 (mine alt)              | GAME-STORY-002   | loss message printed; no further input accepted                           |
| GAME-STORY-002-S2     | Chapter 1 FR-5, Chapter 6 Runtime View 6.3                         | GAME-STORY-002   | check_win() returns True; win message printed; loop exits                 |
| GAME-STORY-002-S3     | Chapter 5 Building Block View — Game                                | GAME-STORY-002   | check_win() returns False; game re-prompts                                |
| GAME-STORY-002-S4     | Chapter 6 Runtime View 6.3, Chapter 9 ADR-004                      | GAME-STORY-002   | E2E: all safe cells revealed → "You win!" → process exits 0              |
| GAME-FE-002.1-S1      | Chapter 6 Runtime View 6.3, Chapter 5 — BoardRenderer              | GAME-FE-002.1    | "You win!" printed to stdout; no prompt follows                           |
| GAME-FE-002.1-S2      | Chapter 6 Runtime View 6.1 (mine alt), Chapter 5 — BoardRenderer   | GAME-FE-002.1    | "BOOM! You hit a mine." printed; no prompt follows                        |
| GAME-BE-002.1-S1      | Chapter 5 Building Block View — Game, Chapter 10 QS-2              | GAME-BE-002.1    | check_win() returns True when all safe cells revealed                     |
| GAME-BE-002.1-S2      | Chapter 5 Building Block View — Game                                | GAME-BE-002.1    | check_win() returns False when any safe cell is unrevealed                |
| GAME-BE-002.2-S1      | Chapter 5 Building Block View — Game, Chapter 10 QS-1              | GAME-BE-002.2    | game.state == LOSS after MINE_HIT; further reveals rejected               |
| GAME-BE-002.2-S2      | Chapter 6 Runtime View 6.3                                          | GAME-BE-002.2    | game.state == WIN after check_win passes                                  |
| GAME-BE-002.3-S1      | Chapter 5 Building Block View — Cell, Chapter 12 Glossary          | GAME-BE-002.3    | flagged-but-unrevealed safe cell keeps check_win() returning False        |
| GAME-INFRA-002.1-S1   | Chapter 1 Quality Goal: Testability, Chapter 10 QS-1, QS-2         | GAME-INFRA-002.1 | pytest runs all win/loss tests with zero I/O dependencies                 |
| GAME-INFRA-002.2-S1   | Chapter 7 Deployment View, Chapter 9 ADR-003                        | GAME-INFRA-002.2 | process exits 0 after win; "You win!" in stdout                           |
| GAME-INFRA-002.2-S2   | Chapter 7 Deployment View, Chapter 9 ADR-003                        | GAME-INFRA-002.2 | process exits 0 after loss; "BOOM!" in stdout                             |
