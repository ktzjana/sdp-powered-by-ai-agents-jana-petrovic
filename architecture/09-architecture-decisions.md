# Architecture Decision Records

## ADR-001: Use In-Memory State for Game Logic

**Status:** Accepted

**Context:**
The Minesweeper application is designed as a single-player game where the entire game session exists only during runtime. The system needs a simple and efficient way to manage the game board, including mine positions, revealed cells, and player actions.

**Decision:**
The game state will be stored in memory during execution, without using any external database or persistent storage.

**Rationale:**
- The application does not require long-term data storage
- In-memory operations are fast and simple to implement
- This approach reduces system complexity
- It is suitable for both CLI and lightweight web versions of the game

**Consequences:**
- The game state is lost when the application is restarted
- There is no support for saving or resuming games
- Future extensions (e.g., multiplayer or persistence) would require architectural changes
