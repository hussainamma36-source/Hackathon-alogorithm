import { useState } from 'react';
import { useStore } from '../store/useStore';
import { useNavigate } from 'react-router-dom';

export function Recommendation() {
  const { latestAnalysis, runAnalysis, submitFeedback } = useStore();
  const navigate = useNavigate();
  const [feedbackSubmitted, setFeedbackSubmitted] = useState<string | null>(null);

  const currentReel = latestAnalysis?.current_reel || 'Java Programming Meme / Software Engineer Lifestyle';
  const interestDetected = latestAnalysis?.interest_detected || 'Software Engineering / Technology';
  const recommendedTitle = latestAnalysis?.recommended_reel || 'DSA Interview Patterns for Software Engineers';
  const recommendedDesc = latestAnalysis?.recommended_description || 'Master the 15 most critical data structures and algorithm patterns asked in FAANG interviews with real examples.';
  const category = latestAnalysis?.category || 'DSA';
  const difficulty = latestAnalysis?.difficulty || 'Intermediate';
  const confidence = latestAnalysis?.confidence || 'High';
  const relevanceScore = latestAnalysis?.relevance_score || 0.92;
  const reason = latestAnalysis?.recommendation_reason ||
    'Across analyzed Reels, the AI detected strong engagement with programming and developer career content. Instead of recommending another Java meme, the agent expanded the interest profile and selected this DSA Reel because it directly connects your programming interest with actionable, career-advancing interview preparation.';
  const recId = latestAnalysis?.recommendation_id;
  const alternatives = latestAnalysis?.alternative_recommendations || [];

  const handleFeedback = (rating: 'useful' | 'not_useful', reasonText?: string) => {
    if (recId) {
      submitFeedback(recId, rating, reasonText);
    }
    setFeedbackSubmitted(rating);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>
            AI Recommendation Result
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Context-aware recommendation built from your inferred technology interest.
          </p>
        </div>

        <button className="btn btn-secondary" onClick={runAnalysis}>
          🔄 Re-Analyze
        </button>
      </div>

      {/* Main Required Conceptual Flow Display */}
      <div
        className="recommendation-card glow-blue"
        style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}
      >
        {/* Flow Visualizer */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'rgba(0,0,0,0.3)',
            padding: '1.25rem 1.5rem',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-subtle)',
            flexWrap: 'wrap',
            gap: '1rem',
          }}
        >
          {/* Current Reel */}
          <div style={{ flex: 1, minWidth: 160 }}>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
              CURRENT REEL
            </div>
            <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-primary)' }}>
              {currentReel}
            </div>
          </div>

          <div style={{ fontSize: '1.25rem', color: 'var(--accent-blue)' }}>➔</div>

          {/* Interest Detected */}
          <div style={{ flex: 1, minWidth: 160 }}>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
              INTEREST DETECTED
            </div>
            <span className="badge badge-purple" style={{ fontSize: '0.875rem' }}>
              {interestDetected}
            </span>
          </div>

          <div style={{ fontSize: '1.25rem', color: 'var(--accent-purple)' }}>➔</div>

          {/* Recommended Reel */}
          <div style={{ flex: 1, minWidth: 160 }}>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
              RECOMMENDED TECH REEL
            </div>
            <div style={{ fontWeight: 700, fontSize: '0.95rem', color: 'var(--accent-cyan)' }}>
              {recommendedTitle}
            </div>
          </div>
        </div>

        {/* Hero Recommended Content Card */}
        <div
          style={{
            background: 'rgba(99,130,255,0.06)',
            border: '1px solid var(--border-active)',
            borderRadius: 'var(--radius-lg)',
            padding: '1.75rem',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <span className="badge badge-blue">{category}</span>
                <span className="badge badge-purple">Difficulty: {difficulty}</span>
                <span className="badge badge-green">Confidence: {confidence}</span>
              </div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>{recommendedTitle}</h2>
            </div>

            <div style={{ textAlign: 'right', background: 'rgba(0,0,0,0.3)', padding: '0.75rem 1.25rem', borderRadius: 'var(--radius-md)' }}>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Relevance Score</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-green)' }}>
                {Math.round(relevanceScore * 100)}%
              </div>
            </div>
          </div>

          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '1.5rem' }}>
            {recommendedDesc}
          </p>

          {/* Why This Recommendation */}
          <div
            style={{
              background: 'rgba(0,0,0,0.3)',
              border: '1px solid rgba(99,130,255,0.2)',
              borderRadius: 'var(--radius-md)',
              padding: '1.25rem',
            }}
          >
            <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.5rem' }}>
              🧠 WHY THIS RECOMMENDATION?
            </div>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.7 }}>
              {reason}
            </p>
          </div>
        </div>

        {/* Feedback Section */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'rgba(0,0,0,0.2)',
            padding: '1rem 1.5rem',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-subtle)',
            flexWrap: 'wrap',
            gap: '1rem',
          }}
        >
          <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            Was this recommendation useful?
          </span>

          {feedbackSubmitted ? (
            <span className="badge badge-green" style={{ fontSize: '0.8125rem' }}>
              ✓ Feedback saved ({feedbackSubmitted})
            </span>
          ) : (
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button className="btn btn-secondary btn-sm" onClick={() => handleFeedback('useful')}>
                👍 Useful
              </button>
              <button className="btn btn-ghost btn-sm" onClick={() => handleFeedback('not_useful', 'too_basic')}>
                👎 Too basic
              </button>
              <button className="btn btn-ghost btn-sm" onClick={() => handleFeedback('not_useful', 'not_relevant')}>
                👎 Not relevant
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Alternative Recommendations */}
      {alternatives.length > 0 && (
        <div className="card">
          <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem' }}>
            Alternative Tech Recommendations Considered
          </h3>
          <div className="grid-3">
            {alternatives.map((alt, i) => (
              <div
                key={i}
                style={{
                  background: 'rgba(0,0,0,0.2)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '1rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span className="badge badge-blue">{alt.category}</span>
                  <span style={{ fontSize: '0.75rem', color: 'var(--accent-green)', fontWeight: 600 }}>
                    {Math.round(alt.relevance_score * 100)}%
                  </span>
                </div>
                <h4 style={{ fontSize: '0.9rem', marginBottom: '0.375rem' }}>{alt.title}</h4>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{alt.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ textAlign: 'center' }}>
        <button className="btn btn-ghost" onClick={() => navigate('/explainability')}>
          🔍 View Full Explainability Pipeline →
        </button>
      </div>
    </div>
  );
}
