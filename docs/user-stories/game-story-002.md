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

### GAME-INFRA-002.1 — Deployment / Execution Environment

**AS A** developer
**I WANT** the process to exit with code 0 on both win and loss outcomes
**SO THAT** automated test runners can verify the game completed without errors

**Architecture Reference:** Chapter 7 Deployment View — 7.3 How to Run; Chapter 9 Architecture Decisions — ADR-003

#### GAME-INFRA-002.1-S1: Process exits cleanly after win

**GIVEN**

* the game is run with `python minesweeper/cli.py --seed 7`
* the player reveals all safe cells

**WHEN**

* the win condition is triggered

**THEN**

* the process exits with code 0
* `"You win!"` was printed before exit

#### GAME-INFRA-002.1-S2: Process exits cleanly after loss

**GIVEN**

* the game is run with `python minesweeper/cli.py --seed 7`
* the player reveals a mine

**WHEN**

* the loss condition is triggered

**THEN**

* the process exits with code 0
* `"BOOM! You hit a mine."` was printed before exit

---

### GAME-INFRA-002.2 — Data Store / State Persistence

**AS A** developer
**I WANT** the game state (including win/loss status) to be held entirely in-memory
**SO THAT** no file I/O is needed to track or persist the game outcome

**Architecture Reference:** Chapter 7 Deployment View — 7.4 Runtime Requirements (Persistent storage: None); Chapter 5 Building Block View — Game, Board

> **Applicability note:** The architecture specifies no persistent storage. `Game.state` (WIN / LOSS / IN_PROGRESS) lives in the in-memory `Game` object. There is no save/resume feature. This story verifies that the win/loss state is never written to disk.

#### GAME-INFRA-002.2-S1: Win/loss state is not written to disk

**GIVEN**

* the game is running and the player triggers a win or loss condition

**WHEN**

* `Game` transitions to WIN or LOSS state

**THEN**

* no files are created or modified in the working directory
* the outcome is communicated solely via stdout and process exit code

---

### GAME-INFRA-002.3 — Event Handling / Integration Points

**AS A** developer
**I WANT** win and loss conditions to be evaluated as discrete post-action events after every reveal
**SO THAT** the game loop terminates correctly and no further input is accepted after a terminal state

**Architecture Reference:** Chapter 5 Building Block View — Game; Chapter 6 Runtime View — 6.1 Scenario: Reveal a Cell, 6.3 Scenario: Win Condition

#### GAME-INFRA-002.3-S1: Game loop stops accepting input after a terminal state is reached

**GIVEN**

* the game has transitioned to WIN or LOSS state

**WHEN**

* the game loop evaluates the next iteration

**THEN**

* no input prompt is shown
* `Game.reveal()` rejects or no-ops any further calls
* the process exits cleanly

---

### GAME-INFRA-002.4 — Monitoring / Observability

**AS A** developer
**I WANT** the win and loss outcomes to produce distinct, visible messages on stdout
**SO THAT** the game result is unambiguous and diagnosable in both manual and automated runs

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — 8.2 Error Handling, 8.3 Logging; Chapter 10 Quality Requirements — QS-1, QS-2

#### GAME-INFRA-002.4-S1: Win outcome is confirmed with a visible message and final board state

**GIVEN**

* the player has just revealed the last safe cell

**WHEN**

* `Game` signals the win condition to the CLI

**THEN**

* the final board is rendered to stdout
* `"You win!"` is printed after the board render
* no further input prompt appears

#### GAME-INFRA-002.4-S2: Loss outcome is confirmed with a visible message and mine position visible

**GIVEN**

* the player has just revealed a mine

**WHEN**

* `Game` signals the loss condition to the CLI

**THEN**

* `"BOOM! You hit a mine."` is printed to stdout
* the board is rendered showing the triggered mine position
* no further input prompt appears

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
| GAME-INFRA-002.1-S1   | Chapter 7 Deployment View — 7.3; Chapter 9 ADR-003                  | GAME-INFRA-002.1 | process exits 0 after win; "You win!" in stdout                           |
| GAME-INFRA-002.1-S2   | Chapter 7 Deployment View — 7.3; Chapter 9 ADR-003                  | GAME-INFRA-002.1 | process exits 0 after loss; "BOOM!" in stdout                             |
| GAME-INFRA-002.2-S1   | Chapter 7 Deployment View — 7.4 (Persistent storage: None)          | GAME-INFRA-002.2 | no files created on win/loss; outcome via stdout and exit code only       |
| GAME-INFRA-002.3-S1   | Chapter 5 Building Block View — Game; Chapter 6 Runtime View 6.3    | GAME-INFRA-002.3 | game loop stops; no prompt shown; further reveals rejected after terminal |
| GAME-INFRA-002.4-S1   | Chapter 8 — 8.2 Error Handling, 8.3 Logging; Chapter 10 QS-2       | GAME-INFRA-002.4 | final board rendered; "You win!" printed; no further prompt               |
| GAME-INFRA-002.4-S2   | Chapter 8 — 8.2 Error Handling, 8.3 Logging; Chapter 10 QS-1       | GAME-INFRA-002.4 | board rendered with mine visible; "BOOM!" printed; no further prompt      |
