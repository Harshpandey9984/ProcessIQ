import apiClient from './api';

const digitalTwinService = {
  /**
   * Get all digital twins
   * @returns {Promise} Promise object represents the digital twins
   */
  getAllDigitalTwins: async () => {
    try {
      const response = await apiClient.get('/digital-twins');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get a specific digital twin by ID
   * @param {string} id - Digital twin ID
   * @returns {Promise} Promise object represents the digital twin
   */
  getDigitalTwinById: async (id) => {
    try {
      const response = await apiClient.get(`/digital-twins/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Create a new digital twin
   * @param {Object} digitalTwinData - Digital twin data
   * @returns {Promise} Promise object represents the created digital twin
   */
  createDigitalTwin: async (digitalTwinData) => {
    try {
      const response = await apiClient.post('/digital-twins', digitalTwinData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Update an existing digital twin
   * @param {string} id - Digital twin ID
   * @param {Object} digitalTwinData - Digital twin data
   * @returns {Promise} Promise object represents the updated digital twin
   */
  updateDigitalTwin: async (id, digitalTwinData) => {
    try {
      const response = await apiClient.put(`/digital-twins/${id}`, digitalTwinData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Delete a digital twin
   * @param {string} id - Digital twin ID
   * @returns {Promise} Promise object represents the operation result
   */
  deleteDigitalTwin: async (id) => {
    try {
      const response = await apiClient.delete(`/digital-twins/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get metrics for a digital twin
   * @param {string} id - Digital twin ID
   * @returns {Promise} Promise object represents the digital twin metrics
   */
  getDigitalTwinMetrics: async (id) => {
    try {
      const response = await apiClient.get(`/digital-twins/${id}/metrics`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Execute a what-if scenario on a digital twin
   * @param {string} id - Digital twin ID
   * @param {Object} scenarioData - What-if scenario data
   * @returns {Promise} Promise object represents the scenario results
   */
  executeWhatIfScenario: async (id, scenarioData) => {
    try {
      const response = await apiClient.post(`/digital-twins/${id}/scenarios`, scenarioData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default digitalTwinService;
