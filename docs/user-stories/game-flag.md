# GAME Domain Stories — Flag / Unflag a Cell

## GAME-STORY-003

**AS A** player
**I WANT** to flag and unflag a cell as a suspected mine
**SO THAT** I can track my guesses visually on the board

**Architecture Reference:** Chapter 1 Introduction and Goals — FR-3; Chapter 5 Building Block View — Board, Game; Chapter 6 Runtime View — 6.2 Scenario: Flag a Cell

---

### GAME-STORY-003-S1: Flag an unrevealed cell

**GIVEN**
- cell (1, 4) is unrevealed and not flagged

**WHEN**
- the player enters `f 1 4`

**THEN**
- `board.cell(1, 4).flagged == True`
- the board re-renders showing the flag marker at (1, 4)

---

### GAME-STORY-003-S2: Unflag a flagged cell (toggle)

**GIVEN**
- cell (1, 4) is already flagged

**WHEN**
- the player enters `f 1 4` again

**THEN**
- `board.cell(1, 4).flagged == False`
- the board re-renders showing (1, 4) as hidden again

---

### GAME-STORY-003-S3: Flag on an already-revealed cell is ignored

**GIVEN**
- cell (2, 2) has already been revealed

**WHEN**
- the player enters `f 2 2`

**THEN**
- the board state is unchanged
- no error or crash occurs
- the game re-prompts

---

### GAME-STORY-003-S4: E2E — flag a cell and verify board display

**GIVEN**
- the game is started with `python minesweeper/cli.py --seed 42`

**WHEN**
- the player enters `f 0 0`

**THEN**
- the board renders with a flag marker at (0, 0)
- all other cells remain in their previous state
- the game continues and re-prompts

---

## FE Sub-Stories

### GAME-FE-003.1

**AS A** player
**I WANT** flagged cells to display a distinct marker on the board
**SO THAT** I can visually distinguish suspected mines from hidden cells

**Architecture Reference:** Chapter 5 Building Block View — BoardRenderer; Chapter 6 Runtime View — 6.2 Scenario: Flag a Cell

#### GAME-FE-003.1-S1: Flagged cell renders with flag marker

**GIVEN**
- cell (1, 4) is flagged

**WHEN**
- the board is rendered

**THEN**
- position (1, 4) displays the flag symbol (e.g. `F`)
- all other unrevealed cells display the hidden symbol

#### GAME-FE-003.1-S2: Unflagged cell reverts to hidden marker

**GIVEN**
- cell (1, 4) was flagged and has just been unflagged

**WHEN**
- the board is rendered

**THEN**
- position (1, 4) displays the hidden symbol again

---

## BE Sub-Stories

### GAME-BE-003.1

**AS A** developer
**I WANT** `Board.toggle_flag()` to flip the `flagged` state of an unrevealed cell
**SO THAT** a single command handles both flag and unflag

**Architecture Reference:** Chapter 5 Building Block View — Board; Chapter 6 Runtime View — 6.2 Scenario: Flag a Cell

#### GAME-BE-003.1-S1: toggle_flag sets flagged=True on an unflagged cell

**GIVEN**
- `board.cell(1, 4).flagged == False` and `revealed == False`

**WHEN**
- `board.toggle_flag(1, 4)` is called

**THEN**
- `board.cell(1, 4).flagged == True`

#### GAME-BE-003.1-S2: toggle_flag sets flagged=False on a flagged cell

**GIVEN**
- `board.cell(1, 4).flagged == True`

**WHEN**
- `board.toggle_flag(1, 4)` is called

**THEN**
- `board.cell(1, 4).flagged == False`

---

### GAME-BE-003.2

**AS A** developer
**I WANT** `Board.toggle_flag()` to silently ignore calls on already-revealed cells
**SO THAT** invalid flag actions never corrupt board state

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — 8.2 Error Handling

#### GAME-BE-003.2-S1: toggle_flag on a revealed cell is a no-op

**GIVEN**
- `board.cell(2, 2).revealed == True`

**WHEN**
- `board.toggle_flag(2, 2)` is called

**THEN**
- `board.cell(2, 2).flagged` remains unchanged
- no exception is raised

---

## INFRA Sub-Stories

### GAME-INFRA-003.1

**AS A** developer
**I WANT** pytest tests for `toggle_flag` to run automatically
**SO THAT** regressions in flag logic are caught immediately

**Architecture Reference:** Chapter 1 Introduction and Goals — Quality Goal: Testability; Chapter 10 Quality Requirements — QS-3

#### GAME-INFRA-003.1-S1: Flag unit tests run via pytest with no I/O

**GIVEN**
- unit tests for `Board.toggle_flag()` exist under `tests/`

**WHEN**
- `pytest` is executed from the project root

**THEN**
- all flag-related tests are discovered and pass
- no stdin/stdout is accessed during the test run

---

## Traceability Table

| Scenario ID           | Architecture Reference                                          | Parent Story     | Testable Assertion                                                    |
|-----------------------|-----------------------------------------------------------------|------------------|-----------------------------------------------------------------------|
| GAME-STORY-003-S1     | Chapter 1 FR-3, Chapter 6 Runtime View 6.2                     | GAME-STORY-003   | flagged==True; board re-renders with flag marker                      |
| GAME-STORY-003-S2     | Chapter 1 FR-3, Chapter 6 Runtime View 6.2                     | GAME-STORY-003   | flagged toggled back to False; board re-renders as hidden             |
| GAME-STORY-003-S3     | Chapter 8 Error Handling                                        | GAME-STORY-003   | flag on revealed cell is no-op; no crash; game re-prompts             |
| GAME-STORY-003-S4     | Chapter 6 Runtime View 6.2, Chapter 9 ADR-004                  | GAME-STORY-003   | E2E: flag marker visible at (0,0); game continues                     |
| GAME-FE-003.1-S1      | Chapter 5 Building Block View — BoardRenderer                   | GAME-FE-003.1    | flagged cell renders with `F` symbol                                  |
| GAME-FE-003.1-S2      | Chapter 5 Building Block View — BoardRenderer                   | GAME-FE-003.1    | unflagged cell reverts to hidden symbol                               |
| GAME-BE-003.1-S1      | Chapter 5 Building Block View — Board, Chapter 6 6.2           | GAME-BE-003.1    | toggle_flag sets flagged=True on unflagged cell                       |
| GAME-BE-003.1-S2      | Chapter 5 Building Block View — Board                           | GAME-BE-003.1    | toggle_flag sets flagged=False on flagged cell                        |
| GAME-BE-003.2-S1      | Chapter 8 Cross-cutting Concepts — Error Handling               | GAME-BE-003.2    | toggle_flag on revealed cell is no-op; no exception                   |
| GAME-INFRA-003.1-S1   | Chapter 1 Quality Goal: Testability, Chapter 10 QS-3           | GAME-INFRA-003.1 | pytest runs all flag tests with zero I/O dependencies                 |
