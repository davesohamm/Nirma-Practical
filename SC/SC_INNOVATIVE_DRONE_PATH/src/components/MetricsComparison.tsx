/**
 * Metrics Comparison Component
 * Displays bar charts and a table comparing algorithm performance
 */

import { PathResult } from '@/lib/algorithms';
import { Card } from '@/components/ui/card';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

// Colors matching each algorithm
const ALGO_COLORS: Record<string, string> = {
  'A*': '#38a169',
  'Dijkstra': '#3b82f6',
  'PSO': '#d4a017',
};

interface MetricsComparisonProps {
  results: PathResult[];
}

export function MetricsComparison({ results }: MetricsComparisonProps) {
  // Prepare data for each metric chart
  const distanceData = results.map(r => ({
    algorithm: r.algorithm,
    value: r.path.length > 0 ? parseFloat(r.distance.toFixed(2)) : 0,
  }));

  const timeData = results.map(r => ({
    algorithm: r.algorithm,
    value: parseFloat(r.timeMs.toFixed(2)),
  }));

  const nodesData = results.map(r => ({
    algorithm: r.algorithm,
    value: r.nodesExplored,
  }));

  // Find the best (shortest distance) algorithm
  const validResults = results.filter(r => r.path.length > 0);
  const bestAlgo = validResults.length > 0
    ? validResults.reduce((a, b) => a.distance < b.distance ? a : b).algorithm
    : null;

  return (
    <div className="mt-6 space-y-4">
      <h2 className="text-xl font-bold text-foreground">Performance Comparison</h2>

      {/* Bar Charts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ChartCard title="Path Distance" unit="units" data={distanceData} />
        <ChartCard title="Computation Time" unit="ms" data={timeData} />
        <ChartCard title="Nodes / Evaluations" unit="" data={nodesData} />
      </div>

      {/* Summary Table */}
      <Card className="p-4 overflow-x-auto">
        <h3 className="text-sm font-semibold text-foreground mb-3">Detailed Metrics</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left py-2 px-3 text-muted-foreground font-medium">Algorithm</th>
              <th className="text-right py-2 px-3 text-muted-foreground font-medium">Distance</th>
              <th className="text-right py-2 px-3 text-muted-foreground font-medium">Time (ms)</th>
              <th className="text-right py-2 px-3 text-muted-foreground font-medium">Nodes Explored</th>
              <th className="text-right py-2 px-3 text-muted-foreground font-medium">Path Found</th>
            </tr>
          </thead>
          <tbody>
            {results.map(r => (
              <tr
                key={r.algorithm}
                className={`border-b border-border/50 ${r.algorithm === bestAlgo ? 'bg-accent/10' : ''}`}
              >
                <td className="py-2 px-3 font-medium">
                  <span className="flex items-center gap-2">
                    <span
                      className="w-3 h-3 rounded-full inline-block"
                      style={{ background: ALGO_COLORS[r.algorithm] }}
                    />
                    {r.algorithm}
                    {r.algorithm === bestAlgo && (
                      <span className="text-xs bg-accent/20 text-accent px-1.5 py-0.5 rounded font-semibold">
                        Best
                      </span>
                    )}
                  </span>
                </td>
                <td className="text-right py-2 px-3">
                  {r.path.length > 0 ? r.distance.toFixed(2) : '—'}
                </td>
                <td className="text-right py-2 px-3">{r.timeMs.toFixed(2)}</td>
                <td className="text-right py-2 px-3">{r.nodesExplored.toLocaleString()}</td>
                <td className="text-right py-2 px-3">
                  {r.path.length > 0 ? (
                    <span className="text-astar font-medium">✓ Yes</span>
                  ) : (
                    <span className="text-destructive font-medium">✗ No</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      {/* Analysis Summary */}
      <Card className="p-4">
        <h3 className="text-sm font-semibold text-foreground mb-2">Analysis</h3>
        <div className="text-sm text-muted-foreground space-y-1">
          <p>
            <strong>A*</strong> uses a heuristic (Euclidean distance) to guide search toward the goal,
            typically finding optimal grid paths while exploring fewer nodes than Dijkstra.
          </p>
          <p>
            <strong>Dijkstra</strong> explores all directions equally without a heuristic, guaranteeing
            the shortest path but usually exploring more nodes.
          </p>
          <p>
            <strong>PSO</strong> uses swarm intelligence with continuous waypoints, producing smoother
            paths that may navigate differently around obstacles. As a metaheuristic, it trades optimality
            for flexibility in complex environments.
          </p>
        </div>
      </Card>
    </div>
  );
}

/** Reusable bar chart card for a single metric */
function ChartCard({
  title,
  unit,
  data,
}: {
  title: string;
  unit: string;
  data: { algorithm: string; value: number }[];
}) {
  return (
    <Card className="p-4">
      <h3 className="text-sm font-semibold text-foreground mb-2">{title}</h3>
      <div className="h-48">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 15%, 88%)" />
            <XAxis dataKey="algorithm" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip
              formatter={(value: number) => [`${value} ${unit}`, title]}
              contentStyle={{
                borderRadius: '8px',
                border: '1px solid hsl(220, 15%, 88%)',
                fontSize: '12px',
              }}
            />
            <Bar dataKey="value" radius={[6, 6, 0, 0]}>
              {data.map((entry) => (
                <Cell
                  key={entry.algorithm}
                  fill={ALGO_COLORS[entry.algorithm] || '#888'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
