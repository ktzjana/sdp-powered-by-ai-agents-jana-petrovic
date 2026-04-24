# Chapter 5: Building Block View

## 5.1 Level 1 — Container Diagram (C4)

![Container Diagram](diagrams/c4-container.svg)

Diagram source: `docs/architecture/diagrams/c4-container.puml`

### Container Responsibilities

| Container       | Module        | Responsibility                                      |
|-----------------|---------------|-----------------------------------------------------|
| CLI             | `cli.py`      | Parse stdin input, invoke controller, render output.|
| Game Controller | `game.py`     | Reveal/flag orchestration and win/loss state transitions. |
| Domain          | `board.py`    | Board state, mine placement, reveal/flag rules.     |

---

## 5.2 Level 2 — Component Diagram (C4)

![Component Diagram](diagrams/c4-component.svg)

Diagram source: `docs/architecture/diagrams/c4-component.puml`

### Component Responsibilities

| Component     | Location        | Responsibility                                              |
|---------------|-----------------|-------------------------------------------------------------|
| Board         | `board.py`      | 2D grid of  cells; exposes reveal/flag operations.           |
| Cell          | `board.py`      | Data class: `is_mine`, `adjacent_count`, `revealed`, `flagged`. |
| MinePlacer    | `board.py`      | Randomly places mines and computes adjacent counts.         |
| RevealService | `board.py`      | Reveals a cell; recursively reveals neighbours if empty.    |
| Game          | `game.py`       | Applies reveal/flag actions and updates game state (`PLAYING`/`WIN`/`LOSS`). |
| BoardRenderer | `renderer.py`   | Renders the board grid and status line to stdout.           |
| InputParser   | `input_parser.py` | Utility parser for `"r 2 3"` / `"f 1 4"` command objects (not wired into the main CLI loop). |

---

## 5.3 Module Structure

```
minesweeper/
├── board.py      # Board, MinePlacer, RevealService
├── input_parser.py # InputParser + Command
├── renderer.py   # BoardRenderer
├── game.py       # Game controller
└── cli.py        # CLI entry point
```
