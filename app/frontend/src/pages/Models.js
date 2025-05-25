import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CardActions, 
  Button,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  LinearProgress,
  Chip,
  Divider
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import AssessmentIcon from '@mui/icons-material/Assessment';

// Mock data until API integration is complete
const SAMPLE_MODELS = [
  {
    id: 'model-001',
    name: 'Defect Predictor',
    type: 'classification',
    algorithm: 'Random Forest',
    accuracy: 0.92,
    created: '2023-05-15',
    lastTrained: '2023-06-20',
    status: 'active'
  },
  {
    id: 'model-002',
    name: 'Process Yield Predictor',
    type: 'regression',
    algorithm: 'XGBoost',
    accuracy: 0.89,
    created: '2023-04-10',
    lastTrained: '2023-06-15',
    status: 'active'
  },
  {
    id: 'model-003',
    name: 'Maintenance Scheduler',
    type: 'time-series',
    algorithm: 'LSTM',
    accuracy: 0.85,
    created: '2023-03-22',
    lastTrained: '2023-05-30',
    status: 'training'
  },
  {
    id: 'model-004',
    name: 'Energy Consumption Optimizer',
    type: 'regression',
    algorithm: 'Neural Network',
    accuracy: 0.91,
    created: '2023-02-18',
    lastTrained: '2023-06-05',
    status: 'active'
  }
];

const ModelStatus = ({ status }) => {
  let color;
  switch (status) {
    case 'active':
      color = 'success';
      break;
    case 'training':
      color = 'warning';
      break;
    case 'failed':
      color = 'error';
      break;
    default:
      color = 'default';
  }
  
  return <Chip label={status} color={color} size="small" />;
};

const Models = () => {
  const [tabValue, setTabValue] = useState(0);
  const [models, setModels] = useState(SAMPLE_MODELS);
  const [openNewModel, setOpenNewModel] = useState(false);
  const [openTrainModel, setOpenTrainModel] = useState(false);
  const [selectedModel, setSelectedModel] = useState(null);

  // This would be replaced with actual API calls
  useEffect(() => {
    // Fetch models from API when implemented
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleNewModel = () => {
    setOpenNewModel(true);
  };

  const handleCloseNewModel = () => {
    setOpenNewModel(false);
  };

  const handleTrainModel = (model) => {
    setSelectedModel(model);
    setOpenTrainModel(true);
  };

  const handleCloseTrainModel = () => {
    setOpenTrainModel(false);
    setSelectedModel(null);
  };

  return (
    <Box className="page-container">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          ML Models
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<AddIcon />}
          onClick={handleNewModel}
        >
          New Model
        </Button>
      </Box>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="All Models" />
          <Tab label="Classification" />
          <Tab label="Regression" />
          <Tab label="Time Series" />
        </Tabs>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Algorithm</TableCell>
              <TableCell>Accuracy</TableCell>
              <TableCell>Last Trained</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {models.map((model) => (
              <TableRow key={model.id}>
                <TableCell>{model.name}</TableCell>
                <TableCell>{model.type}</TableCell>
                <TableCell>{model.algorithm}</TableCell>
                <TableCell>{model.accuracy.toFixed(2)}</TableCell>
                <TableCell>{model.lastTrained}</TableCell>
                <TableCell>
                  <ModelStatus status={model.status} />
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button size="small" startIcon={<PlayArrowIcon />} onClick={() => handleTrainModel(model)}>
                      Train
                    </Button>
                    <Button size="small" startIcon={<AssessmentIcon />}>
                      Evaluate
                    </Button>
                    <Button size="small" startIcon={<EditIcon />}>
                      Edit
                    </Button>
                    <Button size="small" color="error" startIcon={<DeleteIcon />}>
                      Delete
                    </Button>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Create New Model Dialog */}
      <Dialog open={openNewModel} onClose={handleCloseNewModel} maxWidth="md" fullWidth>
        <DialogTitle>Create New ML Model</DialogTitle>
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Model Name"
                variant="outlined"
                required
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Model Type</InputLabel>
                <Select label="Model Type">
                  <MenuItem value="classification">Classification</MenuItem>
                  <MenuItem value="regression">Regression</MenuItem>
                  <MenuItem value="time-series">Time Series</MenuItem>
                  <MenuItem value="clustering">Clustering</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Algorithm</InputLabel>
                <Select label="Algorithm">
                  <MenuItem value="random-forest">Random Forest</MenuItem>
                  <MenuItem value="xgboost">XGBoost</MenuItem>
                  <MenuItem value="neural-network">Neural Network</MenuItem>
                  <MenuItem value="lstm">LSTM</MenuItem>
                  <MenuItem value="svm">SVM</MenuItem>
                  <MenuItem value="knn">KNN</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Data Source</InputLabel>
                <Select label="Data Source">
                  <MenuItem value="production-line-1">Production Line 1</MenuItem>
                  <MenuItem value="production-line-2">Production Line 2</MenuItem>
                  <MenuItem value="quality-control">Quality Control</MenuItem>
                  <MenuItem value="custom">Custom Upload</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Intel Optimization Options
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Hardware Target</InputLabel>
                    <Select label="Hardware Target" defaultValue="cpu-avx512">
                      <MenuItem value="cpu-avx512">CPU (AVX-512)</MenuItem>
                      <MenuItem value="gpu">GPU</MenuItem>
                      <MenuItem value="nnpi">Neural Network Processor</MenuItem>
                      <MenuItem value="vpu">Vision Processing Unit</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={4}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Optimization Level</InputLabel>
                    <Select label="Optimization Level" defaultValue="2">
                      <MenuItem value="0">None</MenuItem>
                      <MenuItem value="1">Basic</MenuItem>
                      <MenuItem value="2">Performance</MenuItem>
                      <MenuItem value="3">Extreme</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={4}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Quantization</InputLabel>
                    <Select label="Quantization" defaultValue="fp16">
                      <MenuItem value="none">None</MenuItem>
                      <MenuItem value="fp16">FP16</MenuItem>
                      <MenuItem value="int8">INT8</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseNewModel}>Cancel</Button>
          <Button variant="contained" color="primary">Create Model</Button>
        </DialogActions>
      </Dialog>

      {/* Train Model Dialog */}
      <Dialog open={openTrainModel} onClose={handleCloseTrainModel} maxWidth="md" fullWidth>
        <DialogTitle>Train Model: {selectedModel?.name}</DialogTitle>
        <DialogContent>
          {selectedModel && (
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Training Dataset</InputLabel>
                  <Select label="Training Dataset">
                    <MenuItem value="recent">Recent Production Data</MenuItem>
                    <MenuItem value="historical">Historical Data</MenuItem>
                    <MenuItem value="synthetic">Synthetic Data</MenuItem>
                    <MenuItem value="custom">Custom Upload</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Validation Split (%)"
                  type="number"
                  defaultValue={20}
                  InputProps={{ inputProps: { min: 0, max: 50 } }}
                />
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2" gutterBottom>
                  Hyperparameters
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Grid container spacing={2}>
                  <Grid item xs={6} md={3}>
                    <TextField
                      fullWidth
                      label="Learning Rate"
                      type="number"
                      defaultValue={0.001}
                      size="small"
                    />
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <TextField
                      fullWidth
                      label="Batch Size"
                      type="number"
                      defaultValue={32}
                      size="small"
                    />
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <TextField
                      fullWidth
                      label="Epochs"
                      type="number"
                      defaultValue={100}
                      size="small"
                    />
                  </Grid>
                  <Grid item xs={6} md={3}>
                    <FormControl fullWidth size="small">
                      <InputLabel>Early Stopping</InputLabel>
                      <Select label="Early Stopping" defaultValue="yes">
                        <MenuItem value="yes">Yes</MenuItem>
                        <MenuItem value="no">No</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </Grid>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2" gutterBottom>
                  Intel Optimization Options
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <FormControl fullWidth size="small">
                      <InputLabel>Hardware Target</InputLabel>
                      <Select label="Hardware Target" defaultValue="cpu-avx512">
                        <MenuItem value="cpu-avx512">CPU (AVX-512)</MenuItem>
                        <MenuItem value="gpu">GPU</MenuItem>
                        <MenuItem value="nnpi">Neural Network Processor</MenuItem>
                        <MenuItem value="vpu">Vision Processing Unit</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <FormControl fullWidth size="small">
                      <InputLabel>MKL Acceleration</InputLabel>
                      <Select label="MKL Acceleration" defaultValue="enabled">
                        <MenuItem value="enabled">Enabled</MenuItem>
                        <MenuItem value="disabled">Disabled</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <FormControl fullWidth size="small">
                      <InputLabel>Thread Count</InputLabel>
                      <Select label="Thread Count" defaultValue="auto">
                        <MenuItem value="auto">Auto</MenuItem>
                        <MenuItem value="4">4</MenuItem>
                        <MenuItem value="8">8</MenuItem>
                        <MenuItem value="16">16</MenuItem>
                        <MenuItem value="32">32</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseTrainModel}>Cancel</Button>
          <Button variant="contained" color="primary">Start Training</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Models;
