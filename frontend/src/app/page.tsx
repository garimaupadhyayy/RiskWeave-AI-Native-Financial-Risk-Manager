/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import React, { useState } from 'react';
import { Activity, ShieldCheck, FileSearch, Zap, TrendingUp } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';
import ReactMarkdown from 'react-markdown';

// Mock response matching our Python backend output for a Rotating Ring attack
const mockPayload = {
  transaction_id: "tx_evil_ring_99",
  timestamp: "2026-09-09 12:05:00",
  amount: 9500.0,
  is_anomalous: true,
  probability_fraud: 0.985,
  action: "REVIEW",
  expected_cost: 45.0,
  cost_breakdown: {
    "ALLOW": 9357.5,
    "MONITOR": 9357.55,
    "STEP_UP": 475.1,
    "REVIEW": 45.0,
    "HOLD": 118.75
  },
  dna_features: [
    { subject: 'Velocity Burst', A: 95 },
    { subject: 'Entity Reuse', A: 120 },
    { subject: 'Amount Escal.', A: 80 },
    { subject: 'Graph Degree', A: 150 },
    { subject: 'Refund Coupling', A: 10 }
  ],
  investigation_summary: `### AI Risk Investigation Report\n\n**Transaction:** \`tx_evil_ring_99\` | **Decision:** \`REVIEW\`\n\nThe XGBoost model assigned a **98.50%** probability of fraud. This transaction exhibits a massive **Velocity Burst** and a high **Graph Degree**, indicating this device has rapidly switched between multiple customer accounts within the last 24 hours (a classic Rotating-Device Ring).\n\nBased on the $9,500.00 transaction amount, the Cost Optimizer determined that a manual \`REVIEW\` is the most financially optimal action (Expected Loss: **$45.00**). Automatically blocking (\`HOLD\`) is mathematically sub-optimal because the $118.75 insult cost of a false positive outweighs the $5.00 manual review fee.`
};

export default function Dashboard() {
  const [transactions, setTransactions] = useState([
    { id: 'tx_legit_1', amount: 45.0, time: '12:01:00', risk: 0.01, action: 'ALLOW' },
    { id: 'tx_legit_2', amount: 120.0, time: '12:02:15', risk: 0.05, action: 'ALLOW' },
    { id: 'tx_susp_3', amount: 450.0, time: '12:03:10', risk: 0.35, action: 'STEP_UP' },
  ]);
  
  const [selectedTx, setSelectedTx] = useState<any>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const simulateIncoming = () => {
    setIsSimulating(true);
    setTimeout(() => {
      setTransactions([{ 
        id: mockPayload.transaction_id, 
        amount: mockPayload.amount, 
        time: '12:05:00', 
        risk: mockPayload.probability_fraud, 
        action: mockPayload.action 
      }, ...transactions]);
      setSelectedTx(mockPayload);
      setIsSimulating(false);
    }, 800);
  };

  const getActionColor = (action: string) => {
    switch(action) {
      case 'ALLOW': return 'bg-green-900/30 text-green-400 border-green-800';
      case 'STEP_UP': return 'bg-yellow-900/30 text-yellow-400 border-yellow-800';
      case 'REVIEW': return 'bg-orange-900/30 text-orange-400 border-orange-800';
      case 'HOLD': return 'bg-red-900/30 text-red-400 border-red-800';
      default: return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  return (
    <div className="h-screen bg-[#020617] p-4 font-sans text-slate-200 overflow-hidden flex flex-col">
      <div className="max-w-[1800px] w-full mx-auto flex flex-col h-full">
        
        {/* Header */}
        <header className="mb-4 shrink-0 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <img src="/icon.svg" className="w-7 h-7" alt="RiskWeave Logo" />
              RiskWeave Dashboard
            </h1>
            <p className="text-sm text-slate-400 mt-0.5">AI-Native Financial Risk Manager</p>
          </div>
          <button 
            onClick={simulateIncoming}
            disabled={isSimulating}
            className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-1.5 rounded-lg text-sm font-medium shadow-sm transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            {isSimulating ? <Activity className="animate-spin" size={16} /> : <Zap size={16} />}
            Simulate Zero-Day Attack
          </button>
        </header>

        {/* Main Content Area */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-4 flex-1 min-h-0">
          
          {/* Left Col: Feed (Stretches full height) */}
          <div className="bg-[#0f172a] rounded-xl shadow-lg border border-slate-800 flex flex-col h-full overflow-hidden">
            <div className="p-3 border-b border-slate-800 bg-slate-900/50 shrink-0">
              <h2 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                <Activity size={16} className="text-slate-400" />
                Live Transaction Feed
              </h2>
            </div>
            <div className="divide-y divide-slate-800 overflow-y-auto flex-1">
              {transactions.map(tx => (
                <div 
                  key={tx.id} 
                  onClick={() => {
                    if (tx.id === mockPayload.transaction_id) {
                      setSelectedTx(mockPayload);
                    } else {
                      setSelectedTx({
                        transaction_id: tx.id,
                        action: tx.action,
                        dna_features: [
                          { subject: 'Velocity', A: tx.risk * 100 },
                          { subject: 'Entity', A: 10 },
                          { subject: 'Amount', A: 20 },
                          { subject: 'Degree', A: 5 },
                          { subject: 'Refund', A: 0 }
                        ],
                        cost_breakdown: {
                          'ALLOW': tx.action === 'ALLOW' ? 0.00 : 100.00,
                          'MONITOR': 0.05,
                          'STEP_UP': tx.action === 'STEP_UP' ? 0.10 : 50.00,
                          'REVIEW': 5.00,
                          'HOLD': tx.amount * 0.25
                        },
                        investigation_summary: `**Routine AI Assessment**\n\nTransaction ${tx.id} was evaluated by the RiskWeave engine. With a calculated risk score of ${(tx.risk*100).toFixed(1)}%, the optimal financial decision was to **${tx.action}**. No graph topology anomalies or severe velocity bursts were detected.`
                      });
                    }
                  }}
                  className={`p-3 hover:bg-slate-800/50 cursor-pointer transition-colors ${selectedTx?.transaction_id === tx.id ? 'bg-indigo-900/20 border-l-4 border-indigo-500' : 'border-l-4 border-transparent'}`}
                >
                  <div className="flex justify-between items-start mb-1.5">
                    <div className="font-mono text-xs text-slate-300">{tx.id}</div>
                    <span className="text-[10px] text-slate-500">{tx.time}</span>
                  </div>
                  <div className="flex justify-between items-end">
                    <div className="text-base font-semibold text-white">${tx.amount.toFixed(2)}</div>
                    <div className="flex items-center gap-2">
                      <div className="text-xs">
                        <span className="text-slate-500 mr-1">Risk:</span>
                        <span className={`font-medium ${tx.risk > 0.5 ? 'text-red-400' : 'text-green-400'}`}>{(tx.risk * 100).toFixed(1)}%</span>
                      </div>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getActionColor(tx.action)}`}>
                        {tx.action}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right Cols: Detail (Stretches full height) */}
          <div className="xl:col-span-2 h-full flex flex-col space-y-4">
            {selectedTx ? (
              <>
                {/* Top Detail Row (Fixed Height) */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 shrink-0">
                  
                  {/* Attack DNA Radar */}
                  <div className="bg-[#0f172a] p-4 rounded-xl shadow-lg border border-slate-800 flex flex-col">
                    <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2 mb-2 shrink-0">
                      <TrendingUp size={16} className="text-indigo-400" />
                      10-D Attack DNA
                    </h3>
                    <div className="flex-1 min-h-[220px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={selectedTx.dna_features}>
                          <PolarGrid stroke="#334155" />
                          <PolarAngleAxis dataKey="subject" tick={{fill: '#94a3b8', fontSize: 10}} />
                          <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                          <Radar name="Transaction" dataKey="A" stroke="#818cf8" fill="#6366f1" fillOpacity={0.4} />
                          <Tooltip contentStyle={{backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc', fontSize: '12px', padding: '4px 8px'}} />
                        </RadarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Cost Optimizer Array */}
                  <div className="bg-[#0f172a] p-4 rounded-xl shadow-lg border border-slate-800 flex flex-col">
                    <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2 mb-3 shrink-0">
                      <Activity size={16} className="text-emerald-400" />
                      Financial Cost Optimizer
                    </h3>
                    <div className="space-y-2 flex-1">
                      {Object.entries(selectedTx.cost_breakdown).map(([action, cost]: [string, any]) => (
                        <div key={action} className={`flex justify-between items-center p-2 rounded-lg border ${selectedTx.action === action ? 'bg-indigo-900/30 border-indigo-500/50' : 'bg-slate-800/50 border-slate-700/50'}`}>
                          <div className="flex items-center gap-2">
                            <span className={`w-1.5 h-1.5 rounded-full ${selectedTx.action === action ? 'bg-indigo-400' : 'bg-slate-600'}`}></span>
                            <span className={`text-xs font-medium ${selectedTx.action === action ? 'text-indigo-300' : 'text-slate-400'}`}>{action}</span>
                          </div>
                          <div className="font-mono text-xs text-slate-200">
                            ${cost.toFixed(2)}
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="mt-3 pt-3 border-t border-slate-800 text-[11px] text-slate-500 shrink-0">
                      Optimal decision mathematically minimizes $E[Cost]$.
                    </div>
                  </div>
                </div>

                {/* Bottom Row: Gemini Summary (Flex-1 to stretch to the bottom!) */}
                <div className="bg-[#0f172a] p-5 rounded-xl shadow-lg border border-slate-800 flex-1 flex flex-col min-h-0">
                  <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2 mb-3 pb-3 border-b border-slate-800 shrink-0">
                    <FileSearch size={16} className="text-purple-400" />
                    Gemini Agent Investigation
                  </h3>
                  <div className="prose prose-invert prose-sm max-w-none text-sm leading-relaxed overflow-y-auto pr-2 custom-scrollbar">
                    <ReactMarkdown>{selectedTx.investigation_summary}</ReactMarkdown>
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-[#0f172a] h-full rounded-xl shadow-lg border border-slate-800 flex flex-col items-center justify-center text-slate-500">
                <ShieldCheck size={48} className="mb-4 text-slate-700" />
                <p>Select a transaction from the feed to view intelligence.</p>
              </div>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
}
