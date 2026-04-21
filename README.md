# Ai-ARI711S Assignment 1 — Ninjas 2026

**Qualification:** Bachelor of Computer Science (Software Development)  
**Course:** Artificial Intelligence (ARI711S)  
**NQF Level:** 7  
**Due Date:** 26 April 2026

---

## Group Members

| Name | Student Number | GitHub Username |
|------|---------------|----------------|
| Haihambo T. Lineekela | 223090506 | lineekela065 |
| Elton Lisho | 216070325 | EltonLisho |
| Moses N. Lasarus | 224067834 | moseslazarus960 |
| Ntinda Simon | 224028162 | 224028162 |
| Amutenya N. Matias | 223100188 | uncledope03 |

---

## Assignment Overview

This repository contains Python notebook solutions for three AI problems:

| Question | Topic | Marks |
|----------|-------|-------|
| Q1 | Search Algorithms — Warehouse Logistics Robot | 25 |
| Q2 | Optimisation — Telecom Tower Placement (CSP) | 25 |
| Q3 | Adversarial Search — Tic-Tac-Toe with Minimax | 25 |

---

## Repository Structure

```
├── README.md
├── LICENSE
├── ARI711S_Assignment1_Ninjas2026.ipynb   ← Combined notebook (all questions)
│
├── question1/
│   ├── question1_warehouse_search.ipynb   ← Q1 standalone notebook
│   └── warehouse.txt                      ← Warehouse layout input file
│
├── question2/
│   └── question2_telecom_tower_placement.ipynb  ← Q2 standalone notebook
│
└── question3/
    └── question3_tictactoe_minimax.ipynb  ← Q3 standalone notebook
```

---

## Question 1 — Warehouse Logistics Robot (Search Algorithms)

**Algorithms implemented:**
- Greedy Best-First Search — priority based on `h(n)` (Euclidean distance to goal)
- A\* Search — priority based on `f(n) = g(n) + h(n)`

**Key components:**
- `Node` class — stores state, parent, action, and path cost `g(n)`
- `Warehouse` class — parses `.txt` layout, locates A/B, stores walls, finds neighbours
- `solve(algorithm)` — priority queue search with cycle prevention
- Visual output: `warehouse_path.png` with colour-coded path, explored cells, and walls

**To run:**
1. Place your `warehouse.txt` file in the `question1/` directory
2. Open and run `question1_warehouse_search.ipynb`

---

## Question 2 — Telecommunication Tower Placement (CSP)

**Problem:** Place 8 signal boosters on a 10×10 grid satisfying:
- No two towers in the same row or column
- No two towers in adjacent cells (including diagonals)
- No towers on mountain (prohibited) cells

**Key components:**
- `Telecom_CSP_Solver` class with backtracking search
- MRV heuristic — selects the most constrained unassigned variable
- Forward Checking — prunes domains after each placement
- `is_consistent()` — validates all constraints before placement

**Test Levels:**
| Level | Name | Mountains |
|-------|------|-----------|
| 1 | Coastal (Easy) | 3 scattered cells |
| 2 | Highlands (Medium) | 7 cells in clusters |
| 3 | Brandberg (Hard) | 10 cells forming an L-wall |

---

## Question 3 — Tic-Tac-Toe with Minimax (Adversarial Search)

**Algorithm:** Minimax with Alpha-Beta Pruning

**Functions implemented:**
- `player(board)` — returns whose turn it is (X or O)
- `actions(board)` — returns all valid moves
- `result(board, action)` — returns new board without modifying original
- `winner(board)` — checks all 8 winning lines
- `terminal(board)` — detects end of game
- `utility(board)` — scores terminal states (+1, −1, 0)
- `minimax(board)` — returns the optimal move

The AI is **unbeatable** — it always wins or draws, never loses.

---

## How to Run

### Requirements

```bash
pip install jupyter matplotlib numpy
```

### Running the combined notebook

```bash
jupyter notebook ARI711S_Assignment1_Ninjas2026.ipynb
```

### Running individual question notebooks

```bash
jupyter notebook question1/question1_warehouse_search.ipynb
jupyter notebook question2/question2_telecom_tower_placement.ipynb
jupyter notebook question3/question3_tictactoe_minimax.ipynb
```

---

## Output Files Generated

| File | Description |
|------|-------------|
| `warehouse_path.png` | A\* path visualisation |
| `warehouse_path_greedy.png` | Greedy path visualisation |
| `warehouse_comparison.png` | Side-by-side algorithm comparison |
| `towers_level1_coastal.png` | Level 1 tower placement grid |
| `towers_level2_highlands.png` | Level 2 tower placement grid |
| `towers_level3_brandberg.png` | Level 3 tower placement grid |
| `towers_all_levels.png` | All three levels comparison |

---

## References

- Russell, S. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.)
- Lecture slides and practical lab materials — ARI711S, NUST 2026
