import { useStore } from '../store/useStore';
import type { Reel } from '../api/endpoints';

export function Feed() {
  const { reels, interactions, updateInteraction, syncInteraction, runAnalysis, loadDemoData } = useStore();

  const getReelEmoji = (id: string) => {
    const emojis: Record<string, string> = {
      reel_001: '🎒',
      reel_002: '☕',
      reel_003: '💼',
      reel_004: '😅',
      reel_005: '💻',
      reel_006: '🧠',
      reel_007: '🔒',
      reel_008: '☁️',
    };
    return emojis[id] || '🎬';
  };

  const handleToggle = (reelId: string, field: 'liked' | 'saved' | 'shared' | 'replayed' | 'skipped' | 'commented' | 'clicked_creator') => {
    const current = interactions[reelId] || {
      watched_percentage: 0,
      watch_time: 0,
      liked: false,
      saved: false,
      shared: false,
      replayed: false,
      skipped: false,
      commented: false,
      clicked_creator: false,
    };

    const updatedValue = !current[field];
    const updates: any = { [field]: updatedValue };

    if (field === 'liked' && updatedValue && current.watched_percentage < 80) {
      updates.watched_percentage = 90;
    }
    if (field === 'saved' && updatedValue && current.watched_percentage < 80) {
      updates.watched_percentage = 92;
    }
    if (field === 'replayed' && updatedValue && current.watched_percentage < 80) {
      updates.watched_percentage = 95;
    }

    updateInteraction(reelId, updates);
    syncInteraction(reelId);
  };

  const handleWatchChange = (reelId: string, percentage: number) => {
    updateInteraction(reelId, { watched_percentage: percentage });
    syncInteraction(reelId);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', marginBottom: '0.25rem' }}>
            Reel Interaction Feed
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Simulate realistic student interaction signals on sample Reels to feed the recommendation engine.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button className="btn btn-ghost btn-sm" onClick={loadDemoData}>
            ⚡ Preset Trap Scenario Data
          </button>
          <button className="btn btn-primary" onClick={runAnalysis}>
            🔍 Analyze My Interactions
          </button>
        </div>
      </div>

      {/* Grid of Reels */}
      <div className="grid-4">
        {reels.map((reel: Reel) => {
          const interaction = interactions[reel.id] || {
            watched_percentage: 0,
            watch_time: 0,
            liked: false,
            saved: false,
            shared: false,
            replayed: false,
            skipped: false,
            commented: false,
            clicked_creator: false,
          };

          return (
            <div key={reel.id} className={`reel-card${interaction.watched_percentage > 50 ? ' active' : ''}`}>
              {/* Thumbnail */}
              <div
                className="reel-thumbnail"
                style={{
                  background: 'linear-gradient(135deg, rgba(99,130,255,0.15), rgba(168,85,247,0.15))',
                }}
              >
                <span>{getReelEmoji(reel.id)}</span>
                <span
                  style={{
                    position: 'absolute',
                    top: 10,
                    right: 10,
                    background: 'rgba(0,0,0,0.6)',
                    backdropFilter: 'blur(8px)',
                    padding: '0.2rem 0.5rem',
                    borderRadius: 4,
                    fontSize: '0.7rem',
                    fontWeight: 600,
                  }}
                >
                  {reel.duration}s
                </span>
                <span
                  style={{
                    position: 'absolute',
                    bottom: 10,
                    left: 10,
                    background: 'rgba(0,0,0,0.6)',
                    backdropFilter: 'blur(8px)',
                    padding: '0.2rem 0.5rem',
                    borderRadius: 4,
                    fontSize: '0.7rem',
                    color: 'var(--accent-cyan)',
                  }}
                >
                  {reel.category}
                </span>
              </div>

              {/* Body */}
              <div className="reel-body">
                <div className="reel-meta">
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>@{reel.creator}</span>
                  <span className="badge badge-purple">{reel.technical_level}</span>
                </div>

                <h3 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: '0.5rem', lineHeight: 1.3 }}>
                  {reel.title}
                </h3>
                <p style={{ fontSize: '0.78125rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.4 }}>
                  {reel.description.length > 90 ? reel.description.substring(0, 90) + '...' : reel.description}
                </p>

                {/* Watch Slider */}
                <div style={{ marginBottom: '1rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>
                    <span>Watch Progress</span>
                    <span style={{ color: 'var(--accent-blue)', fontWeight: 600 }}>{interaction.watched_percentage}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={interaction.watched_percentage}
                    onChange={(e) => handleWatchChange(reel.id, Number(e.target.value))}
                    style={{ width: '100%', accentColor: '#6382ff', cursor: 'pointer' }}
                  />
                </div>

                {/* Technical/Edu Indicators */}
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.5rem' }}>
                  <span style={{ fontSize: '0.6875rem', color: 'var(--text-muted)' }}>
                    Edu: <strong style={{ color: 'var(--text-primary)' }}>{Math.round(reel.educational_value * 100)}%</strong>
                  </span>
                  <span style={{ fontSize: '0.6875rem', color: 'var(--text-muted)' }}>
                    Tech Rel: <strong style={{ color: 'var(--text-primary)' }}>{Math.round(reel.technical_relevance * 100)}%</strong>
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="reel-actions" style={{ flexWrap: 'wrap' }}>
                <button
                  className={`action-btn${interaction.liked ? ' liked' : ''}`}
                  onClick={() => handleToggle(reel.id, 'liked')}
                >
                  ❤️ {interaction.liked ? 'Liked' : 'Like'}
                </button>

                <button
                  className={`action-btn${interaction.saved ? ' saved' : ''}`}
                  onClick={() => handleToggle(reel.id, 'saved')}
                >
                  📌 {interaction.saved ? 'Saved' : 'Save'}
                </button>

                <button
                  className={`action-btn${interaction.replayed ? ' active' : ''}`}
                  onClick={() => handleToggle(reel.id, 'replayed')}
                >
                  🔄 Replay
                </button>

                <button
                  className={`action-btn${interaction.skipped ? ' skipped' : ''}`}
                  onClick={() => handleToggle(reel.id, 'skipped')}
                >
                  ⏭️ Skip
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
