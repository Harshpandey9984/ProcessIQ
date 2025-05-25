import React, { useState, useEffect } from 'react';
import { 
  Box,
  Typography,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Grid,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Tabs,
  Tab
} from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import VpnKeyIcon from '@mui/icons-material/VpnKey';
import authService from '../services/authService';

const ProfileManagement = () => {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');
  const [profileData, setProfileData] = useState({
    full_name: '',
    email: '',
    company: ''
  });
  
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    if (currentUser) {
      setProfileData({
        full_name: currentUser.full_name || '',
        email: currentUser.email || '',
        company: currentUser.company || ''
      });
    }
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    setSuccess('');
    setError('');
  };

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({ ...prev, [name]: value }));
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({ ...prev, [name]: value }));
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await authService.updateProfile({
        full_name: profileData.full_name,
        company: profileData.company
      });
      
      setSuccess('Profile updated successfully');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validation
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setError('New passwords do not match');
      return;
    }

    if (passwordData.newPassword.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setLoading(true);
    try {
      await authService.changePassword(
        passwordData.currentPassword,
        passwordData.newPassword
      );
      
      setSuccess('Password changed successfully');
      setPasswordData({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Account Settings
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="profile tabs">
          <Tab 
            icon={<AccountCircleIcon />} 
            label="Profile Information" 
            id="profile-tab-0" 
            aria-controls="profile-tabpanel-0" 
          />
          <Tab 
            icon={<VpnKeyIcon />} 
            label="Security" 
            id="profile-tab-1" 
            aria-controls="profile-tabpanel-1" 
          />
        </Tabs>
      </Box>

      {/* Profile Information Tab */}
      <div
        role="tabpanel"
        hidden={tabValue !== 0}
        id="profile-tabpanel-0"
        aria-labelledby="profile-tab-0"
      >
        {tabValue === 0 && (
          <Card>
            <CardHeader title="Profile Information" />
            <Divider />
            <CardContent>
              {success && <Alert severity="success" sx={{ mb: 3 }}>{success}</Alert>}
              {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

              <Box component="form" onSubmit={handleProfileSubmit}>
                <Grid container spacing={3}>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Email Address"
                      name="email"
                      value={profileData.email}
                      disabled
                      helperText="Email cannot be changed"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Full Name"
                      name="full_name"
                      value={profileData.full_name}
                      onChange={handleProfileChange}
                      required
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Company"
                      name="company"
                      value={profileData.company}
                      onChange={handleProfileChange}
                    />
                  </Grid>
                </Grid>
                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                  <Button
                    type="submit"
                    variant="contained"
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Save Changes'}
                  </Button>
                </Box>
              </Box>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Security Tab */}
      <div
        role="tabpanel"
        hidden={tabValue !== 1}
        id="profile-tabpanel-1"
        aria-labelledby="profile-tab-1"
      >
        {tabValue === 1 && (
          <Card>
            <CardHeader title="Change Password" />
            <Divider />
            <CardContent>
              {success && <Alert severity="success" sx={{ mb: 3 }}>{success}</Alert>}
              {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

              <Box component="form" onSubmit={handlePasswordSubmit}>
                <Grid container spacing={3}>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Current Password"
                      name="currentPassword"
                      type="password"
                      value={passwordData.currentPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="New Password"
                      name="newPassword"
                      type="password"
                      value={passwordData.newPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Confirm New Password"
                      name="confirmPassword"
                      type="password"
                      value={passwordData.confirmPassword}
                      onChange={handlePasswordChange}
                      required
                    />
                  </Grid>
                </Grid>
                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Change Password'}
                  </Button>
                </Box>
              </Box>
            </CardContent>
          </Card>
        )}
      </div>
    </Box>
  );
};

export default ProfileManagement;
