"""
Matplotlib figures for comparing algorithms (used by Flask and importable from notebooks).
"""

from __future__ import annotations

import base64
import io
from typing import Any, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _finite_distance(d: Any) -> float:
    if d is None or (isinstance(d, float) and (np.isnan(d) or np.isinf(d))):
        return 0.0
    return float(d)


def build_comparison_png_bytes(results: List[dict]) -> bytes:
    """
    One figure with:
      - Bar chart: path distance, time (ms), nodes explored
      - Line chart: PSO best fitness per iteration (if present)
    """
    names = [r["algorithm"] for r in results]
    dists = [_finite_distance(r.get("distance")) for r in results]
    times = [float(r.get("timeMs", 0) or 0) for r in results]
    nodes = [int(r.get("nodesExplored", 0) or 0) for r in results]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle("PSO vs A* vs Dijkstra — comparison", fontsize=14, fontweight="bold")

    colors = ["#38a169", "#3b82f6", "#d4a017"]
    x = np.arange(len(names))

    ax = axes[0, 0]
    ax.bar(x, dists, color=colors[: len(names)])
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("Path length (grid cost / Euclidean)")
    ax.set_title("Path distance / length")

    ax = axes[0, 1]
    ax.bar(x, times, color=colors[: len(names)])
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("Milliseconds")
    ax.set_title("Computation time")

    ax = axes[1, 0]
    ax.bar(x, nodes, color=colors[: len(names)])
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("Count")
    ax.set_title("Nodes expanded / PSO evaluations")

    ax = axes[1, 1]
    pso = next((r for r in results if r.get("algorithm") == "PSO"), None)
    hist = pso.get("fitnessHistory") if pso else None
    if hist and len(hist) > 0:
        ax.plot(range(1, len(hist) + 1), hist, color="#d4a017", linewidth=2, marker=".", markersize=4)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Best fitness (lower is better)")
        ax.set_title("PSO convergence (best fitness)")
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, "No PSO history", ha="center", va="center", transform=ax.transAxes)
        ax.set_axis_off()

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()


def png_to_data_url(png_bytes: bytes) -> str:
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return f"data:image/png;base64,{b64}"


def build_analysis_text(results: List[dict]) -> str:
    """Short comparison for the web page (plain text paragraphs)."""
    lines: List[str] = []

    def dist(r):
        d = r.get("distance")
        if d is None or (isinstance(d, float) and np.isinf(d)):
            return None
        return float(d)

    valid = [(r, dist(r)) for r in results if r.get("path") and dist(r) is not None]
    if valid:
        best = min(valid, key=lambda t: t[1])
        lines.append(
            f"Shortest grid-optimal style path among successful runs: {best[0]['algorithm']} "
            f"with cost/length about {best[1]:.2f}. "
            "Note: PSO optimizes a smooth polyline with penalties, so its length is not directly "
            "comparable to the graph shortest-path cost of A* and Dijkstra."
        )
    else:
        lines.append("No complete path was found for all algorithms; try clearing obstacles or moving endpoints.")

    astar = next((r for r in results if r["algorithm"] == "A*"), None)
    dij = next((r for r in results if r["algorithm"] == "Dijkstra"), None)
    if astar and dij and astar.get("path") and dij.get("path"):
        ae, de = astar.get("nodesExplored", 0), dij.get("nodesExplored", 0)
        if de > 0:
            lines.append(
                f"A* expanded {ae} cells vs Dijkstra {de}. "
                "With an admissible heuristic, A* typically expands fewer cells while still "
                "finding the same optimal cost as Dijkstra on this grid."
            )

    lines.append(
        "Dijkstra explores in increasing cost rings from the start; it has no lookahead toward the goal, "
        "so it is systematic but can be slower than A*."
    )
    lines.append(
        "PSO maintains a swarm of candidate waypoint chains. It is useful when you want a continuous-looking "
        "trajectory and can encode obstacles as penalties, but it does not guarantee global optimality."
    )
    return "\n\n".join(lines)
