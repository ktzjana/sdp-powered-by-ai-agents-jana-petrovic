# Chapter 1: Introduction and Goals

## 1.1 Purpose

Minesweeper is a CLI-based puzzle game implemented in Python. The player uncovers cells on a grid, avoids mines, and wins by revealing all safe cells.

## 1.2 Functional Requirements

| ID   | Requirement                                                  |
|------|--------------------------------------------------------------|
| FR-1 | The game generates a grid of configurable size with randomly placed mines. |
| FR-2 | The player can reveal a cell by coordinates.                 |
| FR-3 | The player can flag/unflag a cell as a suspected mine.       |
| FR-4 | Revealing a mine ends the game (loss).                       |
| FR-5 | Revealing all safe cells ends the game (win).                |
| FR-6 | Revealing an empty cell (no adjacent mines) auto-reveals its neighbours. |
| FR-7 | The CLI displays the current board state after each action.  |

## 1.3 Quality Goals

| Priority | Quality Goal   | Motivation                                              |
|----------|----------------|---------------------------------------------------------|
| 1        | Correctness    | Game rules must be implemented accurately.              |
| 2        | Testability    | Core logic must be unit-testable without the CLI layer. |
| 3        | Simplicity     | Small kata; avoid over-engineering.                     |

## 1.4 Stakeholders

| Role       | Expectation                                      |
|------------|--------------------------------------------------|
| Player     | A playable, rule-correct Minesweeper game in CLI.|
| Developer  | Clean, testable code with clear separation of concerns. |
