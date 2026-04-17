/**
 * Project Header Component
 * Displays university logo, project title, subject info, and student details
 */

import { Users, BookOpen } from 'lucide-react';
import { useState } from 'react';

// Student details for the project team
const STUDENTS = [
  { roll: '25MCD004', name: 'Harsh Bhatt' },
  { roll: '25MCD005', name: 'Soham Dave' },
  { roll: '25MCD012', name: 'Nikhil Parejiya' },
  { roll: '25MCD015', name: 'Dev Patel' },
  { roll: '25MCD019', name: 'Raagi Raj' },
];

/** Served from `public/`; BASE_URL supports subpath deploys (Vite default ends with `/`). */
const LOGO_SRC = `${import.meta.env.BASE_URL}uorlogo.jpg`;

export function ProjectHeader() {
  const [logoError, setLogoError] = useState(false);

  return (
    <header className="bg-primary text-primary-foreground">
      {/* Main header bar */}
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center gap-4 flex-wrap">
          {/* University logo - uses uorlogo.jpg from public folder */}
          <div className="flex-shrink-0">
            {!logoError ? (
              <img
                src={LOGO_SRC}
                alt="Nirma University Logo"
                width={64}
                height={64}
                decoding="async"
                className="h-16 w-16 rounded-lg object-contain bg-primary-foreground/10 p-1 border border-primary-foreground/20"
                onError={() => setLogoError(true)}
              />
            ) : (
              <div className="h-16 w-16 rounded-lg bg-primary-foreground/10 flex items-center justify-center text-xs text-center font-bold leading-tight">
                NU
              </div>
            )}
          </div>

          {/* Title section */}
          <div className="flex-1 min-w-0">
            <h1 className="text-xl md:text-2xl font-bold tracking-tight">
              PSO-Based UAV Path Planning
            </h1>
            <p className="text-primary-foreground/70 text-sm mt-0.5">
              Particle Swarm Optimization for Autonomous Drone Navigation in Dynamic Environments
            </p>
          </div>

          {/* Subject info */}
          <div className="flex-shrink-0 text-right hidden md:block">
            <div className="flex items-center gap-1.5 text-primary-foreground/80 text-sm">
              <BookOpen className="w-4 h-4" />
              <span>Soft Computing — 6CS268ME25</span>
            </div>
            <p className="text-primary-foreground/60 text-xs mt-0.5">
              MTech Data Science • Institute of Technology, Nirma University
            </p>
            <p className="text-primary-foreground/60 text-xs">
              Faculty guide: Dr. Priyank Thakkar
            </p>
          </div>
        </div>
      </div>

      {/* Student info bar */}
      <div className="bg-primary-foreground/5 border-t border-primary-foreground/10">
        <div className="container mx-auto px-4 py-2">
          <div className="flex items-center gap-3 flex-wrap text-sm">
            <div className="flex items-center gap-1.5 text-primary-foreground/70">
              <Users className="w-4 h-4" />
              <span className="font-medium">Team:</span>
            </div>
            {STUDENTS.map((s) => (
              <span
                key={s.roll}
                className="bg-primary-foreground/10 px-2 py-0.5 rounded text-xs"
              >
                {s.roll} — {s.name}
              </span>
            ))}
          </div>
          {/* Mobile-only subject info */}
          <div className="md:hidden mt-2 text-xs text-primary-foreground/60">
            Soft Computing (6CS268ME25) • Faculty guide: Dr. Priyank Thakkar
          </div>
        </div>
      </div>
    </header>
  );
}
