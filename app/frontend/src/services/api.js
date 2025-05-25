import axios from 'axios';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: '', // Remove the '/api' as it's already being added in the endpoint paths
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 seconds timeout
});

// Function to get token from localStorage to avoid circular dependency
const getToken = () => localStorage.getItem('dt_auth_token');

// Request interceptor for API calls
apiClient.interceptors.request.use(
  config => {
    // Add authentication token from local storage if available
    const token = getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Response interceptor for API calls
apiClient.interceptors.response.use(
  response => {
    // You can handle successful responses here
    return response;
  },
  error => {
    // Handle API errors here
    console.error('API Error:', error);
    
    // You can add custom error handling here
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Error data:', error.response.data);
      console.error('Error status:', error.response.status);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received:', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error message:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
