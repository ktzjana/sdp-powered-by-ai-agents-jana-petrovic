# CLI Domain Stories — Board Rendering

## CLI-STORY-002

**AS A** player
**I WANT** the board to be rendered clearly in the terminal after each action
**SO THAT** I can see the current game state at all times

**Architecture Reference:** Chapter 1 Introduction and Goals — FR-7; Chapter 5 Building Block View — BoardRenderer; Chapter 6 Runtime View — 6.1, 6.2, 6.3

---

### CLI-STORY-002-S1: Hidden cells render as the hidden symbol

**GIVEN**
- the board has been initialised and no cells have been revealed or flagged

**WHEN**
- the board is rendered

**THEN**
- every cell displays the hidden symbol (e.g. `.`)
- the grid dimensions match the configured rows × cols

---

### CLI-STORY-002-S2: Revealed numbered cell shows its adjacent count

**GIVEN**
- cell (2, 3) has been revealed and has `adjacent_count == 2`

**WHEN**
- the board is rendered

**THEN**
- position (2, 3) displays `2`
- all other unrevealed cells still display the hidden symbol

---

### CLI-STORY-002-S3: Flagged cell displays the flag marker

**GIVEN**
- cell (1, 4) is flagged and not revealed

**WHEN**
- the board is rendered

**THEN**
- position (1, 4) displays the flag symbol (e.g. `F`)
- all other unrevealed cells display the hidden symbol

---

### CLI-STORY-002-S4: Revealed empty cell displays a blank or zero marker

**GIVEN**
- cell (0, 0) has been revealed and has `adjacent_count == 0`

**WHEN**
- the board is rendered

**THEN**
- position (0, 0) displays a blank or `0` marker (consistent with the chosen convention)

---

### CLI-STORY-002-S5: E2E — board state is visible after each player action

**GIVEN**
- the game is started with `python minesweeper/cli.py --seed 42`

**WHEN**
- the player types `r 0 0` (safe cell)
- then types `f 0 1`

**THEN**
- after `r 0 0` the board is printed with at least (0, 0) revealed
- after `f 0 1` the board is printed with `F` at (0, 1)
- both renders appear on stdout before the next prompt

---

## FE Sub-Stories

### CLI-FE-002.1

**AS A** player
**I WANT** the board to re-render to stdout after every action
**SO THAT** I always see the latest game state without having to request it

**Architecture Reference:** Chapter 5 Building Block View — BoardRenderer; Chapter 6 Runtime View — 6.1, 6.2

#### CLI-FE-002.1-S1: Board is printed after a reveal action

**GIVEN**
- the player has just entered a valid reveal command

**WHEN**
- the CLI processes the result from `Game`

**THEN**
- the updated board is printed to stdout before the next input prompt

#### CLI-FE-002.1-S2: Board is printed after a flag action

**GIVEN**
- the player has just entered a valid flag command

**WHEN**
- the CLI processes the result from `Game`

**THEN**
- the updated board is printed to stdout before the next input prompt

---

## BE Sub-Stories

### CLI-BE-002.1

**AS A** developer
**I WANT** `BoardRenderer` to produce a consistent ASCII grid from the board state
**SO THAT** the display logic is isolated and independently testable

**Architecture Reference:** Chapter 5 Building Block View — BoardRenderer; Chapter 9 Architecture Decisions — ADR-001, ADR-003

#### CLI-BE-002.1-S1: Renderer outputs correct number of rows and columns

**GIVEN**
- a 3 × 4 board with all cells hidden

**WHEN**
- `BoardRenderer.render(board)` is called

**THEN**
- the output contains exactly 3 rows
- each row contains exactly 4 cell symbols

#### CLI-BE-002.1-S2: Renderer uses distinct symbols for hidden, flagged, and revealed cells

**GIVEN**
- a board where cell (0,0) is hidden, (0,1) is flagged, and (0,2) is revealed with `adjacent_count == 1`

**WHEN**
- `BoardRenderer.render(board)` is called

**THEN**
- (0,0) displays the hidden symbol
- (0,1) displays the flag symbol
- (0,2) displays `1`

---

## INFRA Sub-Stories

### CLI-INFRA-002.1 — Deployment / Execution Environment

**AS A** developer
**I WANT** the board renderer to produce correct output in the same single-command execution environment
**SO THAT** rendering works on any OS with Python 3.10+ without additional dependencies

**Architecture Reference:** Chapter 7 Deployment View — 7.3 How to Run, 7.4 Runtime Requirements; Chapter 9 Architecture Decisions — ADR-003

#### CLI-INFRA-002.1-S1: BoardRenderer produces correct output with no third-party packages

**GIVEN**

* Python 3.10+ is installed on the host machine
* no virtual environment or package installation has been performed

**WHEN**

* `python minesweeper/cli.py` is executed and the board is rendered

**THEN**

* the ASCII grid is printed to stdout correctly
* no import errors or missing-dependency errors occur

---

### CLI-INFRA-002.2 — Data Store / State Persistence

**AS A** developer
**I WANT** `BoardRenderer` to read board state directly from the in-memory `Board` object on every render
**SO THAT** no intermediate file or cache is needed to produce the display

**Architecture Reference:** Chapter 7 Deployment View — 7.4 Runtime Requirements (Persistent storage: None); Chapter 5 Building Block View — BoardRenderer, Board

> **Applicability note:** The architecture specifies no persistent storage. `BoardRenderer` reads `Cell` state directly from the in-memory `Board` aggregate on each call. There is no render cache or output file. This story verifies that constraint holds in the rendering path.

#### CLI-INFRA-002.2-S1: Renderer reads board state in-memory without disk I/O

**GIVEN**

* the game is running and the board has been updated by a reveal or flag action

**WHEN**

* `BoardRenderer.render(board)` is called

**THEN**

* the rendered output reflects the current in-memory `Board` state
* no files are read from or written to disk during rendering

---

### CLI-INFRA-002.3 — Event Handling / Integration Points

**AS A** developer
**I WANT** `BoardRenderer` to be invoked automatically after every game action that changes board state
**SO THAT** the player always sees an up-to-date view without having to request a refresh

**Architecture Reference:** Chapter 5 Building Block View — BoardRenderer, Game; Chapter 6 Runtime View — 6.1 Scenario: Reveal a Cell, 6.2 Scenario: Flag a Cell

#### CLI-INFRA-002.3-S1: Renderer is called after every state-changing action

**GIVEN**

* the game is running

**WHEN**

* the player enters a valid reveal or flag command

**THEN**

* `BoardRenderer.render(board)` is called once after the action completes
* the updated board appears on stdout before the next input prompt

---

### CLI-INFRA-002.4 — Monitoring / Observability

**AS A** developer
**I WANT** rendering errors (e.g. unexpected cell state) to produce a visible diagnostic on stdout rather than a silent crash
**SO THAT** display bugs are immediately visible during development and manual testing

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — 8.2 Error Handling, 8.3 Logging; Chapter 10 Quality Requirements — QS-4

#### CLI-INFRA-002.4-S1: Renderer uses distinct, unambiguous symbols for all cell states

**GIVEN**

* a board containing hidden, flagged, revealed-numbered, and revealed-empty cells

**WHEN**

* `BoardRenderer.render(board)` is called

**THEN**

* each cell state maps to a distinct symbol (e.g. `.` hidden, `F` flagged, digit for numbered, ` ` or `0` for empty)
* no cell renders as an empty string or whitespace that could be confused with another state

#### CLI-INFRA-002.4-S2: Renderer output is written to stdout and is immediately visible

**GIVEN**

* the game is running

**WHEN**

* `BoardRenderer.render(board)` is called after any action

**THEN**

* the rendered board is flushed to stdout before the next input prompt
* no buffering delay causes the board to appear after the prompt

---

## Traceability Table

| Scenario ID          | Architecture Reference                                              | Parent Story    | Testable Assertion                                                        |
|----------------------|---------------------------------------------------------------------|-----------------|---------------------------------------------------------------------------|
| CLI-STORY-002-S1     | Chapter 1 FR-7, Chapter 5 — BoardRenderer                          | CLI-STORY-002   | all cells show hidden symbol; grid matches configured dimensions           |
| CLI-STORY-002-S2     | Chapter 1 FR-7, Chapter 5 — BoardRenderer, Cell                    | CLI-STORY-002   | revealed numbered cell shows adjacent_count; others remain hidden         |
| CLI-STORY-002-S3     | Chapter 1 FR-3, FR-7, Chapter 5 — BoardRenderer                    | CLI-STORY-002   | flagged cell shows flag symbol; others remain hidden                      |
| CLI-STORY-002-S4     | Chapter 1 FR-6, FR-7, Chapter 5 — BoardRenderer                    | CLI-STORY-002   | revealed empty cell shows blank or 0 marker                               |
| CLI-STORY-002-S5     | Chapter 6 Runtime View 6.1, 6.2, Chapter 9 ADR-004                 | CLI-STORY-002   | E2E: board printed after reveal and after flag; both visible on stdout    |
| CLI-FE-002.1-S1      | Chapter 5 — BoardRenderer, Chapter 6 Runtime View 6.1              | CLI-FE-002.1    | updated board printed to stdout after reveal, before next prompt          |
| CLI-FE-002.1-S2      | Chapter 5 — BoardRenderer, Chapter 6 Runtime View 6.2              | CLI-FE-002.1    | updated board printed to stdout after flag, before next prompt            |
| CLI-BE-002.1-S1      | Chapter 5 — BoardRenderer, Chapter 9 ADR-001                       | CLI-BE-002.1    | render output has correct row and column count                            |
| CLI-BE-002.1-S2      | Chapter 5 — BoardRenderer, Cell                                     | CLI-BE-002.1    | hidden/flagged/revealed cells use distinct symbols                        |
| CLI-INFRA-002.1-S1   | Chapter 7 Deployment View — 7.3, 7.4; Chapter 9 ADR-003             | CLI-INFRA-002.1 | renderer produces correct ASCII output; no packages required              |
| CLI-INFRA-002.2-S1   | Chapter 7 Deployment View — 7.4 (Persistent storage: None)          | CLI-INFRA-002.2 | renderer reads in-memory Board; no disk I/O during rendering              |
| CLI-INFRA-002.3-S1   | Chapter 5 — BoardRenderer, Game; Chapter 6 Runtime View 6.1, 6.2   | CLI-INFRA-002.3 | render called once after each action; board visible before next prompt    |
| CLI-INFRA-002.4-S1   | Chapter 8 — 8.2 Error Handling, 8.3 Logging; Chapter 10 QS-4       | CLI-INFRA-002.4 | each cell state maps to a distinct unambiguous symbol                     |
| CLI-INFRA-002.4-S2   | Chapter 8 — 8.3 Logging; Chapter 5 — BoardRenderer                 | CLI-INFRA-002.4 | board flushed to stdout before next prompt; no buffering delay            |
