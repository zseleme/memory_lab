import React, { useState } from 'react';

export interface ConceptNode {
  id: string;
  name: string;
  x: number;
  y: number;
  activation: number;
  category: string;
}

export interface ConceptEdge {
  source: string;
  target: string;
  weight: number;
}

const INITIAL_NODES: ConceptNode[] = [
  { id: '1', name: 'SQLite WAL', x: 250, y: 180, activation: 1.0, category: 'Storage' },
  { id: '2', name: 'FTS5 Porter', x: 140, y: 280, activation: 0.85, category: 'Index' },
  { id: '3', name: 'MCP Stdio', x: 420, y: 150, activation: 0.92, category: 'Interface' },
  { id: '4', name: 'Task-Spec Hook', x: 550, y: 240, activation: 0.78, category: 'Lifecycle' },
  { id: '5', name: 'Working Ceiling', x: 340, y: 320, activation: 0.65, category: 'Attention' },
  { id: '6', name: 'ACT-R Power Law', x: 480, y: 360, activation: 0.70, category: 'Procedural' },
];

const INITIAL_EDGES: ConceptEdge[] = [
  { source: '1', target: '2', weight: 0.90 },
  { source: '1', target: '3', weight: 0.85 },
  { source: '3', target: '4', weight: 0.88 },
  { source: '1', target: '5', weight: 0.75 },
  { source: '4', target: '6', weight: 0.80 },
  { source: '5', target: '6', weight: 0.65 },
];

export const GraphExplorer: React.FC<{
  className?: string;
}> = ({ className = '' }) => {
  const [nodes, setNodes] = useState<ConceptNode[]>(INITIAL_NODES);
  const [selectedNode, setSelectedNode] = useState<ConceptNode | null>(nodes[0]);
  const [decay] = useState<number>(0.85);

  const handleNodeClick = (node: ConceptNode) => {
    setSelectedNode(node);
    // Simulate spreading activation: propagate energy to directly linked nodes
    setNodes((prevNodes) =>
      prevNodes.map((n) => {
        if (n.id === node.id) {
          return { ...n, activation: 1.0 };
        }
        const edge = INITIAL_EDGES.find(
          (e) =>
            (e.source === node.id && e.target === n.id) ||
            (e.target === node.id && e.source === n.id)
        );
        if (edge) {
          const spreadEnergy = Math.min(1.0, edge.weight * decay);
          return { ...n, activation: Math.max(n.activation, spreadEnergy) };
        }
        return { ...n, activation: n.activation * 0.9 }; // slight decay
      })
    );
  };

  return (
    <div className={`p-6 bg-neutral-950/80 border border-white/[0.06] rounded-2xl ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-serif text-xl text-neutral-100 font-light">
            Semantic Association Graph Explorer
          </h3>
          <p className="font-mono text-xs text-neutral-500">
            Interactive Spreading Activation · Click any concept node to pulse energy
          </p>
        </div>
        {selectedNode && (
          <div className="font-mono text-xs px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300">
            Active: <span className="font-semibold text-neutral-100">{selectedNode.name}</span> (
            {(selectedNode.activation * 100).toFixed(0)}% energy)
          </div>
        )}
      </div>

      <div className="relative w-full h-[400px] bg-black/50 rounded-xl border border-white/[0.04] overflow-hidden">
        <svg className="w-full h-full">
          {/* Edges */}
          {INITIAL_EDGES.map((edge, idx) => {
            const s = nodes.find((n) => n.id === edge.source);
            const t = nodes.find((n) => n.id === edge.target);
            if (!s || !t) return null;

            const isHighlighted =
              selectedNode &&
              (selectedNode.id === s.id || selectedNode.id === t.id);

            return (
              <g key={`edge-${idx}`}>
                <line
                  x1={s.x}
                  y1={s.y}
                  x2={t.x}
                  y2={t.y}
                  stroke={isHighlighted ? '#f59e0b' : 'rgba(255, 255, 255, 0.15)'}
                  strokeWidth={isHighlighted ? edge.weight * 3 : 1}
                  strokeDasharray={isHighlighted ? '4 2' : 'none'}
                  className="transition-all duration-300"
                />
              </g>
            );
          })}

          {/* Nodes */}
          {nodes.map((node) => {
            const isSelected = selectedNode?.id === node.id;
            const haloRadius = 18 + node.activation * 14;

            return (
              <g
                key={node.id}
                className="cursor-pointer group"
                onClick={() => handleNodeClick(node)}
              >
                {/* Spreading Activation Energy Halo */}
                <circle
                  cx={node.x}
                  cy={node.y}
                  r={haloRadius}
                  fill="url(#amber-halo)"
                  opacity={node.activation * 0.4}
                  className="transition-all duration-500"
                />

                {/* Core Node Circle */}
                <circle
                  cx={node.x}
                  cy={node.y}
                  r={14}
                  fill={isSelected ? '#d97706' : '#1c1917'}
                  stroke={isSelected ? '#fbbf24' : '#78716c'}
                  strokeWidth={isSelected ? 2 : 1}
                  className="transition-all duration-200 group-hover:scale-110"
                />

                {/* Label */}
                <text
                  x={node.x}
                  y={node.y + 26}
                  textAnchor="middle"
                  fill="#d4d4d4"
                  className="font-mono text-[11px] pointer-events-none select-none"
                >
                  {node.name}
                </text>
              </g>
            );
          })}

          <defs>
            <radialGradient id="amber-halo">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.8" />
              <stop offset="60%" stopColor="#d97706" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#b45309" stopOpacity="0" />
            </radialGradient>
          </defs>
        </svg>
      </div>
    </div>
  );
};

export default GraphExplorer;

