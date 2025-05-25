import React, { useState, useEffect } from 'react';
import { 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  CardActions,
  Button,
  Fab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Divider,
  CircularProgress,
  Snackbar,
  Alert
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import digitalTwinService from '../services/digitalTwinService';

const DigitalTwins = () => {
  const [open, setOpen] = useState(false);
  const [digitalTwins, setDigitalTwins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success'
  });
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    process_type: 'injection_molding',
    description: '',
    parameters: {
      temperature: 230,
      pressure: 100,
      cooling_time: 20,
      injection_speed: 80
    },
    simulation_settings: {
      update_frequency: 1,
      simulation_speed_factor: 1
    }
  });

  // Load digital twins on component mount
  useEffect(() => {
    fetchDigitalTwins();
  }, []);

  // Function to fetch digital twins from the API
  const fetchDigitalTwins = async () => {
    setLoading(true);
    try {
      const data = await digitalTwinService.getAllDigitalTwins();
      setDigitalTwins(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching digital twins:', err);
      setError('Failed to load digital twins. Please try again later.');
      // If API fails, use mock data as fallback
      setDigitalTwins([
        {
          id: '1',
          name: 'Injection Molding Line #1',
          process_type: 'injection_molding',
          status: 'running',
          created_at: '2023-04-01T10:30:00Z',
          current_metrics: {
            quality_score: 0.92,
            defect_rate: 0.012,
            energy_consumption: 120.5,
            throughput: 42.3
          }
        },
        {
          id: '2',
          name: 'CNC Machining Cell',
          process_type: 'cnc_machining',
          status: 'running',
          created_at: '2023-04-02T09:15:00Z',
          current_metrics: {
            quality_score: 0.89,
            defect_rate: 0.021,
            energy_consumption: 75.2,
            throughput: 18.7
          }
        },
        {
          id: '3',
          name: 'Assembly Line #3',
          process_type: 'assembly_line',
          status: 'running',
          created_at: '2023-04-03T14:45:00Z',
          current_metrics: {
            quality_score: 0.95,
            defect_rate: 0.008,
            energy_consumption: 62.8,
            throughput: 156.2
          }
        }
      ]);
    } finally {
      setLoading(false);
    }
  };
  
  const handleClickOpen = () => {
    setOpen(true);
  };
  
  const handleClose = () => {
    setOpen(false);
    // Reset form data
    setFormData({
      name: '',
      process_type: 'injection_molding',
      description: '',
      parameters: {
        temperature: 230,
        pressure: 100,
        cooling_time: 20,
        injection_speed: 80
      },
      simulation_settings: {
        update_frequency: 1,
        simulation_speed_factor: 1
      }
    });
  };
  
  const handleInputChange = (e) => {
    const { id, value } = e.target;
    if (id === 'name' || id === 'description') {
      setFormData({
        ...formData,
        [id]: value
      });
    } else if (id === 'process-type') {
      setFormData({
        ...formData,
        process_type: value
      });
    } else if (id.startsWith('param-')) {
      const paramName = id.replace('param-', '').replace(/-/g, '_');
      setFormData({
        ...formData,
        parameters: {
          ...formData.parameters,
          [paramName]: Number(value)
        }
      });
    } else if (id === 'update-frequency' || id === 'simulation-speed-factor') {
      const settingName = id.replace(/-/g, '_');
      setFormData({
        ...formData,
        simulation_settings: {
          ...formData.simulation_settings,
          [settingName]: Number(value)
        }
      });
    }
  };

  const handleCreateDigitalTwin = async () => {
    try {
      await digitalTwinService.createDigitalTwin(formData);
      setSnackbar({
        open: true,
        message: 'Digital Twin created successfully!',
        severity: 'success'
      });
      handleClose();
      fetchDigitalTwins(); // Refresh the list
    } catch (err) {
      console.error('Error creating digital twin:', err);
      setSnackbar({
        open: true,
        message: 'Failed to create Digital Twin. Please try again.',
        severity: 'error'
      });
    }
  };
  
  const handleViewDetails = (id) => {
    // Navigate to details page or open details dialog
    console.log(`View details for twin ${id}`);
  };
  
  const handleRunScenario = (id) => {
    // Navigate to simulation page or open scenario dialog
    console.log(`Run scenario for twin ${id}`);
  };
  
  const handleOptimize = (id) => {
    // Navigate to optimization page or open optimization dialog
    console.log(`Optimize twin ${id}`);
  };

  const handleCloseSnackbar = () => {
    setSnackbar({...snackbar, open: false});
  };

  return (
    <Box className="page-container">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Digital Twins
        </Typography>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
      ) : digitalTwins.length === 0 ? (
        <Box sx={{ textAlign: 'center', my: 4 }}>
          <Typography variant="body1" color="text.secondary">
            No digital twins found. Click the + button to create your first digital twin.
          </Typography>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {digitalTwins.map((twin) => (
            <Grid item xs={12} md={4} key={twin.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" component="div">
                    {twin.name}
                  </Typography>
                  <Typography color="textSecondary" sx={{ mb: 2 }}>
                    Status: {twin.status.charAt(0).toUpperCase() + twin.status.slice(1)}
                  </Typography>
                  
                  <Typography variant="body2" component="p" gutterBottom>
                    Process Type: {twin.process_type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </Typography>
                  
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2" component="div">
                      Quality Score: {twin.current_metrics.quality_score.toFixed(2)}
                    </Typography>
                    <Typography variant="body2" component="div">
                      Defect Rate: {(twin.current_metrics.defect_rate * 100).toFixed(1)}%
                    </Typography>
                    <Typography variant="body2" component="div">
                      Energy Consumption: {twin.current_metrics.energy_consumption.toFixed(1)} kWh/h
                    </Typography>
                    <Typography variant="body2" component="div">
                      Throughput: {twin.current_metrics.throughput.toFixed(1)} units/h
                    </Typography>
                  </Box>
                </CardContent>
                <CardActions>
                  <Button size="small" color="primary" onClick={() => handleViewDetails(twin.id)}>
                    View Details
                  </Button>
                  <Button size="small" onClick={() => handleRunScenario(twin.id)}>
                    Run Scenario
                  </Button>
                  <Button size="small" color="secondary" onClick={() => handleOptimize(twin.id)}>
                    Optimize
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Fab 
        color="primary" 
        aria-label="add" 
        sx={{ position: 'fixed', bottom: 20, right: 20 }}
        onClick={handleClickOpen}
      >
        <AddIcon />
      </Fab>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Digital Twin</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Digital Twin Name"
              type="text"
              fullWidth
              variant="outlined"
              value={formData.name}
              onChange={handleInputChange}
              sx={{ mb: 2 }}
            />            <TextField
              select
              margin="dense"
              id="process-type"
              label="Process Type"
              fullWidth
              variant="outlined"
              value={formData.process_type}
              onChange={handleInputChange}
              sx={{ mb: 2 }}
            >
              <MenuItem value="injection_molding">Injection Molding</MenuItem>
              <MenuItem value="cnc_machining">CNC Machining</MenuItem>
              <MenuItem value="assembly_line">Assembly Line</MenuItem>
              <MenuItem value="chemical_process">Chemical Process</MenuItem>
              <MenuItem value="packaging_line">Packaging Line</MenuItem>
            </TextField>
            
            <TextField
              margin="dense"
              id="description"
              label="Description"
              type="text"
              fullWidth
              multiline
              rows={2}
              variant="outlined"
              value={formData.description}
              onChange={handleInputChange}
              sx={{ mb: 2 }}
            />
            
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle1" gutterBottom>
              Initial Parameters
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="dense"
                  id="param-temperature"
                  label="Temperature (°C)"
                  type="number"
                  fullWidth
                  variant="outlined"
                  value={formData.parameters.temperature}
                  onChange={handleInputChange}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="dense"
                  id="param-pressure"
                  label="Pressure (MPa)"
                  type="number"
                  fullWidth
                  variant="outlined"
                  value={formData.parameters.pressure}
                  onChange={handleInputChange}
                />              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="dense"
                  id="param-cooling-time"
                  label="Cooling Time (s)"
                  type="number"
                  fullWidth
                  variant="outlined"
                  value={formData.parameters.cooling_time}
                  onChange={handleInputChange}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="dense"
                  id="param-injection-speed"
                  label="Injection Speed (cm³/s)"
                  type="number"
                  fullWidth
                  variant="outlined"
                  value={formData.parameters.injection_speed}
                  onChange={handleInputChange}
                />
              </Grid>
            </Grid>
            
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle1" gutterBottom>
              Simulation Settings
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="dense"
                  id="update-frequency"
                  label="Update Frequency (Hz)"
                  type="number"
                  fullWidth
                  variant="outlined"
                  value={formData.simulation_settings.update_frequency}
                  onChange={handleInputChange}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  margin="dense"
                  id="simulation-speed-factor"
                  label="Simulation Speed Factor"
                  type="number"
                  fullWidth
                  variant="outlined"
                  value={formData.simulation_settings.simulation_speed_factor}
                  onChange={handleInputChange}
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleCreateDigitalTwin} variant="contained" color="primary">Create</Button>
        </DialogActions>
      </Dialog>
      
      <Snackbar 
        open={snackbar.open} 
        autoHideDuration={6000} 
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default DigitalTwins;
