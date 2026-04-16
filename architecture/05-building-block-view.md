# Chapter 5: Building Block View

## 5.1 Level 1 — Container Diagram (C4)

Diagram source: `architecture/diagrams/c4-container.puml`

```plantuml
@startuml c4-container
!include c4-lib/C4_Container.puml

Person(player, "Player", "Interacts via terminal")

System_Boundary(minesweeper, "Minesweeper") {
  Container(cli, "CLI", "Python module", "Reads stdin, renders board to stdout")
  Container(controller, "Game Controller", "Python module", "Orchestrates game loop and input handling")
  Container(domain, "Domain", "Python module", "Board state, mine placement, reveal/flag logic")
}

Rel(player, cli, "Types commands", "stdin/stdout")
Rel(cli, controller, "Parsed command")
Rel(controller, domain, "Calls")

@enduml
```

### Container Responsibilities

| Container       | Module        | Responsibility                                      |
|-----------------|---------------|-----------------------------------------------------|
| CLI             | `cli.py`      | Parse stdin input, invoke controller, render output.|
| Game Controller | `game.py`     | Game loop, win/loss detection, command dispatch.    |
| Domain          | `board.py`, `cell.py` | Board state, mine placement, reveal/flag rules. |

---

## 5.2 Level 2 — Component Diagram (C4)

Diagram source: `architecture/diagrams/c4-component.puml`

```plantuml
@startuml c4-component
!include c4-lib/C4_Component.puml

Container_Boundary(domain, "Domain") {
  Component(board, "Board", "Class", "Holds cell grid, mine positions, revealed/flagged state")
  Component(cell, "Cell", "Class", "Represents a single cell: mine, adjacent count, state")
  Component(mine_placer, "MinePlacer", "Function", "Randomly distributes mines on the board")
  Component(reveal, "RevealService", "Function", "Reveals a cell; triggers flood-fill for empty cells")
}

Container_Boundary(ctrl, "Game Controller") {
  Component(game, "Game", "Class", "Game loop, win/loss detection, delegates to domain")
}

Container_Boundary(cli_layer, "CLI") {
  Component(renderer, "BoardRenderer", "Function", "Formats and prints board to stdout")
  Component(parser, "InputParser", "Function", "Parses raw input string into command + coordinates")
}

Rel(game, board, "Reads/mutates")
Rel(game, reveal, "Calls")
Rel(reveal, board, "Reads/mutates")
Rel(board, cell, "Contains")
Rel(mine_placer, board, "Populates")
Rel(parser, game, "Passes command")
Rel(game, renderer, "Passes board snapshot")

@enduml
```

### Component Responsibilities

| Component     | Location        | Responsibility                                              |
|---------------|-----------------|-------------------------------------------------------------|
| Board         | `board.py`      | 2D grid of cells; exposes reveal/flag operations.           |
| Cell          | `cell.py`       | Data class: `is_mine`, `adjacent_count`, `revealed`, `flagged`. |
| MinePlacer    | `board.py`      | Randomly places mines and computes adjacent counts.         |
| RevealService | `board.py`      | Reveals a cell; recursively reveals neighbours if empty.    |
| Game          | `game.py`       | Runs the game loop; checks win/loss after each action.      |
| BoardRenderer | `cli.py`        | Renders the board grid and status line to stdout.           |
| InputParser   | `cli.py`        | Parses `"r 2 3"` / `"f 1 4"` into structured commands.     |

---

## 5.3 Module Structure

```
minesweeper/
├── cell.py       # Cell data class
├── board.py      # Board, MinePlacer, RevealService
├── game.py       # Game controller
└── cli.py        # InputParser, BoardRenderer, entry point
```
