import React, { useState, useEffect } from 'react';
import { 
  Typography, 
  Box, 
  IconButton, 
  Avatar, 
  Tooltip, 
  Menu, 
  MenuItem, 
  ListItemIcon, 
  ListItemText, 
  Divider,
  Badge
} from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import HelpIcon from '@mui/icons-material/Help';
import SettingsIcon from '@mui/icons-material/Settings';
import PersonIcon from '@mui/icons-material/Person';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { useNavigate } from 'react-router-dom';
import authService from '../../services/authService';

const Header = () => {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const [user, setUser] = useState(null);
  const [notificationCount, setNotificationCount] = useState(3);
  
  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    setUser(currentUser);
  }, []);

  const handleOpenUserMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseUserMenu = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <>
      <Typography
        variant="h6"
        noWrap
        component="div"
        sx={{ flexGrow: 1 }}
      >
        Digital Twin Optimization Platform
      </Typography>
      
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <Tooltip title="Notifications">
          <IconButton color="inherit">
            <Badge badgeContent={notificationCount} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Tooltip>
        
        <Tooltip title="Help">
          <IconButton color="inherit">
            <HelpIcon />
          </IconButton>
        </Tooltip>
        
        <Tooltip title="Settings">
          <IconButton color="inherit" onClick={() => navigate('/settings')}>
            <SettingsIcon />
          </IconButton>
        </Tooltip>
          <Tooltip title="Account">
          <IconButton
            onClick={handleOpenUserMenu}
            size="small"
            sx={{ ml: 1 }}
            aria-controls="user-menu"
            aria-haspopup="true"
          >
            <Avatar 
              sx={{ 
                width: 32, 
                height: 32,
                bgcolor: 'primary.main'
              }} 
            >
              {user ? user.full_name ? user.full_name[0].toUpperCase() : 'U' : 'U'}
            </Avatar>
          </IconButton>
        </Tooltip>
        
        <Menu
          id="user-menu"
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleCloseUserMenu}
          onClick={handleCloseUserMenu}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
          PaperProps={{
            elevation: 0,
            sx: {
              overflow: 'visible',
              filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.2))',
              mt: 1.5,
              width: 200,
              '& .MuiAvatar-root': {
                width: 32,
                height: 32,
                ml: -0.5,
                mr: 1,
              },
            },
          }}
        >
          {user && (
            <MenuItem disabled sx={{ opacity: 0.8 }}>
              <Typography variant="body2">{user.email}</Typography>
            </MenuItem>
          )}
          
          <Divider />
          
          <MenuItem onClick={() => navigate('/settings')}>
            <ListItemIcon>
              <SettingsIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Settings</ListItemText>
          </MenuItem>
          
          <MenuItem onClick={() => navigate('/profile')}>
            <ListItemIcon>
              <PersonIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>My Account</ListItemText>
          </MenuItem>
          
          <Divider />
          
          <MenuItem onClick={handleLogout}>
            <ListItemIcon>
              <ExitToAppIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText>Logout</ListItemText>
          </MenuItem>
        </Menu>
      </Box>
    </>
  );
};

export default Header;
