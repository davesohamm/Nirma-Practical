/**
 * 2D grid UI + API calls + exploration playback + path draw fix (dash length = path length).
 */
const CELL = 24;
const PATH_STYLE = {
  "A*": { stroke: "#38a169", width: 2.8 },
  Dijkstra: { stroke: "#3b82f6", width: 2.4 },
  PSO: { stroke: "#d4a017", width: 3.2 },
};

let grid = [];
let start = { x: 1, y: 1 };
let end = { x: 18, y: 18 };
let mode = "obstacle";
let results = [];
let showPaths = { astar: true, dijkstra: true, pso: true };
let exploreTimer = null;
let exploreAlgo = "A*";
let runCount = 0;

const els = {
  svg: null,
  gridLayer: null,
  exploreLayer: null,
  pathLayer: null,
  chart: null,
  analysis: null,
  status: null,
  resultsPanel: null,
  resultsMeta: null,
  tbodyLatest: null,
  tbodyHistory: null,
};

function cellCenter(p) {
  return { cx: p.x * CELL + CELL / 2, cy: p.y * CELL + CELL / 2 };
}

/** Build points string; supports float x/y from PSO. */
function pathToPoints(path) {
  return path
    .map((p) => {
      const cx = p.x * CELL + CELL / 2;
      const cy = p.y * CELL + CELL / 2;
      return `${cx},${cy}`;
    })
    .join(" ");
}

/**
 * Fixed-length dash animation hid long paths. Use actual polyline length.
 */
function animatePolyline(poly) {
  try {
    const len = poly.getTotalLength();
    poly.style.strokeDasharray = String(len);
    poly.style.strokeDashoffset = String(len);
    poly.style.transition = "none";
    // force reflow
    void poly.getBoundingClientRect();
    requestAnimationFrame(() => {
      poly.style.transition = "stroke-dashoffset 1.4s ease-in-out";
      poly.style.strokeDashoffset = "0";
    });
  } catch {
    /* SVG might not be in DOM yet */
  }
}

function drawGrid() {
  if (!grid.length) return;
  const rows = grid.length;
  const cols = grid[0].length;
  const w = cols * CELL;
  const h = rows * CELL;
  els.svg.setAttribute("viewBox", `0 0 ${w} ${h}`);

  els.gridLayer.innerHTML = "";
  els.exploreLayer.innerHTML = "";
  els.pathLayer.innerHTML = "";

  const bg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  bg.setAttribute("width", w);
  bg.setAttribute("height", h);
  bg.setAttribute("fill", "#1e293b");
  els.gridLayer.appendChild(bg);

  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const cell = grid[y][x];
      const isS = x === start.x && y === start.y;
      const isE = x === end.x && y === end.y;
      let fill = "#334155";
      if (cell === 1) fill = "#3d4f66";
      if (isS) fill = "#38a169";
      if (isE) fill = "#e53e3e";

      const r = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      r.setAttribute("x", x * CELL + 0.5);
      r.setAttribute("y", y * CELL + 0.5);
      r.setAttribute("width", CELL - 1);
      r.setAttribute("height", CELL - 1);
      r.setAttribute("rx", 2);
      r.setAttribute("fill", fill);
      r.setAttribute("stroke", "#475569");
      r.setAttribute("stroke-width", "0.5");
      r.dataset.x = x;
      r.dataset.y = y;
      r.style.cursor = "pointer";
      r.addEventListener("click", onCellClick);
      els.gridLayer.appendChild(r);
    }
  }

  const sc = cellCenter(start);
  const ec = cellCenter(end);
  for (const [pt, label] of [
    [sc, "S"],
    [ec, "E"],
  ]) {
    const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
    t.setAttribute("x", pt.cx);
    t.setAttribute("y", pt.cy + 1);
    t.setAttribute("text-anchor", "middle");
    t.setAttribute("dominant-baseline", "middle");
    t.setAttribute("fill", "#fff");
    t.setAttribute("font-size", "11");
    t.setAttribute("font-weight", "bold");
    t.textContent = label;
    els.gridLayer.appendChild(t);
  }

  drawPaths();
}

function drawPaths() {
  els.pathLayer.querySelectorAll("polyline").forEach((n) => n.remove());
  for (const r of results) {
    const key =
      r.algorithm === "A*"
        ? "astar"
        : r.algorithm === "Dijkstra"
          ? "dijkstra"
          : "pso";
    if (!showPaths[key]) continue;
    if (!r.path || r.path.length < 2) continue;
    const pl = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
    pl.setAttribute("points", pathToPoints(r.path));
    pl.setAttribute("fill", "none");
    const st = PATH_STYLE[r.algorithm] || { stroke: "#888", width: 2 };
    pl.setAttribute("stroke", st.stroke);
    pl.setAttribute("stroke-width", st.width);
    pl.setAttribute("stroke-linecap", "round");
    pl.setAttribute("stroke-linejoin", "round");
    pl.setAttribute("opacity", "0.92");
    els.pathLayer.appendChild(pl);
    requestAnimationFrame(() => animatePolyline(pl));
  }

  if (window.__updateThree) {
    window.__updateThree(grid, start, end, results, showPaths);
  }
}

function formatDistance(r) {
  const d = r.distance;
  if (d == null || !Number.isFinite(Number(d))) return "—";
  return Number(d).toFixed(3);
}

function renderLatestResultsTable(results) {
  if (!els.tbodyLatest) return;
  els.tbodyLatest.innerHTML = "";
  const order = ["A*", "Dijkstra", "PSO"];
  for (const name of order) {
    const r = results.find((x) => x.algorithm === name);
    if (!r) continue;
    const tr = document.createElement("tr");
    const found = r.path && r.path.length > 0;
    const pts = found ? r.path.length : 0;
    tr.innerHTML = [
      `<td><span class="algo-tag algo-tag--${name === "A*" ? "astar" : name === "Dijkstra" ? "dijkstra" : "pso"}">${name}</span></td>`,
      `<td>${found ? "Yes" : "No"}</td>`,
      `<td class="num">${formatDistance(r)}</td>`,
      `<td class="num">${Number(r.timeMs).toFixed(3)}</td>`,
      `<td class="num">${Number(r.nodesExplored).toLocaleString()}</td>`,
      `<td class="num">${pts}</td>`,
    ].join("");
    els.tbodyLatest.appendChild(tr);
  }
}

function appendHistoryRow(results, runNum) {
  if (!els.tbodyHistory) return;
  const now = new Date();
  const ts = now.toLocaleString();

  const pick = (name) => {
    const r = results.find((x) => x.algorithm === name);
    return r ? formatDistance(r) : "—";
  };
  const times = results
    .map((r) => (Number.isFinite(Number(r.timeMs)) ? Number(r.timeMs) : Infinity))
    .filter((t) => t < Infinity);
  const fastest = times.length ? Math.min(...times).toFixed(3) : "—";

  const tr = document.createElement("tr");
  tr.innerHTML = [
    `<td class="num">${runNum}</td>`,
    `<td>${ts}</td>`,
    `<td class="num">${pick("A*")}</td>`,
    `<td class="num">${pick("Dijkstra")}</td>`,
    `<td class="num">${pick("PSO")}</td>`,
    `<td class="num">${fastest}</td>`,
  ].join("");
  els.tbodyHistory.appendChild(tr);
}

function updateResultsSection(results) {
  if (!results || !results.length) return;
  runCount += 1;
  if (els.resultsPanel) els.resultsPanel.style.display = "block";
  if (els.resultsMeta) {
    els.resultsMeta.textContent = `Latest run #${runCount} — ${new Date().toLocaleString()}`;
  }
  renderLatestResultsTable(results);
  appendHistoryRow(results, runCount);
}

function onCellClick(ev) {
  const x = +ev.currentTarget.dataset.x;
  const y = +ev.currentTarget.dataset.y;
  if (mode === "obstacle") {
    if ((x === start.x && y === start.y) || (x === end.x && y === end.y)) return;
    grid[y][x] = grid[y][x] === 1 ? 0 : 1;
    results = [];
    clearExplore();
    drawGrid();
    setStatus("Grid changed — run algorithms again.");
  } else if (mode === "start") {
    if (grid[y][x] === 0 && !(x === end.x && y === end.y)) {
      start = { x, y };
      mode = "obstacle";
      syncModeButtons();
      results = [];
      clearExplore();
      drawGrid();
    }
  } else if (mode === "end") {
    if (grid[y][x] === 0 && !(x === start.x && y === start.y)) {
      end = { x, y };
      mode = "obstacle";
      syncModeButtons();
      results = [];
      clearExplore();
      drawGrid();
    }
  }
}

function syncModeButtons() {
  document.querySelectorAll(".mode-btns button").forEach((b) => {
    b.classList.toggle("active", b.dataset.mode === mode);
  });
}

function setStatus(msg) {
  if (els.status) els.status.textContent = msg;
}

async function randomizeGrid() {
  const size = +document.getElementById("gridSize").value || 20;
  const density = +document.getElementById("density").value || 0.25;
  setStatus("Generating grid…");
  const res = await fetch("/api/random_grid", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ size, density }),
  });
  const data = await res.json();
  grid = data.grid;
  start = data.start;
  end = data.end;
  results = [];
  clearExplore();
  drawGrid();
  setStatus("New random grid ready.");
}

async function runAlgorithms() {
  if (!grid.length) return;
  setStatus("Computing on server…");
  const pso = {
    particles: +document.getElementById("psoParticles").value || 30,
    iterations: +document.getElementById("psoIter").value || 100,
    waypoints: +document.getElementById("psoWp").value || 5,
  };
  const res = await fetch("/api/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ grid, start, end, pso }),
  });
  if (!res.ok) {
    setStatus("Server error.");
    return;
  }
  const data = await res.json();
  results = data.results || [];
  if (els.chart && data.plotDataUrl) {
    els.chart.src = data.plotDataUrl;
    els.chart.style.display = "block";
  }
  if (els.analysis) {
    els.analysis.textContent = data.analysis || "";
  }
  updateResultsSection(results);
  drawGrid();
  setStatus("Done — paths snap to S and E; see results table, 3D view, and charts.");
}

function clearExplore() {
  if (exploreTimer) {
    clearInterval(exploreTimer);
    exploreTimer = null;
  }
  els.exploreLayer.innerHTML = "";
}

function playExploration() {
  clearExplore();
  const r = results.find((x) => x.algorithm === exploreAlgo);
  if (!r || !r.explored || !r.explored.length) {
    setStatus("No exploration trace for this algorithm (or run algorithms first).");
    return;
  }
  const rows = grid.length;
  const cols = grid[0].length;
  let i = 0;
  exploreTimer = setInterval(() => {
    if (i >= r.explored.length) {
      clearExplore();
      setStatus("Exploration playback finished.");
      return;
    }
    const c = r.explored[i];
    const dot = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    dot.setAttribute("x", c.x * CELL + 2);
    dot.setAttribute("y", c.y * CELL + 2);
    dot.setAttribute("width", CELL - 4);
    dot.setAttribute("height", CELL - 4);
    dot.setAttribute("rx", 2);
    dot.setAttribute("fill", "rgba(147, 197, 253, 0.35)");
    dot.setAttribute("pointer-events", "none");
    els.exploreLayer.appendChild(dot);
    i++;
  }, 12);
  setStatus(`Playing ${exploreAlgo} expansion…`);
}

function init() {
  els.svg = document.getElementById("grid-svg");
  els.gridLayer = document.getElementById("layer-grid");
  els.exploreLayer = document.getElementById("layer-explore");
  els.pathLayer = document.getElementById("layer-paths");
  els.chart = document.getElementById("chart-img");
  els.analysis = document.getElementById("analysis-text");
  els.status = document.getElementById("status");
  els.resultsPanel = document.getElementById("results-panel");
  els.resultsMeta = document.getElementById("results-run-meta");
  els.tbodyLatest = document.getElementById("results-tbody-latest");
  els.tbodyHistory = document.getElementById("results-tbody-history");

  document.getElementById("btnRandom").addEventListener("click", randomizeGrid);
  document.getElementById("btnRun").addEventListener("click", runAlgorithms);
  document.getElementById("btnExplore").addEventListener("click", playExploration);

  document.querySelectorAll(".mode-btns button").forEach((b) => {
    b.addEventListener("click", () => {
      mode = b.dataset.mode;
      syncModeButtons();
    });
  });

  document.getElementById("exploreAlgo").addEventListener("change", (e) => {
    exploreAlgo = e.target.value;
  });

  ["showAstar", "showDijkstra", "showPso"].forEach((id) => {
    document.getElementById(id).addEventListener("change", (e) => {
      if (id === "showAstar") showPaths.astar = e.target.checked;
      if (id === "showDijkstra") showPaths.dijkstra = e.target.checked;
      if (id === "showPso") showPaths.pso = e.target.checked;
      drawPaths();
    });
  });

  syncModeButtons();
  randomizeGrid();
}

document.addEventListener("DOMContentLoaded", init);
