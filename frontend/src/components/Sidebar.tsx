import { NavLink } from 'react-router-dom';
import { useStore } from '../store/useStore';

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊', exact: true },
  { path: '/feed', label: 'Reel Feed', icon: '🎬' },
  { path: '/analysis', label: 'Interest Analysis', icon: '🔍' },
  { path: '/recommendation', label: 'Recommendation', icon: '🎯' },
  { path: '/explainability', label: 'Explainability', icon: '🧠' },
  { path: '/history', label: 'History', icon: '📜' },
  { path: '/settings', label: 'Settings', icon: '⚙️' },
];

export function Sidebar({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const { healthStatus, aiProvider, interactions } = useStore();

  const interactionCount = Object.keys(interactions).length;
  const likedCount = Object.values(interactions).filter((i) => i.liked).length;

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          style={{
            position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)',
            zIndex: 49, display: 'none'
          }}
          onClick={onClose}
          className="mobile-overlay"
        />
      )}

      <aside className={`sidebar${isOpen ? ' open' : ''}`}>
        {/* Logo */}
        <div className="nav-logo">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <span style={{ fontSize: '1.5rem' }}>🧠</span>
            <span className="nav-logo-text">ReelMind AI</span>
          </div>
          <div className="nav-tagline">Turn your scrolling into smarter learning.</div>
        </div>

        {/* Navigation */}
        <div className="nav-section" style={{ flex: 1 }}>
          <div className="nav-section-label">Navigation</div>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.exact}
              className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
              onClick={onClose}
            >
              <span className="nav-item-icon">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </div>

        {/* Status section */}
        <div
          style={{
            padding: '1rem',
            borderTop: '1px solid var(--border-subtle)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.625rem',
          }}
        >
          {/* Interaction stats */}
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <div style={{ textAlign: 'center', flex: 1 }}>
              <div style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--accent-blue)' }}>
                {interactionCount}
              </div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)' }}>Reels</div>
            </div>
            <div style={{ textAlign: 'center', flex: 1 }}>
              <div style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--accent-pink)' }}>
                {likedCount}
              </div>
              <div style={{ fontSize: '0.6875rem', color: 'var(--text-muted)' }}>Liked</div>
            </div>
          </div>

          {/* AI Provider */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.5rem 0.75rem',
              background: 'rgba(99, 130, 255, 0.08)',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div
              style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: healthStatus === 'ok' ? 'var(--accent-green)' : 'var(--accent-red)',
                flexShrink: 0,
                boxShadow: healthStatus === 'ok' ? '0 0 6px var(--accent-green)' : 'none',
              }}
            />
            <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {aiProvider || 'local_semantic_engine'}
            </span>
          </div>
        </div>
      </aside>
    </>
  );
}
