import { useStore } from '../store/useStore';

export function Explainability() {
  const { latestAnalysis } = useStore();

  const stages = latestAnalysis?.pipeline_stages || [
    { stage: 'Interaction Analysis', description: 'Analyzed viewing behavior and engagement signals across 5 Reels', status: 'complete', detail: 'Weighted signal matrix: watch%, like, save, replay, skip' },
    { stage: 'Content Understanding', description: 'Mapped Reels into semantic domain vectors and concept clusters', status: 'complete', detail: 'Extracted tech relevance, educational depth, and career alignment' },
    { stage: 'Interest Inference', description: 'Inferred primary domain: Software Engineering / Technology', status: 'complete', detail: 'Neighborhood traversal expanding beyond single surface topic' },
    { stage: 'Candidate Scoring', description: 'Evaluated 8 educational technology candidates', status: 'complete', detail: 'Multi-factor: domain match, edu value, career usefulness, diversity' },
    { stage: 'Hype Filter', description: 'Evaluated hype noise and clickbait patterns', status: 'complete', detail: 'Down-ranked sensationalist listicles with exaggerated claims' },
    { stage: 'Final Selection', description: 'Selected highest scoring educational recommendation', status: 'complete', detail: 'DSA Interview Patterns for Software Engineers' },
  ];

  const evidenceList = latestAnalysis?.interest_evidence || [
    'High watch completion (>88%) across programming and technical content',
    'Repeated save & like interactions on software engineering lifestyle & interview Reels',
    'Skipped non-technical general entertainment Reels',
    'Cross-Reel domain convergence indicates broader Software Engineering focus',
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>
          Why Did the AI Recommend This?
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Transparent explainability breakdown showing every stage of the AI recommendation pipeline.
        </p>
      </div>

      {/* Pipeline Stage Visualization */}
      <div className="card">
        <h3 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          ⚙️ Multi-Stage AI Recommendation Pipeline
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {stages.map((stage, idx) => (
            <div key={idx}>
              <div className="pipeline-stage active">
                <div
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: '50%',
                    background: 'var(--gradient-primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 700,
                    fontSize: '0.875rem',
                    flexShrink: 0,
                  }}
                >
                  {idx + 1}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                    <h4 style={{ fontSize: '1rem', fontWeight: 600 }}>{stage.stage}</h4>
                    <span className="badge badge-green">Executed</span>
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
                    {stage.description}
                  </p>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    🔍 {stage.detail}
                  </div>
                </div>
              </div>
              {idx < stages.length - 1 && <div className="pipeline-connector" />}
            </div>
          ))}
        </div>
      </div>

      {/* Evidence Cards */}
      <div className="card">
        <h3 style={{ fontSize: '1.25rem', marginBottom: '1.25rem' }}>
          Evidence & Signal Validation
        </h3>

        <div className="grid-2">
          {evidenceList.map((item, i) => (
            <div
              key={i}
              style={{
                background: 'rgba(0,0,0,0.2)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                padding: '1.25rem',
                display: 'flex',
                gap: '0.75rem',
              }}
            >
              <span style={{ fontSize: '1.25rem' }}>🛡️</span>
              <div>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-blue)', textTransform: 'uppercase', marginBottom: '0.25rem' }}>
                  Signal Factor #{i + 1}
                </div>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-primary)', lineHeight: 1.5 }}>
                  {item}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quality & Hype Defense Explanation */}
      <div
        style={{
          background: 'rgba(168,85,247,0.06)',
          border: '1px solid rgba(168,85,247,0.25)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.5rem',
        }}
      >
        <h3 style={{ fontSize: '1.125rem', color: 'var(--accent-purple)', marginBottom: '0.75rem' }}>
          🛡️ Hype Content Rejection Logic
        </h3>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          The AI engine continuously scans candidate content against 20+ clickbait and exaggerated claim patterns (e.g. "Get a job in 7 days", "10 AI tools guaranteed to get you hired"). High quality educational content (such as deep architectural guides and system design fundamentals) is prioritized over shallow hype.
        </p>
      </div>
    </div>
  );
}
