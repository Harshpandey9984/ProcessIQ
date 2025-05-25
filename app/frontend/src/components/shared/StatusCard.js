import React from 'react';
import { Box, Card, CardContent, Typography, LinearProgress } from '@mui/material';
import { 
  CheckCircle as CheckCircleIcon, 
  Error as ErrorIcon,
  Warning as WarningIcon,
  HourglassEmpty as HourglassEmptyIcon,
  Pause as PauseIcon
} from '@mui/icons-material';

/**
 * A component for displaying status information in a card format
 * @param {Object} props - Component properties
 * @param {string} props.title - Card title
 * @param {string} props.status - Status value ('success', 'error', 'warning', 'progress', 'idle')
 * @param {string} props.message - Status message to display
 * @param {number} props.progress - Progress percentage (0-100) when status is 'progress'
 * @param {Object} props.sx - Additional styles to apply to the card
 * @param {Node} props.action - Optional action component to display in the card
 */
const StatusCard = ({ title, status, message, progress, sx, action }) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'success':
        return <CheckCircleIcon sx={{ color: 'success.main', fontSize: 32 }} />;
      case 'error':
        return <ErrorIcon sx={{ color: 'error.main', fontSize: 32 }} />;
      case 'warning':
        return <WarningIcon sx={{ color: 'warning.main', fontSize: 32 }} />;
      case 'progress':
        return <HourglassEmptyIcon sx={{ color: 'info.main', fontSize: 32 }} />;
      case 'idle':
        return <PauseIcon sx={{ color: 'text.secondary', fontSize: 32 }} />;
      default:
        return null;
    }
  };

  return (
    <Card sx={{ height: '100%', ...sx }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6" component="div" gutterBottom>
            {title}
          </Typography>
          <Box>
            {getStatusIcon()}
          </Box>
        </Box>
        <Typography variant="body2" color="text.secondary">
          {message}
        </Typography>
        {status === 'progress' && progress !== undefined && (
          <Box sx={{ width: '100%', mt: 2 }}>
            <LinearProgress variant="determinate" value={progress} />
            <Typography variant="body2" color="text.secondary" align="right" sx={{ mt: 0.5 }}>
              {Math.round(progress)}%
            </Typography>
          </Box>
        )}
        {action && (
          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
            {action}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default StatusCard;
