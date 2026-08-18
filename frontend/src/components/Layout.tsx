import { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { AnalysisLoader } from './AnalysisLoader';
import { useStore } from '../store/useStore';

export function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { error, clearError, checkHealth, loadReels, loadInteractions } = useStore();

  useEffect(() => {
    checkHealth();
    loadReels();
    loadInteractions();
  }, []);

  return (
    <div className="layout">
      {/* Background Orbs */}
      <div className="bg-orb bg-orb-1" />
      <div className="bg-orb bg-orb-2" />

      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content */}
      <div className="main-content">
        {/* Top Navbar / Mobile header */}
        <header className="page-header">
          <button
            className="btn btn-ghost btn-sm"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            style={{ display: 'none' }}
          >
            ☰
          </button>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              ReelMind AI Agent v1.0
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => useStore.getState().loadDemoData()}
            >
              🚀 Load Hackathon Demo Data
            </button>
          </div>
        </header>

        {/* Global Error Banner */}
        {error && (
          <div style={{ padding: '1rem 2rem 0' }}>
            <div className="error-banner">
              <span>⚠️ {error}</span>
              <button
                className="btn btn-ghost btn-sm"
                onClick={clearError}
                style={{ marginLeft: 'auto', padding: '0.2rem 0.5rem' }}
              >
                ✕
              </button>
            </div>
          </div>
        )}

        {/* Page Content */}
        <main className="page-content">
          <Outlet />
        </main>
      </div>

      {/* Analysis Overlay Loader */}
      <AnalysisLoader />
    </div>
  );
}
