"""
Flask server for PSO-Based UAV Path Planning (Soft Computing project).

Run from repo root or from this folder:
  pip install -r requirements.txt
  python app.py

Open http://127.0.0.1:5000
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any, List

# Allow `from algorithms import ...` when running `python app.py` from python_app/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify

from algorithms import generate_grid, clear_corridor, run_astar, run_dijkstra, run_pso
from plots import build_comparison_png_bytes, png_to_data_url, build_analysis_text

app = Flask(__name__)


def _sanitize_result(r: dict) -> dict:
    """Make JSON-safe (no Infinity)."""
    out = dict(r)
    d = out.get("distance")
    if isinstance(d, float) and math.isinf(d):
        out["distance"] = None
        out["pathFound"] = False
    else:
        out["pathFound"] = bool(out.get("path"))
    # explored can be large; keep as-is (already capped in algorithms)
    return out


@app.route("/")
def index():
    return render_template("index.html", title="PSO-Based UAV Path Planning")


@app.post("/api/run")
def api_run():
    """
    JSON body:
      grid: 2D list 0/1
      start: {x,y}, end: {x,y}
      pso: optional {particles, iterations, waypoints, seed}
    """
    data = request.get_json(force=True, silent=True) or {}
    grid = data.get("grid")
    start = data.get("start")
    end = data.get("end")
    pso_cfg = data.get("pso") or {}

    if not grid or start is None or end is None:
        return jsonify({"error": "Missing grid, start, or end"}), 400

    sx, sy = int(start["x"]), int(start["y"])
    ex, ey = int(end["x"]), int(end["y"])

    results: List[dict] = []
    results.append(_sanitize_result(run_astar(grid, sx, sy, ex, ey)))
    results.append(_sanitize_result(run_dijkstra(grid, sx, sy, ex, ey)))
    results.append(
        _sanitize_result(
            run_pso(
                grid,
                sx,
                sy,
                ex,
                ey,
                num_particles=int(pso_cfg.get("particles", 30)),
                num_waypoints=int(pso_cfg.get("waypoints", 5)),
                max_iterations=int(pso_cfg.get("iterations", 100)),
                seed=pso_cfg.get("seed"),
            )
        )
    )

    png = build_comparison_png_bytes(results)
    analysis = build_analysis_text(results)

    return jsonify(
        {
            "results": results,
            "plotDataUrl": png_to_data_url(png),
            "analysis": analysis,
        }
    )


@app.post("/api/random_grid")
def api_random_grid():
    """Generate a grid with cleared neighborhoods around default corners."""
    data = request.get_json(force=True, silent=True) or {}
    n = int(data.get("size", 20))
    density = float(data.get("density", 0.25))
    seed = data.get("seed")
    g = generate_grid(n, n, density, seed=seed)
    sx, sy = 1, 1
    ex, ey = n - 2, n - 2
    clear_corridor(g, sx, sy, 1)
    clear_corridor(g, ex, ey, 1)
    return jsonify(
        {
            "grid": g,
            "start": {"x": sx, "y": sy},
            "end": {"x": ex, "y": ey},
        }
    )


if __name__ == "__main__":
    # threaded=True helps quick successive API calls during animation setup
    app.run(host="127.0.0.1", port=5000, debug=True, threaded=True)
