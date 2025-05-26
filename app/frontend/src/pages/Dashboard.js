import React from 'react';
import { 
  Grid, 
  Typography, 
  Box, 
  Paper,
  Button,
  Card,
  CardContent,
  CardActions,
  Divider
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

// Sample dashboard component that would be connected to the actual API
const Dashboard = () => {
  return (
    <Box className="page-container">
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          startIcon={<AddIcon />}
        >
          New Digital Twin
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Summary Cards */}
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography variant="h6" color="textSecondary" gutterBottom>
              Active Digital Twins
            </Typography>
            <Typography variant="h3" component="div" sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              3
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography variant="h6" color="textSecondary" gutterBottom>
              Optimization Runs
            </Typography>
            <Typography variant="h3" component="div" sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              12
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography variant="h6" color="textSecondary" gutterBottom>
              Avg. Quality Improvement
            </Typography>
            <Typography variant="h3" component="div" sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              +14.3%
            </Typography>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 140 }}>
            <Typography variant="h6" color="textSecondary" gutterBottom>
              Energy Savings
            </Typography>
            <Typography variant="h3" component="div" sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              -8.7%
            </Typography>
          </Paper>
        </Grid>

        {/* Active Digital Twins */}
        <Grid item xs={12}>
          <Typography variant="h5" sx={{ mt: 2, mb: 2 }}>Active Digital Twins</Typography>
          <Divider />
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card className="dashboard-card">
            <CardContent className="dashboard-card-content">
              <Typography variant="h6" component="div">
                Injection Molding Line #1
              </Typography>
              <Typography color="textSecondary" sx={{ mb: 2 }}>
                Status: Running
              </Typography>
              
              <Typography variant="body2" component="p" gutterBottom>
                Process Type: Injection Molding
              </Typography>
              
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" component="div">
                  Current Quality Score: 0.92
                </Typography>
                <Typography variant="body2" component="div">
                  Defect Rate: 1.2%
                </Typography>
                <Typography variant="body2" component="div">
                  Energy Efficiency: High
                </Typography>
              </Box>
            </CardContent>
            <CardActions>
              <Button size="small" color="primary">View Details</Button>
              <Button size="small">Run Scenario</Button>
            </CardActions>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card className="dashboard-card">
            <CardContent className="dashboard-card-content">
              <Typography variant="h6" component="div">
                CNC Machining Cell
              </Typography>
              <Typography color="textSecondary" sx={{ mb: 2 }}>
                Status: Running
              </Typography>
              
              <Typography variant="body2" component="p" gutterBottom>
                Process Type: CNC Machining
              </Typography>
              
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" component="div">
                  Current Quality Score: 0.89
                </Typography>
                <Typography variant="body2" component="div">
                  Defect Rate: 2.1%
                </Typography>
                <Typography variant="body2" component="div">
                  Energy Efficiency: Medium
                </Typography>
              </Box>
            </CardContent>
            <CardActions>
              <Button size="small" color="primary">View Details</Button>
              <Button size="small">Run Scenario</Button>
            </CardActions>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card className="dashboard-card">
            <CardContent className="dashboard-card-content">
              <Typography variant="h6" component="div">
                Assembly Line #3
              </Typography>
              <Typography color="textSecondary" sx={{ mb: 2 }}>
                Status: Running
              </Typography>
              
              <Typography variant="body2" component="p" gutterBottom>
                Process Type: Assembly Line
              </Typography>
              
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" component="div">
                  Current Quality Score: 0.95
                </Typography>
                <Typography variant="body2" component="div">
                  Defect Rate: 0.8%
                </Typography>
                <Typography variant="body2" component="div">
                  Energy Efficiency: Very High
                </Typography>
              </Box>
            </CardContent>
            <CardActions>
              <Button size="small" color="primary">View Details</Button>
              <Button size="small">Run Scenario</Button>
            </CardActions>
          </Card>
        </Grid>

        {/* Recent Optimizations */}
        <Grid item xs={12}>
          <Typography variant="h5" sx={{ mt: 2, mb: 2 }}>Recent Optimizations</Typography>
          <Divider />
          
          <Paper sx={{ mt: 2, overflow: 'hidden' }}>
            <Box sx={{ p: 2 }}>
              <Typography variant="h6">
                Injection Molding Parameter Optimization
              </Typography>
              <Typography variant="body2">
                Completed 2 hours ago • Quality Score: +8.5% • Energy: -12.3%
              </Typography>
            </Box>
            <Divider />
            
            <Box sx={{ p: 2 }}>
              <Typography variant="h6">
                CNC Tool Path Optimization
              </Typography>
              <Typography variant="body2">
                Completed 5 hours ago • Cycle Time: -15.2% • Tool Wear: -24.8%
              </Typography>
            </Box>
            <Divider />
            
            <Box sx={{ p: 2 }}>
              <Typography variant="h6">
                Assembly Line Sequence Optimization
              </Typography>
              <Typography variant="body2">
                Completed 1 day ago • Throughput: +5.7% • Quality Score: +2.3%
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
