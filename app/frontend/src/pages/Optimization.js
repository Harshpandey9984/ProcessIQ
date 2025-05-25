import React, { useState } from 'react';
import {
  Typography,
  Box,
  Grid,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Chip,
  Stack,
  Button,
  TextField,
  FormControlLabel,
  Switch,
  Card,
  CardContent,
  CardActions,
  List,
  ListItem,
  ListItemText,
  LinearProgress,
  Alert
} from '@mui/material';
import TuneIcon from '@mui/icons-material/Tune';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

const Optimization = () => {
  const [processType, setProcessType] = useState('injection_molding');
  const [targetVariable, setTargetVariable] = useState('quality_score');
  const [optimizationAlgorithm, setOptimizationAlgorithm] = useState('bayesian_optimization');
  const [maximize, setMaximize] = useState(true);
  const [selectedParameters, setSelectedParameters] = useState([
    'temperature',
    'pressure',
    'cooling_time',
    'injection_speed'
  ]);

  const handleProcessTypeChange = (event) => {
    setProcessType(event.target.value);
    // Reset selected parameters based on process type
    if (event.target.value === 'injection_molding') {
      setSelectedParameters([
        'temperature',
        'pressure',
        'cooling_time',
        'injection_speed'
      ]);
    } else if (event.target.value === 'cnc_machining') {
      setSelectedParameters([
        'spindle_speed',
        'feed_rate',
        'cut_depth'
      ]);
    }
  };

  const handleTargetVariableChange = (event) => {
    const variable = event.target.value;
    setTargetVariable(variable);
    
    // Automatically set maximize/minimize based on variable
    if (variable === 'energy_consumption' || variable === 'defect_rate') {
      setMaximize(false);
    } else {
      setMaximize(true);
    }
  };

  const getAvailableParameters = () => {
    if (processType === 'injection_molding') {
      return [
        { name: 'temperature', label: 'Temperature (°C)' },
        { name: 'pressure', label: 'Pressure (MPa)' },
        { name: 'cooling_time', label: 'Cooling Time (s)' },
        { name: 'injection_speed', label: 'Injection Speed (cm³/s)' },
        { name: 'mold_temperature', label: 'Mold Temperature (°C)' }
      ];
    } else if (processType === 'cnc_machining') {
      return [
        { name: 'spindle_speed', label: 'Spindle Speed (RPM)' },
        { name: 'feed_rate', label: 'Feed Rate (mm/min)' },
        { name: 'cut_depth', label: 'Cut Depth (mm)' },
        { name: 'tool_diameter', label: 'Tool Diameter (mm)' }
      ];
    }
    return [];
  };

  const getAvailableTargetVariables = () => {
    return [
      { name: 'quality_score', label: 'Quality Score' },
      { name: 'energy_consumption', label: 'Energy Consumption' },
      { name: 'throughput', label: 'Throughput' },
      { name: 'defect_rate', label: 'Defect Rate' },
      { name: 'cycle_time', label: 'Cycle Time' }
    ];
  };

  const toggleParameterSelection = (paramName) => {
    if (selectedParameters.includes(paramName)) {
      setSelectedParameters(selectedParameters.filter(p => p !== paramName));
    } else {
      setSelectedParameters([...selectedParameters, paramName]);
    }
  };

  return (
    <Box className="page-container">
      <Typography variant="h4" component="h1" gutterBottom>
        Optimization
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Optimization Configuration
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
              <InputLabel id="target-variable-label">Optimization Target</InputLabel>
              <Select
                labelId="target-variable-label"
                id="target-variable"
                value={targetVariable}
                label="Optimization Target"
                onChange={handleTargetVariableChange}
              >
                {getAvailableTargetVariables().map((variable) => (
                  <MenuItem key={variable.name} value={variable.name}>
                    {variable.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <FormControlLabel
                control={
                  <Switch
                    checked={maximize}
                    onChange={(e) => setMaximize(e.target.checked)}
                  />
                }
                label={maximize ? "Maximize target" : "Minimize target"}
              />
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="algorithm-label">Optimization Algorithm</InputLabel>
              <Select
                labelId="algorithm-label"
                id="algorithm"
                value={optimizationAlgorithm}
                label="Optimization Algorithm"
                onChange={(e) => setOptimizationAlgorithm(e.target.value)}
              >
                <MenuItem value="bayesian_optimization">Bayesian Optimization</MenuItem>
                <MenuItem value="genetic_algorithm">Genetic Algorithm</MenuItem>
                <MenuItem value="grid_search">Grid Search</MenuItem>
              </Select>
            </FormControl>
            
            <Box sx={{ mt: 3 }}>
              <Button
                variant="contained"
                color="primary"
                startIcon={<TuneIcon />}
                fullWidth
              >
                Run Optimization
              </Button>
              <Button
                variant="outlined"
                startIcon={<CompareArrowsIcon />}
                fullWidth
                sx={{ mt: 2 }}
              >
                Multi-Objective Optimization
              </Button>
            </Box>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Optimization History
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <List disablePadding>
              <ListItem divider>
                <ListItemText
                  primary="Quality Score Optimization"
                  secondary="Injection Molding • 2023-04-18"
                  primaryTypographyProps={{ variant: 'subtitle2' }}
                />
                <Chip 
                  icon={<ArrowUpwardIcon fontSize="small" />} 
                  label="+14.2%" 
                  color="success" 
                  size="small"
                />
              </ListItem>
              
              <ListItem divider>
                <ListItemText
                  primary="Energy Consumption Optimization"
                  secondary="Injection Molding • 2023-04-17"
                  primaryTypographyProps={{ variant: 'subtitle2' }}
                />
                <Chip 
                  icon={<ArrowDownwardIcon fontSize="small" />} 
                  label="-8.7%" 
                  color="success" 
                  size="small"
                />
              </ListItem>
              
              <ListItem>
                <ListItemText
                  primary="Throughput Optimization"
                  secondary="CNC Machining • 2023-04-15"
                  primaryTypographyProps={{ variant: 'subtitle2' }}
                />
                <Chip 
                  icon={<ArrowUpwardIcon fontSize="small" />} 
                  label="+5.3%" 
                  color="success" 
                  size="small"
                />
              </ListItem>
            </List>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Parameters to Optimize
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
              Select parameters to optimize:
            </Typography>
            
            <Grid container spacing={1}>
              {getAvailableParameters().map((param) => (
                <Grid item key={param.name}>
                  <Chip
                    label={param.label}
                    color={selectedParameters.includes(param.name) ? "primary" : "default"}
                    variant={selectedParameters.includes(param.name) ? "filled" : "outlined"}
                    onClick={() => toggleParameterSelection(param.name)}
                    sx={{ m: 0.5 }}
                  />
                </Grid>
              ))}
            </Grid>
            
            <Typography variant="body2" color="textSecondary" sx={{ mt: 3, mb: 2 }}>
              Constraints (optional):
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Maximum Energy Consumption"
                  variant="outlined"
                  type="number"
                  fullWidth
                  InputProps={{
                    endAdornment: <Typography variant="caption">kWh/h</Typography>
                  }}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Maximum Defect Rate"
                  variant="outlined"
                  type="number"
                  fullWidth
                  InputProps={{
                    endAdornment: <Typography variant="caption">%</Typography>
                  }}
                />
              </Grid>
              
              <Grid item xs={12}>
                <FormControlLabel
                  control={<Switch defaultChecked />}
                  label="Treat constraints as hard limits"
                />
              </Grid>
            </Grid>
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Optimization Results
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Alert severity="info" sx={{ mb: 3 }}>
              Run an optimization to see results here. Optimization typically takes 2-5 minutes depending on complexity.
            </Alert>
            
            <Box sx={{ mb: 3, display: 'none' }}>
              <Typography variant="body2" sx={{ mb: 1 }}>
                Optimization in progress...
              </Typography>
              <LinearProgress />
              <Typography variant="caption" color="textSecondary" sx={{ mt: 0.5, display: 'block' }}>
                Iteration 23/100 - Estimated time remaining: 2 minutes
              </Typography>
            </Box>
            
            <Grid container spacing={3} sx={{ display: 'none' }}>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      Optimization Summary
                    </Typography>
                    <Typography variant="body2">
                      Target Variable: Quality Score
                    </Typography>
                    <Typography variant="body2">
                      Initial Value: 0.82
                    </Typography>
                    <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <span>Optimized Value: 0.94</span>
                      <Chip
                        size="small"
                        label="+14.6%"
                        color="success"
                        sx={{ ml: 1 }}
                      />
                    </Typography>
                    
                    <Divider sx={{ my: 1 }} />
                    
                    <Typography variant="subtitle2">
                      Impact on other metrics:
                    </Typography>
                    <Grid container>
                      <Grid item xs={8}>
                        <Typography variant="body2">
                          Energy Consumption:
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography variant="body2" color="error">
                          +5.2%
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={8}>
                        <Typography variant="body2">
                          Throughput:
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography variant="body2" color="success">
                          +2.3%
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={8}>
                        <Typography variant="body2">
                          Defect Rate:
                        </Typography>
                      </Grid>
                      <Grid item xs={4}>
                        <Typography variant="body2" color="success">
                          -8.7%
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                  <CardActions>
                    <Button size="small">Apply to Digital Twin</Button>
                    <Button size="small">Export</Button>
                  </CardActions>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      Optimized Parameters
                    </Typography>
                    
                    <Grid container>
                      <Grid item xs={7}>
                        <Typography variant="body2">
                          Temperature:
                        </Typography>
                      </Grid>
                      <Grid item xs={5}>
                        <Typography variant="body2">
                          215°C (was 230°C)
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={7}>
                        <Typography variant="body2">
                          Pressure:
                        </Typography>
                      </Grid>
                      <Grid item xs={5}>
                        <Typography variant="body2">
                          120 MPa (was 100 MPa)
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={7}>
                        <Typography variant="body2">
                          Cooling Time:
                        </Typography>
                      </Grid>
                      <Grid item xs={5}>
                        <Typography variant="body2">
                          15s (was 20s)
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={7}>
                        <Typography variant="body2">
                          Injection Speed:
                        </Typography>
                      </Grid>
                      <Grid item xs={5}>
                        <Typography variant="body2">
                          65 cm³/s (was 80 cm³/s)
                        </Typography>
                      </Grid>
                    </Grid>
                    
                    <Divider sx={{ my: 1 }} />
                    
                    <Typography variant="subtitle2" gutterBottom>
                      Confidence Score: 92%
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Based on 100 simulation iterations
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Optimization;
