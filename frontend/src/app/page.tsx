/* eslint-disable */
"use client";
import React, { useState, useEffect } from 'react';
import { Activity, ShieldCheck, FileSearch, Zap, TrendingUp, Search, Clock, Cpu, Network, Database, CheckCircle, XCircle, AlertCircle, BarChart3, Map, ShieldAlert, DollarSign, LayoutDashboard, History, Settings, Play } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip as RechartsTooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, LineChart, Line } from 'recharts';
import ReactMarkdown from 'react-markdown';
import ReactFlow, { Background, Controls, MarkerType } from 'reactflow';
import 'reactflow/dist/style.css';

// -----------------------------------------------------------------------------
// MOCK DATA & SIMULATOR PAYLOADS
// -----------------------------------------------------------------------------

const mockThreatData = [
  { time: '10:00', volume: 450, anomalies: 12 },
  { time: '11:00', volume: 520, anomalies: 18 },
  { time: '12:00', volume: 480, anomalies: 15 },
  { time: '13:00', volume: 1200, anomalies: 350 },
  { time: '14:00', volume: 900, anomalies: 210 },
  { time: '15:00', volume: 510, anomalies: 25 },
];

const initialNodes = [
  { id: 'c1', data: { label: 'Account A' }, position: { x: 250, y: 50 }, style: { background: '#1e293b', color: '#fff', border: '1px solid #334155', borderRadius: '8px', padding: '10px' } },
  { id: 'c2', data: { label: 'Account B' }, position: { x: 450, y: 50 }, style: { background: '#1e293b', color: '#fff', border: '1px solid #334155', borderRadius: '8px', padding: '10px' } },
  { id: 'c3', data: { label: 'Account C' }, position: { x: 50, y: 50 }, style: { background: '#1e293b', color: '#fff', border: '1px solid #334155', borderRadius: '8px', padding: '10px' } },
  { id: 'd1', data: { label: 'Device: D-182\n(CRITICAL)' }, position: { x: 250, y: 150 }, style: { background: '#7f1d1d', color: '#fff', border: '2px solid #ef4444', borderRadius: '8px', padding: '10px', fontWeight: 'bold' } },
  { id: 'ip1', data: { label: 'IP: 192.168.1.45' }, position: { x: 250, y: 250 }, style: { background: '#1e293b', color: '#fff', border: '1px solid #334155', borderRadius: '8px', padding: '10px' } },
  { id: 'm1', data: { label: 'Merchant: Razorpay Gateway' }, position: { x: 250, y: 350 }, style: { background: '#1e293b', color: '#fff', border: '1px solid #334155', borderRadius: '8px', padding: '10px' } },
];

const initialEdges = [
  { id: 'e1', source: 'c1', target: 'd1', animated: true, style: { stroke: '#ef4444', strokeWidth: 2 } },
  { id: 'e2', source: 'c2', target: 'd1', animated: true, style: { stroke: '#ef4444', strokeWidth: 2 } },
  { id: 'e3', source: 'c3', target: 'd1', animated: true, style: { stroke: '#ef4444', strokeWidth: 2 } },
  { id: 'e4', source: 'd1', target: 'ip1', animated: true, style: { stroke: '#ef4444', strokeWidth: 2 } },
  { id: 'e5', source: 'ip1', target: 'm1', animated: true, style: { stroke: '#ef4444', strokeWidth: 2 } },
];

const mockZeroDayPayload = {
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
    { subject: 'Refund Coupling', A: 10 },
    { subject: 'Auth Fail Rate', A: 85 },
    { subject: 'Merchant Conc.', A: 90 }
  ],
  investigation_summary: `### Executive Finding\n**CRITICAL:** High probability (98.5%) of a **Rotating-Device Attack Ring**.\n\n### Structured Evidence\n* **Velocity Burst:** 95th percentile acceleration.\n* **Graph Degree:** Device \`D-182\` is linked to 37 distinct customer accounts in 24h.\n* **Temporal Density:** Highly unnatural transaction arrival rate.\n\n### Safety Gate Status\n✅ **PASSED.** Policy Engine has intercepted Gemini recommendation and applied deterministic financial optimization.\n\n### Financial Conclusion\nBlocking (\`HOLD\`) incurs a ₹118.75 false-positive insult cost. Manual \`REVIEW\` minimizes expected loss to **₹45.00**.`
};

// -----------------------------------------------------------------------------
// MAIN DASHBOARD COMPONENT
// -----------------------------------------------------------------------------

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [isSimulating, setIsSimulating] = useState(false);
  const [simStep, setSimStep] = useState(0);
  const [transactions, setTransactions] = useState([
    { id: 'tx_legit_1', amount: 45.0, time: '12:01:00', risk: 0.01, action: 'ALLOW' },
    { id: 'tx_legit_2', amount: 120.0, time: '12:02:15', risk: 0.05, action: 'ALLOW' },
    { id: 'tx_susp_3', amount: 450.0, time: '12:03:10', risk: 0.35, action: 'STEP_UP' },
  ]);
  const [selectedTx, setSelectedTx] = useState<any>(null);

  const simulateIncoming = () => {
    setActiveTab('investigation');
    setIsSimulating(true);
    setSimStep(1); // Detection
    
    setTimeout(() => setSimStep(2), 1000); // Graph
    setTimeout(() => setSimStep(3), 2000); // XGBoost
    setTimeout(() => setSimStep(4), 3000); // Optimizer
    setTimeout(() => {
      setSimStep(5); // Final
      setTransactions([{ 
        id: mockZeroDayPayload.transaction_id, 
        amount: mockZeroDayPayload.amount, 
        time: '12:05:00', 
        risk: mockZeroDayPayload.probability_fraud, 
        action: mockZeroDayPayload.action 
      }, ...transactions]);
      setSelectedTx(mockZeroDayPayload);
      setIsSimulating(false);
    }, 4000);
  };

  const getActionColor = (action: string) => {
    switch(action) {
      case 'ALLOW': return 'bg-emerald-900/30 text-emerald-400 border-emerald-800';
      case 'STEP_UP': return 'bg-yellow-900/30 text-yellow-400 border-yellow-800';
      case 'REVIEW': return 'bg-orange-900/30 text-orange-400 border-orange-800';
      case 'HOLD': return 'bg-red-900/30 text-red-400 border-red-800';
      default: return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  // -----------------------------------------------------------------------------
  // TAB VIEWS
  // -----------------------------------------------------------------------------

  const renderOverview = () => (
    <div className="flex flex-col gap-6 h-full overflow-y-auto pr-2 pb-10">
      {/* KPI Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <p className="text-slate-400 text-sm font-medium mb-1">Current Exposure</p>
          <h3 className="text-3xl font-bold text-white mb-2">₹8.4L</h3>
          <p className="text-xs text-slate-500">Potential 24h Blast Radius: <span className="text-red-400 font-semibold">₹21.7L</span></p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <p className="text-slate-400 text-sm font-medium mb-1">Expected Loss Prevented</p>
          <h3 className="text-3xl font-bold text-emerald-400 mb-2">₹4.8L</h3>
          <p className="text-xs text-slate-500">vs. counterfactual ALLOW policy</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <p className="text-slate-400 text-sm font-medium mb-1">Active Attack Clusters</p>
          <h3 className="text-3xl font-bold text-red-500 mb-2">3</h3>
          <p className="text-xs text-slate-500">1 CRITICAL, 2 HIGH</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <p className="text-slate-400 text-sm font-medium mb-1">Transactions Analyzed</p>
          <h3 className="text-3xl font-bold text-white mb-2">512,408</h3>
          <p className="text-xs text-emerald-500 font-semibold">↑ 100% Coverage</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <TrendingUp size={18} className="text-indigo-400" />
              Live Threat Activity
            </h2>
            <span className="text-[10px] uppercase font-bold tracking-widest bg-slate-800 text-slate-400 border border-slate-700 px-2 py-1 rounded">EXPERIMENTAL SIMULATION</span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockThreatData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#475569" fontSize={12} />
                <YAxis yAxisId="left" stroke="#475569" fontSize={12} />
                <YAxis yAxisId="right" orientation="right" stroke="#ef4444" fontSize={12} />
                <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9' }} />
                <Line yAxisId="left" type="monotone" dataKey="volume" stroke="#6366f1" strokeWidth={2} name="Tx Volume" dot={false} />
                <Line yAxisId="right" type="monotone" dataKey="anomalies" stroke="#ef4444" strokeWidth={2} name="Anomalies" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2 mb-4">
            <ShieldAlert size={18} className="text-red-400" />
            Active Attack Rings
          </h2>
          <div className="flex-1 overflow-y-auto flex flex-col gap-3">
            <div className="bg-slate-800/50 p-3 rounded-lg border border-red-900/50 hover:bg-slate-800 transition cursor-pointer" onClick={() => setActiveTab('graph')}>
              <div className="flex justify-between items-start mb-2">
                <span className="text-sm font-bold text-slate-200">CLUSTER-A92</span>
                <span className="text-[10px] font-bold bg-red-500/20 text-red-400 px-2 py-0.5 rounded border border-red-500/30">CRITICAL</span>
              </div>
              <p className="text-xs text-slate-400 mb-2">Rotating-Device Ring</p>
              <div className="flex justify-between text-xs text-slate-500">
                <span>37 Accounts</span>
                <span>Exposure: <span className="text-slate-300 font-semibold">₹4.2L</span></span>
              </div>
            </div>
            <div className="bg-slate-800/50 p-3 rounded-lg border border-orange-900/50 hover:bg-slate-800 transition cursor-pointer">
              <div className="flex justify-between items-start mb-2">
                <span className="text-sm font-bold text-slate-200">CLUSTER-B14</span>
                <span className="text-[10px] font-bold bg-orange-500/20 text-orange-400 px-2 py-0.5 rounded border border-orange-500/30">HIGH</span>
              </div>
              <p className="text-xs text-slate-400 mb-2">Auth Brute Force</p>
              <div className="flex justify-between text-xs text-slate-500">
                <span>12 IPs</span>
                <span>Exposure: <span className="text-slate-300 font-semibold">₹1.8L</span></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderInvestigation = () => (
    <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 h-full overflow-hidden pb-6">
      {/* Left Col: Feed & Timeline */}
      <div className="flex flex-col gap-4 h-full">
        <div className="bg-slate-900 rounded-xl shadow-sm border border-slate-800 flex flex-col h-1/2 overflow-hidden">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Activity size={16} className="text-slate-400" />
              Live Feed
            </h2>
          </div>
          <div className="flex-1 overflow-y-auto p-2">
            {transactions.map(tx => (
              <div 
                key={tx.id} 
                onClick={() => setSelectedTx(tx)}
                className={`p-3 mb-2 rounded-lg border cursor-pointer transition-all ${
                  selectedTx?.id === tx.id 
                    ? 'bg-slate-800 border-indigo-500' 
                    : 'bg-slate-800/40 border-slate-700/50 hover:bg-slate-800'
                }`}
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="font-mono text-xs text-slate-300">{tx.id}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getActionColor(tx.action)}`}>
                    {tx.action}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-white">₹{tx.amount.toFixed(2)}</span>
                  <span className="text-xs text-slate-500">{tx.time} | Risk: {(tx.risk * 100).toFixed(1)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Decision Timeline Simulator */}
        <div className="bg-slate-900 rounded-xl shadow-sm border border-slate-800 p-4 h-1/2 flex flex-col">
          <h2 className="text-sm font-semibold text-white flex items-center gap-2 mb-4">
            <Clock size={16} className="text-slate-400" />
            Decision Timeline
          </h2>
          <div className="flex-1 flex flex-col justify-between relative pl-4 border-l-2 border-slate-800">
            {[
              { step: 1, label: 'Isolation Forest Anomaly Detection' },
              { step: 2, label: 'MySQL 2-Hop Graph Expansion' },
              { step: 3, label: 'XGBoost Risk Prediction' },
              { step: 4, label: 'Expected Cost Optimization' },
              { step: 5, label: 'Deterministic Policy Execution' }
            ].map(item => (
              <div key={item.step} className="relative">
                <div className={`absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full ${simStep >= item.step ? 'bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.8)]' : 'bg-slate-700'}`}></div>
                <p className={`text-sm ${simStep >= item.step ? 'text-white font-medium' : 'text-slate-500'}`}>{item.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Middle & Right Col: Details */}
      <div className="xl:col-span-2 bg-slate-900 rounded-xl shadow-sm border border-slate-800 flex flex-col h-full overflow-hidden">
        {selectedTx ? (
          <div className="flex-1 overflow-y-auto p-6">
            <div className="flex justify-between items-start mb-6 border-b border-slate-800 pb-4">
              <div>
                <h2 className="text-2xl font-bold text-white mb-1">{selectedTx.transaction_id}</h2>
                <p className="text-slate-400 text-sm">Amount: <span className="text-white font-semibold">₹{selectedTx.amount.toFixed(2)}</span> | {selectedTx.timestamp}</p>
              </div>
              <div className="text-right">
                <p className="text-[10px] font-bold tracking-widest text-slate-500 mb-1 uppercase">Policy Decision</p>
                <span className={`text-lg px-4 py-1 rounded-md border font-bold shadow-sm ${getActionColor(selectedTx.action)}`}>
                  {selectedTx.action}
                </span>
              </div>
            </div>

            {selectedTx.dna_features && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                
                {/* XGBoost & SHAP */}
                <div className="bg-[#0a0f1c] p-5 rounded-xl border border-slate-800 shadow-inner">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                      <Cpu size={16} className="text-indigo-400" />
                      XGBoost Next-Move Prediction
                    </h3>
                    <span className="text-[10px] text-slate-500 uppercase font-bold border border-slate-700 px-1.5 py-0.5 rounded">Model Output</span>
                  </div>
                  <div className="mb-4">
                    <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Predicted Attacker Action</p>
                    <p className="text-xl font-bold text-red-400">DEVICE ROTATION</p>
                    <p className="text-xs text-slate-500 mt-1">Confidence: <span className="text-slate-300 font-semibold">87.4%</span></p>
                  </div>
                  <div className="h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart cx="50%" cy="50%" outerRadius="70%" data={selectedTx.dna_features}>
                        <PolarGrid stroke="#1e293b" />
                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 10 }} />
                        <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                        <Radar name="Attack DNA" dataKey="A" stroke="#ef4444" fill="#ef4444" fillOpacity={0.2} />
                        <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', fontSize: 12 }} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Financial Optimizer */}
                <div className="bg-[#0a0f1c] p-5 rounded-xl border border-slate-800 shadow-inner flex flex-col">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                      <DollarSign size={16} className="text-emerald-400" />
                      Financial Cost Optimizer
                    </h3>
                    <span className="text-[10px] text-slate-500 font-bold uppercase border border-slate-700 px-1.5 py-0.5 rounded">Math Engine</span>
                  </div>
                  <p className="text-xs text-slate-400 mb-4">Expected Loss ($E[Cost]$) calculated via Probability × Cost Matrix.</p>
                  
                  <div className="flex-1 flex flex-col gap-2">
                    {Object.entries(selectedTx.cost_breakdown).map(([action, cost]: any) => (
                      <div key={action} className={`flex justify-between items-center p-2.5 rounded-lg border ${action === selectedTx.action ? 'bg-indigo-900/20 border-indigo-500/50' : 'bg-slate-900 border-slate-800/50'}`}>
                        <span className={`text-sm font-medium ${action === selectedTx.action ? 'text-indigo-300' : 'text-slate-400'}`}>{action}</span>
                        <span className={`font-mono ${action === selectedTx.action ? 'text-white font-bold' : 'text-slate-500'}`}>₹{cost.toFixed(2)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Gemini Investigator */}
            {selectedTx.investigation_summary && (
              <div className="bg-[#0a0f1c] p-6 rounded-xl border border-slate-800 shadow-inner">
                <div className="flex justify-between items-center mb-4 pb-3 border-b border-slate-800">
                  <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                    <FileSearch size={16} className="text-blue-400" />
                    Gemini AI Investigation Console
                  </h3>
                  <div className="flex gap-2">
                    <span className="text-[10px] font-bold text-green-400 uppercase border border-green-900 bg-green-900/20 px-2 py-0.5 rounded flex items-center gap-1">
                      <CheckCircle size={10} /> Safety Gate Passed
                    </span>
                    <span className="text-[10px] font-bold text-slate-500 uppercase border border-slate-700 px-2 py-0.5 rounded">Explanation Only</span>
                  </div>
                </div>
                <div className="prose prose-invert prose-sm max-w-none text-slate-300 marker:text-slate-500 prose-headings:text-slate-200">
                  <ReactMarkdown>{selectedTx.investigation_summary}</ReactMarkdown>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-slate-500 flex-col gap-3">
            <Search size={32} className="opacity-20" />
            <p>Select a transaction to investigate or Simulate a Zero-Day Attack.</p>
          </div>
        )}
      </div>
    </div>
  );

  const renderGraph = () => (
    <div className="h-full w-full bg-slate-900 rounded-xl border border-slate-800 overflow-hidden relative shadow-inner">
      <div className="absolute top-4 left-4 z-10 bg-slate-950/90 p-5 rounded-xl border border-slate-700 backdrop-blur-md max-w-sm shadow-xl">
        <h3 className="text-white font-bold mb-2 flex items-center gap-2"><Network size={18} className="text-indigo-400"/> MySQL Recursive CTE</h3>
        <p className="text-xs text-slate-300 leading-relaxed mb-4">Visualizing the 2-hop entity radius surrounding Transaction <span className="font-mono text-indigo-300 bg-indigo-900/30 px-1 rounded">tx_evil_ring_99</span>. The graph engine identified a Rotating-Device Ring targeting multiple accounts.</p>
        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
            <p className="text-slate-400 mb-1">Query Latency</p>
            <p className="text-white font-bold text-sm">42 ms</p>
          </div>
          <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
            <p className="text-slate-400 mb-1">Nodes Traversed</p>
            <p className="text-white font-bold text-sm">184</p>
          </div>
        </div>
      </div>
      <ReactFlow nodes={initialNodes} edges={initialEdges} fitView attributionPosition="bottom-right">
        <Background color="#1e293b" gap={16} />
        <Controls style={{ backgroundColor: '#0f172a', fill: '#f8fafc', border: '1px solid #1e293b' }} />
      </ReactFlow>
    </div>
  );

  const renderEvaluation = () => (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 h-full overflow-y-auto pb-10 pr-2">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
        <h2 className="text-lg font-bold text-white mb-2 flex items-center gap-2"><BarChart3 size={20} className="text-indigo-400"/> Architecture Ablation Study</h2>
        <p className="text-sm text-slate-400 mb-6">Proving the performance gain of MySQL Graph features over standard ML.</p>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-700 text-xs text-slate-400 uppercase tracking-wider">
                <th className="pb-3 font-semibold">Architecture</th>
                <th className="pb-3 font-semibold">Precision</th>
                <th className="pb-3 font-semibold">Recall</th>
                <th className="pb-3 font-semibold">F1-Score</th>
              </tr>
            </thead>
            <tbody className="text-sm">
              <tr className="border-b border-slate-800/50">
                <td className="py-4 text-slate-300">1. Rules Only</td>
                <td className="py-4 text-slate-400">0.42</td>
                <td className="py-4 text-slate-400">0.31</td>
                <td className="py-4 text-slate-400">0.35</td>
              </tr>
              <tr className="border-b border-slate-800/50">
                <td className="py-4 text-slate-300">2. ML Only (XGBoost)</td>
                <td className="py-4 text-slate-400">0.81</td>
                <td className="py-4 text-slate-400">0.76</td>
                <td className="py-4 text-slate-400">0.78</td>
              </tr>
              <tr className="bg-indigo-900/10 border-l-2 border-indigo-500">
                <td className="py-4 pl-3 text-indigo-300 font-bold">3. Full RiskWeave (ML + Graph)</td>
                <td className="py-4 text-emerald-400 font-bold">0.94</td>
                <td className="py-4 text-emerald-400 font-bold">0.89</td>
                <td className="py-4 text-emerald-400 font-bold">0.91</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex flex-col gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><Database size={20} className="text-emerald-400"/> System Health & Infrastructure</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-[#0a0f1c] p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400 mb-1">API Engine (FastAPI)</p>
              <p className="text-sm font-bold text-emerald-400 flex items-center gap-1"><CheckCircle size={14}/> HEALTHY (12ms)</p>
            </div>
            <div className="bg-[#0a0f1c] p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400 mb-1">TiDB Graph Database</p>
              <p className="text-sm font-bold text-emerald-400 flex items-center gap-1"><CheckCircle size={14}/> 42ms P95 Latency</p>
            </div>
            <div className="bg-[#0a0f1c] p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400 mb-1">Render Redis Cache</p>
              <p className="text-sm font-bold text-emerald-400 flex items-center gap-1"><CheckCircle size={14}/> HEALTHY (3ms)</p>
            </div>
            <div className="bg-[#0a0f1c] p-4 rounded-xl border border-slate-800">
              <p className="text-xs text-slate-400 mb-1">Gemini AI Engine</p>
              <p className="text-sm font-bold text-emerald-400 flex items-center gap-1"><CheckCircle size={14}/> ONLINE (1.2s)</p>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
          <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-2"><Activity size={16} className="text-indigo-400"/> Population Stability Index (PSI)</h3>
          <p className="text-xs text-slate-400 mb-4">Monitoring data drift across 10-D Attack DNA.</p>
          <div className="w-full bg-slate-800 rounded-full h-2 mb-2 overflow-hidden border border-slate-700">
            <div className="bg-emerald-500 h-2 rounded-full" style={{ width: '15%' }}></div>
          </div>
          <div className="flex justify-between text-xs text-slate-500 font-medium">
            <span className="text-emerald-400">Score: 0.04 (Stable)</span>
            <span>Threshold: 0.20</span>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="h-screen bg-[#020617] font-sans text-slate-200 overflow-hidden flex selection:bg-indigo-500/30">
      
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-[#0a0f1c] border-r border-slate-800 flex flex-col shrink-0 z-20">
        <div className="p-6 border-b border-slate-800">
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <img src="/icon.svg" className="w-7 h-7" alt="RiskWeave Logo" />
            RiskWeave
          </h1>
          <p className="text-[10px] text-slate-500 mt-1.5 uppercase tracking-widest font-bold">SOC Command Center</p>
        </div>
        <nav className="flex-1 p-4 flex flex-col gap-2">
          <button onClick={() => setActiveTab('overview')} className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${activeTab === 'overview' ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'}`}>
            <LayoutDashboard size={18} /> Risk Overview
          </button>
          <button onClick={() => setActiveTab('investigation')} className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${activeTab === 'investigation' ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'}`}>
            <FileSearch size={18} /> Transaction Investigation
          </button>
          <button onClick={() => setActiveTab('graph')} className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${activeTab === 'graph' ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'}`}>
            <Network size={18} /> Attack Graph
          </button>
          <button onClick={() => setActiveTab('evaluation')} className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${activeTab === 'evaluation' ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'}`}>
            <BarChart3 size={18} /> Evaluation & Health
          </button>
        </nav>
        <div className="p-4 m-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-indigo-900/50 flex items-center justify-center text-indigo-300 font-bold border border-indigo-800">A</div>
          <div>
            <p className="text-white font-medium text-sm">Analyst Mode</p>
            <p className="text-[10px] text-slate-400">Read & Resolve</p>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden bg-slate-950/50">
        
        {/* Topbar */}
        <header className="h-16 border-b border-slate-800 bg-[#0a0f1c] flex items-center justify-between px-8 shrink-0 z-10">
          <div className="flex items-center gap-6">
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input type="text" placeholder="Search TxID, IP, or Customer..." className="bg-slate-900 border border-slate-700 text-sm rounded-lg pl-9 pr-4 py-2 focus:outline-none focus:border-indigo-500 w-72 text-slate-200 placeholder:text-slate-500 transition-colors" />
            </div>
            <span className="text-[10px] uppercase font-bold tracking-widest bg-indigo-900/40 text-indigo-400 border border-indigo-800/50 px-2 py-1 rounded">DEMO ENVIRONMENT</span>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="flex bg-slate-900 rounded-lg border border-slate-700 p-1">
              {['1H', '24H', '7D', '30D'].map(t => (
                <button key={t} className={`text-xs px-4 py-1.5 rounded-md font-bold transition-all ${t === '24H' ? 'bg-slate-700 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'}`}>{t}</button>
              ))}
            </div>
            <button 
              onClick={simulateIncoming}
              disabled={isSimulating}
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2 rounded-lg text-sm font-bold shadow-lg shadow-indigo-900/20 transition-all flex items-center gap-2 disabled:opacity-50"
            >
              {isSimulating ? <Activity className="animate-spin" size={16} /> : <Play size={16} fill="currentColor" />}
              Simulate Zero-Day Attack
            </button>
          </div>
        </header>

        {/* Tab Content */}
        <main className="flex-1 p-8 overflow-hidden relative">
          <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-900/10 via-transparent to-transparent"></div>
          {activeTab === 'overview' && renderOverview()}
          {activeTab === 'investigation' && renderInvestigation()}
          {activeTab === 'graph' && renderGraph()}
          {activeTab === 'evaluation' && renderEvaluation()}
        </main>
      </div>
    </div>
  );
}

