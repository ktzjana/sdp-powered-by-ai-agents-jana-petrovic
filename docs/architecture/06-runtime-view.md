# Chapter 6: Runtime View

Three key scenarios are documented below.

---

## 6.1 Scenario: Reveal a Cell

Diagram source: `docs/architecture/diagrams/seq-reveal-cell.puml`

```plantuml
@startuml seq-reveal-cell
participant Player
participant CLI
participant Game
participant Board

Player -> CLI : "r 2 3"
CLI -> CLI : InputParser.parse("r 2 3")
CLI -> Game : reveal(row=2, col=3)
Game -> Board : reveal(2, 3)
alt cell is mine
  Board --> Game : MINE_HIT
  Game --> CLI : game_over(loss)
  CLI --> Player : "BOOM! You hit a mine."
else cell is empty (no adjacent mines)
  Board -> Board : flood_fill(2, 3)
  Board --> Game : OK
  Game -> Game : check_win()
  Game --> CLI : board_state
  CLI --> Player : rendered board
else cell has adjacent mines
  Board --> Game : OK
  Game -> Game : check_win()
  Game --> CLI : board_state
  CLI --> Player : rendered board
end
@enduml
```

---

## 6.2 Scenario: Flag a Cell

Diagram source: `docs/architecture/diagrams/seq-flag-cell.puml`

```plantuml
@startuml seq-flag-cell
participant Player
participant CLI
participant Game
participant Board

Player -> CLI : "f 1 4"
CLI -> CLI : InputParser.parse("f 1 4")
CLI -> Game : flag(row=1, col=4)
Game -> Board : toggle_flag(1, 4)
Board --> Game : OK
Game --> CLI : board_state
CLI --> Player : rendered board
@enduml
```

---

## 6.3 Scenario: Win Condition

Diagram source: `docs/architecture/diagrams/seq-win.puml`

```plantuml
@startuml seq-win
participant Player
participant CLI
participant Game
participant Board

Player -> CLI : "r 3 3"
CLI -> Game : reveal(row=3, col=3)
Game -> Board : reveal(3, 3)
Board --> Game : OK
Game -> Game : check_win()
note right: all safe cells revealed?
Game --> CLI : game_over(win)
CLI --> Player : "You win!"
@enduml
```
