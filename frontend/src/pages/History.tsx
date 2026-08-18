import { useEffect } from 'react';
import { useStore } from '../store/useStore';

export function History() {
  const { history, loadHistory } = useStore();

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>
          Recommendation History & Audit Log
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Review previous AI recommendations, detected interests, and confidence levels.
        </p>
      </div>

      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        {history.length === 0 ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            No recommendation history available yet. Run an analysis on the Dashboard or Feed!
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Date / Time</th>
                <th>Inferred Interest</th>
                <th>Recommended Tech Content</th>
                <th>Category</th>
                <th>Confidence</th>
                <th>Relevance Score</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id}>
                  <td style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                    {new Date(item.created_at).toLocaleString()}
                  </td>
                  <td>
                    <span className="badge badge-purple">{item.interest_detected}</span>
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                    {item.recommended_title}
                  </td>
                  <td>
                    <span className="badge badge-blue">{item.category}</span>
                  </td>
                  <td>
                    <span className="badge badge-green">{item.confidence}</span>
                  </td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-cyan)' }}>
                    {Math.round(item.relevance_score * 100)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
