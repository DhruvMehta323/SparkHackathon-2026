// src/services/collabService.js
// Collaboration API calls

import apiClient from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export const collabService = {
  // Create collaboration request
  createRequest: async (requestData) => {
    try {
      const response = await apiClient.post(
        API_ENDPOINTS.COLLAB.CREATE_REQUEST,
        requestData
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get matches for a request
  getMatches: async (requestId) => {
    try {
      const response = await apiClient.get(
        API_ENDPOINTS.COLLAB.GET_MATCHES(requestId)
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Accept a match
  acceptMatch: async (requestId, matchId) => {
    try {
      const response = await apiClient.post(
        API_ENDPOINTS.COLLAB.ACCEPT_MATCH(requestId, matchId)
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};