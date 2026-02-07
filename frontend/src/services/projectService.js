// src/services/projectService.js
// Project API calls

import apiClient from './apiClient';
import { API_ENDPOINTS } from '../config/api';

export const projectService = {
  // Get all projects with filters
  getProjects: async (filters = {}) => {
    try {
      const params = new URLSearchParams();
      
      if (filters.genre) params.append('genre', filters.genre);
      if (filters.status) params.append('status', filters.status);
      if (filters.search) params.append('search', filters.search);
      if (filters.limit) params.append('limit', filters.limit);
      if (filters.offset) params.append('offset', filters.offset);
      if (filters.fair_discovery) params.append('fair_discovery', 'true');
      
      const response = await apiClient.get(
        `${API_ENDPOINTS.PROJECTS.LIST}?${params.toString()}`
      );
      
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get single project by ID
  getProjectById: async (projectId) => {
    try {
      const response = await apiClient.get(API_ENDPOINTS.PROJECTS.DETAIL(projectId));
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get similar projects
  getSimilarProjects: async (projectId) => {
    try {
      const response = await apiClient.get(API_ENDPOINTS.PROJECTS.SIMILAR(projectId));
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Create new project
  createProject: async (projectData) => {
    try {
      const response = await apiClient.post(API_ENDPOINTS.PROJECTS.CREATE, projectData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Update project
  updateProject: async (projectId, updates) => {
    try {
      const response = await apiClient.put(
        API_ENDPOINTS.PROJECTS.UPDATE(projectId),
        updates
      );
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Delete project
  deleteProject: async (projectId) => {
    try {
      const response = await apiClient.delete(API_ENDPOINTS.PROJECTS.DELETE(projectId));
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};