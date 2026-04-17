"""
A* search on the same 8-connected grid as Dijkstra.

Core idea:
  - Each cell n has:
      g(n) = actual best cost found so far from start to n
      h(n) = heuristic estimate from n to goal (we use Euclidean distance)
      f(n) = g(n) + h(n)
  - We always expand the cell with the smallest f. The heuristic is "admissible"
    (never overestimates true cost), so the first time we pop the goal, g(goal)
    is optimal — same optimal path cost as Dijkstra, usually fewer expansions.

This is the standard textbook A* on a grid with nonnegative edge costs.
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional, Tuple

from .grid import Grid, euclidean_dist, neighbors_8, point_key, parse_key

Cell = Tuple[int, int]


def run_astar(
    grid: Grid,
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    max_explored_record: int = 800,
) -> dict:
    """
    Run A* from start to goal.

    Return shape matches Dijkstra (path, distance, nodesExplored, timeMs, explored).
    """
    t0 = time.perf_counter()

    if grid[start_y][start_x] != 0 or grid[end_y][end_x] != 0:
        return _empty_result("A*", t0)

    start: Cell = (start_x, start_y)
    goal: Cell = (end_x, end_y)

    def h(x: int, y: int) -> float:
        return euclidean_dist(x, y, end_x, end_y)

    g_score: Dict[str, float] = {point_key(*start): 0.0}
    came_from: Dict[str, str] = {}
    closed: set[str] = set()

    # (f, g, x, y)
    open_list: List[Tuple[float, float, int, int]] = [(h(*start), 0.0, start_x, start_y)]

    nodes_explored = 0
    explored_order: List[dict] = []

    while open_list:
        open_list.sort(key=lambda t: t[0])
        f, g, cx, cy = open_list.pop(0)
        ck = point_key(cx, cy)
        if ck in closed:
            continue
        if g > g_score.get(ck, float("inf")):
            continue

        closed.add(ck)
        nodes_explored += 1

        if len(explored_order) < max_explored_record:
            explored_order.append({"x": cx, "y": cy})

        if (cx, cy) == goal:
            path = _reconstruct_path(came_from, start, goal)
            return {
                "algorithm": "A*",
                "path": path,
                "distance": g_score[ck],
                "nodesExplored": nodes_explored,
                "timeMs": (time.perf_counter() - t0) * 1000.0,
                "explored": explored_order,
            }

        for nx, ny, step_cost in neighbors_8(grid, cx, cy):
            nk = point_key(nx, ny)
            if nk in closed:
                continue
            tentative_g = g + step_cost
            if tentative_g < g_score.get(nk, float("inf")):
                came_from[nk] = ck
                g_score[nk] = tentative_g
                f_new = tentative_g + h(nx, ny)
                open_list.append((f_new, tentative_g, nx, ny))

    return {
        "algorithm": "A*",
        "path": [],
        "distance": float("inf"),
        "nodesExplored": nodes_explored,
        "timeMs": (time.perf_counter() - t0) * 1000.0,
        "explored": explored_order,
    }


def _reconstruct_path(came_from: Dict[str, str], start: Cell, goal: Cell) -> List[dict]:
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
