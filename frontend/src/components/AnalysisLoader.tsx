import { useEffect, useRef } from 'react';
import { useStore } from '../store/useStore';
import { useNavigate } from 'react-router-dom';

const STAGES = [
  { label: 'Analyzing viewing behavior...', icon: '👁️' },
  { label: 'Understanding Reel context...', icon: '🎬' },
  { label: 'Inferring broader interests...', icon: '🔍' },
  { label: 'Finding relevant technology content...', icon: '💡' },
  { label: 'Checking content quality...', icon: '🛡️' },
  { label: 'Generating recommendation...', icon: '🎯' },
  { label: 'Building explanation...', icon: '🧠' },
];

export function AnalysisLoader() {
  const { isAnalyzing, analyzeStage, analyzeProgress } = useStore();
  const navigate = useNavigate();
  const prevAnalyzing = useRef(false);

  useEffect(() => {
    if (prevAnalyzing.current && !isAnalyzing) {
      // Analysis just completed → navigate to recommendation
      navigate('/recommendation');
    }
    prevAnalyzing.current = isAnalyzing;
  }, [isAnalyzing, navigate]);

  if (!isAnalyzing) return null;

  const currentStageIndex = STAGES.findIndex((s) => s.label === analyzeStage);

  return (
    <div className="analysis-overlay animate-fadeIn">
      <div className="analysis-modal animate-fadeInUp">
        {/* Animated logo */}
        <div
          style={{
            width: 80,
            height: 80,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, rgba(99,130,255,0.2), rgba(168,85,247,0.2))',
            border: '2px solid rgba(99,130,255,0.4)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '2rem',
            margin: '0 auto 1.5rem',
            animation: 'pulse-glow 2s ease-in-out infinite',
          }}
        >
          🧠
        </div>

        <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
          AI Analysis Running
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '2rem' }}>
          The multi-stage recommendation pipeline is processing your interactions
        </p>

        {/* Progress bar */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginBottom: '0.5rem',
              fontSize: '0.8125rem',
              color: 'var(--text-secondary)',
            }}
          >
            <span style={{ color: 'var(--accent-blue)', fontWeight: 600 }}>{analyzeStage}</span>
            <span>{analyzeProgress}%</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${analyzeProgress}%` }} />
          </div>
        </div>

        {/* Stage list */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', textAlign: 'left' }}>
          {STAGES.map((stage, i) => {
            const isComplete = i < currentStageIndex;
            const isCurrent = i === currentStageIndex;
            return (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  padding: '0.5rem 0.75rem',
                  borderRadius: 'var(--radius-sm)',
                  background: isCurrent
                    ? 'rgba(99,130,255,0.08)'
                    : isComplete
                    ? 'rgba(16,185,129,0.05)'
                    : 'transparent',
                  border: isCurrent ? '1px solid rgba(99,130,255,0.2)' : '1px solid transparent',
                  transition: 'all 0.3s ease',
                  opacity: i > currentStageIndex + 1 ? 0.4 : 1,
                }}
              >
                <span style={{ fontSize: '1rem', width: 24 }}>
                  {isComplete ? '✅' : isCurrent ? stage.icon : '⏳'}
                </span>
                <span
                  style={{
                    fontSize: '0.8125rem',
                    color: isCurrent
                      ? 'var(--accent-blue)'
                      : isComplete
                      ? 'var(--accent-green)'
                      : 'var(--text-muted)',
                    fontWeight: isCurrent ? 600 : 400,
                  }}
                >
                  {stage.label}
                </span>
                {isCurrent && (
                  <div className="spinner spinner-sm" style={{ marginLeft: 'auto' }} />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
