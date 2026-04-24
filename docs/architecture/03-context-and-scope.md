# Chapter 3: System Scope and Context

## 3.1 System Scope

Minesweeper is a self-contained CLI application. It has no external systems, databases, or network dependencies. The only actor is the human player interacting through a terminal.

## 3.2 Context Diagram (C4 Level 1)

Diagram source: `docs/architecture/diagrams/c4-context.puml`

```plantuml
@startuml c4-context
!include c4-lib/C4_Context.puml

Person(player, "Player", "Runs the game via CLI and interacts by typing commands")
System(minesweeper, "Minesweeper", "CLI-based puzzle game. Manages board state, processes player input, and displays results.")

Rel(player, minesweeper, "Reveal cell / Flag cell / Start game", "stdin/stdout")

@enduml
```

## 3.3 External Interfaces

| Interface | Direction | Description                              |
|-----------|-----------|------------------------------------------|
| stdin     | In        | Player types commands (e.g. `r 2 3`, `f 1 4`). |
| stdout    | Out       | Game renders the board and status messages. |

There are no other external interfaces.
