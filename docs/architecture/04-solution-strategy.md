# Chapter 4: Solution Strategy

## 4.1 Core Approach

Separate the domain logic from I/O using a three-layer structure:

| Layer      | Responsibility                                      |
|------------|-----------------------------------------------------|
| Domain     | Board state, mine placement, reveal/flag rules.     |
| Controller | Translates player input into domain operations.     |
| CLI View   | Renders board and messages to stdout.               |

This keeps the domain fully unit-testable without touching the terminal.

## 4.2 Key Design Decisions

| Decision                          | Rationale                                                  |
|-----------------------------------|------------------------------------------------------------|
| In-memory board as a 2D structure | No persistence needed; simple and direct.                  |
| Flood-fill reveal via recursion   | Natural fit for the empty-cell auto-reveal rule (FR-6).    |
| Single-process, synchronous flow  | CLI kata; no concurrency or async complexity needed.       |
| No third-party libraries          | Keeps the kata self-contained (TC-4).                      |

## 4.3 Quality Goal Mapping

| Quality Goal | Strategy                                                        |
|--------------|-----------------------------------------------------------------|
| Correctness  | Domain logic encapsulated in `Board`; rules enforced centrally. |
| Testability  | Domain layer has no I/O dependencies; pure functions where possible. |
| Simplicity   | Three layers, no frameworks, no over-abstraction.               |
