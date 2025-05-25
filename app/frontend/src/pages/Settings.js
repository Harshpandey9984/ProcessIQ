import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CardHeader,
  Button,
  TextField,
  FormControl,
  FormControlLabel,
  FormGroup,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  Divider,
  Tabs,
  Tab,
  Alert,
  Slider,
  Chip
} from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import SecurityIcon from '@mui/icons-material/Security';
import StorageIcon from '@mui/icons-material/Storage';
import TuneIcon from '@mui/icons-material/Tune';
import NotificationsIcon from '@mui/icons-material/Notifications';
import SettingsBackupRestoreIcon from '@mui/icons-material/SettingsBackupRestore';
import IntegrationInstructionsIcon from '@mui/icons-material/IntegrationInstructions';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const Settings = () => {
  const [tabValue, setTabValue] = useState(0);
  const [saved, setSaved] = useState(false);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    setSaved(false);
  };

  const handleSave = () => {
    // This would call an API to save settings
    setSaved(true);
    setTimeout(() => {
      setSaved(false);
    }, 3000);
  };

  return (
    <Box className="page-container">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Settings
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<SaveIcon />}
          onClick={handleSave}
        >
          Save Settings
        </Button>
      </Box>

      {saved && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Settings saved successfully!
        </Alert>
      )}

      <Card>
        <CardContent>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="settings tabs">
              <Tab icon={<TuneIcon />} label="General" />
              <Tab icon={<SecurityIcon />} label="Security" />
              <Tab icon={<StorageIcon />} label="Data Storage" />
              <Tab icon={<NotificationsIcon />} label="Notifications" />
              <Tab icon={<IntegrationInstructionsIcon />} label="API" />
              <Tab icon={<SettingsBackupRestoreIcon />} label="Backup" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Platform Settings</Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <TextField label="Platform Name" variant="outlined" defaultValue="Digital Twin Optimization Platform" />
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Default View</InputLabel>
                  <Select 
                    label="Default View" 
                    defaultValue="dashboard"
                  >
                    <MenuItem value="dashboard">Dashboard</MenuItem>
                    <MenuItem value="digital-twins">Digital Twins</MenuItem>
                    <MenuItem value="simulation">Simulation</MenuItem>
                    <MenuItem value="optimization">Optimization</MenuItem>
                    <MenuItem value="models">Models</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Intel Hardware Configuration</Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Default Compute Device</InputLabel>
                  <Select 
                    label="Default Compute Device" 
                    defaultValue="cpu"
                  >
                    <MenuItem value="cpu">CPU (Intel Xeon)</MenuItem>
                    <MenuItem value="gpu">Intel Iris Xe GPU</MenuItem>
                    <MenuItem value="nnpi">Intel Neural Network Processor</MenuItem>
                    <MenuItem value="vpu">Intel Vision Processing Unit</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Thread Allocation</InputLabel>
                  <Select 
                    label="Thread Allocation" 
                    defaultValue="auto"
                  >
                    <MenuItem value="auto">Automatic (Recommended)</MenuItem>
                    <MenuItem value="manual">Manual Configuration</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography id="performance-slider" gutterBottom>
                  Performance Mode
                </Typography>
                <Slider
                  defaultValue={2}
                  step={1}
                  marks={[
                    { value: 0, label: 'Energy Efficient' },
                    { value: 1, label: 'Balanced' },
                    { value: 2, label: 'Performance' },
                    { value: 3, label: 'Max Performance' }
                  ]}
                  min={0}
                  max={3}
                  valueLabelDisplay="off"
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormGroup>
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable Intel® Advanced Matrix Extensions (AMX)" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable Intel® Math Kernel Library (MKL)" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Use OpenVINO™ for inference acceleration" 
                  />
                </FormGroup>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>UI Preferences</Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Theme</InputLabel>
                  <Select 
                    label="Theme" 
                    defaultValue="system"
                  >
                    <MenuItem value="system">System Default</MenuItem>
                    <MenuItem value="light">Light</MenuItem>
                    <MenuItem value="dark">Dark</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormGroup>
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Show detailed tooltips" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable animations" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Auto-refresh data" 
                  />
                </FormGroup>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Authentication Settings</Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Authentication Method</InputLabel>
                  <Select 
                    label="Authentication Method" 
                    defaultValue="oauth2"
                  >
                    <MenuItem value="local">Local Authentication</MenuItem>
                    <MenuItem value="ldap">LDAP</MenuItem>
                    <MenuItem value="oauth2">OAuth 2.0</MenuItem>
                    <MenuItem value="saml">SAML</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <TextField 
                    label="Session Timeout (minutes)" 
                    type="number" 
                    variant="outlined" 
                    defaultValue={30} 
                  />
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormGroup>
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Require 2FA for all users" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Auto-lock inactive sessions" 
                  />
                </FormGroup>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Password Policy</InputLabel>
                  <Select 
                    label="Password Policy" 
                    defaultValue="strong"
                  >
                    <MenuItem value="basic">Basic</MenuItem>
                    <MenuItem value="standard">Standard</MenuItem>
                    <MenuItem value="strong">Strong</MenuItem>
                    <MenuItem value="custom">Custom</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={tabValue} index={2}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Data Storage Configuration</Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Primary Storage</InputLabel>
                  <Select 
                    label="Primary Storage" 
                    defaultValue="postgres"
                  >
                    <MenuItem value="postgres">PostgreSQL</MenuItem>
                    <MenuItem value="mysql">MySQL</MenuItem>
                    <MenuItem value="sqlserver">SQL Server</MenuItem>
                    <MenuItem value="mongodb">MongoDB</MenuItem>
                    <MenuItem value="timescaledb">TimescaleDB</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <TextField 
                    label="Database Connection String" 
                    variant="outlined" 
                    defaultValue="postgresql://user:password@localhost:5432/digitaltwin" 
                  />
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Time Series Storage</InputLabel>
                  <Select 
                    label="Time Series Storage" 
                    defaultValue="influxdb"
                  >
                    <MenuItem value="influxdb">InfluxDB</MenuItem>
                    <MenuItem value="timescaledb">TimescaleDB</MenuItem>
                    <MenuItem value="prometheus">Prometheus</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <TextField 
                    label="Data Retention Period (days)" 
                    type="number" 
                    variant="outlined" 
                    defaultValue={90} 
                  />
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <FormGroup>
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable data compression" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable automatic backups" 
                  />
                  <FormControlLabel 
                    control={<Switch />} 
                    label="Store data in Intel® Optane™ Memory" 
                  />
                </FormGroup>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={tabValue} index={3}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Notification Settings</Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1">Email Notifications</Typography>
                <FormGroup>
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Send critical alerts" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Send optimization recommendations" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Send system updates" 
                  />
                </FormGroup>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1">In-App Notifications</Typography>
                <FormGroup>
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Show simulation completion alerts" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Show model training updates" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Show digital twin status changes" 
                  />
                </FormGroup>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth sx={{ mt: 2 }}>
                  <TextField 
                    label="Email Recipients (comma separated)" 
                    variant="outlined" 
                    defaultValue="admin@example.com, alerts@example.com" 
                  />
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel>Alert Priority Threshold</InputLabel>
                  <Select 
                    label="Alert Priority Threshold" 
                    defaultValue="medium"
                  >
                    <MenuItem value="low">Low (All Alerts)</MenuItem>
                    <MenuItem value="medium">Medium (Important & Critical)</MenuItem>
                    <MenuItem value="high">High (Critical Only)</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={tabValue} index={4}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>API Configuration</Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <TextField 
                    label="API Base URL" 
                    variant="outlined" 
                    defaultValue="https://api.example.com/v1" 
                  />
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>API Rate Limiting</InputLabel>
                  <Select 
                    label="API Rate Limiting" 
                    defaultValue="medium"
                  >
                    <MenuItem value="low">Low (100 req/min)</MenuItem>
                    <MenuItem value="medium">Medium (500 req/min)</MenuItem>
                    <MenuItem value="high">High (1000 req/min)</MenuItem>
                    <MenuItem value="unlimited">Unlimited</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="subtitle1" sx={{ mt: 2 }}>API Keys</Typography>
                <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="body2" color="text.secondary">Production API Key</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                        <TextField 
                          variant="outlined" 
                          size="small" 
                          value="•••••••••••••••••••••••••••••••"
                          fullWidth
                          InputProps={{ readOnly: true }} 
                        />
                        <Button size="small" variant="outlined">Regenerate</Button>
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="body2" color="text.secondary">Development API Key</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                        <TextField 
                          variant="outlined" 
                          size="small" 
                          value="•••••••••••••••••••••••••••••••"
                          fullWidth
                          InputProps={{ readOnly: true }} 
                        />
                        <Button size="small" variant="outlined">Regenerate</Button>
                      </Box>
                    </Grid>
                  </Grid>
                </Box>
              </Grid>
              
              <Grid item xs={12}>
                <FormGroup>
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable CORS" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable API authentication" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable API versioning" 
                  />
                  <FormControlLabel 
                    control={<Switch />} 
                    label="Enable API analytics" 
                  />
                </FormGroup>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={tabValue} index={5}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Backup & Restore</Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1">Scheduled Backups</Typography>
                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel>Backup Frequency</InputLabel>
                  <Select 
                    label="Backup Frequency" 
                    defaultValue="daily"
                  >
                    <MenuItem value="hourly">Hourly</MenuItem>
                    <MenuItem value="daily">Daily</MenuItem>
                    <MenuItem value="weekly">Weekly</MenuItem>
                    <MenuItem value="monthly">Monthly</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1">Backup Location</Typography>
                <FormControl fullWidth sx={{ mt: 2 }}>
                  <InputLabel>Storage Type</InputLabel>
                  <Select 
                    label="Storage Type" 
                    defaultValue="s3"
                  >
                    <MenuItem value="local">Local Storage</MenuItem>
                    <MenuItem value="s3">Amazon S3</MenuItem>
                    <MenuItem value="azure">Azure Blob Storage</MenuItem>
                    <MenuItem value="gcp">Google Cloud Storage</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <TextField 
                    label="Retention Period (days)" 
                    type="number" 
                    variant="outlined" 
                    defaultValue={30} 
                  />
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormGroup>
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Enable data encryption" 
                  />
                  <FormControlLabel 
                    control={<Switch defaultChecked />} 
                    label="Compress backups" 
                  />
                </FormGroup>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="subtitle1" sx={{ mt: 2 }}>Manual Backup</Typography>
                <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
                  <Button variant="contained">Create Backup Now</Button>
                  <Button variant="outlined">Restore from Backup</Button>
                </Box>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="subtitle1" sx={{ mt: 2 }}>Recent Backups</Typography>
                <Box sx={{ mt: 1 }}>
                  <Grid container spacing={1}>
                    {['2023-07-01 01:00', '2023-06-30 01:00', '2023-06-29 01:00'].map((date, i) => (
                      <Grid item xs={12} key={i}>
                        <Box sx={{ 
                          display: 'flex', 
                          justifyContent: 'space-between', 
                          alignItems: 'center',
                          p: 1.5,
                          borderRadius: 1,
                          bgcolor: 'background.paper',
                          mb: 1
                        }}>
                          <Box>
                            <Typography variant="body2">{date}</Typography>
                            <Typography variant="caption" color="text.secondary">
                              Size: 256 MB {i === 0 && <Chip label="Latest" size="small" color="primary" sx={{ ml: 1 }} />}
                            </Typography>
                          </Box>
                          <Box>
                            <Button size="small">Download</Button>
                            <Button size="small">Restore</Button>
                          </Box>
                        </Box>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              </Grid>
            </Grid>
          </TabPanel>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Settings;
