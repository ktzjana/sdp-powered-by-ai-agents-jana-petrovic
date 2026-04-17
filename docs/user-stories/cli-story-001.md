# CLI Domain Stories — Input Parsing

## CLI-STORY-001

**AS A** player
**I WANT** to type commands like `r 2 3` or `f 1 4` in the terminal
**SO THAT** I can interact with the game without a graphical interface

**Architecture Reference:** Chapter 1 Introduction and Goals — FR-2, FR-3; Chapter 3 Context and Scope — 3.3 External Interfaces (stdin); Chapter 5 Building Block View — InputParser, CLI; Chapter 8 Cross-cutting Concepts — 8.4 Input Validation

---

### CLI-STORY-001-S1: Valid reveal command is parsed and dispatched

**GIVEN**
- the game is running and waiting for input

**WHEN**
- the player types `r 2 3`

**THEN**
- `InputParser` produces a reveal command with `row=2`, `col=3`
- `Game.reveal(2, 3)` is called
- the board re-renders after the action

---

### CLI-STORY-001-S2: Valid flag command is parsed and dispatched

**GIVEN**
- the game is running and waiting for input

**WHEN**
- the player types `f 1 4`

**THEN**
- `InputParser` produces a flag command with `row=1`, `col=4`
- `Game.flag(1, 4)` is called
- the board re-renders after the action

---

### CLI-STORY-001-S3: Invalid input prints a usage hint and re-prompts

**GIVEN**
- the game is running and waiting for input

**WHEN**
- the player types `xyz` or `r abc`

**THEN**
- the CLI prints a usage hint (e.g. `"Usage: r <row> <col> | f <row> <col> | q"`)
- the game re-prompts for input
- no domain call is made
- the process does not exit or raise an unhandled exception

---

### CLI-STORY-001-S4: Quit command exits the game cleanly

**GIVEN**
- the game is running and waiting for input

**WHEN**
- the player types `q`

**THEN**
- the game loop exits
- the process terminates with exit code 0

---

### CLI-STORY-001-S5: E2E — sequence of valid and invalid commands

**GIVEN**
- the game is started with `python minesweeper/cli.py --seed 42`

**WHEN**
- the player types `xyz` (invalid)
- then types `r 0 0` (valid reveal)
- then types `f 0 1` (valid flag)
- then types `q` (quit)

**THEN**
- `xyz` triggers a usage hint and re-prompt
- `r 0 0` reveals the cell and re-renders the board
- `f 0 1` flags the cell and re-renders the board
- `q` exits the process with code 0

---

## FE Sub-Stories

### CLI-FE-001.1

**AS A** player
**I WANT** a usage hint to appear whenever I type an unrecognised command
**SO THAT** I know the correct command format without consulting external documentation

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — 8.4 Input Validation; Chapter 5 Building Block View — InputParser

#### CLI-FE-001.1-S1: Usage hint is printed for unrecognised input

**GIVEN**
- the game is running

**WHEN**
- the player enters any string that does not match `r <int> <int>`, `f <int> <int>`, or `q`

**THEN**
- the CLI prints a single usage hint line to stdout
- the input prompt reappears immediately after

#### CLI-FE-001.1-S2: No usage hint is printed for valid commands

**GIVEN**
- the game is running

**WHEN**
- the player enters `r 1 2`

**THEN**
- no usage hint is printed
- the board renders normally

---

## BE Sub-Stories

### CLI-BE-001.1

**AS A** developer
**I WANT** `InputParser.parse()` to return a structured command object for valid input
**SO THAT** the CLI layer can dispatch to the correct `Game` method without string manipulation outside the parser

**Architecture Reference:** Chapter 5 Building Block View — InputParser; Chapter 4 Solution Strategy — Controller layer

#### CLI-BE-001.1-S1: parse returns reveal command for `r <row> <col>`

**GIVEN**
- the raw input string is `"r 2 3"`

**WHEN**
- `InputParser.parse("r 2 3")` is called

**THEN**
- the result has `action == "reveal"`, `row == 2`, `col == 3`

#### CLI-BE-001.1-S2: parse returns flag command for `f <row> <col>`

**GIVEN**
- the raw input string is `"f 1 4"`

**WHEN**
- `InputParser.parse("f 1 4")` is called

**THEN**
- the result has `action == "flag"`, `row == 1`, `col == 4`

#### CLI-BE-001.1-S3: parse returns quit command for `q`

**GIVEN**
- the raw input string is `"q"`

**WHEN**
- `InputParser.parse("q")` is called

**THEN**
- the result has `action == "quit"`

#### CLI-BE-001.1-S4: parse raises or returns error sentinel for invalid input

**GIVEN**
- the raw input string is `"xyz"` or `"r abc"`

**WHEN**
- `InputParser.parse(...)` is called

**THEN**
- the result signals a parse error (raises `ValueError` or returns an error sentinel)
- no domain method is called

---

## INFRA Sub-Stories

### CLI-INFRA-001.1

**AS A** developer
**I WANT** pytest tests for `InputParser` to run automatically
**SO THAT** regressions in command parsing are caught immediately

**Architecture Reference:** Chapter 1 Introduction and Goals — Quality Goal: Testability; Chapter 10 Quality Requirements — QS-3, QS-4

#### CLI-INFRA-001.1-S1: InputParser unit tests run via pytest with no I/O

**GIVEN**
- unit tests for `InputParser.parse()` exist under `tests/`

**WHEN**
- `pytest` is executed from the project root

**THEN**
- all parser-related tests are discovered and pass
- no stdin/stdout is accessed during the test run

---

### CLI-INFRA-001.2

**AS A** developer
**I WANT** the game to handle `EOF` on stdin gracefully
**SO THAT** automated piped-input tests do not leave the process hanging

**Architecture Reference:** Chapter 8 Cross-cutting Concepts — 8.2 Error Handling; Chapter 7 Deployment View

#### CLI-INFRA-001.2-S1: EOF on stdin exits the game cleanly

**GIVEN**
- the game is started and stdin reaches EOF (e.g. piped input ends)

**WHEN**
- the game loop attempts to read the next command

**THEN**
- the process exits with code 0
- no unhandled exception is raised

---

## Traceability Table

| Scenario ID          | Architecture Reference                                              | Parent Story    | Testable Assertion                                                          |
|----------------------|---------------------------------------------------------------------|-----------------|-----------------------------------------------------------------------------|
| CLI-STORY-001-S1     | Chapter 1 FR-2, Chapter 5 — InputParser, Chapter 6 Runtime View 6.1 | CLI-STORY-001  | reveal command parsed; Game.reveal called; board re-renders                 |
| CLI-STORY-001-S2     | Chapter 1 FR-3, Chapter 5 — InputParser, Chapter 6 Runtime View 6.2 | CLI-STORY-001  | flag command parsed; Game.flag called; board re-renders                     |
| CLI-STORY-001-S3     | Chapter 8 — 8.4 Input Validation, Chapter 10 QS-4                  | CLI-STORY-001   | invalid input prints usage hint; re-prompts; no crash; no domain call       |
| CLI-STORY-001-S4     | Chapter 8 — 8.4 Input Validation, Chapter 7 Deployment View        | CLI-STORY-001   | `q` exits the game loop; process exits with code 0                          |
| CLI-STORY-001-S5     | Chapter 6 Runtime View, Chapter 9 ADR-004                           | CLI-STORY-001   | E2E: invalid → hint; reveal → board; flag → board; quit → exit 0            |
| CLI-FE-001.1-S1      | Chapter 8 — 8.4 Input Validation, Chapter 5 — InputParser          | CLI-FE-001.1    | usage hint printed for unrecognised input; prompt reappears                 |
| CLI-FE-001.1-S2      | Chapter 5 — InputParser                                             | CLI-FE-001.1    | no usage hint for valid command; board renders normally                     |
| CLI-BE-001.1-S1      | Chapter 5 — InputParser, Chapter 4 Solution Strategy               | CLI-BE-001.1    | parse("r 2 3") returns action=reveal, row=2, col=3                          |
| CLI-BE-001.1-S2      | Chapter 5 — InputParser                                             | CLI-BE-001.1    | parse("f 1 4") returns action=flag, row=1, col=4                            |
| CLI-BE-001.1-S3      | Chapter 5 — InputParser, Chapter 8 — 8.4 Input Validation          | CLI-BE-001.1    | parse("q") returns action=quit                                              |
| CLI-BE-001.1-S4      | Chapter 8 — 8.4 Input Validation, Chapter 10 QS-4                  | CLI-BE-001.1    | parse raises/returns error for invalid input; no domain call made           |
| CLI-INFRA-001.1-S1   | Chapter 1 Quality Goal: Testability, Chapter 10 QS-3               | CLI-INFRA-001.1 | pytest discovers and runs all parser tests with zero I/O dependencies       |
| CLI-INFRA-001.2-S1   | Chapter 8 — 8.2 Error Handling, Chapter 7 Deployment View          | CLI-INFRA-001.2 | EOF on stdin exits cleanly with code 0; no unhandled exception              |
