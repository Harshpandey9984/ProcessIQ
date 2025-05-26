import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

const NotFound = () => {
  const navigate = useNavigate();
  
  return (
    <Container maxWidth="md">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '80vh',
          textAlign: 'center'
        }}
      >
        <ErrorOutlineIcon sx={{ fontSize: 120, color: 'text.secondary', mb: 4 }} />
        <Typography variant="h2" component="h1" gutterBottom color="text.primary">
          404
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom color="text.primary">
          Page Not Found
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Sorry, we couldn't find the page you're looking for. Please check the URL or navigate back to the dashboard.
        </Typography>
        <Box sx={{ mt: 4 }}>
          <Button
            variant="contained"
            color="primary"
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/')}
            size="large"
          >
            Back to Dashboard
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default NotFound;
