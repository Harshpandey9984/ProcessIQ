import React from 'react';
import { Box, Card, CardContent, Typography, useTheme } from '@mui/material';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip as ChartTooltip,
  Legend
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  ChartTooltip,
  Legend
);

/**
 * A reusable bar graph component using Chart.js
 * @param {Object} props - Component properties
 * @param {string} props.title - Graph title
 * @param {Array} props.labels - X-axis labels
 * @param {Array} props.datasets - Chart.js datasets
 * @param {string} props.xAxisTitle - X-axis title
 * @param {string} props.yAxisTitle - Y-axis title
 * @param {boolean} props.showLegend - Whether to show the legend
 * @param {boolean} props.horizontal - Whether to display bars horizontally
 * @param {boolean} props.stacked - Whether to stack the bars
 * @param {Object} props.options - Additional Chart.js options
 * @param {Object} props.sx - Additional styles for the container
 * @param {number} props.height - Chart height
 */
const BarGraph = ({
  title,
  labels,
  datasets,
  xAxisTitle,
  yAxisTitle,
  showLegend = true,
  horizontal = false,
  stacked = false,
  options = {},
  sx = {},
  height = 300
}) => {
  const theme = useTheme();

  // Prepare chart data
  const data = {
    labels,
    datasets: datasets.map(dataset => ({
      borderRadius: 4,
      ...dataset
    }))
  };

  // Prepare chart options
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: horizontal ? 'y' : 'x',
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
        stacked: stacked,
        grid: {
          display: !horizontal,
          color: theme.palette.divider
        },
        title: xAxisTitle ? {
          display: true,
          text: horizontal ? yAxisTitle : xAxisTitle
        } : undefined
      },
      y: {
        stacked: stacked,
        grid: {
          display: horizontal,
          color: theme.palette.divider
        },
        title: yAxisTitle ? {
          display: true,
          text: horizontal ? xAxisTitle : yAxisTitle
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
          <Bar data={data} options={chartOptions} />
        </Box>
      </CardContent>
    </Card>
  );
};

export default BarGraph;
