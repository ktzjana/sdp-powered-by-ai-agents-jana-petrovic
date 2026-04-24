# Chapter 9: Architecture Decisions

## ADR-001: Three-Layer Architecture (CLI / Controller / Domain)

### Status
Accepted

### Context
The game needs to be unit-testable, but also needs a CLI interface. Mixing I/O with game logic makes testing hard.

### Decision
Separate the codebase into three layers: CLI (I/O), Game Controller (orchestration), Domain (rules and state).

### Rationale
The domain layer has zero I/O dependencies, making it directly testable with plain `assert` statements. The boundary is cheap to enforce in a small Python project.

### Consequences
- (+) Domain logic is fully testable without mocking stdin/stdout.
- (+) CLI can be swapped (e.g. for a GUI) without touching the domain.
- (-) Slightly more files than a single-script solution, acceptable for a kata.

---

## ADR-002: Recursive Flood-fill for Empty Cell Reveal

### Status
Accepted

### Context
FR-6 requires that revealing an empty cell (zero adjacent mines) automatically reveals all connected empty cells and their numbered neighbours.

### Decision
Implement flood-fill as a recursive function inside `Board.reveal()`.

### Rationale
Recursion maps naturally to the problem. Grid sizes in a kata are small (typically ≤ 30×30), so stack depth is not a concern.

### Consequences
- (+) Simple, readable implementation.
- (-) Not suitable for very large grids due to Python's default recursion limit; irrelevant at kata scale.

---

## ADR-003: No Third-party Libraries

### Status
Accepted

### Context
The kata is self-contained and must be easy to run anywhere Python 3.12+ is installed.

### Decision
Use Python stdlib only (`random`, `dataclasses`, `sys`).

### Rationale
Zero installation friction. No dependency management needed. All required functionality is available in the stdlib.

### Consequences
- (+) `python3 minesweeper/cli.py` is enough to run the game locally.
- (-) No rich terminal rendering (colours, cursor control); plain ASCII board only.

---

## ADR-004: Optional Random Seed for Reproducibility

### Status
Accepted

### Context
Deterministic board generation is needed for automated testing of game scenarios.

### Decision
Accept an optional `--seed` CLI argument passed to `random.seed()` before mine placement.

### Rationale
Costs one line of code; makes the entire game flow testable end-to-end without mocking `random`.

### Consequences
- (+) Test scenarios can use a fixed seed to assert exact board states.
- (-) None significant.
