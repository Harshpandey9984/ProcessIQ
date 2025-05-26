import apiClient from './api';

const modelService = {
  /**
   * Get all ML models
   * @returns {Promise} Promise object represents the models
   */
  getAllModels: async () => {
    try {
      const response = await apiClient.get('/models');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get a specific model by ID
   * @param {string} id - Model ID
   * @returns {Promise} Promise object represents the model
   */
  getModelById: async (id) => {
    try {
      const response = await apiClient.get(`/models/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Create a new model
   * @param {Object} modelData - Model configuration data
   * @returns {Promise} Promise object represents the created model
   */
  createModel: async (modelData) => {
    try {
      const response = await apiClient.post('/models', modelData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Update an existing model
   * @param {string} id - Model ID
   * @param {Object} modelData - Model configuration data
   * @returns {Promise} Promise object represents the updated model
   */
  updateModel: async (id, modelData) => {
    try {
      const response = await apiClient.put(`/models/${id}`, modelData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Delete a model
   * @param {string} id - Model ID
   * @returns {Promise} Promise object represents the operation result
   */
  deleteModel: async (id) => {
    try {
      const response = await apiClient.delete(`/models/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Train a model
   * @param {string} id - Model ID
   * @param {Object} trainingData - Training configuration
   * @returns {Promise} Promise object represents the training job
   */
  trainModel: async (id, trainingData) => {
    try {
      const response = await apiClient.post(`/models/${id}/train`, trainingData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Use a model to make predictions
   * @param {string} id - Model ID
   * @param {Object} inputData - Input data for prediction
   * @returns {Promise} Promise object represents the prediction results
   */
  predict: async (id, inputData) => {
    try {
      const response = await apiClient.post(`/models/${id}/predict`, inputData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get model metrics and performance data
   * @param {string} id - Model ID
   * @returns {Promise} Promise object represents the model metrics
   */
  getModelMetrics: async (id) => {
    try {
      const response = await apiClient.get(`/models/${id}/metrics`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Export a trained model
   * @param {string} id - Model ID
   * @param {string} format - Export format (e.g., 'onnx', 'openvino')
   * @returns {Promise} Promise object represents the export job
   */
  exportModel: async (id, format) => {
    try {
      const response = await apiClient.post(`/models/${id}/export`, { format });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Import a pre-trained model
   * @param {FormData} modelData - Form data containing the model file and metadata
   * @returns {Promise} Promise object represents the imported model
   */
  importModel: async (modelData) => {
    try {
      const response = await apiClient.post('/models/import', modelData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get model training status
   * @param {string} id - Model ID
   * @param {string} trainingJobId - Training job ID
   * @returns {Promise} Promise object represents the training status
   */
  getTrainingStatus: async (id, trainingJobId) => {
    try {
      const response = await apiClient.get(`/models/${id}/train/${trainingJobId}/status`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Stop a model training job
   * @param {string} id - Model ID
   * @param {string} trainingJobId - Training job ID
   * @returns {Promise} Promise object represents the operation result
   */
  stopTraining: async (id, trainingJobId) => {
    try {
      const response = await apiClient.post(`/models/${id}/train/${trainingJobId}/stop`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default modelService;
