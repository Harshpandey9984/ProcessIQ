import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  Link,
  CircularProgress,
  Container,
  Divider
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import authService from '../services/authService';
import { debugLogin } from '../services/debug-auth';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState(location.state?.email || '');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [registrationSuccess, setRegistrationSuccess] = useState(location.state?.registrationSuccess || false);
  
  // Get the intended destination from location state or default to dashboard
  const from = location.state?.from?.pathname || '/';

  // Check if user is already logged in
  useEffect(() => {
    if (authService.isAuthenticated()) {
      navigate(from);
    }
  }, [navigate, from]);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Use debug login to track the authentication process
      await debugLogin(email, password, authService);
      navigate(from);
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box 
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          py: 4
        }}
      >
        <Card sx={{ width: '100%', boxShadow: 3 }}>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
              <Box 
                sx={{ 
                  bgcolor: 'primary.main', 
                  color: 'white',
                  borderRadius: '50%',
                  p: 1,
                  mb: 2
                }}
              >
                <LockOutlinedIcon fontSize="large" />
              </Box>
              <Typography component="h1" variant="h5">
                Digital Twin Optimization Platform
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" sx={{ mt: 1 }}>
                Sign in to your account
              </Typography>
            </Box>
            
            {registrationSuccess && (
              <Alert severity="success" sx={{ mb: 3 }}>
                Registration successful! Please sign in with your new credentials.
              </Alert>
            )}
            
            {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
            
            <form onSubmit={handleSubmit}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
              
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2, py: 1.5 }}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Sign In'}
              </Button>
              
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                <Link component={RouterLink} to="/forgot-password" variant="body2">
                  Forgot password?
                </Link>
                
                <Link component={RouterLink} to="/register" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Box>
            </form>
            
            <Box sx={{ mt: 4 }}>
              <Divider sx={{ mb: 2 }}>
                <Typography variant="caption" color="text.secondary">
                  Sample Credentials
                </Typography>
              </Divider>
              
              <Box sx={{ display: 'flex', justifyContent: 'space-around' }}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Regular User:
                  </Typography>
                  <Typography variant="caption" display="block">
                    user@example.com
                  </Typography>
                  <Typography variant="caption" display="block">
                    password
                  </Typography>
                </Box>
                
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Administrator:
                  </Typography>
                  <Typography variant="caption" display="block">
                    admin@example.com
                  </Typography>
                  <Typography variant="caption" display="block">
                    password
                  </Typography>
                </Box>
              </Box>
            </Box>
          </CardContent>
        </Card>
        
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            Powered by Intel® Technologies
          </Typography>
          <Typography variant="caption" color="text.secondary" display="block">
            © 2025 Digital Twin Optimization Platform
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default Login;
