/**
 * Three.js 3D view: instanced obstacle blocks + cylindrical tubes along each path.
 * Grid (gx, gy) maps to XZ; Y is up. Paths sit at cruise height above the floor.
 *
 * Uses `three` + `three/addons/` bare imports — document must include an import map
 * (see templates/index.html) so OrbitControls' internal `from 'three'` resolves.
 */
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const COLORS = {
  astar: 0x38a169,
  dijkstra: 0x3b82f6,
  pso: 0xd4a017,
  floor: 0x1e293b,
  obstacle: 0x5a6a80,
  gridLine: 0x334155,
};

const UP = new THREE.Vector3(0, 1, 0);

let renderer = null;
let scene = null;
let camera = null;
let controls = null;
let rootGroup = null;
let containerEl = null;
let resizeObserver = null;
/** Reposition camera only when grid size changes (so orbit is not reset every tick). */
let lastGridKey = "";

function disposeObject3D(obj) {
  obj.traverse((child) => {
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      const mats = Array.isArray(child.material) ? child.material : [child.material];
      mats.forEach((m) => m.dispose());
    }
  });
}

/**
 * Place a cylinder mesh between world points a and b (tube segment).
 */
function addTubeSegment(group, a, b, radius, material) {
  const dir = new THREE.Vector3().subVectors(b, a);
  const len = dir.length();
  if (len < 1e-5) return;

  const geom = new THREE.CylinderGeometry(radius, radius, len, 12, 1, false);
  const mesh = new THREE.Mesh(geom, material);
  const mid = new THREE.Vector3().addVectors(a, b).multiplyScalar(0.5);
  mesh.position.copy(mid);
  const n = dir.clone().normalize();
  mesh.quaternion.setFromUnitVectors(UP, n);
  group.add(mesh);
}

/**
 * Build path as chained tube segments (works for grid steps and PSO float waypoints).
 */
function addPathTubes(group, path, cell, ox, oz, cruiseY, radius, hexColor) {
  if (!path || path.length < 2) return;

  const mat = new THREE.MeshStandardMaterial({
    color: hexColor,
    roughness: 0.35,
    metalness: 0.15,
    emissive: hexColor,
    emissiveIntensity: 0.12,
  });

  const pts = path.map((p) => {
    const px = ox + Number(p.x) * cell + cell / 2;
    const pz = oz + Number(p.y) * cell + cell / 2;
    return new THREE.Vector3(px, cruiseY, pz);
  });

  for (let i = 0; i < pts.length - 1; i++) {
    addTubeSegment(group, pts[i], pts[i + 1], radius, mat);
  }
}

/**
 * One instanced mesh for all obstacle cells (performance + clean look).
 */
function addObstacleInstances(group, grid, cell, ox, oz, blockH) {
  const rows = grid.length;
  const cols = grid[0].length;
  let count = 0;
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      if (grid[y][x] === 1) count++;
    }
  }
  if (count === 0) return;

  const geom = new THREE.BoxGeometry(cell * 0.92, blockH, cell * 0.92);
  const mat = new THREE.MeshStandardMaterial({
    color: COLORS.obstacle,
    roughness: 0.55,
    metalness: 0.2,
  });
  const mesh = new THREE.InstancedMesh(geom, mat, count);
  const m = new THREE.Matrix4();
  const pos = new THREE.Vector3();
  const quat = new THREE.Quaternion();
  const scl = new THREE.Vector3(1, 1, 1);
  let i = 0;
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      if (grid[y][x] !== 1) continue;
      pos.set(ox + x * cell + cell / 2, blockH / 2, oz + y * cell + cell / 2);
      m.compose(pos, quat, scl);
      mesh.setMatrixAt(i++, m);
    }
  }
  mesh.instanceMatrix.needsUpdate = true;
  mesh.castShadow = false;
  mesh.receiveShadow = false;
  group.add(mesh);
}

function addFloorAndGrid(group, cols, rows, cell, ox, oz) {
  const w = cols * cell;
  const d = rows * cell;
  const cx = ox + w / 2;
  const cz = oz + d / 2;

  const floorGeo = new THREE.PlaneGeometry(w, d);
  const floorMat = new THREE.MeshStandardMaterial({
    color: COLORS.floor,
    roughness: 0.92,
    metalness: 0.05,
  });
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(cx, 0, cz);
  floor.receiveShadow = true;
  group.add(floor);

  const gridHelper = new THREE.GridHelper(
    Math.max(w, d),
    Math.max(cols, rows),
    COLORS.gridLine,
    COLORS.gridLine
  );
  gridHelper.position.set(cx, 0.02, cz);
  group.add(gridHelper);
}

export function resizeThreeToContainer() {
  if (!containerEl || !renderer || !camera) return;
  const r = containerEl.getBoundingClientRect();
  const nw = Math.max(Math.floor(r.width), 200);
  const nh = Math.max(Math.floor(r.height), 280);
  if (nw < 4 || nh < 4) return;
  camera.aspect = nw / nh;
  camera.updateProjectionMatrix();
  renderer.setSize(nw, nh, false);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
}

export function initThree(el) {
  if (!el) return;
  containerEl = el;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0f1419);

  const r = el.getBoundingClientRect();
  const w = Math.max(Math.floor(r.width), 320);
  const h = Math.max(Math.floor(r.height), 320);

  camera = new THREE.PerspectiveCamera(48, w / h, 0.1, 500);
  camera.position.set(20, 24, 20);

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(w, h, false);
  if ("outputColorSpace" in renderer) {
    renderer.outputColorSpace = THREE.SRGBColorSpace;
  }
  el.innerHTML = "";
  el.appendChild(renderer.domElement);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.minDistance = 6;
  controls.maxDistance = 120;

  scene.add(new THREE.AmbientLight(0xffffff, 0.45));
  const key = new THREE.DirectionalLight(0xffffff, 0.95);
  key.position.set(14, 28, 18);
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xa8c4ff, 0.35);
  fill.position.set(-12, 14, -10);
  scene.add(fill);

  rootGroup = new THREE.Group();
  scene.add(rootGroup);

  function loop() {
    requestAnimationFrame(loop);
    if (controls) controls.update();
    if (renderer && scene && camera) renderer.render(scene, camera);
  }
  loop();

  const onResize = () => resizeThreeToContainer();
  window.addEventListener("resize", onResize);

  if (typeof ResizeObserver !== "undefined") {
    resizeObserver = new ResizeObserver(() => resizeThreeToContainer());
    resizeObserver.observe(el);
  }

  requestAnimationFrame(() => resizeThreeToContainer());
}

export function updateThreeScene(grid, start, end, pathResults, showPaths) {
  if (!rootGroup || !scene || !camera || !controls) return;
  if (!grid || !grid.length || !grid[0] || !grid[0].length) return;

  const safeShow = showPaths || { astar: true, dijkstra: true, pso: true };

  disposeObject3D(rootGroup);
  rootGroup.clear();

  const rows = grid.length;
  const cols = grid[0].length;
  const cell = 1;
  const ox = (-cols * cell) / 2;
  const oz = (-rows * cell) / 2;
  const blockH = 2.4;
  const cruiseY = 1.75;

  addFloorAndGrid(rootGroup, cols, rows, cell, ox, oz);
  addObstacleInstances(rootGroup, grid, cell, ox, oz, blockH);

  const markGeo = new THREE.SphereGeometry(0.38, 20, 20);
  const startMat = new THREE.MeshStandardMaterial({
    color: 0x38a169,
    emissive: 0x14532d,
    emissiveIntensity: 0.35,
    roughness: 0.4,
  });
  const endMat = new THREE.MeshStandardMaterial({
    color: 0xe53e3e,
    emissive: 0x5c1515,
    emissiveIntensity: 0.35,
    roughness: 0.4,
  });
  const sm = new THREE.Mesh(markGeo, startMat);
  sm.position.set(ox + start.x * cell + cell / 2, cruiseY + 0.15, oz + start.y * cell + cell / 2);
  rootGroup.add(sm);
  const em = new THREE.Mesh(markGeo, endMat);
  em.position.set(ox + end.x * cell + cell / 2, cruiseY + 0.15, oz + end.y * cell + cell / 2);
  rootGroup.add(em);

  const algoMap = {
    "A*": { key: "astar", color: COLORS.astar, radius: 0.1 },
    Dijkstra: { key: "dijkstra", color: COLORS.dijkstra, radius: 0.085 },
    PSO: { key: "pso", color: COLORS.pso, radius: 0.12 },
  };

  for (const r of pathResults || []) {
    const cfg = algoMap[r.algorithm];
    if (!cfg || !safeShow[cfg.key]) continue;
    const pathGroup = new THREE.Group();
    addPathTubes(pathGroup, r.path, cell, ox, oz, cruiseY, cfg.radius, cfg.color);
    rootGroup.add(pathGroup);
  }

  const gridKey = `${cols}x${rows}`;
  if (gridKey !== lastGridKey) {
    lastGridKey = gridKey;
    const center = new THREE.Vector3(ox + (cols * cell) / 2, 0, oz + (rows * cell) / 2);
    const span = Math.max(cols, rows) * cell;
    const dist = span * 0.95;
    camera.position.set(center.x + dist * 0.85, span * 0.75, center.z + dist * 0.85);
    controls.target.copy(center);
    controls.update();
  }

  if (renderer && scene && camera) {
    renderer.render(scene, camera);
  }
}
