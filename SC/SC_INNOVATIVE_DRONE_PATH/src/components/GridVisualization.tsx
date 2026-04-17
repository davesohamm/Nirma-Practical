/**
 * Grid Visualization Component
 * Renders the UAV environment as an interactive SVG grid
 * Shows obstacles, start/end points, and algorithm paths
 */

import { useLayoutEffect, useRef } from 'react';
import { Grid, Point, PathResult } from '@/lib/algorithms';

// Size of each cell in the SVG (in SVG units)
const CELL_SIZE = 28;

// Colors for each algorithm's path
const PATH_COLORS: Record<string, string> = {
  'PSO': 'hsl(43, 90%, 55%)',
  'A*': 'hsl(152, 60%, 40%)',
  'Dijkstra': 'hsl(210, 80%, 50%)',
};

// Stroke widths for visual distinction
const PATH_WIDTHS: Record<string, number> = {
  'PSO': 3.5,
  'A*': 2.5,
  'Dijkstra': 2.5,
};

interface GridVisualizationProps {
  grid: Grid;
  start: Point;
  end: Point;
  results: PathResult[];
  showPaths: { pso: boolean; astar: boolean; dijkstra: boolean };
  onCellClick: (x: number, y: number) => void;
  mode: 'obstacle' | 'start' | 'end';
}

export function GridVisualization({
  grid,
  start,
  end,
  results,
  showPaths,
  onCellClick,
  mode,
}: GridVisualizationProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  if (grid.length === 0) return null;

  const rows = grid.length;
  const cols = grid[0].length;
  const svgWidth = cols * CELL_SIZE;
  const svgHeight = rows * CELL_SIZE;

  // Convert a grid point to SVG center coordinates
  const toCenter = (p: Point) => ({
    cx: p.x * CELL_SIZE + CELL_SIZE / 2,
    cy: p.y * CELL_SIZE + CELL_SIZE / 2,
  });

  // Build SVG polyline points string from a path
  const pathToPoints = (path: Point[]) =>
    path.map(p => {
      const c = toCenter(p);
      return `${c.cx},${c.cy}`;
    }).join(' ');

  // Decide which results to show based on toggle state
  const visibleResults = results.filter(r => {
    if (r.algorithm === 'PSO') return showPaths.pso;
    if (r.algorithm === 'A*') return showPaths.astar;
    if (r.algorithm === 'Dijkstra') return showPaths.dijkstra;
    return false;
  });

  // Fixed strokeDasharray (e.g. 1000) made long paths look like they miss S/E; use true path length.
  useLayoutEffect(() => {
    const svg = svgRef.current;
    if (!svg) return;
    svg.querySelectorAll<SVGPolylineElement>('.algo-path').forEach((pl) => {
      const len = pl.getTotalLength();
      pl.style.transition = 'none';
      pl.style.strokeDasharray = String(len);
      pl.style.strokeDashoffset = String(len);
      void pl.getBoundingClientRect();
      requestAnimationFrame(() => {
        pl.style.transition = 'stroke-dashoffset 1.5s ease-in-out';
        pl.style.strokeDashoffset = '0';
      });
    });
  }, [visibleResults, grid, start.x, start.y, end.x, end.y]);

  // Cursor style based on current edit mode
  const cursorClass =
    mode === 'start' ? 'cursor-crosshair' :
    mode === 'end' ? 'cursor-crosshair' :
    'cursor-pointer';

  return (
    <div className="bg-card rounded-lg border border-border p-4 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-semibold text-foreground">
          UAV Environment Grid
        </h2>
        <div className="flex gap-2 text-xs text-muted-foreground">
          <span>Click to {mode === 'obstacle' ? 'toggle obstacles' : mode === 'start' ? 'set start' : 'set end'}</span>
        </div>
      </div>

      <svg
        ref={svgRef}
        viewBox={`0 0 ${svgWidth} ${svgHeight}`}
        className={`w-full h-auto rounded-md border border-border ${cursorClass}`}
        style={{ maxHeight: '65vh' }}
      >
        {/* Grid background */}
        <rect width={svgWidth} height={svgHeight} fill="hsl(220, 20%, 95%)" />

        {/* Render each cell */}
        {grid.map((row, y) =>
          row.map((cell, x) => {
            const isStart = x === start.x && y === start.y;
            const isEnd = x === end.x && y === end.y;

            let fill = 'hsl(220, 20%, 95%)'; // Free cell
            if (cell === 1) fill = 'hsl(220, 30%, 30%)'; // Obstacle
            if (isStart) fill = 'hsl(152, 70%, 45%)';    // Start (green)
            if (isEnd) fill = 'hsl(0, 75%, 55%)';        // End (red)

            return (
              <rect
                key={`${x}-${y}`}
                x={x * CELL_SIZE + 0.5}
                y={y * CELL_SIZE + 0.5}
                width={CELL_SIZE - 1}
                height={CELL_SIZE - 1}
                fill={fill}
                rx={3}
                ry={3}
                stroke="hsl(220, 15%, 88%)"
                strokeWidth={0.5}
                onClick={() => onCellClick(x, y)}
                className="transition-colors duration-100 hover:opacity-80"
              />
            );
          })
        )}

        {/* Render algorithm paths */}
        {visibleResults.map((result) => (
          result.path.length > 0 && (
            <polyline
              key={result.algorithm}
              className="algo-path"
              points={pathToPoints(result.path)}
              fill="none"
              stroke={PATH_COLORS[result.algorithm] || '#888'}
              strokeWidth={PATH_WIDTHS[result.algorithm] || 2}
              strokeLinecap="round"
              strokeLinejoin="round"
              opacity={0.85}
            />
          )
        ))}

        {/* Start marker label */}
        {(() => {
          const sc = toCenter(start);
          return (
            <text
              x={sc.cx}
              y={sc.cy + 1}
              textAnchor="middle"
              dominantBaseline="central"
              fill="white"
              fontSize={11}
              fontWeight="bold"
            >
              S
            </text>
          );
        })()}

        {/* End marker label */}
        {(() => {
          const ec = toCenter(end);
          return (
            <text
              x={ec.cx}
              y={ec.cy + 1}
              textAnchor="middle"
              dominantBaseline="central"
              fill="white"
              fontSize={11}
              fontWeight="bold"
            >
              E
            </text>
          );
        })()}
      </svg>

      {/* Path legend */}
      <div className="flex items-center gap-4 mt-3 text-sm">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm" style={{ background: 'hsl(152, 70%, 45%)' }} />
          <span className="text-muted-foreground">Start</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm" style={{ background: 'hsl(0, 75%, 55%)' }} />
          <span className="text-muted-foreground">End</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm" style={{ background: 'hsl(220, 30%, 30%)' }} />
          <span className="text-muted-foreground">Obstacle</span>
        </div>
        {visibleResults.map(r => (
          <div key={r.algorithm} className="flex items-center gap-1.5">
            <div
              className="w-6 h-0.5 rounded"
              style={{ background: PATH_COLORS[r.algorithm], height: '3px' }}
            />
            <span className="text-muted-foreground">{r.algorithm}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
