import React from 'react';
import { Box, Card, CardContent, Typography, CircularProgress, Tooltip } from '@mui/material';
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material';
import InfoIcon from '@mui/icons-material/Info';

/**
 * A component for displaying a metric or KPI in a card format
 * @param {Object} props - Component properties
 * @param {string} props.title - Metric title
 * @param {string|number} props.value - Metric value
 * @param {string} props.unit - Metric unit (optional)
 * @param {string} props.trend - Trend direction ('up', 'down', 'flat')
 * @param {number} props.changePercent - Percentage change
 * @param {string} props.description - Additional description or info about the metric
 * @param {boolean} props.loading - Whether the metric is loading
 * @param {Object} props.sx - Additional styles to apply to the card
 */
const MetricCard = ({
  title,
  value,
  unit,
  trend,
  changePercent,
  description,
  loading = false,
  sx
}) => {
  // Determine trend color
  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'success.main';
      case 'down':
        return 'error.main';
      case 'flat':
      default:
        return 'text.secondary';
    }
  };

  // Determine trend icon
  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp sx={{ fontSize: 20, color: getTrendColor() }} />;
      case 'down':
        return <TrendingDown sx={{ fontSize: 20, color: getTrendColor() }} />;
      case 'flat':
      default:
        return <TrendingFlat sx={{ fontSize: 20, color: getTrendColor() }} />;
    }
  };

  return (
    <Card sx={{ height: '100%', ...sx }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="subtitle2" color="text.secondary">
            {title}
          </Typography>
          {description && (
            <Tooltip title={description} arrow placement="top">
              <InfoIcon fontSize="small" color="action" />
            </Tooltip>
          )}
        </Box>
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
            <CircularProgress size={30} />
          </Box>
        ) : (
          <>
            <Typography variant="h4" component="div" sx={{ fontWeight: 500 }}>
              {value}
              {unit && <Typography component="span" variant="body2" sx={{ ml: 0.5 }}>{unit}</Typography>}
            </Typography>
            
            {trend && changePercent !== undefined && (
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                {getTrendIcon()}
                <Typography 
                  variant="body2" 
                  sx={{ ml: 0.5, color: getTrendColor() }}
                >
                  {changePercent > 0 ? '+' : ''}{changePercent}%
                </Typography>
              </Box>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default MetricCard;
