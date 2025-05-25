import apiClient from './api';

const optimizationService = {
  /**
   * Get all optimization jobs
   * @returns {Promise} Promise object represents the optimization jobs
   */
  getAllOptimizationJobs: async () => {
    try {
      const response = await apiClient.get('/optimizations');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get a specific optimization job by ID
   * @param {string} id - Optimization job ID
   * @returns {Promise} Promise object represents the optimization job
   */
  getOptimizationJobById: async (id) => {
    try {
      const response = await apiClient.get(`/optimizations/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Create a new optimization job
   * @param {Object} optimizationData - Optimization configuration data
   * @returns {Promise} Promise object represents the created optimization job
   */
  createOptimizationJob: async (optimizationData) => {
    try {
      const response = await apiClient.post('/optimizations', optimizationData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Update an existing optimization job
   * @param {string} id - Optimization job ID
   * @param {Object} optimizationData - Optimization configuration data
   * @returns {Promise} Promise object represents the updated optimization job
   */
  updateOptimizationJob: async (id, optimizationData) => {
    try {
      const response = await apiClient.put(`/optimizations/${id}`, optimizationData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Delete an optimization job
   * @param {string} id - Optimization job ID
   * @returns {Promise} Promise object represents the operation result
   */
  deleteOptimizationJob: async (id) => {
    try {
      const response = await apiClient.delete(`/optimizations/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Start an optimization job
   * @param {string} id - Optimization job ID
   * @returns {Promise} Promise object represents the started optimization job
   */
  startOptimizationJob: async (id) => {
    try {
      const response = await apiClient.post(`/optimizations/${id}/start`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Stop an optimization job
   * @param {string} id - Optimization job ID
   * @returns {Promise} Promise object represents the operation result
   */
  stopOptimizationJob: async (id) => {
    try {
      const response = await apiClient.post(`/optimizations/${id}/stop`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get optimization job results
   * @param {string} id - Optimization job ID
   * @returns {Promise} Promise object represents the optimization results
   */
  getOptimizationResults: async (id) => {
    try {
      const response = await apiClient.get(`/optimizations/${id}/results`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get optimization job status
   * @param {string} id - Optimization job ID
   * @returns {Promise} Promise object represents the optimization status
   */
  getOptimizationStatus: async (id) => {
    try {
      const response = await apiClient.get(`/optimizations/${id}/status`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Apply optimization results to a digital twin
   * @param {string} optimizationId - Optimization job ID
   * @param {string} digitalTwinId - Digital twin ID
   * @returns {Promise} Promise object represents the operation result
   */
  applyOptimizationToDigitalTwin: async (optimizationId, digitalTwinId) => {
    try {
      const response = await apiClient.post(`/optimizations/${optimizationId}/apply`, {
        digitalTwinId
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default optimizationService;
