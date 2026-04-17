"""
Particle Swarm Optimization (PSO) for a simple UAV path shape.

This is NOT the same problem as grid-shortest-path:
  - A* and Dijkstra snap the drone to grid centers and only allow 8-connected moves.
  - Here each particle owns a few *continuous* waypoints between fixed start and goal.
    The path is: start -> waypoint_1 -> ... -> waypoint_k -> goal, with straight segments.

Fitness penalizes:
  - long total length
  - samples along each segment that hit obstacle cells (soft constraint via penalty)

Why use PSO in a Soft Computing course?
  - It is a population-based metaheuristic: many candidate solutions cooperate through
    "personal best" and "global best" without explicit gradient formulas.
  - Good for explaining exploration vs exploitation (inertia w, cognitive c1, social c2).

Limitations (honest, for your report):
  - Does not guarantee the true shortest path or even a collision-free path unless
    the penalty is large enough and the swarm has time to converge.
  - Waypoints are ordered by distance from start for drawing; this is a simple
    heuristic to get a single polyline order.
"""

from __future__ import annotations

import math
import random
import time
from typing import List, Sequence, Tuple

from .grid import Grid, euclidean_dist

PointF = Tuple[float, float]


def _count_line_collisions(grid: Grid, x1: float, y1: float, x2: float, y2: float) -> int:
    """
    Sample along the segment from (x1,y1) to (x2,y2) in grid space.
    Count samples that land on obstacle cells (grid value 1).
    """
    steps = max(1, int(math.ceil(max(abs(x2 - x1), abs(y2 - y1)) * 3)))
    hits = 0
    rows, cols = len(grid), len(grid[0])
    for i in range(steps + 1):
        t = i / steps
        x = int(round(x1 + t * (x2 - x1)))
        y = int(round(y1 + t * (y2 - y1)))
        if 0 <= y < rows and 0 <= x < cols and grid[y][x] == 1:
            hits += 1
    return hits


def _fitness(
    grid: Grid,
    sx: float,
    sy: float,
    ex: float,
    ey: float,
    waypoints: Sequence[PointF],
) -> Tuple[float, float]:
    """
    Return (fitness, geometric_length) where lower fitness is better.
    fitness = length + penalty_weight * collision_samples
    """
    ordered = sorted(waypoints, key=lambda p: euclidean_dist(sx, sy, p[0], p[1]))
    full: List[PointF] = [(sx, sy)] + list(ordered) + [(ex, ey)]

    length = 0.0
    penalty = 0.0
    wpen = 10.0  # same spirit as the original TS implementation
    for i in range(len(full) - 1):
        ax, ay = full[i]
        bx, by = full[i + 1]
        length += euclidean_dist(ax, ay, bx, by)
        penalty += wpen * _count_line_collisions(grid, ax, ay, bx, by)

    return length + penalty, length


def run_pso(
    grid: Grid,
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    num_particles: int = 30,
    num_waypoints: int = 5,
    max_iterations: int = 100,
    seed: int | None = None,
) -> dict:
    """
    Run PSO and return JSON-friendly result.

    Extra fields vs graph algorithms:
      fitnessHistory: best fitness per iteration (for line charts)
      path: polyline as {x,y} floats (frontend snaps to cell centers for drawing)
    """
    t0 = time.perf_counter()
    if seed is not None:
        random.seed(seed)

    rows, cols = len(grid), len(grid[0])
    sx, sy = float(start_x), float(start_y)
    ex, ey = float(end_x), float(end_y)

    w = 0.7
    c1 = 1.5
    c2 = 1.5

    # Each particle: waypoints + velocities + personal best
    particles: List[dict] = []
    global_best_wp: List[PointF] = []
    global_best_fitness = float("inf")
    global_best_length = float("inf")

    def rand_wp() -> PointF:
        return (random.random() * (cols - 1), random.random() * (rows - 1))

    for _ in range(num_particles):
        wps = [rand_wp() for _ in range(num_waypoints)]
        vel = [((random.random() - 0.5) * 2.0, (random.random() - 0.5) * 2.0) for _ in range(num_waypoints)]
        fit, ln = _fitness(grid, sx, sy, ex, ey, wps)
        particles.append(
            {
                "wps": wps,
                "vel": vel,
                "pbest": list(wps),
                "pbest_f": fit,
            }
        )
        if fit < global_best_fitness:
            global_best_fitness = fit
            global_best_length = ln
            global_best_wp = [tuple(p) for p in wps]

    fitness_history: List[float] = []

    for _ in range(max_iterations):
        for p in particles:
            wps: List[PointF] = p["wps"]
            vel: List[Tuple[float, float]] = p["vel"]
            pbest: List[PointF] = p["pbest"]

            for j in range(num_waypoints):
                r1, r2 = random.random(), random.random()
                gx, gy = global_best_wp[j]
                px, py = pbest[j]
                vx, vy = vel[j]
                vx = w * vx + c1 * r1 * (px - wps[j][0]) + c2 * r2 * (gx - wps[j][0])
                vy = w * vy + c1 * r1 * (py - wps[j][1]) + c2 * r2 * (gy - wps[j][1])
                vel[j] = (vx, vy)
                nx = max(0.0, min(float(cols - 1), wps[j][0] + vx))
                ny = max(0.0, min(float(rows - 1), wps[j][1] + vy))
                wps[j] = (nx, ny)

            fit, ln = _fitness(grid, sx, sy, ex, ey, wps)
            if fit < p["pbest_f"]:
                p["pbest_f"] = fit
                p["pbest"] = list(wps)
            if fit < global_best_fitness:
                global_best_fitness = fit
                global_best_length = ln
                global_best_wp = [tuple(q) for q in wps]

        fitness_history.append(global_best_fitness)

    # Build display path: exact grid endpoints + ordered waypoints (float OK for SVG centers)
    ordered_best = sorted(global_best_wp, key=lambda p: euclidean_dist(sx, sy, p[0], p[1]))
    path_points: List[dict] = [{"x": start_x, "y": start_y}]
    for wx, wy in ordered_best:
        path_points.append({"x": wx, "y": wy})
    path_points.append({"x": end_x, "y": end_y})

    # Remove duplicate consecutive points (numerical noise)
    deduped: List[dict] = []
    for pt in path_points:
        if not deduped:
            deduped.append(pt)
            continue
        if abs(pt["x"] - deduped[-1]["x"]) < 1e-6 and abs(pt["y"] - deduped[-1]["y"]) < 1e-6:
            continue
        deduped.append(pt)
    # Force exact endpoints again after dedupe
    if deduped:
        deduped[0] = {"x": int(start_x), "y": int(start_y)}
        deduped[-1] = {"x": int(end_x), "y": int(end_y)}

    total_dist = sum(
        euclidean_dist(deduped[i]["x"], deduped[i]["y"], deduped[i + 1]["x"], deduped[i + 1]["y"])
        for i in range(len(deduped) - 1)
    )

    return {
        "algorithm": "PSO",
        "path": deduped,
        "distance": total_dist,
        "nodesExplored": num_particles * max_iterations,
        "timeMs": (time.perf_counter() - t0) * 1000.0,
        "explored": [],
        "fitnessHistory": fitness_history,
    }
