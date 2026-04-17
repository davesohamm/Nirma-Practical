"""
Shared grid utilities for 2D UAV path planning.

The environment is a rectangular grid:
  - 0 = free cell (drone may occupy the center of that cell)
  - 1 = obstacle (blocked)

Coordinates follow the same convention as the original web app:
  x = column index (left to right)
  y = row index (top to bottom)
"""

from __future__ import annotations

import math
import random
from typing import List, Tuple

Grid = List[List[int]]

# Eight directions: 4 orthogonal + 4 diagonal (typical for UAV on a grid).
# Diagonal steps cost sqrt(2); orthogonal steps cost 1 (same as Dijkstra/A* in the TS app).
DIRECTIONS_8: Tuple[Tuple[int, int], ...] = (
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
    (-1, -1),
    (1, -1),
    (-1, 1),
    (1, 1),
)


def euclidean_dist(ax: float, ay: float, bx: float, by: float) -> float:
    """Straight-line (Euclidean) distance between two points in the plane."""
    return math.hypot(ax - bx, ay - by)


def is_valid(grid: Grid, x: int, y: int) -> bool:
    """True if (x, y) is inside the grid and not an obstacle."""
    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return False
    return grid[y][x] == 0


def move_cost(dx: int, dy: int) -> float:
    """Cost of one step from (0,0) to (dx,dy) with 8-connectivity."""
    if dx != 0 and dy != 0:
        return math.sqrt(2.0)
    return 1.0


def neighbors_8(grid: Grid, x: int, y: int) -> List[Tuple[int, int, float]]:
    """
    Return list of (nx, ny, step_cost) for reachable neighbors from (x, y).
    Skips obstacles and cells outside the grid.
    """
    out: List[Tuple[int, int, float]] = []
    for dx, dy in DIRECTIONS_8:
        nx, ny = x + dx, y + dy
        if is_valid(grid, nx, ny):
            out.append((nx, ny, move_cost(dx, dy)))
    return out


def generate_grid(rows: int, cols: int, density: float = 0.25, seed: int | None = None) -> Grid:
    """
    Build a random obstacle field.

    density: probability [0, 1] that a cell is an obstacle.
    seed: optional RNG seed for reproducible demos / notebooks.
    """
    if seed is not None:
        random.seed(seed)
    grid: Grid = []
    for _ in range(rows):
        row = [1 if random.random() < density else 0 for _ in range(cols)]
        grid.append(row)
    return grid


def clear_corridor(grid: Grid, cx: int, cy: int, radius: int = 1) -> None:
    """Force a small neighborhood around (cx, cy) to be free (in-place)."""
    rows, cols = len(grid), len(grid[0])
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < rows and 0 <= nx < cols:
                grid[ny][nx] = 0


def point_key(x: int, y: int) -> str:
    """Stable string key for dict/set storage of grid cells."""
    return f"{x},{y}"


def parse_key(k: str) -> Tuple[int, int]:
    a, b = k.split(",")
    return int(a), int(b)
