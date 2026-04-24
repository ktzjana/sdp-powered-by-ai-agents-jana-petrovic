# Chapter 10: Quality Requirements

## 10.1 Quality Tree

| Quality Goal | Scenario                                              | Measure                                              |
|--------------|-------------------------------------------------------|------------------------------------------------------|
| Correctness  | Player reveals a mine → game ends immediately as loss. | All game-rule scenarios pass unit tests.             |
| Correctness  | Player reveals last safe cell → game ends as win.     | Win condition verified by unit test with fixed seed. |
| Correctness  | Flood-fill reveals all connected empty cells.         | Board state matches expected after reveal.           |
| Testability  | Domain logic is tested without CLI.                   | All domain tests run with no stdin/stdout dependency.|
| Simplicity   | New developer understands the codebase quickly.       | ≤ 5 core source files, each with a single clear responsibility. |
| Robustness   | Player enters malformed input.                        | Game prints usage and re-prompts without crashing.   |

## 10.2 Quality Scenarios (arc42 format)

### QS-1: Correctness — Mine Hit
- **Stimulus:** Player reveals a cell containing a mine.
- **Response:** `Board.reveal()` returns `MINE_HIT`; `Game` transitions to loss state.
- **Measure:** Verified by unit test; no exceptions thrown.

### QS-2: Correctness — Win Detection
- **Stimulus:** Player reveals the last unrevealed safe cell.
- **Response:** `Game.check_win()` returns `True`; CLI prints win message.
- **Measure:** Verified by unit test with fixed seed.

### QS-3: Testability — Domain Isolation
- **Stimulus:** Developer runs domain unit tests.
- **Response:** All tests pass with no mocking of I/O.
- **Measure:** `pytest tests/test_board.py tests/test_game.py tests/test_flag.py tests/test_win_loss.py` passes with no I/O mocking.

### QS-4: Robustness — Malformed Input
- **Stimulus:** Player types `"xyz"` or `"r a b"`.
- **Response:** CLI prints a usage hint and re-prompts.
- **Measure:** Process does not exit or raise an unhandled exception.
