"""
Simplified script to check frontend to backend connectivity.
"""
import http.server
import socketserver
import webbrowser
import os
import threading
import time

# Configure the server
PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# HTML content to serve
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Digital Twin Platform - API Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #333; }
        .card { background: white; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 20px; margin-bottom: 20px; }
        button { background: #4CAF50; border: none; color: white; padding: 10px 15px; cursor: pointer; margin-right: 10px; border-radius: 4px; }
        button:hover { background: #45a049; }
        pre { background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }
        .error { color: red; }
        .success { color: green; }
        .log-container { max-height: 300px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Digital Twin Platform - API Test</h1>
        
        <div class="card">
            <h2>1. Server Health Check</h2>
            <button onclick="checkHealth()">Check Backend Health</button>
            <div id="health-result"></div>
        </div>
        
        <div class="card">
            <h2>2. Authentication Test</h2>
            <button onclick="testLogin()">Test Login</button>
            <div id="auth-result"></div>
        </div>
        
        <div class="card">
            <h2>3. API Data Test</h2>
            <button onclick="fetchData()">Fetch Digital Twins</button>
            <div id="data-result"></div>
        </div>
        
        <div class="card">
            <h2>Log</h2>
            <div class="log-container">
                <pre id="log"></pre>
            </div>
        </div>
    </div>

    <script>
        // Function to log messages
        function log(message, isError = false) {
            const logElement = document.getElementById('log');
            const timestamp = new Date().toLocaleTimeString();
            const logMessage = `[${timestamp}] ${message}`;
            
            if (isError) {
                console.error(logMessage);
                logElement.innerHTML += `<span style="color:red">${logMessage}</span>\n`;
            } else {
                console.log(logMessage);
                logElement.innerHTML += `${logMessage}\n`;
            }
            
            // Auto-scroll to bottom
            logElement.scrollTop = logElement.scrollHeight;
        }
        
        // Health check
        async function checkHealth() {
            const resultElement = document.getElementById('health-result');
            resultElement.innerHTML = 'Checking health...';
            
            try {
                log('Checking backend health at http://localhost:8001/health');
                const response = await fetch('http://localhost:8001/health');
                const data = await response.json();
                
                if (response.ok) {
                    resultElement.innerHTML = `<div class="success">Backend is healthy!</div><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    log('Backend health check: SUCCESS');
                } else {
                    resultElement.innerHTML = `<div class="error">Backend health check failed with status ${response.status}</div>`;
                    log(`Backend health check failed: ${response.status}`, true);
                }
            } catch (error) {
                resultElement.innerHTML = `<div class="error">Backend connectivity error: ${error.message}</div>`;
                log(`Backend health check error: ${error.message}`, true);
            }
        }
        
        // Login test
        async function testLogin() {
            const resultElement = document.getElementById('auth-result');
            resultElement.innerHTML = 'Testing login...';
            
            try {
                // Create form data
                const formData = new URLSearchParams();
                formData.append('username', 'admin@example.com');
                formData.append('password', 'password');
                
                log('Testing login with admin@example.com / password');
                log(`POST http://localhost:8001/api/auth/token`);
                log(`Content-Type: application/x-www-form-urlencoded`);
                log(`Body: ${formData.toString()}`);
                
                const response = await fetch('http://localhost:8001/api/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    resultElement.innerHTML = `<div class="success">Login successful!</div><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    log('Login test: SUCCESS');
                    // Store token
                    localStorage.setItem('dt_auth_token', data.access_token);
                } else {
                    resultElement.innerHTML = `<div class="error">Login failed with status ${response.status}</div><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    log(`Login test failed: ${response.status} - ${JSON.stringify(data)}`, true);
                }
            } catch (error) {
                resultElement.innerHTML = `<div class="error">Login error: ${error.message}</div>`;
                log(`Login test error: ${error.message}`, true);
            }
        }
        
        // Fetch data test
        async function fetchData() {
            const resultElement = document.getElementById('data-result');
            resultElement.innerHTML = 'Fetching data...';
            
            // Get token
            const token = localStorage.getItem('dt_auth_token');
            if (!token) {
                resultElement.innerHTML = `<div class="error">No auth token found. Please login first.</div>`;
                log('Fetch data failed: No auth token', true);
                return;
            }
            
            try {
                log('Fetching digital twins data');
                log(`GET http://localhost:8001/api/digital-twin`);
                log(`Authorization: Bearer ${token.substring(0, 10)}...`);
                
                const response = await fetch('http://localhost:8001/api/digital-twin', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    resultElement.innerHTML = `<div class="success">Data fetched successfully!</div><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    log('Fetch data test: SUCCESS');
                } else {
                    resultElement.innerHTML = `<div class="error">Data fetch failed with status ${response.status}</div><pre>${JSON.stringify(data, null, 2)}</pre>`;
                    log(`Fetch data test failed: ${response.status} - ${JSON.stringify(data)}`, true);
                }
            } catch (error) {
                resultElement.innerHTML = `<div class="error">Data fetch error: ${error.message}</div>`;
                log(`Fetch data test error: ${error.message}`, true);
            }
        }
        
        // Log startup
        log('API Test tool loaded. Ready for testing.');
    </script>
</body>
</html>
"""

# Create a custom request handler
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML content for any request
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode())

def start_server():
    with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Server started at http://localhost:{PORT}")
        httpd.serve_forever()

def main():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait a moment for the server to start
    time.sleep(1)
    
    # Open the browser
    url = f"http://localhost:{PORT}"
    print(f"Opening API test tool in browser: {url}")
    webbrowser.open(url)
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    main()
