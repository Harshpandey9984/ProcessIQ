/**
 * Debug utilities for authentication issues
 */

// Export auth state monitor
export const debugLogin = async (email, password, authService) => {
  try {
    console.log("Login attempt with:", { email });
    
    // Create the URLSearchParams object
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    
    console.log("Request payload:", params.toString());
    console.log("Login endpoint: /api/auth/token");
    
    // Add logging to track the request
    const response = await authService.login(email, password);
    console.log("Login successful:", response);
    return response;
  } catch (error) {
    console.error("Login error details:", {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
    });
    throw error;
  }
};

export const debugRegister = async (userData, authService) => {
  try {
    console.log("Registration attempt with:", userData);
    const response = await authService.register(userData);
    console.log("Registration successful:", response);
    return response;
  } catch (error) {
    console.error("Registration error details:", {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
    });
    throw error;
  }
};
