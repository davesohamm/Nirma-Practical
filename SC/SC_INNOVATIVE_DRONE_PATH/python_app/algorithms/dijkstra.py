"""
Dijkstra's shortest-path algorithm on an 8-connected grid.

Idea (intuitive):
  - We keep a "frontier" of cells we can reach, each with the best known cost from the start.
  - Always expand the cheapest cell first (no guess about where the goal is).
  - When we pop the goal, we have proved that no cheaper route exists — classic Dijkstra.

Compared to A*:
  - A* adds a heuristic h(n) so it tends to expand fewer cells toward the goal.
  - Dijkstra is the same logic with h(n) = 0 everywhere.

Time complexity (with a binary heap): O(E log V). Here we use a simple sorted list for
clarity in coursework; for large grids you would swap in heapq.
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional, Tuple

from .grid import Grid, neighbors_8, point_key, parse_key

# Internal node id
Cell = Tuple[int, int]


def run_dijkstra(
    grid: Grid,
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    max_explored_record: int = 800,
) -> dict:
    """
    Run Dijkstra from (start_x, start_y) to (end_x, end_y).

    Returns a dict suitable for JSON:
      path: list of {x, y} from start to goal (inclusive), or [] if unreachable
      distance: sum of step costs along the path (inf if no path)
      nodesExplored: number of cell expansions
      timeMs: wall time
      explored: sampled list of {x,y} in expansion order (for visualization)
    """
    t0 = time.perf_counter()

    if grid[start_y][start_x] != 0 or grid[end_y][end_x] != 0:
        return _empty_result("Dijkstra", t0)

    start: Cell = (start_x, start_y)
    goal: Cell = (end_x, end_y)

    # Best known cost from start to each cell
    dist: Dict[str, float] = {point_key(*start): 0.0}
    # For path reconstruction: predecessor of each cell
    came_from: Dict[str, str] = {}
    closed: set[str] = set()

    # Priority queue as (distance, x, y) — list we sort each iteration (simple, readable)
    open_list: List[Tuple[float, int, int]] = [(0.0, start_x, start_y)]

    nodes_explored = 0
    explored_order: List[dict] = []
    sample_stride = 1

    while open_list:
        open_list.sort(key=lambda t: t[0])
        d, cx, cy = open_list.pop(0)
        ck = point_key(cx, cy)
        if ck in closed:
            continue

        # Skip stale entries (we relaxed this cell again with lower cost later)
        if d > dist.get(ck, float("inf")):
            continue

        closed.add(ck)
        nodes_explored += 1

        if len(explored_order) < max_explored_record:
            if nodes_explored % sample_stride == 0:
                explored_order.append({"x": cx, "y": cy})

        if (cx, cy) == goal:
            path = _reconstruct_path(came_from, start, goal)
            return {
                "algorithm": "Dijkstra",
                "path": path,
                "distance": dist[ck],
                "nodesExplored": nodes_explored,
                "timeMs": (time.perf_counter() - t0) * 1000.0,
                "explored": explored_order,
            }

        for nx, ny, step_cost in neighbors_8(grid, cx, cy):
            nk = point_key(nx, ny)
            if nk in closed:
                continue
            tentative = d + step_cost
            if tentative < dist.get(nk, float("inf")):
                dist[nk] = tentative
                came_from[nk] = ck
                open_list.append((tentative, nx, ny))

    return {
        "algorithm": "Dijkstra",
        "path": [],
        "distance": float("inf"),
        "nodesExplored": nodes_explored,
        "timeMs": (time.perf_counter() - t0) * 1000.0,
        "explored": explored_order,
    }


def _reconstruct_path(came_from: Dict[str, str], start: Cell, goal: Cell) -> List[dict]:
    """Walk predecessors from goal back to start, then reverse."""
    path_cells: List[Cell] = []
    cur: Optional[Cell] = goal
    sk = point_key(*start)

    while cur is not None:
        path_cells.append(cur)
        if point_key(*cur) == sk:
            break
        pk = point_key(*cur)
        if pk not in came_from:
            return []
        px, py = parse_key(came_from[pk])
        cur = (px, py)
    else:
        return []

    path_cells.reverse()
    # Guarantee exact endpoints (integer grid cells)
    out = [{"x": int(x), "y": int(y)} for x, y in path_cells]
    if out:
        out[0] = {"x": start[0], "y": start[1]}
        out[-1] = {"x": goal[0], "y": goal[1]}
    return out


def _empty_result(name: str, t0: float) -> dict:
    return {
        "algorithm": name,
        "path": [],
        "distance": float("inf"),
        "nodesExplored": 0,
        "timeMs": (time.perf_counter() - t0) * 1000.0,
        "explored": [],
    }
