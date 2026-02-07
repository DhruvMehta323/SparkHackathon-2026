// src/services/engagementService.js
// Engagement API calls (likes, comments)

import apiClient from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export const engagementService = {
  // Like a project
  likeProject: async (projectId, creatorId) => {
    try {
      const response = await apiClient.post(API_ENDPOINTS.ENGAGEMENTS.CREATE, {
        project_id: projectId,
        creator_id: creatorId,
        reaction: 'like',
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Comment on project
  commentOnProject: async (projectId, creatorId, comment) => {
    try {
      const response = await apiClient.post(API_ENDPOINTS.ENGAGEMENTS.CREATE, {
        project_id: projectId,
        creator_id: creatorId,
        reaction: 'comment',
        comment_text: comment,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get engagements for a project
  getProjectEngagements: async (projectId) => {
    try {
      const response = await apiClient.get(
        API_ENDPOINTS.ENGAGEMENTS.LIST(projectId)
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};