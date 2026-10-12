import React, { useState } from 'react';
import { AmberCascades } from './components/AmberCascades';
import { GraphExplorer } from './components/GraphExplorer';

// LiquidGlass interactive button component with SVG displacement filter
export const LiquidGlassButton: React.FC<{
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  variant?: 'amber' | 'neutral';
}> = ({ children, onClick, className = '', variant = 'amber' }) => {
  const [isHovered, setIsHovered] = useState(false);

  const baseColors =
    variant === 'amber'
      ? 'border-amber-500/30 text-amber-200 shadow-[0_0_20px_rgba(245,158,11,0.15)] hover:border-amber-400/60 hover:shadow-[0_0_30px_rgba(245,158,11,0.3)]'
      : 'border-white/10 text-neutral-300 hover:border-white/20';

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        filter: isHovered ? 'url(#liquid-glass-disp)' : 'none',
        transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
      }}
      className={`relative px-5 py-2.5 rounded-xl font-mono text-xs tracking-wider uppercase font-medium bg-neutral-900/60 border ${baseColors} transition-all duration-300 cursor-pointer overflow-hidden ${className}`}
    >
      <span className="relative z-10 flex items-center gap-2">{children}</span>
      <div
        className={`absolute inset-0 bg-gradient-to-r from-amber-500/10 via-amber-400/5 to-transparent opacity-0 transition-opacity duration-300 ${
          isHovered ? 'opacity-100' : ''
        }`}
      />
    </button>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'episodic' | 'semantic' | 'working' | 'procedural'>('overview');
  const [workingTokens, setWorkingTokens] = useState<number>(1420);
  const [semanticNodesCount, setSemanticNodesCount] = useState<number>(48);
  const [episodesCount, setEpisodesCount] = useState<number>(184);
  const [skillsCount, setSkillsCount] = useState<number>(12);

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-neutral-200 relative selection:bg-amber-500/20 selection:text-amber-200 overflow-x-hidden">
      {/* Background Amber Cascades Particle Simulation */}
      <AmberCascades />

      {/* SVG LiquidGlass filter definition */}
      <svg className="hidden" aria-hidden="true">
        <defs>
          <filter id="liquid-glass-disp" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.035"
              numOctaves="3"
              result="noise"
            />
            <feDisplacementMap
              in="SourceGraphic"
              in2="noise"
              scale="7"
              xChannelSelector="R"
              yChannelSelector="G"
            />
          </filter>
        </defs>
      </svg>

      {/* Luxury Header */}
      <header className="border-b border-white/[0.06] bg-black/40 backdrop-blur-md sticky top-0 z-50 px-8 py-5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-lg border border-amber-500/40 bg-amber-500/10 flex items-center justify-center text-amber-400 font-mono text-sm font-bold shadow-[0_0_15px_rgba(245,158,11,0.2)]">
              M
            </div>
            <div>
              <h1 className="font-serif text-2xl tracking-wide text-neutral-100 font-normal">
                Memory Lab
              </h1>
              <p className="font-mono text-[11px] text-neutral-500 uppercase tracking-widest">
                4-Tier Cognitive Architecture
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <LiquidGlassButton
              onClick={() => {
                setWorkingTokens((prev) => Math.min(4000, prev + 250));
                setEpisodesCount((prev) => prev + 1);
              }}
            >
              + Ingest Episode
            </LiquidGlassButton>
            <LiquidGlassButton
              variant="neutral"
              onClick={() => setWorkingTokens((prev) => Math.max(0, prev - 400))}
            >
              Evict Buffer
            </LiquidGlassButton>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-8 py-10">
        {/* Metric Overview Banners */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
          <div className="p-5 rounded-2xl bg-neutral-900/40 border border-white/[0.06] backdrop-blur-sm relative overflow-hidden">
            <span className="font-mono text-[10px] uppercase tracking-wider text-neutral-500 block mb-1">
              Tier 1 · Working Context
            </span>
            <div className="flex items-baseline gap-2">
              <span className="font-mono text-2xl text-amber-300 font-semibold">
                {workingTokens}
              </span>
              <span className="font-mono text-xs text-neutral-500">/ 4000 tokens</span>
            </div>
            <div className="w-full bg-neutral-800 h-1.5 rounded-full mt-3 overflow-hidden">
              <div
                className="bg-amber-400 h-full transition-all duration-500"
                style={{ width: `${(workingTokens / 4000) * 100}%` }}
              />
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-neutral-900/40 border border-white/[0.06] backdrop-blur-sm">
            <span className="font-mono text-[10px] uppercase tracking-wider text-neutral-500 block mb-1">
              Tier 2 · Episodic Traces
            </span>
            <span className="font-mono text-2xl text-neutral-100 font-semibold">
              {episodesCount}
            </span>
            <span className="font-mono text-xs text-neutral-500 block mt-1">SQLite WAL & FTS5</span>
          </div>

          <div className="p-5 rounded-2xl bg-neutral-900/40 border border-white/[0.06] backdrop-blur-sm">
            <span className="font-mono text-[10px] uppercase tracking-wider text-neutral-500 block mb-1">
              Tier 3 · Semantic Graph
            </span>
            <span className="font-mono text-2xl text-neutral-100 font-semibold">
              {semanticNodesCount}
            </span>
            <span className="font-mono text-xs text-neutral-500 block mt-1">Decay: 0.85 · Max Hops: 2</span>
          </div>

          <div className="p-5 rounded-2xl bg-neutral-900/40 border border-white/[0.06] backdrop-blur-sm">
            <span className="font-mono text-[10px] uppercase tracking-wider text-neutral-500 block mb-1">
              Tier 4 · Procedural Skills
            </span>
            <span className="font-mono text-2xl text-neutral-100 font-semibold">
              {skillsCount}
            </span>
            <span className="font-mono text-xs text-neutral-500 block mt-1">ACT-R Power Law Dynamic</span>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-white/[0.06] mb-8 gap-8">
          {(['overview', 'episodic', 'semantic', 'working', 'procedural'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`pb-3 font-mono text-xs uppercase tracking-widest transition-all duration-200 cursor-pointer ${
                activeTab === tab
                  ? 'text-amber-400 border-b-2 border-amber-400 font-semibold'
                  : 'text-neutral-500 hover:text-neutral-300'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Panel Content */}
        <div className="bg-neutral-950/60 border border-white/[0.06] rounded-3xl p-8 backdrop-blur-md">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h2 className="font-serif text-3xl text-neutral-100 font-light">
                Cognitive Architecture Runtime
              </h2>
              <p className="text-neutral-400 text-sm leading-relaxed max-w-3xl">
                Memory Lab implements a four-tier cognitive persistence pipeline for autonomous
                software engineering agents. State is strictly partitioned across transient working
                attention, persistent episodic records, associative concept graphs, and reinforced
                procedural capabilities.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
                <div className="p-5 rounded-xl border border-white/[0.04] bg-neutral-900/20">
                  <h3 className="font-mono text-sm text-amber-400 mb-2">WAL Storage Engine</h3>
                  <p className="text-xs text-neutral-400">
                    Local-first embedded SQLite engine with WAL journaling, FTS5 porter indexing, and
                    sub-100ms transactional persistence.
                  </p>
                </div>
                <div className="p-5 rounded-xl border border-white/[0.04] bg-neutral-900/20">
                  <h3 className="font-mono text-sm text-amber-400 mb-2">Model Context Protocol</h3>
                  <p className="text-xs text-neutral-400">
                    Standard JSON-RPC 2.0 stdio server interface exposing memory tools directly to
                    Claude, Cursor, and Converge loops.
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'episodic' && (
            <div>
              <h3 className="font-serif text-2xl mb-4 text-neutral-100">Episodic Timeline</h3>
              <div className="space-y-3 font-mono text-xs">
                <div className="p-4 rounded-xl bg-neutral-900/30 border border-white/[0.04] flex justify-between">
                  <div>
                    <span className="text-amber-400">[agent-executor]</span> Initialized SQLite WAL storage
                  </div>
                  <span className="text-neutral-500">Salience: 0.95</span>
                </div>
                <div className="p-4 rounded-xl bg-neutral-900/30 border border-white/[0.04] flex justify-between">
                  <div>
                    <span className="text-amber-400">[operator]</span> Gated Tier-1 crypto signatures
                  </div>
                  <span className="text-neutral-500">Salience: 0.90</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'semantic' && (
            <div>
              <h3 className="font-serif text-2xl mb-4 text-neutral-100">Associative Knowledge</h3>
              <p className="text-neutral-400 text-xs mb-4">
                Bidirectional concept edges with decay-weighted spreading activation queries.
              </p>
              <div className="grid grid-cols-3 gap-3 font-mono text-xs mb-6">
                <div className="p-3 bg-neutral-900/30 rounded-lg border border-white/[0.04]">
                  <span className="text-amber-300">SQLite &lt;-&gt; WAL</span> (weight: 0.95)
                </div>
                <div className="p-3 bg-neutral-900/30 rounded-lg border border-white/[0.04]">
                  <span className="text-amber-300">Python &lt;-&gt; SQLite</span> (weight: 0.85)
                </div>
                <div className="p-3 bg-neutral-900/30 rounded-lg border border-white/[0.04]">
                  <span className="text-amber-300">MCP &lt;-&gt; Converge</span> (weight: 0.90)
                </div>
              </div>
              <GraphExplorer />
            </div>
          )}

          {activeTab === 'working' && (
            <div>
              <h3 className="font-serif text-2xl mb-4 text-neutral-100">Working Memory Buffer</h3>
              <p className="text-neutral-400 text-xs mb-4">
                Strict 4000 token maximum. Lowest salience items automatically evicted on pressure.
              </p>
              <div className="font-mono text-xs space-y-2">
                <div className="p-3 bg-neutral-900/30 rounded-lg border border-white/[0.04] flex justify-between">
                  <span>Task-Spec active execution profile</span>
                  <span className="text-amber-400">720 tokens</span>
                </div>
                <div className="p-3 bg-neutral-900/30 rounded-lg border border-white/[0.04] flex justify-between">
                  <span>Recent episodic execution trace</span>
                  <span className="text-amber-400">450 tokens</span>
                </div>
                <div className="p-3 bg-neutral-900/30 rounded-lg border border-white/[0.04] flex justify-between">
                  <span>Associative concept activations</span>
                  <span className="text-amber-400">250 tokens</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'procedural' && (
            <div>
              <h3 className="font-serif text-2xl mb-4 text-neutral-100">Procedural Skills</h3>
              <p className="text-neutral-400 text-xs mb-4">
                Reinforced operational procedures tracked under ACT-R power law of practice.
              </p>
              <div className="font-mono text-xs space-y-2">
                <div className="p-3 bg-neutral-900/30 rounded-lg border border-white/[0.04] flex justify-between">
                  <span>taskspec_accept_stamp</span>
                  <span className="text-amber-400">Activation: 2.14 · Successes: 6</span>
                </div>
                <div className="p-3 bg-neutral-900/30 rounded-lg border border-white/[0.04] flex justify-between">
                  <span>compile_and_test</span>
                  <span className="text-amber-400">Activation: 1.85 · Successes: 5</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
