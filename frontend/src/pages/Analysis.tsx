import { useStore } from '../store/useStore';
import { useNavigate } from 'react-router-dom';

export function Analysis() {
  const { latestAnalysis, interestProfile, runAnalysis, isAnalyzing } = useStore();
  const navigate = useNavigate();


  const primaryInterest = latestAnalysis?.interest_detected || interestProfile?.primary_interest || 'Technology';
  const confidence = latestAnalysis?.confidence || interestProfile?.confidence || 'Medium';
  const confidenceScore = latestAnalysis?.confidence_score || interestProfile?.confidence_score || 0.75;
  const evidence = latestAnalysis?.interest_evidence || interestProfile?.secondary_interests || [
    'High watch completion on programming content',
    'Repeated interaction with developer career content',
    'Saved hardware & technical comparison Reels',
  ];

  const interestScores = latestAnalysis?.interest_scores || interestProfile?.interest_scores || {
    'Software Engineering': 0.85,
    'Programming': 0.74,
    'Developer Career': 0.61,
    'Technical Interview Prep': 0.55,
    'Computer Hardware': 0.47,
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Top Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>
            Interest Analysis & Inference Engine
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            See how the AI infers deeper technical interests beyond surface-level Reel tags.
          </p>
        </div>

        <button className="btn btn-primary btn-lg" onClick={runAnalysis} disabled={isAnalyzing}>
          ⚡ Run Interest Inference
        </button>
      </div>

      {/* Primary Inferred Interest Hero */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(99,130,255,0.12) 0%, rgba(168,85,247,0.12) 100%)',
          border: '1px solid rgba(99,130,255,0.3)',
          padding: '2rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1.5rem',
        }}
      >
        <div>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.5rem' }}>
            Dominant Inferred Technology Domain
          </div>
          <h2 style={{ fontSize: '2.25rem', fontWeight: 800, background: 'var(--gradient-primary)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: '0.5rem' }}>
            {primaryInterest}
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', maxWidth: 520 }}>
            Inferred through multi-signal domain expansion across observed interaction vectors.
          </p>
        </div>

        <div style={{ textAlign: 'right', background: 'rgba(0,0,0,0.3)', padding: '1.25rem 1.75rem', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>AI Confidence</div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: confidence === 'High' ? 'var(--accent-green)' : 'var(--accent-blue)' }}>
            {confidence} ({Math.round(confidenceScore * 100)}%)
          </div>
        </div>
      </div>

      {/* Critical Hackathon Distinction Box */}
      <div
        style={{
          background: 'rgba(34,211,238,0.05)',
          border: '1px solid rgba(34,211,238,0.25)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.5rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
          <span style={{ fontSize: '1.5rem' }}>💡</span>
          <h3 style={{ fontSize: '1.125rem' }}>
            Observed Topics vs. Inferred Broader Interests
          </h3>
        </div>

        <div className="grid-2">
          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-amber)', marginBottom: '0.5rem' }}>
              📌 Observed Surface Topics (Watched)
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
              <span className="badge badge-amber">Java Meme</span>
              <span className="badge badge-amber">Developer Lifestyle</span>
              <span className="badge badge-amber">Coding Interview Joke</span>
              <span className="badge badge-amber">Laptop Specs</span>
            </div>
          </div>

          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-green)', marginBottom: '0.5rem' }}>
              🚀 Inferred Broader Interest (AI Agent)
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
              <span className="badge badge-green">Software Engineering</span>
              <span className="badge badge-blue">DSA / Algorithms</span>
              <span className="badge badge-purple">System Design</span>
              <span className="badge badge-cyan">Backend Engineering</span>
            </div>
          </div>
        </div>
      </div>

      {/* Multi-Dimensional Interest Breakdown */}
      <div className="card">
        <h3 style={{ fontSize: '1.25rem', marginBottom: '1.5rem' }}>
          Multidimensional Interest Breakdown
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {Object.entries(interestScores).map(([topic, score]) => {
            const pct = Math.round((score as number) * 100);
            return (
              <div key={topic}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.375rem', fontSize: '0.875rem' }}>
                  <span style={{ fontWeight: 600 }}>{topic}</span>
                  <span style={{ color: 'var(--accent-blue)', fontWeight: 700 }}>{pct}%</span>
                </div>
                <div className="progress-track">
                  <div className="progress-fill" style={{ width: `${pct}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Evidence & Interaction Signals */}
      <div className="card">
        <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>
          Interaction Evidence & Signals
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {Array.isArray(evidence) && evidence.map((item, idx) => (
            <div
              key={idx}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.75rem 1rem',
                background: 'rgba(255,255,255,0.03)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-subtle)',
              }}
            >
              <span style={{ color: 'var(--accent-green)', fontSize: '1.125rem' }}>✓</span>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{item}</span>
            </div>
          ))}
        </div>

        <div style={{ marginTop: '1.5rem', textAlign: 'right' }}>
          <button className="btn btn-primary" onClick={() => navigate('/recommendation')}>
            View Recommended Content →
          </button>
        </div>
      </div>
    </div>
  );
}
