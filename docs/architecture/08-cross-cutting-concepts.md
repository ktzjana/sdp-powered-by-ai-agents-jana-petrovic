# Chapter 8: Cross-cutting Concepts

## 8.1 Authentication & Authorisation

Not applicable. This is a single-user local CLI game with no access control.

---

## 8.2 Error Handling

| Error Scenario                  | Handling Strategy                                              |
|---------------------------------|----------------------------------------------------------------|
| Invalid input format            | `InputParser` catches parse errors, prints usage hint, re-prompts. |
| Out-of-bounds coordinates       | `Board` raises `ValueError`; `Game` catches and re-prompts.   |
| Reveal on already-revealed cell | `Board` silently ignores; no state change.                     |
| Flag on already-revealed cell   | `Board` silently ignores; no state change.                     |

Errors never crash the process; the game loop continues until win, loss, or quit.

---

## 8.3 Logging

No logging framework is used. The CLI renders board state and status messages directly to stdout after every action. This is sufficient for a kata-sized application.

---

## 8.4 Input Validation

`InputParser` enforces the command grammar before any domain call is made:

- Accepted commands: `r <row> <col>`, `f <row> <col>`, `q` (quit)
- Coordinates must be integers within board bounds
- Any other input prints a usage line and re-prompts

---

## 8.5 Randomness

Mine placement uses Python's `random` module. A seed can optionally be accepted at startup to make games reproducible (useful for testing).
