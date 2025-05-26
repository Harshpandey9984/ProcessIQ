import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tooltip
} from '@mui/material';

import DashboardIcon from '@mui/icons-material/Dashboard';
import DeviceHubIcon from '@mui/icons-material/DeviceHub';
import ScienceIcon from '@mui/icons-material/Science';
import TuneIcon from '@mui/icons-material/Tune';
import PsychologyIcon from '@mui/icons-material/Psychology';
import SettingsIcon from '@mui/icons-material/Settings';

const menuItems = [
  {
    text: 'Dashboard',
    icon: <DashboardIcon />,
    path: '/'
  },
  {
    text: 'Digital Twins',
    icon: <DeviceHubIcon />,
    path: '/digital-twins'
  },
  {
    text: 'Simulation',
    icon: <ScienceIcon />,
    path: '/simulation'
  },
  {
    text: 'Optimization',
    icon: <TuneIcon />,
    path: '/optimization'
  },
  {
    text: 'ML Models',
    icon: <PsychologyIcon />,
    path: '/models'
  },
  {
    text: 'Settings',
    icon: <SettingsIcon />,
    path: '/settings'
  }
];

const Sidebar = ({ open }) => {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <List>
      {menuItems.map((item) => (
        <ListItem key={item.text} disablePadding sx={{ display: 'block' }}>
          <ListItemButton
            sx={{
              minHeight: 48,
              justifyContent: open ? 'initial' : 'center',
              px: 2.5,
              backgroundColor: location.pathname === item.path ? 'rgba(0, 113, 197, 0.08)' : 'transparent',
            }}
            onClick={() => navigate(item.path)}
          >
            <Tooltip title={open ? '' : item.text} placement="right">
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: open ? 3 : 'auto',
                  justifyContent: 'center',
                  color: location.pathname === item.path ? 'primary.main' : 'inherit'
                }}
              >
                {item.icon}
              </ListItemIcon>
            </Tooltip>
            <ListItemText 
              primary={item.text} 
              sx={{ 
                opacity: open ? 1 : 0,
                color: location.pathname === item.path ? 'primary.main' : 'inherit',
                fontWeight: location.pathname === item.path ? 500 : 400
              }} 
            />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );
};

export default Sidebar;
