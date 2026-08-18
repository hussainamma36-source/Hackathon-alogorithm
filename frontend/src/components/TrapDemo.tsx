import { useStore } from '../store/useStore';

export function TrapDemo() {
  const { latestAnalysis } = useStore();

  const shallowRec = latestAnalysis?.shallow_recommendation || 'Another Java Programming Meme';
  const shallowReason = latestAnalysis?.shallow_reason || 'Matched keyword: "Java" from most watched reel';
  const aiInterest = latestAnalysis?.interest_detected || 'Software Engineering / Technology';
  const aiRec = latestAnalysis?.recommended_reel || 'DSA Interview Patterns for Software Engineers';
  const aiReason = latestAnalysis?.recommendation_reason ||
    'Inferred broader software engineering interest from cross-content interaction patterns — expanding beyond surface keyword.';

  return (
    <div
      style={{
        background: 'linear-gradient(135deg, #0d1424 0%, #0a1020 100%)',
        border: '1px solid rgba(99,130,255,0.2)',
        borderRadius: 'var(--radius-xl)',
        padding: '2rem',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Background decoration */}
      <div
        style={{
          position: 'absolute',
          top: -40,
          right: -40,
          width: 200,
          height: 200,
          background: 'radial-gradient(circle, rgba(99,130,255,0.08) 0%, transparent 70%)',
          pointerEvents: 'none',
        }}
      />

      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.375rem 1rem',
            background: 'rgba(168,85,247,0.12)',
            border: '1px solid rgba(168,85,247,0.25)',
            borderRadius: '100px',
            marginBottom: '1rem',
          }}
        >
          <span>⚡</span>
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-purple)' }}>
            TRAP DEMONSTRATION
          </span>
        </div>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
          Why Context Beats Keywords
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', maxWidth: 500, margin: '0 auto' }}>
          The same interaction history produces completely different recommendations depending on the engine.
        </p>
      </div>

      {/* Shared input */}
      <div
        style={{
          background: 'rgba(255,255,255,0.03)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          padding: '1rem 1.5rem',
          marginBottom: '1.5rem',
        }}
      >
        <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          📥 Input: Interaction History
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {[
            { label: '☕ Java meme', color: 'var(--accent-amber)', bg: 'rgba(245,158,11,0.1)' },
            { label: '💻 SE lifestyle', color: 'var(--accent-blue)', bg: 'rgba(99,130,255,0.1)' },
            { label: '😅 Interview joke', color: 'var(--accent-cyan)', bg: 'rgba(34,211,238,0.1)' },
            { label: '🖥️ Laptop comparison', color: 'var(--accent-purple)', bg: 'rgba(168,85,247,0.1)' },
          ].map((tag) => (
            <span
              key={tag.label}
              style={{
                padding: '0.375rem 0.875rem',
                background: tag.bg,
                border: `1px solid ${tag.color}33`,
                borderRadius: '100px',
                fontSize: '0.8125rem',
                color: tag.color,
                fontWeight: 500,
              }}
            >
              {tag.label}
            </span>
          ))}
        </div>
      </div>

      {/* Side-by-side comparison */}
      <div className="comparison-grid">
        {/* Left: Shallow */}
        <div
          style={{
            background: 'rgba(239,68,68,0.05)',
            border: '1px solid rgba(239,68,68,0.2)',
            borderRadius: 'var(--radius-lg)',
            padding: '1.5rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: 'var(--radius-sm)',
                background: 'rgba(239,68,68,0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1rem',
              }}
            >
              🔑
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-red)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                Shallow Keyword Engine
              </div>
            </div>
          </div>

          <div
            style={{
              background: 'rgba(239,68,68,0.08)',
              borderRadius: 'var(--radius-sm)',
              padding: '0.75rem',
              marginBottom: '1rem',
            }}
          >
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>LOGIC</div>
            <code style={{ fontSize: '0.8125rem', color: 'var(--accent-red)' }}>
              if "Java" in text:<br />
              &nbsp;&nbsp;recommend Java
            </code>
          </div>

          <div style={{ marginBottom: '0.75rem' }}>
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', marginBottom: '0.375rem', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              Detected Interest
            </div>
            <span className="badge badge-red">Java</span>
          </div>

          <div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', marginBottom: '0.375rem', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              Recommended
            </div>
            <div
              style={{
                background: 'rgba(239,68,68,0.1)',
                border: '1px solid rgba(239,68,68,0.2)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.75rem',
              }}
            >
              <div style={{ fontWeight: 600, marginBottom: '0.25rem', fontSize: '0.9rem' }}>
                ❌ {shallowRec}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                {shallowReason}
              </div>
            </div>
          </div>
        </div>

        {/* VS divider */}
        <div className="comparison-vs">VS</div>

        {/* Right: AI */}
        <div
          style={{
            background: 'rgba(16,185,129,0.05)',
            border: '1px solid rgba(16,185,129,0.25)',
            borderRadius: 'var(--radius-lg)',
            padding: '1.5rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: 'var(--radius-sm)',
                background: 'rgba(16,185,129,0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1rem',
              }}
            >
              🧠
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-green)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                ReelMind AI Agent
              </div>
            </div>
          </div>

          <div
            style={{
              background: 'rgba(16,185,129,0.08)',
              borderRadius: 'var(--radius-sm)',
              padding: '0.75rem',
              marginBottom: '1rem',
            }}
          >
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', marginBottom: '0.375rem' }}>PIPELINE</div>
            <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.8 }}>
              Interaction signals → Content understanding → Domain expansion → Interest inference → Quality filter
            </div>
          </div>

          <div style={{ marginBottom: '0.75rem' }}>
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', marginBottom: '0.375rem', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              Detected Interest
            </div>
            <span className="badge badge-green">{aiInterest}</span>
          </div>

          <div>
            <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)', marginBottom: '0.375rem', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
              Recommended
            </div>
            <div
              style={{
                background: 'rgba(16,185,129,0.1)',
                border: '1px solid rgba(16,185,129,0.25)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.75rem',
              }}
            >
              <div style={{ fontWeight: 600, marginBottom: '0.375rem', fontSize: '0.9rem' }}>
                ✅ {aiRec}
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                {aiReason.length > 180 ? aiReason.substring(0, 180) + '...' : aiReason}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom insight */}
      <div
        style={{
          marginTop: '1.5rem',
          padding: '1rem 1.5rem',
          background: 'rgba(99,130,255,0.06)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center',
        }}
      >
        <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          💡{' '}
          <strong style={{ color: 'var(--text-primary)' }}>Core Innovation:</strong>{' '}
          "We don't recommend what you watched. We infer{' '}
          <em style={{ color: 'var(--accent-blue)' }}>why</em> you engaged with it."
        </span>
      </div>
    </div>
  );
}
