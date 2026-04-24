# Chapter 8: Cross-cutting Concepts

## 8.1 Authentication & Authorisation

Not applicable. This is a single-user local CLI game with no access control.

---

## 8.2 Error Handling

| Error Scenario                  | Handling Strategy                                              |
|---------------------------------|----------------------------------------------------------------|
| Invalid input format            | `cli.py` validates command shape/integer conversion, prints usage hint, re-prompts. |
| Out-of-bounds coordinates       | No explicit bounds validation in CLI/game; currently a known gap (see Chapter 11). |
| Reveal on already-revealed cell | `Board` silently ignores; no state change.                     |
| Flag on already-revealed cell   | `Board` silently ignores; no state change.                     |

For malformed command format, the game loop continues until win, loss, or quit.

---

## 8.3 Logging

No logging framework is used. The CLI renders board state and status messages directly to stdout after every action. This is sufficient for a kata-sized application.

---

## 8.4 Input Validation

`cli.py` currently enforces the command grammar before domain calls:

- Accepted commands: `r <row> <col>`, `f <row> <col>`, `q` (quit)
- Coordinates are parsed as integers
- Any malformed input prints a usage line and re-prompts
- Bounds validation is not yet enforced in CLI (tracked as technical debt)

---

## 8.5 Randomness

Mine placement uses Python's `random` module. A seed can optionally be accepted at startup to make games reproducible (useful for testing).
