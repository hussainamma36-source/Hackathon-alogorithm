import { useStore } from '../store/useStore';

export function Settings() {
  const { aiProvider, healthStatus, checkHealth } = useStore();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>
          AI Configuration & Settings
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Inspect active recommendation providers, database connections, and environment parameters.
        </p>
      </div>

      <div className="card">
        <h3 style={{ fontSize: '1.25rem', marginBottom: '1.25rem' }}>
          Active Provider Status
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '1rem',
              background: 'rgba(0,0,0,0.2)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>Recommendation Engine</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                {aiProvider === 'local_semantic_engine'
                  ? 'Local Multi-Stage Semantic Engine (No external API needed)'
                  : `Configured External Provider: ${aiProvider}`}
              </div>
            </div>

            <span className={`badge ${healthStatus === 'ok' ? 'badge-green' : 'badge-red'}`}>
              {healthStatus === 'ok' ? 'Active' : 'Offline'}
            </span>
          </div>

          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '1rem',
              background: 'rgba(0,0,0,0.2)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div>
              <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>External LLM Key (AI_API_KEY)</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Optional environment variable. System automatically uses local fallback when absent.
              </div>
            </div>

            <span className="badge badge-purple">
              {import.meta.env.VITE_AI_API_KEY ? 'Configured' : 'Local Fallback Active'}
            </span>
          </div>
        </div>

        <div style={{ marginTop: '1.5rem' }}>
          <button className="btn btn-secondary" onClick={checkHealth}>
            🔄 Refresh System Status
          </button>
        </div>
      </div>

      <div className="card">
        <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>
          Environment Parameters
        </h3>
        <div style={{ background: 'rgba(0,0,0,0.4)', padding: '1rem', borderRadius: 'var(--radius-md)', fontFamily: 'monospace', fontSize: '0.8125rem' }}>
          <div>VITE_API_BASE_URL: {import.meta.env.VITE_API_BASE_URL || 'Auto-Resolved'}</div>
          <div>MODE: {import.meta.env.MODE}</div>
          <div>DEV: {import.meta.env.DEV ? 'true' : 'false'}</div>
        </div>

      </div>
    </div>
  );
}
