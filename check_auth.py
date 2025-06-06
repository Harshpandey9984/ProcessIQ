import
requests
print
Checking health endpoint...
try:
    response = requests.get('http://localhost:8001/health')
    print(f'Health endpoint status: {response.status_code}')
    print(f'Response: {response.json()}')
except
Exception
as
e:
    print(f'Error checking health: {str(e)}')
print
\nChecking debug auth config...
try:
    response = requests.get('http://localhost:8001/debug/auth')
    print(f'Debug auth config status: {response.status_code}')
    print(f'Response: {response.json()}')
except
Exception
as
e:
    print(f'Error checking debug auth: {str(e)}')
