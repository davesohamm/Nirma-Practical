/**
 * ============================================================
 * PSO-Based UAV Path Planning — Algorithm Implementations
 * ============================================================
 * 
 * This file contains three pathfinding algorithms:
 *   1. A* (A-Star)  — Heuristic-based shortest path
 *   2. Dijkstra     — Classic shortest path (no heuristic)
 *   3. PSO          — Particle Swarm Optimization for path planning
 * 
 * All algorithms work on a 2D grid where:
 *   0 = free cell (UAV can fly here)
 *   1 = obstacle (building, no-fly zone, etc.)
 * 
 * Subject: Soft Computing (6CS268ME25)
 * Institute of Technology, Nirma University
 * ============================================================
 */

// ---- TYPE DEFINITIONS ----

/** A point on the grid with x (column) and y (row) */
export type Point = { x: number; y: number };

/** The grid is a 2D array: 0 = free, 1 = obstacle */
export type Grid = number[][];

/** Result returned by each algorithm */
export interface PathResult {
  path: Point[];          // The sequence of points forming the path
  distance: number;       // Total path distance (Euclidean)
  nodesExplored: number;  // How many nodes/iterations were processed
  timeMs: number;         // Computation time in milliseconds
  algorithm: string;      // Name of the algorithm
}

// ---- UTILITY FUNCTIONS ----

/** Calculate Euclidean distance between two points */
function euclideanDist(a: Point, b: Point): number {
  return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2);
}

/** Check if a grid cell is valid (within bounds and not an obstacle) */
function isValid(grid: Grid, x: number, y: number): boolean {
  return (
    y >= 0 && y < grid.length &&
    x >= 0 && x < grid[0].length &&
    grid[y][x] === 0
  );
}

/**
 * 8 possible movement directions:
 * Up, Down, Left, Right, and 4 diagonals
 * This allows the UAV to move in any direction
 */
const DIRECTIONS = [
  { x: 0, y: -1 },   // Up
  { x: 0, y: 1 },    // Down
  { x: -1, y: 0 },   // Left
  { x: 1, y: 0 },    // Right
  { x: -1, y: -1 },  // Up-Left
  { x: 1, y: -1 },   // Up-Right
  { x: -1, y: 1 },   // Down-Left
  { x: 1, y: 1 },    // Down-Right
];

/**
 * Generate a random grid with obstacles
 * @param rows - Number of rows
 * @param cols - Number of columns
 * @param density - Probability of a cell being an obstacle (0 to 1)
 */
export function generateGrid(rows: number, cols: number, density: number = 0.25): Grid {
  const grid: Grid = [];
  for (let y = 0; y < rows; y++) {
    const row: number[] = [];
    for (let x = 0; x < cols; x++) {
      // Each cell has a 'density' chance of being an obstacle
      row.push(Math.random() < density ? 1 : 0);
    }
    grid.push(row);
  }
  return grid;
}


// ================================================================
// ALGORITHM 1: A* (A-Star) Search
// ================================================================
/**
 * A* Algorithm — finds the shortest path using a heuristic
 * 
 * How it works:
 *   - Maintains an "open set" of nodes to explore
 *   - For each node, calculates:
 *       g(n) = actual cost from start to n
 *       h(n) = estimated cost from n to end (heuristic)
 *       f(n) = g(n) + h(n)
 *   - Always expands the node with the lowest f(n)
 *   - Uses Euclidean distance as the heuristic
 * 
 * Advantage over Dijkstra: The heuristic guides search toward
 * the goal, so it explores fewer nodes.
 */
export function astar(grid: Grid, start: Point, end: Point): PathResult {
  const startTime = performance.now();
  let nodesExplored = 0;

  // Helper to create a unique key for each grid position
  const key = (p: Point) => `${p.x},${p.y}`;

  // Open set: nodes we still need to explore, sorted by f-score
  const openSet: { point: Point; f: number }[] = [{ point: start, f: 0 }];

  // g-score: actual distance from start to each node
  const gScore = new Map<string, number>();
  gScore.set(key(start), 0);

  // Track where we came from to reconstruct the path
  const cameFrom = new Map<string, Point>();

  // Closed set: nodes we've already fully explored
  const closed = new Set<string>();

  while (openSet.length > 0) {
    // Pick the node with the lowest f-score
    openSet.sort((a, b) => a.f - b.f);
    const current = openSet.shift()!.point;
    const currentKey = key(current);
    nodesExplored++;

    // Did we reach the goal?
    if (current.x === end.x && current.y === end.y) {
      // Reconstruct the path by following cameFrom links
      const path: Point[] = [];
      let node: Point | undefined = current;
      while (node) {
        path.unshift(node);
        node = cameFrom.get(key(node));
      }
      return {
        path,
        distance: gScore.get(currentKey)!,
        nodesExplored,
        timeMs: performance.now() - startTime,
        algorithm: 'A*',
      };
    }

    closed.add(currentKey);

    // Explore all 8 neighbors
    for (const dir of DIRECTIONS) {
      const nx = current.x + dir.x;
      const ny = current.y + dir.y;

      // Skip if out of bounds, obstacle, or already explored
      if (!isValid(grid, nx, ny)) continue;
      const neighborKey = `${nx},${ny}`;
      if (closed.has(neighborKey)) continue;

      // Diagonal moves cost √2, straight moves cost 1
      const moveCost = (dir.x !== 0 && dir.y !== 0) ? Math.SQRT2 : 1;
      const tentativeG = (gScore.get(currentKey) ?? Infinity) + moveCost;

      // Only update if we found a shorter path to this neighbor
      if (tentativeG < (gScore.get(neighborKey) ?? Infinity)) {
        gScore.set(neighborKey, tentativeG);
        cameFrom.set(neighborKey, current);
        // f = g + h (heuristic is Euclidean distance to goal)
        const h = euclideanDist({ x: nx, y: ny }, end);
        openSet.push({ point: { x: nx, y: ny }, f: tentativeG + h });
      }
    }
  }

  // No path found
  return { path: [], distance: Infinity, nodesExplored, timeMs: performance.now() - startTime, algorithm: 'A*' };
}


// ================================================================
// ALGORITHM 2: Dijkstra's Algorithm
// ================================================================
/**
 * Dijkstra's Algorithm — finds the shortest path without a heuristic
 * 
 * How it works:
 *   - Similar to A*, but does NOT use a heuristic
 *   - Explores nodes in order of their distance from the start
 *   - Guarantees the shortest path
 * 
 * Difference from A*: Without the heuristic, Dijkstra explores
 * more nodes because it doesn't know which direction the goal is.
 * This makes it slower but more "thorough".
 */
export function dijkstra(grid: Grid, start: Point, end: Point): PathResult {
  const startTime = performance.now();
  let nodesExplored = 0;

  const key = (p: Point) => `${p.x},${p.y}`;

  // Open set sorted by distance (no heuristic, just distance)
  const openSet: { point: Point; dist: number }[] = [{ point: start, dist: 0 }];

  // Distance from start to each node
  const dist = new Map<string, number>();
  dist.set(key(start), 0);

  const cameFrom = new Map<string, Point>();
  const closed = new Set<string>();

  while (openSet.length > 0) {
    // Pick node with smallest distance
    openSet.sort((a, b) => a.dist - b.dist);
    const current = openSet.shift()!.point;
    const currentKey = key(current);
    nodesExplored++;

    // Reached the goal?
    if (current.x === end.x && current.y === end.y) {
      const path: Point[] = [];
      let node: Point | undefined = current;
      while (node) {
        path.unshift(node);
        node = cameFrom.get(key(node));
      }
      return {
        path,
        distance: dist.get(currentKey)!,
        nodesExplored,
        timeMs: performance.now() - startTime,
        algorithm: 'Dijkstra',
      };
    }

    closed.add(currentKey);

    // Explore all 8 neighbors (same as A*)
    for (const dir of DIRECTIONS) {
      const nx = current.x + dir.x;
      const ny = current.y + dir.y;

      if (!isValid(grid, nx, ny)) continue;
      const neighborKey = `${nx},${ny}`;
      if (closed.has(neighborKey)) continue;

      const moveCost = (dir.x !== 0 && dir.y !== 0) ? Math.SQRT2 : 1;
      const tentativeD = (dist.get(currentKey) ?? Infinity) + moveCost;

      if (tentativeD < (dist.get(neighborKey) ?? Infinity)) {
        dist.set(neighborKey, tentativeD);
        cameFrom.set(neighborKey, current);
        // Key difference: no heuristic added, just raw distance
        openSet.push({ point: { x: nx, y: ny }, dist: tentativeD });
      }
    }
  }

  return { path: [], distance: Infinity, nodesExplored, timeMs: performance.now() - startTime, algorithm: 'Dijkstra' };
}


// ================================================================
// ALGORITHM 3: Particle Swarm Optimization (PSO)
// ================================================================

/**
 * A single particle in the swarm
 * Each particle represents a candidate path solution
 */
interface Particle {
  waypoints: Point[];              // Current waypoint positions
  velocity: { vx: number; vy: number }[];  // Velocity of each waypoint
  personalBest: Point[];           // Best waypoints this particle has found
  personalBestFitness: number;     // Fitness of the personal best
}

/**
 * Count how many obstacle cells a line segment passes through
 * We sample points along the line and check each one
 */
function countLineCollisions(grid: Grid, p1: Point, p2: Point): number {
  const steps = Math.ceil(Math.max(Math.abs(p2.x - p1.x), Math.abs(p2.y - p1.y)) * 3);
  if (steps === 0) return 0;

  let collisions = 0;
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const x = Math.round(p1.x + t * (p2.x - p1.x));
    const y = Math.round(p1.y + t * (p2.y - p1.y));
    if (y >= 0 && y < grid.length && x >= 0 && x < grid[0].length && grid[y][x] === 1) {
      collisions++;
    }
  }
  return collisions;
}

/**
 * Calculate how good a path is (lower = better)
 * Fitness = total path length + heavy penalty for obstacle collisions
 */
function calculateFitness(
  grid: Grid, start: Point, end: Point, waypoints: Point[]
): { fitness: number; distance: number } {
  // Sort waypoints by distance from start to create a logical path order
  const sorted = [...waypoints].sort(
    (a, b) => euclideanDist(start, a) - euclideanDist(start, b)
  );

  // Full path: Start → Waypoint1 → Waypoint2 → ... → End
  const fullPath = [start, ...sorted, end];

  let distance = 0;
  let collisionPenalty = 0;

  for (let i = 0; i < fullPath.length - 1; i++) {
    distance += euclideanDist(fullPath[i], fullPath[i + 1]);
    // Each collision adds a penalty of 10 (to strongly discourage obstacle paths)
    collisionPenalty += countLineCollisions(grid, fullPath[i], fullPath[i + 1]) * 10;
  }

  return { fitness: distance + collisionPenalty, distance };
}

/**
 * PSO Algorithm — Uses swarm intelligence to find good UAV paths
 * 
 * How it works:
 *   - Create a "swarm" of particles, each with random waypoints
 *   - Each particle's waypoints define a path: Start → Waypoints → End
 *   - In each iteration, particles:
 *       1. Evaluate their current path quality (fitness)
 *       2. Remember their best personal solution
 *       3. Share information about the global best solution
 *       4. Update their waypoint positions using velocity equations:
 *          v = w*v + c1*r1*(personalBest - current) + c2*r2*(globalBest - current)
 *          position = position + velocity
 * 
 * Parameters:
 *   w  = inertia weight (0.7) — how much to keep previous velocity
 *   c1 = cognitive factor (1.5) — attraction to personal best
 *   c2 = social factor (1.5) — attraction to global best
 * 
 * PSO is a metaheuristic: it doesn't guarantee the optimal solution
 * but finds good solutions quickly, especially in complex environments.
 */
export function pso(
  grid: Grid,
  start: Point,
  end: Point,
  numParticles: number = 30,
  numWaypoints: number = 5,
  maxIterations: number = 100
): PathResult {
  const startTime = performance.now();
  const rows = grid.length;
  const cols = grid[0].length;

  // PSO parameters
  const w = 0.7;    // Inertia weight: controls exploration vs exploitation
  const c1 = 1.5;   // Cognitive coefficient: pull toward personal best
  const c2 = 1.5;   // Social coefficient: pull toward global best

  // Track the best solution found by any particle
  let globalBest: Point[] = [];
  let globalBestFitness = Infinity;

  // Step 1: Initialize the swarm with random waypoints
  const particles: Particle[] = [];
  for (let i = 0; i < numParticles; i++) {
    const waypoints: Point[] = [];
    const velocity: { vx: number; vy: number }[] = [];

    for (let j = 0; j < numWaypoints; j++) {
      // Random position within the grid
      waypoints.push({
        x: Math.random() * (cols - 1),
        y: Math.random() * (rows - 1),
      });
      // Random initial velocity
      velocity.push({
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
      });
    }

    // Evaluate this particle's initial path
    const { fitness } = calculateFitness(grid, start, end, waypoints);

    particles.push({
      waypoints,
      velocity,
      personalBest: waypoints.map(wp => ({ ...wp })),
      personalBestFitness: fitness,
    });

    // Update global best if this particle is better
    if (fitness < globalBestFitness) {
      globalBestFitness = fitness;
      globalBest = waypoints.map(wp => ({ ...wp }));
    }
  }

  // Step 2: Main PSO loop — iterate and improve
  for (let iter = 0; iter < maxIterations; iter++) {
    for (const particle of particles) {
      for (let j = 0; j < numWaypoints; j++) {
        const r1 = Math.random(); // Random factor for cognitive component
        const r2 = Math.random(); // Random factor for social component

        // Update velocity using PSO equation:
        // v_new = w * v_old + c1 * r1 * (pBest - current) + c2 * r2 * (gBest - current)
        particle.velocity[j].vx =
          w * particle.velocity[j].vx +
          c1 * r1 * (particle.personalBest[j].x - particle.waypoints[j].x) +
          c2 * r2 * (globalBest[j].x - particle.waypoints[j].x);

        particle.velocity[j].vy =
          w * particle.velocity[j].vy +
          c1 * r1 * (particle.personalBest[j].y - particle.waypoints[j].y) +
          c2 * r2 * (globalBest[j].y - particle.waypoints[j].y);

        // Update position: x_new = x_old + v_new
        // Clamp to grid bounds so waypoints stay inside the environment
        particle.waypoints[j].x = Math.max(0, Math.min(
          cols - 1,
          particle.waypoints[j].x + particle.velocity[j].vx
        ));
        particle.waypoints[j].y = Math.max(0, Math.min(
          rows - 1,
          particle.waypoints[j].y + particle.velocity[j].vy
        ));
      }

      // Evaluate the new path
      const { fitness } = calculateFitness(grid, start, end, particle.waypoints);

      // Update personal best
      if (fitness < particle.personalBestFitness) {
        particle.personalBestFitness = fitness;
        particle.personalBest = particle.waypoints.map(wp => ({ ...wp }));
      }

      // Update global best
      if (fitness < globalBestFitness) {
        globalBestFitness = fitness;
        globalBest = particle.waypoints.map(wp => ({ ...wp }));
      }
    }
  }

  // Step 3: Build the final path from the best solution
  const sortedBest = [...globalBest].sort(
    (a, b) => euclideanDist(start, a) - euclideanDist(start, b)
  );
  const finalPath = [start, ...sortedBest, end];

  // Calculate total distance of the final path
  let totalDist = 0;
  for (let i = 0; i < finalPath.length - 1; i++) {
    totalDist += euclideanDist(finalPath[i], finalPath[i + 1]);
  }

  return {
    path: finalPath,
    distance: totalDist,
    nodesExplored: numParticles * maxIterations, // Total evaluations
    timeMs: performance.now() - startTime,
    algorithm: 'PSO',
  };
}
