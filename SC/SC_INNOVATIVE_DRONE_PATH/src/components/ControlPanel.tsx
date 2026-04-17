/**
 * Control Panel Component
 * Provides buttons and sliders to interact with the simulation
 */

import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Play, RotateCcw, Shuffle, MapPin, Target, Square } from 'lucide-react';

interface ControlPanelProps {
  mode: 'obstacle' | 'start' | 'end';
  onSetMode: (mode: 'obstacle' | 'start' | 'end') => void;
  onRun: () => void;
  onClear: () => void;
  onRandomize: () => void;
  gridSize: number;
  onGridSizeChange: (size: number) => void;
  psoConfig: { particles: number; iterations: number; waypoints: number };
  onPsoConfigChange: (config: { particles: number; iterations: number; waypoints: number }) => void;
  showPaths: { pso: boolean; astar: boolean; dijkstra: boolean };
  onTogglePath: (algo: 'pso' | 'astar' | 'dijkstra') => void;
  hasResults: boolean;
}

export function ControlPanel({
  mode,
  onSetMode,
  onRun,
  onClear,
  onRandomize,
  gridSize,
  onGridSizeChange,
  psoConfig,
  onPsoConfigChange,
  showPaths,
  onTogglePath,
  hasResults,
}: ControlPanelProps) {
  return (
    <div className="space-y-4">
      {/* Edit Mode Selection */}
      <Card className="p-4">
        <h3 className="text-sm font-semibold text-foreground mb-3">Edit Mode</h3>
        <div className="grid grid-cols-3 gap-2">
          <Button
            size="sm"
            variant={mode === 'obstacle' ? 'default' : 'outline'}
            onClick={() => onSetMode('obstacle')}
            className="text-xs"
          >
            <Square className="w-3 h-3 mr-1" />
            Obstacle
          </Button>
          <Button
            size="sm"
            variant={mode === 'start' ? 'default' : 'outline'}
            onClick={() => onSetMode('start')}
            className="text-xs"
          >
            <MapPin className="w-3 h-3 mr-1" />
            Start
          </Button>
          <Button
            size="sm"
            variant={mode === 'end' ? 'default' : 'outline'}
            onClick={() => onSetMode('end')}
            className="text-xs"
          >
            <Target className="w-3 h-3 mr-1" />
            End
          </Button>
        </div>
      </Card>

      {/* Run & Reset Controls */}
      <Card className="p-4">
        <h3 className="text-sm font-semibold text-foreground mb-3">Actions</h3>
        <div className="space-y-2">
          <Button onClick={onRun} className="w-full bg-accent text-accent-foreground hover:bg-accent/90">
            <Play className="w-4 h-4 mr-2" />
            Run All Algorithms
          </Button>
          <div className="grid grid-cols-2 gap-2">
            <Button variant="outline" size="sm" onClick={onClear} disabled={!hasResults}>
              <RotateCcw className="w-3 h-3 mr-1" />
              Clear Paths
            </Button>
            <Button variant="outline" size="sm" onClick={onRandomize}>
              <Shuffle className="w-3 h-3 mr-1" />
              New Grid
            </Button>
          </div>
        </div>
      </Card>

      {/* Grid Size */}
      <Card className="p-4">
        <h3 className="text-sm font-semibold text-foreground mb-3">Grid Size: {gridSize}×{gridSize}</h3>
        <Slider
          value={[gridSize]}
          onValueChange={([v]) => onGridSizeChange(v)}
          min={10}
          max={30}
          step={5}
        />
        <p className="text-xs text-muted-foreground mt-1">Smaller = faster, Larger = more complex</p>
      </Card>

      {/* PSO Parameters */}
      <Card className="p-4">
        <h3 className="text-sm font-semibold text-foreground mb-3">PSO Parameters</h3>
        <div className="space-y-3">
          <div>
            <Label className="text-xs">Particles: {psoConfig.particles}</Label>
            <Slider
              value={[psoConfig.particles]}
              onValueChange={([v]) => onPsoConfigChange({ ...psoConfig, particles: v })}
              min={10}
              max={100}
              step={5}
            />
          </div>
          <div>
            <Label className="text-xs">Iterations: {psoConfig.iterations}</Label>
            <Slider
              value={[psoConfig.iterations]}
              onValueChange={([v]) => onPsoConfigChange({ ...psoConfig, iterations: v })}
              min={20}
              max={300}
              step={10}
            />
          </div>
          <div>
            <Label className="text-xs">Waypoints: {psoConfig.waypoints}</Label>
            <Slider
              value={[psoConfig.waypoints]}
              onValueChange={([v]) => onPsoConfigChange({ ...psoConfig, waypoints: v })}
              min={2}
              max={10}
              step={1}
            />
          </div>
        </div>
      </Card>

      {/* Path Visibility Toggles */}
      <Card className="p-4">
        <h3 className="text-sm font-semibold text-foreground mb-3">Show Paths</h3>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="algo-badge-pso text-xs">PSO</div>
            </div>
            <Switch checked={showPaths.pso} onCheckedChange={() => onTogglePath('pso')} />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="algo-badge-astar text-xs">A*</div>
            </div>
            <Switch checked={showPaths.astar} onCheckedChange={() => onTogglePath('astar')} />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="algo-badge-dijkstra text-xs">Dijkstra</div>
            </div>
            <Switch checked={showPaths.dijkstra} onCheckedChange={() => onTogglePath('dijkstra')} />
          </div>
        </div>
      </Card>
    </div>
  );
}
