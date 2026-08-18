import { create } from 'zustand';
import { api } from '../api/endpoints';
import type { Reel, AnalyzeResponse, InterestProfile, RecommendationHistory } from '../api/endpoints';

interface InteractionState {
  [reelId: string]: {
    watched_percentage: number;
    watch_time: number;
    liked: boolean;
    saved: boolean;
    shared: boolean;
    replayed: boolean;
    skipped: boolean;
    commented: boolean;
    clicked_creator: boolean;
  };
}

interface AppStore {
  // Session
  sessionId: string;

  // Data
  reels: Reel[];
  interactions: InteractionState;
  latestAnalysis: AnalyzeResponse | null;
  interestProfile: InterestProfile | null;
  history: RecommendationHistory[];

  // UI state
  isAnalyzing: boolean;
  analyzeStage: string;
  analyzeProgress: number;
  error: string | null;
  isDemoMode: boolean;
  healthStatus: 'unknown' | 'ok' | 'error';
  aiProvider: string;

  // Actions
  setSessionId: (id: string) => void;
  loadReels: () => Promise<void>;
  loadInteractions: () => Promise<void>;
  updateInteraction: (reelId: string, updates: Partial<InteractionState[string]>) => void;
  syncInteraction: (reelId: string) => Promise<void>;
  runAnalysis: () => Promise<void>;
  loadDemoData: () => Promise<void>;
  loadHistory: () => Promise<void>;
  submitFeedback: (recommendationId: number, rating: string, reason?: string) => Promise<void>;
  checkHealth: () => Promise<void>;
  clearError: () => void;
}

const DEMO_INTERACTIONS: Record<string, Partial<InteractionState[string]>> = {
  reel_002: { watched_percentage: 95, watch_time: 21, liked: true, replayed: true },
  reel_003: { watched_percentage: 92, watch_time: 53, liked: true, saved: true, clicked_creator: true },
  reel_004: { watched_percentage: 88, watch_time: 31, liked: true, commented: true },
  reel_005: { watched_percentage: 90, watch_time: 66, saved: true },
  reel_001: { watched_percentage: 45, watch_time: 13, skipped: true },
};

const defaultInteraction = () => ({
  watched_percentage: 0,
  watch_time: 0,
  liked: false,
  saved: false,
  shared: false,
  replayed: false,
  skipped: false,
  commented: false,
  clicked_creator: false,
});

const ANALYSIS_STAGES = [
  'Analyzing viewing behavior...',
  'Understanding Reel context...',
  'Inferring broader interests...',
  'Finding relevant technology content...',
  'Checking content quality...',
  'Generating recommendation...',
  'Building explanation...',
];

export const useStore = create<AppStore>((set, get) => ({
  sessionId: 'default',
  reels: [],
  interactions: {},
  latestAnalysis: null,
  interestProfile: null,
  history: [],
  isAnalyzing: false,
  analyzeStage: '',
  analyzeProgress: 0,
  error: null,
  isDemoMode: false,
  healthStatus: 'unknown',
  aiProvider: 'local_semantic_engine',

  setSessionId: (id) => set({ sessionId: id }),

  clearError: () => set({ error: null }),

  checkHealth: async () => {
    try {
      const health = await api.health();
      set({ healthStatus: 'ok', aiProvider: health.ai_provider });
    } catch {
      set({ healthStatus: 'error' });
    }
  },

  loadReels: async () => {
    try {
      const reels = await api.getReels();
      set({ reels });
    } catch (err: any) {
      set({ error: err.message });
    }
  },

  loadInteractions: async () => {
    try {
      const { sessionId } = get();
      const serverInteractions = await api.getInteractions(sessionId);
      const state: InteractionState = {};
      for (const i of serverInteractions) {
        state[i.reel_id] = {
          watched_percentage: i.watched_percentage,
          watch_time: i.watch_time,
          liked: i.liked,
          saved: i.saved,
          shared: i.shared,
          replayed: i.replayed,
          skipped: i.skipped,
          commented: i.commented,
          clicked_creator: i.clicked_creator,
        };
      }
      set({ interactions: state });
    } catch {
      // non-fatal
    }
  },

  updateInteraction: (reelId, updates) => {
    const { interactions } = get();
    const current = interactions[reelId] || defaultInteraction();
    set({
      interactions: {
        ...interactions,
        [reelId]: { ...current, ...updates },
      },
    });
  },

  syncInteraction: async (reelId) => {
    const { interactions, sessionId } = get();
    const interaction = interactions[reelId];
    if (!interaction) return;
    try {
      await api.createInteraction({
        reel_id: reelId,
        session_id: sessionId,
        ...interaction,
      });
    } catch (err: any) {
      set({ error: err.message });
    }
  },

  loadDemoData: async () => {
    const { sessionId } = get();
    set({ isDemoMode: true, error: null });


    // Set demo interactions locally
    const interactionState: InteractionState = {};
    for (const [reelId, data] of Object.entries(DEMO_INTERACTIONS)) {
      interactionState[reelId] = { ...defaultInteraction(), ...data };
    }
    set({ interactions: interactionState });

    // Sync each to backend
    for (const [reelId, data] of Object.entries(DEMO_INTERACTIONS)) {
      try {
        await api.createInteraction({
          reel_id: reelId,
          session_id: sessionId,
          watched_percentage: data.watched_percentage ?? 0,
          watch_time: data.watch_time ?? 0,
          liked: data.liked ?? false,
          saved: data.saved ?? false,
          shared: data.shared ?? false,
          replayed: data.replayed ?? false,
          skipped: data.skipped ?? false,
          commented: data.commented ?? false,
          clicked_creator: data.clicked_creator ?? false,
        });
      } catch {
        // continue
      }
    }
  },

  runAnalysis: async () => {
    set({ isAnalyzing: true, error: null, analyzeProgress: 0 });

    // Animate through stages
    for (let i = 0; i < ANALYSIS_STAGES.length; i++) {
      set({
        analyzeStage: ANALYSIS_STAGES[i],
        analyzeProgress: Math.round(((i + 1) / ANALYSIS_STAGES.length) * 90),
      });
      await new Promise((r) => setTimeout(r, 600));
    }

    try {
      const { sessionId } = get();
      const result = await api.analyze(sessionId);
      set({
        latestAnalysis: result,
        analyzeProgress: 100,
        analyzeStage: 'Complete!',
      });

      // Also refresh interest profile and history
      try {
        const profile = await api.getInterests(sessionId);
        set({ interestProfile: profile });
      } catch {
        // non-fatal
      }

      setTimeout(() => {
        set({ isAnalyzing: false, analyzeStage: '', analyzeProgress: 0 });
      }, 800);
    } catch (err: any) {
      set({ error: err.message, isAnalyzing: false, analyzeStage: '', analyzeProgress: 0 });
    }
  },

  loadHistory: async () => {
    try {
      const { sessionId } = get();
      const history = await api.getHistory(sessionId);
      set({ history });
    } catch {
      // non-fatal
    }
  },

  submitFeedback: async (recommendationId, rating, reason) => {
    try {
      const { sessionId } = get();
      await api.submitFeedback(recommendationId, rating, reason, sessionId);
    } catch (err: any) {
      set({ error: err.message });
    }
  },
}));
