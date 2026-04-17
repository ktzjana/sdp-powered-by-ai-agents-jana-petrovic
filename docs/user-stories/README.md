# User Stories

## Domains

The following domains are derived from the bounded contexts identified in the architecture:

- **BOARD** — Domain layer: holds the cell grid, manages mine placement, tracks revealed/flagged state, and executes the flood-fill reveal logic (`board.py`, `cell.py`)
- **GAME** — Game Controller layer: orchestrates the game loop, dispatches reveal/flag commands to the domain, and evaluates win/loss conditions (`game.py`)
- **CLI** — Presentation layer: parses player input from stdin, invokes the controller, and renders the board to stdout (`cli.py`)

These domains directly map to the containers defined in the Building Block View (Chapter 5) and are used as the basis for story IDs and traceability.

---

## DDD Building Blocks

> Architecture reference: Chapter 5 Building Block View, Chapter 12 Glossary

### Entities

- `Cell` — has a unique identity defined by its coordinates `(row, col)` on the board; its state (`revealed`, `flagged`, `is_mine`, `adjacent_count`) changes over the course of the game

### Aggregates

- `Board` — aggregate root that owns the full 2D grid of `Cell` objects and mine positions; all reveal and flag operations are routed through `Board` to maintain consistency (Chapter 5 Building Block View)

### Value Objects

- `(row, col)` coordinates — immutable pair that identifies a cell position; defined by its value, not identity
- `adjacent_count` — immutable integer computed once during mine placement; describes how many of the 8 neighbours contain a mine

### Domain Services

- `MinePlacer` — stateless service that randomly distributes mines across the board and computes adjacent counts for all safe cells (Chapter 5 Building Block View)
- `RevealService` — stateless service that reveals a cell and recursively triggers flood-fill for empty cells (Chapter 5 Building Block View, Chapter 6 Runtime View)
- `Game` — stateless orchestration service that runs the game loop and checks win/loss after every player action (Chapter 5 Building Block View)

---

## Prioritized Story Inventory

### Core Stories (Pareto 20%)

- `BOARD-STORY-001`
  **AS A** player
  **I WANT** the game to generate a grid with randomly placed mines
  **SO THAT** each game session presents a unique challenge

- `GAME-STORY-001`
  **AS A** player
  **I WANT** to reveal a cell by entering its coordinates
  **SO THAT** I can uncover the board and progress toward winning

- `GAME-STORY-002`
  **AS A** player
  **I WANT** the game to detect when I have won or lost
  **SO THAT** the game ends with clear feedback

### Supporting Stories (Remaining 80%)

- `GAME-STORY-003`
  **AS A** player
  **I WANT** to flag and unflag a cell as a suspected mine
  **SO THAT** I can track my guesses visually on the board

- `CLI-STORY-001`
  **AS A** player
  **I WANT** to type commands like `r 2 3` or `f 1 4` in the terminal
  **SO THAT** I can interact with the game without a graphical interface

- `CLI-STORY-002`
  **AS A** player
  **I WANT** the board to be rendered clearly in the terminal after each action
  **SO THAT** I can see the current game state at all times

---

## Pareto Prioritization

The three core stories represent the minimal viable Minesweeper game. They are chosen because:

1. `BOARD-STORY-001` — without board initialisation and mine placement, no game state exists; it unblocks every other story
2. `GAME-STORY-001` — revealing cells is the central player action; it exercises `Board`, `RevealService`, `Game`, and `CLI` together and directly delivers the main user value of the kata
3. `GAME-STORY-002` — without win/loss detection, the game loop never terminates correctly; it closes the end-to-end gameplay flow

Together they exercise all three architectural layers (CLI → Game Controller → Domain) and the key runtime scenarios described in Chapter 6. All supporting stories are extensions or refinements of these three.

---

## Progress Tracking

📊 Pareto Progress: 3/3 core stories (100% of 20% core stories)
🎯 Supporting story coverage: 5/5 supporting stories written — all stories complete

| Story Bundle      | Status       | File                                    |
|-------------------|--------------|-----------------------------------------|
| `BOARD-STORY-001` | ✅ Written   | `docs/user-stories/board.md`            |
| `GAME-STORY-001`  | ✅ Written   | `docs/user-stories/game-reveal.md`      |
| `GAME-STORY-002`  | ✅ Written   | `docs/user-stories/game-win-loss.md`    |
| `GAME-STORY-003`  | ✅ Written   | `docs/user-stories/game-flag.md`        |
| `CLI-STORY-001`   | ✅ Written   | `docs/user-stories/cli-story-001.md`    |
| `CLI-STORY-002`   | ✅ Written   | `docs/user-stories/cli-story-002.md`    |
