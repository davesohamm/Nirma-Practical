# PSO-Based UAV Path Planning

Soft Computing course project: compare **particle swarm optimization (PSO)** with **A\*** and **Dijkstra** for path planning on a 2D grid (obstacles, start, goal). Includes simulation, metrics, Matplotlib charts, optional 3D visualization, and a Jupyter notebook for experiments.

**Faculty guide:** Dr. Priyank Thakkar  

**Team:** 25MCD004 Harsh Bhatt, 25MCD005 Soham Dave, 25MCD012 Nikhil Parejiya, 25MCD015 Dev Patel, 25MCD019 Raagi Raj  

**Course:** Soft Computing (6CS268ME25) · MTech Data Science · Institute of Technology, Nirma University

---

## What’s in the repository

| Part | Description |
|------|-------------|
| **`python_app/`** | Primary implementation: **Python** algorithms (A\*, Dijkstra, PSO), **Flask** API, web UI (2D grid, results tables, 3D view, charts), and **notebook**. |
| **Root (`src/`)** | **React + Vite + TypeScript** UI with the same three algorithms in the browser (optional demo without Flask). |

Pathfinding logic for the Flask demo lives entirely in **`python_app/algorithms/`** (well-commented for report and viva).

---

## Python / Flask (recommended for submission)

### Prerequisites

- Python 3.10+ recommended  
- `pip`

### Setup and run

```bash
cd python_app
pip install -r requirements.txt
python app.py
```

On Windows, if `python` is not on your PATH:

```powershell
cd python_app
py -3 -m pip install -r requirements.txt
py -3 app.py
```

Open **http://127.0.0.1:5000** in your browser.

### What the Flask app does

- **POST `/api/run`** — runs A\*, Dijkstra, and PSO on the current grid; returns paths, timings, exploration traces, PSO fitness history, a **Matplotlib** comparison figure (base64), and short text analysis.
- **POST `/api/random_grid`** — random obstacles with cleared corridors near start and goal.
- **Web UI** — edit grid, run algorithms, **results table** (latest + run history), **search expansion playback** for A\* / Dijkstra, **Three.js 3D** scene (obstacles + path tubes), comparison image, written analysis.

The page expects an **import map** for Three.js (already in the template). The browser must be able to load the Three.js modules from the CDN (or adapt the template to vendor them locally if you are offline).

### Notebook

```bash
cd python_app/notebooks
jupyter notebook algorithm_comparison.ipynb
```

Adjust grid size, density, and PSO parameters in the first code cell, then run all cells for tables and **matplotlib / seaborn** plots. The notebook imports the same `algorithms` package as Flask (set the working directory to `python_app` or open the notebook from `python_app/notebooks` as documented in the notebook).

---

## React / Vite (optional browser-only UI)

Algorithms are also implemented in **`src/lib/algorithms.ts`** for a standalone SPA.

```bash
npm install
npm run dev
```

Default dev server: **http://localhost:8080** (see `vite.config.ts`).

```bash
npm run build    # production build to dist/
npm run preview  # preview production build
```

---

## Logo

Place the institute logo as **`public/uorlogo.jpg`** (JPEG). The Flask app serves a copy from **`python_app/static/uorlogo.jpg`**; keep both in sync if you change the file. The React header loads the logo via `import.meta.env.BASE_URL` + `uorlogo.jpg`.

---

## Project layout (short)

```
python_app/
  app.py                 # Flask entry
  algorithms/            # grid, astar, dijkstra, pso
  plots.py               # comparison figures + analysis text
  templates/index.html   # main web page
  static/                # css, js (main.js, scene3d.js), uorlogo.jpg
  notebooks/
src/
  lib/algorithms.ts      # TS versions of the three methods
  components/            # grid, controls, metrics, header
  pages/Index.tsx
public/
  uorlogo.jpg
```

---

## Algorithms (summary)

- **Dijkstra** — shortest path on an 8-connected grid with diagonal cost √2; no heuristic.  
- **A\*** — same model with Euclidean heuristic; typically fewer expansions than Dijkstra.  
- **PSO** — swarm optimizes continuous waypoints between fixed start and goal; fitness combines path length and obstacle penalties (metaheuristic, not guaranteed grid-optimal).

---

## License / academic use

This repository is maintained for coursework submission. Adapt or cite appropriately if you reuse any part for other academic work.
