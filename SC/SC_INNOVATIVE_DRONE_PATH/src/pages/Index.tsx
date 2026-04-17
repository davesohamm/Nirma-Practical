/**
 * Main Page — PSO-Based UAV Path Planning Simulator
 * 
 * This page brings together:
 *   - An interactive grid environment (SVG)
 *   - Three pathfinding algorithms (A*, Dijkstra, PSO)
 *   - Performance comparison charts and metrics
 * 
 * Users can:
 *   - Click to place/remove obstacles
 *   - Set start and end points
 *   - Adjust PSO parameters
 *   - Run and compare all three algorithms
 */

import { useState, useEffect, useCallback } from 'react';
import { ProjectHeader } from '@/components/ProjectHeader';
import { GridVisualization } from '@/components/GridVisualization';
import { ControlPanel } from '@/components/ControlPanel';
import { MetricsComparison } from '@/components/MetricsComparison';
import {
  astar,
  dijkstra,
  pso,
  generateGrid,
  type Point,
  type Grid,
  type PathResult,
} from '@/lib/algorithms';

const Index = () => {
  // Grid configuration
  const [gridSize, setGridSize] = useState(20);
  const [grid, setGrid] = useState<Grid>([]);

  // Start and end positions for the UAV
  const [start, setStart] = useState<Point>({ x: 1, y: 1 });
  const [end, setEnd] = useState<Point>({ x: 18, y: 18 });

  // Current click mode: what happens when user clicks a cell
  const [mode, setMode] = useState<'obstacle' | 'start' | 'end'>('obstacle');

  // Algorithm results
  const [results, setResults] = useState<PathResult[]>([]);

  // Which algorithm paths are visible
  const [showPaths, setShowPaths] = useState({
    pso: true,
    astar: true,
    dijkstra: true,
  });

  // PSO configuration (adjustable via sliders)
  const [psoConfig, setPsoConfig] = useState({
    particles: 30,
    iterations: 100,
    waypoints: 5,
  });

  /** Generate a fresh random grid */
  const resetGrid = useCallback(() => {
    const newStart = { x: 1, y: 1 };
    const newEnd = { x: gridSize - 2, y: gridSize - 2 };
    setStart(newStart);
    setEnd(newEnd);

    // Generate random obstacles
    const newGrid = generateGrid(gridSize, gridSize, 0.25);

    // Clear area around start and end points so they're always accessible
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        const sy = newStart.y + dy, sx = newStart.x + dx;
        if (sy >= 0 && sy < gridSize && sx >= 0 && sx < gridSize) {
          newGrid[sy][sx] = 0;
        }
        const ey = newEnd.y + dy, ex = newEnd.x + dx;
        if (ey >= 0 && ey < gridSize && ex >= 0 && ex < gridSize) {
          newGrid[ey][ex] = 0;
        }
      }
    }

    setGrid(newGrid);
    setResults([]); // Clear previous results
  }, [gridSize]);

  // Initialize grid on first load and when grid size changes
  useEffect(() => {
    resetGrid();
  }, [resetGrid]);

  /** Run all three algorithms and store results */
  const runAlgorithms = () => {
    if (grid.length === 0) return;

    const newResults: PathResult[] = [];

    // Run A* algorithm
    newResults.push(astar(grid, start, end));

    // Run Dijkstra's algorithm
    newResults.push(dijkstra(grid, start, end));

    // Run PSO algorithm with current configuration
    newResults.push(
      pso(grid, start, end, psoConfig.particles, psoConfig.waypoints, psoConfig.iterations)
    );

    setResults(newResults);
  };

  /** Handle click on a grid cell */
  const handleCellClick = (x: number, y: number) => {
    if (mode === 'obstacle') {
      // Don't allow blocking start or end positions
      if ((x === start.x && y === start.y) || (x === end.x && y === end.y)) return;

      // Toggle obstacle on/off
      const newGrid = grid.map(row => [...row]);
      newGrid[y][x] = newGrid[y][x] === 1 ? 0 : 1;
      setGrid(newGrid);
    } else if (mode === 'start') {
      // Set new start position (only on free cells)
      if (grid[y][x] === 0 && !(x === end.x && y === end.y)) {
        setStart({ x, y });
        setMode('obstacle'); // Switch back to obstacle mode
      }
    } else if (mode === 'end') {
      // Set new end position (only on free cells)
      if (grid[y][x] === 0 && !(x === start.x && y === start.y)) {
        setEnd({ x, y });
        setMode('obstacle');
      }
    }

    // Clear results when grid changes
    setResults([]);
  };

  /** Toggle visibility of a specific algorithm's path */
  const togglePath = (algo: 'pso' | 'astar' | 'dijkstra') => {
    setShowPaths(prev => ({ ...prev, [algo]: !prev[algo] }));
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header with project info */}
      <ProjectHeader />

      {/* Main content area */}
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Grid visualization (takes 3/4 of the width on large screens) */}
          <div className="lg:col-span-3">
            <GridVisualization
              grid={grid}
              start={start}
              end={end}
              results={results}
              showPaths={showPaths}
              onCellClick={handleCellClick}
              mode={mode}
            />
          </div>

          {/* Control panel (1/4 of the width) */}
          <div className="lg:col-span-1">
            <ControlPanel
              mode={mode}
              onSetMode={setMode}
              onRun={runAlgorithms}
              onClear={() => setResults([])}
              onRandomize={resetGrid}
              gridSize={gridSize}
              onGridSizeChange={setGridSize}
              psoConfig={psoConfig}
              onPsoConfigChange={setPsoConfig}
              showPaths={showPaths}
              onTogglePath={togglePath}
              hasResults={results.length > 0}
            />
          </div>
        </div>

        {/* Performance comparison (shown after running algorithms) */}
        {results.length > 0 && <MetricsComparison results={results} />}

        {/* Footer */}
        <footer className="mt-8 py-4 text-center text-xs text-muted-foreground border-t border-border space-y-1">
          <p>
            PSO-Based UAV Path Planning • Soft Computing (6CS268ME25) • MTech Data Science • Institute of
            Technology, Nirma University
          </p>
          <p>Faculty guide: Dr. Priyank Thakkar</p>
          <p>
            25MCD004 Harsh Bhatt, 25MCD005 Soham Dave, 25MCD012 Nikhil Parejiya, 25MCD015 Dev Patel, 25MCD019 Raagi Raj
          </p>
        </footer>
      </main>
    </div>
  );
};

export default Index;
