import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';

// Layout components
import Layout from './components/layout/Layout';

// Auth components
import ProtectedRoute from './components/auth/ProtectedRoute';

// Page components
import Dashboard from './pages/Dashboard';
import DigitalTwins from './pages/DigitalTwins';
import Simulation from './pages/Simulation';
import Optimization from './pages/Optimization';
import Models from './pages/Models';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import ProfileManagement from './pages/ProfileManagement';

function App() {
  return (
    <Box sx={{ display: 'flex' }}>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        
        {/* Protected routes */}
        <Route path="/" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="digital-twins" element={<DigitalTwins />} />
          <Route path="simulation" element={<Simulation />} />
          <Route path="optimization" element={<Optimization />} />
          <Route path="models" element={<Models />} />
          <Route path="settings" element={<Settings />} />
          <Route path="profile" element={<ProfileManagement />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Box>
  );
}

export default App;
