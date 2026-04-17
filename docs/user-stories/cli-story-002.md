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

### CLI-INFRA-002.1

**AS A** developer
**I WANT** pytest tests for `BoardRenderer` to run automatically
**SO THAT** regressions in board display are caught immediately

**Architecture Reference:** Chapter 1 Introduction and Goals — Quality Goal: Testability; Chapter 10 Quality Requirements — QS-3

#### CLI-INFRA-002.1-S1: BoardRenderer unit tests run via pytest with no I/O side-effects

**GIVEN**
- unit tests for `BoardRenderer.render()` exist under `tests/`

**WHEN**
- `pytest` is executed from the project root

**THEN**
- all renderer tests are discovered and pass
- tests assert on the returned string, not on stdout directly

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
| CLI-INFRA-002.1-S1   | Chapter 1 Quality Goal: Testability, Chapter 10 QS-3               | CLI-INFRA-002.1 | pytest runs all renderer tests; assertions on returned string, not stdout |
