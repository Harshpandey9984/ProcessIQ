import apiClient from './api';

const simulationService = {
  /**
   * Get all simulations
   * @returns {Promise} Promise object represents the simulations
   */
  getAllSimulations: async () => {
    try {
      const response = await apiClient.get('/simulations');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get a specific simulation by ID
   * @param {string} id - Simulation ID
   * @returns {Promise} Promise object represents the simulation
   */
  getSimulationById: async (id) => {
    try {
      const response = await apiClient.get(`/simulations/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Create a new simulation
   * @param {Object} simulationData - Simulation configuration data
   * @returns {Promise} Promise object represents the created simulation
   */
  createSimulation: async (simulationData) => {
    try {
      const response = await apiClient.post('/simulations', simulationData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Update an existing simulation
   * @param {string} id - Simulation ID
   * @param {Object} simulationData - Simulation configuration data
   * @returns {Promise} Promise object represents the updated simulation
   */
  updateSimulation: async (id, simulationData) => {
    try {
      const response = await apiClient.put(`/simulations/${id}`, simulationData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Delete a simulation
   * @param {string} id - Simulation ID
   * @returns {Promise} Promise object represents the operation result
   */
  deleteSimulation: async (id) => {
    try {
      const response = await apiClient.delete(`/simulations/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Run a simulation
   * @param {string} id - Simulation ID
   * @param {Object} runParameters - Optional run-specific parameters
   * @returns {Promise} Promise object represents the simulation run
   */
  runSimulation: async (id, runParameters = {}) => {
    try {
      const response = await apiClient.post(`/simulations/${id}/run`, runParameters);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get simulation results
   * @param {string} id - Simulation ID
   * @param {string} runId - Simulation run ID
   * @returns {Promise} Promise object represents the simulation results
   */
  getSimulationResults: async (id, runId) => {
    try {
      const response = await apiClient.get(`/simulations/${id}/runs/${runId}/results`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Stop a running simulation
   * @param {string} id - Simulation ID
   * @param {string} runId - Simulation run ID
   * @returns {Promise} Promise object represents the operation result
   */
  stopSimulation: async (id, runId) => {
    try {
      const response = await apiClient.post(`/simulations/${id}/runs/${runId}/stop`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get simulation status
   * @param {string} id - Simulation ID
   * @param {string} runId - Simulation run ID
   * @returns {Promise} Promise object represents the simulation status
   */
  getSimulationStatus: async (id, runId) => {
    try {
      const response = await apiClient.get(`/simulations/${id}/runs/${runId}/status`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default simulationService;
