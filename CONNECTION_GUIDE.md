# Digital Twin Platform Connection Guide

## Server Status

The Digital Twin Optimization Platform consists of two main components:

1. **Backend (FastAPI)**: Running on port 8001
2. **Frontend (React)**: Running on port 3000

Both servers appear to be running according to our diagnostics.

## Connection Instructions

### Method 1: Using IP Address (127.0.0.1)

Try accessing the application using the explicit IP address:
- Frontend: http://127.0.0.1:3000
- Backend API: http://127.0.0.1:8001/docs

### Method 2: Using localhost 

Try accessing the application using localhost:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001/docs

### Method 3: Direct API Testing

We've created a testing page to verify the API directly:
1. Open the file `platform_test.html` in your browser
2. Click the buttons to test connections to both servers

## Troubleshooting Steps

If you're still seeing connection issues:

1. **Firewall Settings**:
   - Check if Windows Firewall is blocking connections
   - Temporarily disable firewall or add exceptions for ports 3000 and 8001

2. **Network Configuration**:
   - Check if you're on a VPN that might block local connections
   - Try disabling any proxy settings in your browser

3. **Browser Issues**:
   - Try using a different browser (Chrome, Firefox, Edge)
   - Clear browser cache and cookies

4. **Server Status**:
   - Check the log files in the `logs` directory for any errors
   - Try restarting both servers using the VS Code tasks

5. **Port Conflicts**:
   - Check if other applications might be using the same ports
   - Try changing the ports in the configuration files

## Authentication Credentials

Once connected, use these credentials to log in:
- Admin: admin@example.com / password
- User: user@example.com / password

## Need More Help?

If you're still experiencing issues, please provide any error messages you're seeing from:
- The browser's console (F12 to open developer tools)
- Log files in the `logs` directory
