import React, { useState } from 'react';
import {
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Slider,
  Paper,
  Divider,
  Chip,
  Stack
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SaveIcon from '@mui/icons-material/Save';
import DownloadIcon from '@mui/icons-material/Download';

const Simulation = () => {
  const [processType, setProcessType] = useState('injection_molding');
  const [duration, setDuration] = useState(60);
  const [parameters, setParameters] = useState({
    temperature: 230,
    pressure: 100,
    cooling_time: 20,
    injection_speed: 80,
    mold_temperature: 50
  });

  const handleProcessTypeChange = (event) => {
    setProcessType(event.target.value);
    
    // Reset parameters based on process type
    if (event.target.value === 'injection_molding') {
      setParameters({
        temperature: 230,
        pressure: 100,
        cooling_time: 20,
        injection_speed: 80,
        mold_temperature: 50
      });
    } else if (event.target.value === 'cnc_machining') {
      setParameters({
        spindle_speed: 5000,
        feed_rate: 300,
        cut_depth: 0.5,
        tool_diameter: 10
      });
    }
    // Add other process types as needed
  };

  const handleParameterChange = (param) => (event, newValue) => {
    const value = newValue !== undefined ? newValue : Number(event.target.value);
    setParameters({
      ...parameters,
      [param]: value
    });
  };

  const handleSliderChange = (param) => (event, newValue) => {
    setParameters({
      ...parameters,
      [param]: newValue
    });
  };

  const getParameterConfig = () => {
    if (processType === 'injection_molding') {
      return [
        { name: 'temperature', label: 'Temperature (°C)', min: 150, max: 350 },
        { name: 'pressure', label: 'Pressure (MPa)', min: 50, max: 200 },
        { name: 'cooling_time', label: 'Cooling Time (s)', min: 5, max: 60 },
        { name: 'injection_speed', label: 'Injection Speed (cm³/s)', min: 10, max: 150 },
        { name: 'mold_temperature', label: 'Mold Temperature (°C)', min: 20, max: 120 }
      ];
    } else if (processType === 'cnc_machining') {
      return [
        { name: 'spindle_speed', label: 'Spindle Speed (RPM)', min: 1000, max: 20000 },
        { name: 'feed_rate', label: 'Feed Rate (mm/min)', min: 50, max: 1000 },
        { name: 'cut_depth', label: 'Cut Depth (mm)', min: 0.1, max: 5 },
        { name: 'tool_diameter', label: 'Tool Diameter (mm)', min: 1, max: 20 }
      ];
    }
    // Add other process types as needed
    return [];
  };

  return (
    <Box className="page-container">
      <Typography variant="h4" component="h1" gutterBottom>
        Simulation
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Simulation Configuration
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="process-type-label">Process Type</InputLabel>
              <Select
                labelId="process-type-label"
                id="process-type"
                value={processType}
                label="Process Type"
                onChange={handleProcessTypeChange}
              >
                <MenuItem value="injection_molding">Injection Molding</MenuItem>
                <MenuItem value="cnc_machining">CNC Machining</MenuItem>
                <MenuItem value="assembly_line">Assembly Line</MenuItem>
                <MenuItem value="chemical_process">Chemical Process</MenuItem>
                <MenuItem value="packaging_line">Packaging Line</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <Typography id="duration-slider" gutterBottom>
                Simulation Duration: {duration} seconds
              </Typography>
              <Slider
                value={duration}
                onChange={(e, newValue) => setDuration(newValue)}
                aria-labelledby="duration-slider"
                min={10}
                max={600}
                step={10}
                marks={[
                  { value: 10, label: '10s' },
                  { value: 300, label: '5m' },
                  { value: 600, label: '10m' }
                ]}
              />
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <Typography gutterBottom>Include Sensor Noise</Typography>
              <Stack direction="row" spacing={1}>
                <Chip 
                  label="Yes" 
                  color="primary" 
                  variant="filled"
                  onClick={() => {}}
                />
                <Chip 
                  label="No" 
                  color="default" 
                  variant="outlined"
                  onClick={() => {}}
                />
              </Stack>
            </FormControl>
            
            <Box sx={{ mt: 3 }}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<PlayArrowIcon />}
                fullWidth
              >
                Run Simulation
              </Button>
            </Box>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Saved Simulations
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
              Previously saved simulation runs:
            </Typography>
            
            <Stack spacing={1}>
              <Card variant="outlined">
                <CardContent sx={{ py: 1 }}>
                  <Typography variant="subtitle2">
                    Injection Molding - High Pressure
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    Created: 2023-04-15 13:45
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small">Load</Button>
                </CardActions>
              </Card>
              
              <Card variant="outlined">
                <CardContent sx={{ py: 1 }}>
                  <Typography variant="subtitle2">
                    CNC Machining - Fine Detail
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    Created: 2023-04-12 09:30
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small">Load</Button>
                </CardActions>
              </Card>
            </Stack>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Process Parameters
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Grid container spacing={3}>
              {getParameterConfig().map((param) => (
                <Grid item xs={12} sm={6} key={param.name}>
                  <Typography id={`${param.name}-slider`} gutterBottom>
                    {param.label}: {parameters[param.name]}
                  </Typography>
                  <Slider
                    value={parameters[param.name] || param.min}
                    onChange={handleSliderChange(param.name)}
                    aria-labelledby={`${param.name}-slider`}
                    min={param.min}
                    max={param.max}
                    step={(param.max - param.min) / 100}
                  />
                </Grid>
              ))}
            </Grid>
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">
                Simulation Results
              </Typography>
              <Box>
                <Button 
                  variant="outlined" 
                  startIcon={<SaveIcon />}
                  sx={{ mr: 1 }}
                >
                  Save
                </Button>
                <Button 
                  variant="outlined" 
                  startIcon={<DownloadIcon />}
                >
                  Export
                </Button>
              </Box>
            </Box>
            <Divider sx={{ mb: 2 }} />
            
            <Box sx={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Typography variant="body1" color="textSecondary">
                Run a simulation to see results here
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Simulation;
