import apiClient from './client';

// ── Types ──────────────────────────────────────────────────────────────────────

export interface Reel {
  id: string;
  title: string;
  description: string;
  transcript: string;
  category: string;
  creator: string;
  duration: number;
  hashtags: string;
  technical_level: string;
  educational_value: number;
  engagement_score: number;
  topic: string;
  subtopic?: string;
  intent: string;
  technical_relevance: number;
  career_relevance: number;
  hype_score: number;
  broader_domain: string;
  related_technologies: string;
  thumbnail_url?: string;
  created_at: string;
}

export interface Interaction {
  id: number;
  reel_id: string;
  session_id: string;
  watched_percentage: number;
  watch_time: number;
  liked: boolean;
  saved: boolean;
  shared: boolean;
  replayed: boolean;
  skipped: boolean;
  commented: boolean;
  clicked_creator: boolean;
  interaction_timestamp: string;
}

export interface InteractionCreate {
  reel_id: string;
  session_id: string;
  watched_percentage: number;
  watch_time: number;
  liked: boolean;
  saved: boolean;
  shared: boolean;
  replayed: boolean;
  skipped: boolean;
  commented: boolean;
  clicked_creator: boolean;
}

export interface AlternativeRecommendation {
  title: string;
  category: string;
  difficulty: string;
  relevance_score: number;
  reason: string;
}

export interface PipelineStage {
  stage: string;
  description: string;
  status: string;
  detail: string;
}

export interface AnalyzeResponse {
  current_reel?: string;
  interest_detected: string;
  interest_evidence: string[];
  recommended_reel: string;
  recommended_description: string;
  category: string;
  recommendation_reason: string;
  difficulty: string;
  confidence: string;
  confidence_score: number;
  relevance_score: number;
  hype_score: number;
  quality_score: number;
  alternative_recommendations: AlternativeRecommendation[];
  interest_scores: Record<string, number>;
  shallow_recommendation: string;
  shallow_reason: string;
  recommendation_id: number;
  pipeline_stages: PipelineStage[];
}

export interface InterestProfile {
  session_id: string;
  primary_interest: string;
  secondary_interests: string[];
  interest_scores: Record<string, number>;
  confidence: string;
  confidence_score: number;
  reels_analyzed: number;
  created_at: string;
}

export interface RecommendationHistory {
  id: number;
  session_id: string;
  recommended_title: string;
  category: string;
  difficulty: string;
  confidence: string;
  confidence_score: number;
  relevance_score: number;
  interest_detected: string;
  recommendation_reason: string;
  created_at: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  ai_provider: string;
  database: string;
}

// ── API Functions ──────────────────────────────────────────────────────────────

export const api = {
  health: (): Promise<HealthResponse> =>
    apiClient.get('/api/health').then((r) => r.data),

  getReels: (): Promise<Reel[]> =>
    apiClient.get('/api/reels').then((r) => r.data),

  getReel: (id: string): Promise<Reel> =>
    apiClient.get(`/api/reels/${id}`).then((r) => r.data),

  getInteractions: (sessionId = 'default'): Promise<Interaction[]> =>
    apiClient.get('/api/interactions', { params: { session_id: sessionId } }).then((r) => r.data),

  createInteraction: (data: InteractionCreate): Promise<Interaction> =>
    apiClient.post('/api/interactions', data).then((r) => r.data),

  analyze: (sessionId = 'default'): Promise<AnalyzeResponse> =>
    apiClient.post('/api/analyze', { session_id: sessionId }).then((r) => r.data),

  getInterests: (sessionId = 'default'): Promise<InterestProfile> =>
    apiClient.get('/api/interests', { params: { session_id: sessionId } }).then((r) => r.data),

  getRecommendations: (sessionId = 'default'): Promise<RecommendationHistory[]> =>
    apiClient.get('/api/recommendations', { params: { session_id: sessionId } }).then((r) => r.data),

  getHistory: (sessionId = 'default'): Promise<RecommendationHistory[]> =>
    apiClient.get('/api/history', { params: { session_id: sessionId } }).then((r) => r.data),

  submitFeedback: (recommendationId: number, rating: string, reason?: string, sessionId = 'default') =>
    apiClient
      .post('/api/feedback', {
        recommendation_id: recommendationId,
        session_id: sessionId,
        rating,
        reason: reason || null,
      })
      .then((r) => r.data),
};
