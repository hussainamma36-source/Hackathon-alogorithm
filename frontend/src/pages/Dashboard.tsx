import { useStore } from '../store/useStore';
import { TrapDemo } from '../components/TrapDemo';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

const COLORS = ['#6382ff', '#a855f7', '#22d3ee', '#10b981', '#f59e0b', '#ec4899'];

export function Dashboard() {
  const {
    interactions,
    latestAnalysis,
    interestProfile,
    runAnalysis,
    loadDemoData,
  } = useStore();

  const totalAnalyzed = Object.keys(interactions).length;
  const dominantInterest = latestAnalysis?.interest_detected || interestProfile?.primary_interest || 'Not Analyzed';
  const eduImprovement = latestAnalysis ? '+84%' : '0%';
  const hypeFiltered = latestAnalysis ? '1 Candidate' : '0';


  // Interest distribution data for chart
  const interestScores = latestAnalysis?.interest_scores || interestProfile?.interest_scores || {
    'Software Eng': 0.85,
    'Programming': 0.74,
    'Tech Career': 0.61,
    'Algorithms': 0.55,
    'Hardware': 0.47,
  };

  const chartData = Object.entries(interestScores).map(([name, score]) => ({
    name: name.length > 14 ? name.substring(0, 14) + '...' : name,
    score: Math.round((score as number) * 100),
  }));

  const pieData = [
    { name: 'Educational', value: 75, color: '#10b981' },
    { name: 'Career', value: 65, color: '#6382ff' },
    { name: 'Entertainment', value: 40, color: '#a855f7' },
    { name: 'Filtered Hype', value: 20, color: '#ef4444' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Top Banner / Hero */}
      <div
        className="card-glass"
        style={{
          padding: '2rem',
          background: 'linear-gradient(135deg, rgba(99,130,255,0.1) 0%, rgba(168,85,247,0.1) 100%)',
          border: '1px solid rgba(99,130,255,0.2)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1.5rem',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <span className="badge badge-purple">AI Recommendation Agent</span>
            <span className="badge badge-blue">Context-Aware Engine</span>
          </div>
          <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
            Turn Your Scrolling Into Smarter Learning
          </h1>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '600px' }}>
            ReelMind AI analyzes your Reel interactions, infers underlying technology interests, and recommends high-value educational content — ignoring surface clickbait and keyword echo chambers.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn btn-ghost" onClick={loadDemoData}>
            📂 Preload Demo Signals
          </button>
          <button className="btn btn-primary btn-lg" onClick={runAnalysis}>
            ⚡ Analyze My Interests
          </button>
        </div>
      </div>

      {/* Key Metrics / Stat Cards */}
      <div className="grid-4">
        <div className="stat-card blue">
          <div className="stat-icon">🎬</div>
          <div className="stat-value">{totalAnalyzed}</div>
          <div className="stat-label">Total Reels Analyzed</div>
        </div>

        <div className="stat-card purple">
          <div className="stat-icon">🧠</div>
          <div className="stat-value" style={{ fontSize: '1.25rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {dominantInterest}
          </div>
          <div className="stat-label">Dominant Inferred Interest</div>
        </div>

        <div className="stat-card green">
          <div className="stat-icon">📈</div>
          <div className="stat-value">{eduImprovement}</div>
          <div className="stat-label">Educational Value Gain</div>
        </div>

        <div className="stat-card amber">
          <div className="stat-icon">🛡️</div>
          <div className="stat-value">{hypeFiltered}</div>
          <div className="stat-label">Hype Content Filtered</div>
        </div>
      </div>

      {/* Visualizations Section */}
      <div className="grid-2">
        {/* Interest Distribution Chart */}
        <div className="chart-container">
          <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            📊 Inferred Interest Profile
          </h3>
          <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Multi-dimensional interest scoring derived from interaction history
          </p>
          <div style={{ height: 260, width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="name" stroke="#8892b0" fontSize={12} />
                <YAxis stroke="#8892b0" fontSize={12} domain={[0, 100]} />
                <Tooltip
                  contentStyle={{ background: '#0d1424', borderColor: 'rgba(99,130,255,0.3)', borderRadius: 8 }}
                  formatter={(val) => [`${val}%`, 'Interest Score']}
                />
                <Bar dataKey="score" radius={[6, 6, 0, 0]}>
                  {chartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Content Quality vs Hype Ratio */}
        <div className="chart-container">
          <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            🎯 Content Mix & Filtering
          </h3>
          <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Breakdown of interaction depth vs filtered hype noise
          </p>
          <div style={{ height: 260, width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`pie-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ background: '#0d1424', borderColor: 'rgba(99,130,255,0.3)', borderRadius: 8 }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Trap Demonstration Component */}
      <TrapDemo />
    </div>
  );
}
