import React from 'react';
import { Box, Card, CardContent, Typography, useTheme } from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
  Filler
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend,
  Filler
);

/**
 * A reusable line graph component using Chart.js
 * @param {Object} props - Component properties
 * @param {string} props.title - Graph title
 * @param {Array} props.labels - X-axis labels
 * @param {Array} props.datasets - Chart.js datasets
 * @param {string} props.xAxisTitle - X-axis title
 * @param {string} props.yAxisTitle - Y-axis title
 * @param {boolean} props.showLegend - Whether to show the legend
 * @param {Object} props.options - Additional Chart.js options
 * @param {Object} props.sx - Additional styles for the container
 * @param {number} props.height - Chart height
 */
const LineGraph = ({
  title,
  labels,
  datasets,
  xAxisTitle,
  yAxisTitle,
  showLegend = true,
  options = {},
  sx = {},
  height = 300
}) => {
  const theme = useTheme();

  // Prepare chart data
  const data = {
    labels,
    datasets: datasets.map(dataset => ({
      tension: 0.4,
      pointRadius: 3,
      pointHoverRadius: 5,
      pointBackgroundColor: theme.palette.background.paper,
      ...dataset
    }))
  };

  // Prepare chart options
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: showLegend,
        position: 'top',
        align: 'end',
        labels: {
          usePointStyle: true,
          boxWidth: 6
        }
      },
      tooltip: {
        backgroundColor: theme.palette.background.paper,
        titleColor: theme.palette.text.primary,
        bodyColor: theme.palette.text.secondary,
        borderColor: theme.palette.divider,
        borderWidth: 1,
        padding: 10,
        boxPadding: 5
      }
    },
    scales: {
      x: {
        grid: {
          display: true,
          color: theme.palette.divider
        },
        title: xAxisTitle ? {
          display: true,
          text: xAxisTitle
        } : undefined
      },
      y: {
        grid: {
          display: true,
          color: theme.palette.divider
        },
        title: yAxisTitle ? {
          display: true,
          text: yAxisTitle
        } : undefined
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
        <Box sx={{ height: height }}>
          <Line data={data} options={chartOptions} />
        </Box>
      </CardContent>
    </Card>
  );
};

export default LineGraph;
