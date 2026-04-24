# Chapter 11: Risks and Technical Debts

## 11.1 Risks

| ID   | Risk                                      | Likelihood | Impact | Mitigation                                              |
|------|-------------------------------------------|------------|--------|---------------------------------------------------------|
| R-1  | Recursive flood-fill hits Python recursion limit on large grids. | Low | Medium | Kata grids are small; document the limit. Convert to iterative if grid size grows. |
| R-2  | Mine placement produces unsolvable board (mine on first reveal). | Medium | Low | Defer first-reveal safety to a future iteration; acceptable for a kata. |
| R-3  | Out-of-bounds coordinates can cause unhandled errors. | Medium | Medium | Add explicit bounds checks in CLI or `Board.cell()` before dispatch. |

## 11.2 Technical Debts

| ID   | Debt                                      | Impact | Resolution Path                                         |
|------|-------------------------------------------|--------|---------------------------------------------------------|
| TD-1 | No first-reveal safety (mine can be at the player's first pick). | Low | Regenerate or relocate mines after first reveal if needed. |
| TD-2 | Plain ASCII rendering; no colour or cursor control. | Low | Replace `BoardRenderer` with a `curses`-based renderer if desired. |
| TD-3 | `InputParser` utility is not wired into `cli.py` main loop. | Low | Route CLI command parsing through `InputParser.parse()`. |
| TD-4 | No explicit coordinate bounds validation in interactive flow. | Medium | Validate `0 <= row < rows` and `0 <= col < cols` before calling `Game`. |
