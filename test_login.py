import requests

def test_login():
    url = "http://localhost:8001/api/auth/token"
    data = {
        "username": "admin@example.com",
        "password": "password"
    }
    print(f"Trying to login with URL: {url}")
    print(f"Data: {data}")
    
    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        print(f"Headers: {headers}")
        response = requests.post(url, data=data, headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")
        if response.status_code == 200:
            print("Login successful!")
    except Exception as e:
        print(f"Exception: {str(e)}")

def manual_test():
    print("\nManually constructing the request...")
    import urllib.parse
    import http.client
    
    try:
        params = urllib.parse.urlencode({
            'username': 'admin@example.com',
            'password': 'password'
        })
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        conn = http.client.HTTPConnection("localhost", 8001)
        conn.request("POST", "/api/auth/token", params, headers)
        response = conn.getresponse()
        print(f"Status: {response.status} {response.reason}")
        data = response.read()
        print(f"Response: {data.decode('utf-8')}")
        conn.close()
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    test_login()
    manual_test()
