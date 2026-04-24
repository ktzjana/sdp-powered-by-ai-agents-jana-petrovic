# Chapter 12: Glossary

| Term              | Definition                                                                 |
|-------------------|----------------------------------------------------------------------------|
| Board             | The 2D grid of cells that represents the game state.                       |
| Cell              | A single position on the board. Has state: hidden, revealed, or flagged.   |
| Mine              | A hidden hazard placed on a cell. Revealing it ends the game as a loss.    |
| Adjacent count    | The number of mines in the 8 neighbouring cells of a given cell.           |
| Reveal            | Player action that uncovers a cell. Triggers flood-fill if cell is empty.  |
| Flag              | Player action that marks a cell as a suspected mine without revealing it.  |
| Flood-fill        | Recursive auto-reveal of all connected empty cells when an empty cell is revealed. |
| Empty cell        | A cell with no mine and an adjacent count of zero.                         |
| Win condition     | All safe (non-mine) cells have been revealed.                              |
| Loss condition    | The player reveals a cell containing a mine.                               |
| CLI               | Command-Line Interface; the terminal-based I/O layer of the application.   |
| Container (C4)    | A deployable/runnable unit within a system in the C4 model.                |
| Component (C4)    | A grouping of related code within a container in the C4 model.             |
| ADR               | Architecture Decision Record; documents a significant design choice.       |
| Kata              | A small, self-contained coding exercise used for practice.                 |
