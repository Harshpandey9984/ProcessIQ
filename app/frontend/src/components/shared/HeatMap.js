import React from 'react';
import { Box, Card, CardContent, Typography, useTheme } from '@mui/material';
import { Scatter } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  Tooltip as ChartTooltip,
  Legend
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  LinearScale,
  PointElement,
  ChartTooltip,
  Legend
);

/**
 * A heat map component for visualization of 2D data
 * @param {Object} props - Component properties
 * @param {string} props.title - Graph title
 * @param {Array} props.data - Data points [{x, y, value}]
 * @param {string} props.xAxisTitle - X-axis title
 * @param {string} props.yAxisTitle - Y-axis title
 * @param {number} props.minValue - Minimum value for color scale
 * @param {number} props.maxValue - Maximum value for color scale
 * @param {Object} props.options - Additional Chart.js options
 * @param {Object} props.sx - Additional styles for the container
 * @param {number} props.height - Chart height
 */
const HeatMap = ({
  title,
  data,
  xAxisTitle,
  yAxisTitle,
  minValue,
  maxValue,
  options = {},
  sx = {},
  height = 400
}) => {
  const theme = useTheme();
  
  // Calculate min/max values if not provided
  const calculatedMin = minValue !== undefined ? minValue : Math.min(...data.map(point => point.value));
  const calculatedMax = maxValue !== undefined ? maxValue : Math.max(...data.map(point => point.value));
  
  // Function to get color based on value
  const getColor = (value) => {
    // Normalize value between 0 and 1
    const normalized = (value - calculatedMin) / (calculatedMax - calculatedMin);
    
    // Convert to hue (240 = blue, 0 = red)
    const hue = (1 - normalized) * 240;
    
    return `hsla(${hue}, 100%, 50%, 0.8)`;
  };

  // Convert data to Chart.js format
  const chartData = {
    datasets: [{
      label: title,
      data: data.map(point => ({
        x: point.x,
        y: point.y,
        value: point.value
      })),
      backgroundColor: data.map(point => getColor(point.value)),
      pointRadius: 10,
      pointHoverRadius: 12
    }]
  };

  // Configure chart options
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => {
            const point = data[context.dataIndex];
            return [
              `X: ${point.x}`,
              `Y: ${point.y}`,
              `Value: ${point.value}`
            ];
          }
        },
        backgroundColor: theme.palette.background.paper,
        titleColor: theme.palette.text.primary,
        bodyColor: theme.palette.text.secondary,
        borderColor: theme.palette.divider,
        borderWidth: 1,
        padding: 10,
        boxPadding: 5
      },
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: xAxisTitle || 'X-Axis'
        },
        grid: {
          color: theme.palette.divider
        }
      },
      y: {
        title: {
          display: true,
          text: yAxisTitle || 'Y-Axis'
        },
        grid: {
          color: theme.palette.divider
        }
      }
    },
    ...options
  };

  return (
    <Card sx={{ height: '100%', ...sx }}>
      <CardContent>
        {title && (
          <Typography variant="h6" gutterBottom>
            {title}
          </Typography>
        )}
        <Box sx={{ height }}>
          <Scatter data={chartData} options={chartOptions} />
        </Box>
        
        {/* Color legend */}
        <Box 
          sx={{ 
            mt: 2, 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center' 
          }}
        >
          <Box 
            sx={{ 
              width: 200, 
              height: 20, 
              background: 'linear-gradient(to right, blue, cyan, lime, yellow, red)'
            }} 
          />
          <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', mt: 0.5 }}>
            <Typography variant="caption">{calculatedMin}</Typography>
            <Typography variant="caption">{calculatedMax}</Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default HeatMap;
