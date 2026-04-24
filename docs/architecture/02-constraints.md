# Chapter 2: Architecture Constraints

## 2.1 Technical Constraints

| ID   | Constraint                                                      |
|------|-----------------------------------------------------------------|
| TC-1 | Implementation language is Python (3.12+).                      |
| TC-2 | Interface is CLI only; no GUI, web, or API layer.               |
| TC-3 | No database or persistent storage; all state is in-memory.      |
| TC-4 | No external runtime dependencies required (stdlib only).        |

## 2.2 Organisational Constraints

| ID   | Constraint                                                      |
|------|-----------------------------------------------------------------|
| OC-1 | This is a kata; scope is intentionally small and self-contained.|
| OC-2 | Code must be unit-testable (core logic decoupled from I/O).     |

## 2.3 Conventions

| ID   | Convention                                                      |
|------|-----------------------------------------------------------------|
| CV-1 | Follow PEP 8 style guidelines.                                  |
| CV-2 | Diagrams use C4 model notation with PlantUML.                   |
