// src/config/api.js
// API Configuration

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Auth endpoints
  AUTH: {
    LOGIN: `${API_BASE_URL}/api/auth/login`,
    REGISTER: `${API_BASE_URL}/api/auth/register`,
    LOGOUT: `${API_BASE_URL}/api/auth/logout`,
  },

  // Projects endpoints
  PROJECTS: {
    LIST: `${API_BASE_URL}/api/projects`,
    DETAIL: (id) => `${API_BASE_URL}/api/projects/${id}`,
    CREATE: `${API_BASE_URL}/api/projects`,
    UPDATE: (id) => `${API_BASE_URL}/api/projects/${id}`,
    DELETE: (id) => `${API_BASE_URL}/api/projects/${id}`,
    SIMILAR: (id) => `${API_BASE_URL}/api/projects/${id}/similar`,
  },

  // Engagements (likes/comments)
  ENGAGEMENTS: {
    CREATE: `${API_BASE_URL}/api/engagements`,
    LIST: (projectId) => `${API_BASE_URL}/api/engagements?project_id=${projectId}`,
  },

  // Creators endpoints
  CREATORS: {
    PROFILE: (id) => `${API_BASE_URL}/api/creators/${id}`,
    REWARDS: (id) => `${API_BASE_URL}/api/creators/${id}/rewards`,
    LEADERBOARD: `${API_BASE_URL}/api/fairrank/top`,
  },

  // Collaboration endpoints
  COLLAB: {
    CREATE_REQUEST: `${API_BASE_URL}/api/collab/requests`,
    GET_MATCHES: (id) => `${API_BASE_URL}/api/collab/requests/${id}/matches`,
    ACCEPT_MATCH: (requestId, matchId) => 
      `${API_BASE_URL}/api/collab/requests/${requestId}/matches/${matchId}/accept`,
  },

  // Engine endpoints (admin)
  ENGINES: {
    FAIRRANK: `${API_BASE_URL}/api/engines/fairrank`,
    SIMILARITY: `${API_BASE_URL}/api/engines/similarity`,
  },

  // Health check
  HEALTH: `${API_BASE_URL}/api/health`,
};

export default API_BASE_URL;