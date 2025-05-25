import apiClient from './api';

const AUTH_TOKEN_KEY = 'dt_auth_token';
const USER_KEY = 'dt_user';

const authService = {
  /**
   * Login user
   * @param {string} email User email
   * @param {string} password User password
   * @returns {Promise} Promise object with user data and token
   */  login: async (email, password) => {
    try {      // The backend expects username and password in URL encoded form data
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);
      
      const response = await apiClient.post('/api/auth/token', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      const { access_token, user } = response.data;
      
      // Save auth data in local storage
      localStorage.setItem(AUTH_TOKEN_KEY, access_token);
      localStorage.setItem(USER_KEY, JSON.stringify(user));
      
      // Set token in API client for future requests
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      return response.data;
    } catch (error) {
      throw error;
    }
  },
    /**
   * Register new user
   * @param {Object} userData User registration data
   * @returns {Promise} Promise object with user data
   */
  register: async (userData) => {
    try {
      // The backend expects specific fields
      const payload = {
        email: userData.email,
        password: userData.password,
        full_name: userData.fullName || userData.full_name || 'User',
        company: userData.company || null,
        role: userData.role || 'user'
      };
        const response = await apiClient.post('/api/auth/register', payload);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Logout user - remove token and user data
   */
  logout: () => {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    delete apiClient.defaults.headers.common['Authorization'];
  },
  
  /**
   * Check if user is authenticated
   * @returns {boolean} True if user is authenticated
   */
  isAuthenticated: () => {
    return !!localStorage.getItem(AUTH_TOKEN_KEY);
  },
  
  /**
   * Get current user
   * @returns {Object|null} User object or null if not authenticated
   */
  getCurrentUser: () => {
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch (e) {
      return null;
    }
  },
  
  /**
   * Get auth token
   * @returns {string|null} Auth token or null if not authenticated
   */
  getToken: () => {
    return localStorage.getItem(AUTH_TOKEN_KEY);
  },
  
  /**
   * Update user profile
   * @param {Object} userData Updated user data
   * @returns {Promise} Promise object with updated user data
   */
  updateProfile: async (userData) => {
    try {
      const response = await apiClient.put('/auth/profile', userData);
      
      // Update user in local storage
      localStorage.setItem(USER_KEY, JSON.stringify(response.data));
      
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Change password
   * @param {string} currentPassword Current password
   * @param {string} newPassword New password
   * @returns {Promise} Promise object with operation result
   */
  changePassword: async (currentPassword, newPassword) => {
    try {
      const response = await apiClient.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Request password reset
   * @param {string} email User email
   * @returns {Promise} Promise object with operation result
   */
  requestPasswordReset: async (email) => {
    try {
      const response = await apiClient.post('/auth/forgot-password', { email });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Reset password with token
   * @param {string} token Reset token
   * @param {string} newPassword New password
   * @returns {Promise} Promise object with operation result
   */
  resetPassword: async (token, newPassword) => {
    try {
      const response = await apiClient.post('/auth/reset-password', {
        token,
        newPassword
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Request password reset link
   * @param {string} email User email
   * @returns {Promise} Promise object with operation result
   */
  forgotPassword: async (email) => {
    try {
      const response = await apiClient.post('/auth/forgot-password', { email });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Reset password using token
   * @param {string} token Password reset token
   * @param {string} newPassword New password
   * @returns {Promise} Promise object with operation result
   */
  resetPassword: async (token, newPassword) => {
    try {
      const response = await apiClient.post('/auth/reset-password', { 
        token, 
        new_password: newPassword 
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Initialize auth from storage if exists
const token = localStorage.getItem(AUTH_TOKEN_KEY);
if (token) {
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export default authService;
