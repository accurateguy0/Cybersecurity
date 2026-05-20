# nmap:  

Useful flags:  

| -sV | version                                                                                             |
| --- | --------------------------------------------------------------------------------------------------- |
| -p  | Used to specify which port to analyze, can also be used to specify a range of ports i.e `-p 1-1000` |
| -sC | Runs default scripts on the port, useful for doing basic analysis on the service running on a port  |
| -A  | Aggressive mode, go all out and try to get as much information as possible                          |
| -v  | verbose                                                                                             |
nmap -sV -sC -A -v 10.82.171.5
nmap -sV -sC -A -v -Pn 10.112.144.183
nmap --script vuln -p 445, 139 10.112.144.183

I learned that in CTFs like this it’s important to scan the full port range with nmap, so I use the `-p-` option and the faster timing template `-T4`. It takes a while to complete.

sudo nmap -p- -sVC -O 10.10.161.36 -T4

Specifically for SMB:
```bash
nmap --script smb-enum-shares,smb-enum-users,smb-os-discovery 10.80.187.215
```
When port scanning with Nmap, there are three basic scan types. These are:

- TCP Connect Scans (`-sT`)
- SYN "Half-open" Scans (`-sS`)
- UDP Scans (`-sU`)

Additionally there are several less common port scan types, some of which we will also cover (albeit in less detail). These are:

- TCP Null Scans (`-sN`)
- TCP FIN Scans (`-sF`)
- TCP Xmas Scans (`-sX`)
# nslookup
|Query type|Result|
|---|---|
|A|IPv4 Addresses|
|AAAA|IPv6 Addresses|
|CNAME|Canonical Name|
|MX|Mail Servers|
|SOA|Start of Authority|
|TXT|TXT Records|

 `nslookup -type=A tryhackme.com 1.1.1.1`

# dig
For more advanced DNS queries and additional functionality, you can use `dig`, the acronym for “Domain Information Groper,” if you are curious. Let’s use `dig` to look up the MX records and compare them to `nslookup`. We can use `dig DOMAIN_NAME`, but to specify the record type, we would use `dig DOMAIN_NAME TYPE`. Optionally, we can select the server we want to query using `dig @SERVER DOMAIN_NAME TYPE`.

- SERVER is the DNS server that you want to query.
- DOMAIN_NAME is the domain name you are looking up.
- TYPE contains the DNS record type, as shown in the table provided earlier.
# Gobuster

Useful flags:  

|            |                                                                                                                                                                   |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -x         | Used to specify file extensions i.e "php,txt,html"                                                                                                                |
| --url      | Used to specify which url to enumerate                                                                                                                            |
| --wordlist | Used to specify which wordlist that is appended on the url path i.e<br><br>"http://url.com/word1"<br><br>"http://url.com/word2"<br><br>"http://url.com/word3.php" |
Recommended wordlist: [big.txt](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/big.txt)
gobuster dir -u http://10.82.171.5/ -w /usr/share/wordlists/dirb/common.txt
gobuster dir -u http://10.82.171.5/ -w /usr/share/seclists/Discovery/Web-Content/common.txt
gobuster dir -u http://10.82.171.5/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt
gobuster dir -u https://10.82.171.5/ -w /usr/share/wordlists/dirb/common.txt -k
gobuster dir -u http://10.82.171.5/ -w /usr/share/wordlists/dirb/common.txt -t 50
gobuster vhost -u http://10.82.171.5/ -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt

Change your protocol from http to https and add the -k flag to skip certificate validation (common for CTFs).

Run this command instead:

```
gobuster dir -u https://bricks.thm:443 -w /usr/share/wordlists/dirb/common.txt -k
```
# sqlmap

Useful Flags:

|   |   |
|---|---|
|-u|Specifies which url to attack|
|--forms|Automatically selects parameters from <form> elements on the page|
|--dump|Used to retrieve data from the db once SQLI is found|
|-a|Grabs just about everything from the db|
```
sqlmap -u "http://10.65.157.87/administrator.php" --forms --batch -a
```

```
sqlmap -u "http://10.82.171.5/api/login" \
  --method=POST \
  --headers="Content-Type: application/json" \
  --data='{"username": "admin", "password": "password"}' \
  --batch
```
sqlmap -u "http://10.82.171.5/api/login" \
  --method=POST \
  --data="username=admin&password=123" \
  --dbms=sqlite \
  --level=5 --risk=3 \
  --batch
### Breakdown of the Flags

- **--method=POST**: Forces sqlmap to use POST (since GET failed with 405).
    
- **--headers="..."**: Tells the server we are sending JSON data (crucial for APIs).
    
- **--data='...'**: Contains the dummy credentials. sqlmap will replace "admin" and "password" with SQL injection payloads to try and break the database.
    
- **--batch**: Automatically answers "Yes" to standard questions so the scan runs without stopping.

**What this does:**

- **--forms**: Finds the username/password fields in the HTML and tries to inject them.
- **--batch**: (Highly recommended) Tells sqlmap **not** to ask you "Do you want to test this?" 50 times. It will just use the smartest default answers.
- **-a**: This is the "All" flag. It tries to get the DB Banner, the DB User, the Hostname, and all Database names.
    

**Step 1: Find the database names first**

codeBash

```
sqlmap -u "http://10.65.157.87/administrator.php" --forms --batch --dbs
```

**Step 2: Find the tables in the database you found (e.g., "users_db")**

codeBash

```
sqlmap -u "http://10.65.157.87/administrator.php" --forms --batch -D users_db --tables
```

**Step 3: Dump the table that looks interesting (e.g., "users")**



```
sqlmap -u "http://10.65.157.87/administrator.php" --forms --batch -D users_db -T users --dump
```

Some great places to find reverse shell payloads are [highoncoffee](https://highon.coffee/blog/reverse-shell-cheat-sheet/) and [Pentestmonkey](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)

# hashcat
```
hashcat -m 1800 unshadow.txt rockyou.txt -O
```


# hydra
Attack ssh, generic

```
hydra -l [username] -P [path/to/password_list.txt] [target_ip] ssh
```

```
hydra -t 4 -l dale -P /usr/share/wordlists/rockyou.txt -vV 10.81.140.90 ftp
```

Let's break it down:

SECTION             FUNCTION  
  
hydra                   Runs the hydra tool  
  
-t 4                    Number of parallel connections per target  
  
-l [user]               Points to the user who's account you're trying to compromise  
  
-P [path to dictionary] Points to the file containing the list of possible passwords  
  
-vV                     Sets verbose mode to very verbose, shows the login+pass combination for each attempt  
  
[machine IP]            The IP address of the target machine  
  
ftp / protocol          Sets the protocol
# ssh
```
ssh -vvv username@target_ip
```

While this won't explicitly say "Username Correct," the debug output (the "logs" of the handshake) will show you which authentication methods the server is offering (e.g., publickey, password).

# shell
Get a fully interactive shell:
script /dev/null -c bash
Then press _Ctrl+Z_ to get the process in background.

Now that you are in your machine execute the next command:

stty raw -echo;fg

Now write `reset xterm` and you should have a better looking shell but you still have to execute a few commands:

export TERM=xterm<br>export SHELL=bash
stty rows 45 columns 184

# Metasploit
1. Launch the console: msfconsole
### 1. Core Console Commands

- **help**: Shows all available commands.
- **search [keyword]**: Searches for modules (exploits, scanners, post-modules) related to a specific software (e.g., search bolt).
- **use [path/to/module]**: Selects the module you want to work with.
- **back**: Moves out of the current module and back to the main prompt.
- **exit**: Closes the Metasploit console.
### 2. Information & Configuration

Once you have selected a module (the prompt will turn red, e.g., msf6 exploit(path) >), use these:
- **info**: Displays detailed information about the module (author, description, CVEs, and what it does).
- **show options**: Shows the variables you need to set (RHOSTS, RPORT, etc.). **This is the most important command.**
- **show targets**: Shows the specific versions or operating systems the exploit supports.
- **show payloads**: Shows the different types of "shells" or actions you can run after the exploit succeeds.
- **set [option] [value]**: Assigns a value to a variable (e.g., set RHOSTS 10.82.148.222).
- **setg [option] [value]**: Sets a **global** value (it stays the same even if you switch modules).
- **check**: (Not all modules support this) Checks if the target is vulnerable without actually attacking it
### 3. Execution Command
- **exploit** or **run**: Launches the module.
- **exploit -j**: Runs the exploit in the "job" (background) so you can keep using the console.
- **jobs**: Lists all running background tasks.
- **kill [ID]**: Stops a background job.
### 4. Session Management (After Success)

If an exploit works, it opens a **Session** (a connection to the target)
- **sessions**: Lists all active connections to compromised machines.
- **sessions -i [ID]**: Interacts with a specific session (takes you into the target’s terminal).
- **background** (or Ctrl+Z): Steps out of a session and back to the MSF prompt without closing the connection.

In your msfconsole:
1. Change the payload to a bind shell:
    ```
    set payload php/meterpreter/bind_tcp
    ```
    now you don't need LHOST.
# Find (Linux)
find / -name flag.txt 2>/dev/null

# ffuf
ffuf -u https://futurevera.thm -H "Host: FUZZ.futurevera.thm"

### 1. Directory Discovery

To find hidden folders or files on a web server running on this IP:

codeBash

```
ffuf -u http://10.112.179.125/FUZZ -w /usr/share/wordlists/dirb/common.txt
```
### 2. Discovering Files with Extensions

If you suspect there are specific file types (like .php, .txt, or .html):

```
ffuf -u http://10.112.179.125/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e .php,.txt,.html
```
### 3. Virtual Host (Vhost) Fuzzing

If the IP hosts multiple websites (common in labs), you can fuzz the Host header. Note the -fs flag to filter out the "default" response size so you only see unique results:
```
ffuf -u http://10.112.179.125 -H "Host: FUZZ.example.thm" -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -fs 1234
```

(Replace 1234 with the size of the default page you get when visiting the IP directly).

|                |                          |                                 |
| -------------- | ------------------------ | ------------------------------- |
| Feature        | Gobuster                 | ffuf                            |
| **Philosophy** | "Tell me what to hide"   | "Tell me what to match"         |
| **Speed**      | Very fast                | Extremely fast                  |
| **Complexity** | Simple/Beginner friendly | Slightly steeper learning curve |
|                |                          |                                 |
### Enumerate the Username

We will use ffuf (a fast web fuzzer) and a standard list of names to find the valid user. We will tell ffuf to hide any responses that contain the phrase "Wrong username" so we only see the valid hits.
```
ffuf -w /usr/share/seclists/Usernames/Names/names.txt -u http://lookup.thm/login.php -X POST -d "username=FUZZ&password=test" -H "Content-Type: application/x-www-form-urlencoded" -fr "Wrong username"
```
Search for extension .ticket:
```
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.112.141.99/island/2100/FUZZ.ticket -mc 200 -ic -t 100
```
### Check for special characters filters
```
ffuf -u 'http://moebius.thm/album.php?short_tag=FUZZ' -w /usr/share/wordlists/SecLists/Fuzzing/special-chars.txt -mr 'Hacking attempt'
```
-mr | **Definition:** **Match Regexp** (Regular Expression).
# md5sum
echo -n "0" | md5sum
(Note: The -n flag is important; it tells the system not to add a invisible "newline" character at the end, which would change the hash.)
# openvpn
sudo openvpn thm.ovpn
### How to know it worked:

1. It will ask for your Linux password.
    
2. You will see a lot of text scroll by.
    
3. **Wait** until you see this specific line at the end:  
    Initialization Sequence Completed
    
4. **Do not close that terminal.** If you close it, the VPN will disconnect. Simply minimize it and open a new terminal tab to start your work.
# curl
Let's try out a `DescribeLayer` request using the command below to answer the final question of the task.

`curl -s "http://10.80.128.170:8080/geoserver/wms?service=WMS&version=1.1.1&request=DescribeLayer&layers=trymapme_offices"`

**Command Breakdown**

- `curl -s` sends an HTTP request to the GeoServer instance from the command line
- `http://10.80.128.170:8080/geoserver/wms` specifies the target IP and GeoServer Web Map Service (WMS) endpoint
- `service=WMS&version=1.1.1&request=DescribeLayer` defines the service type, protocol version, and operation being requested
- `layers=trymapme_offices` specifies the layer for which metadata should be returned

curl -X HEAD http://pyrat.thm:8000  
curl -X POST http://pyrat.thm:8000  
curl -X OPTIONS http://pyrat.thm:8000
# grep
**-R (Recursive)**: This flag tells grep to look inside the current directory, every subdirectory, and every file within them.
# binwalk
The primary option to extract files from a firmware image using Binwalk is **-e** (short for **--extract**).

```
binwalk -e firmware_name.img
```
# fastcoll
```
sudo apt update
sudo apt install -y g++ libboost-all-dev git
git clone https://github.com/brimstone/fastcoll.git
cd fastcoll
make
```

### Step 2: Generate the Collision Pair

Now you will take your original dog image and create two new files (dog_A.jpg and dog_B.jpg) that look identical but have different data and the **same MD5 hash**.

Assuming your image is named dog.jpg:

```
./fastcoll_tool -p dog.jpg -o dog_A.jpg dog_B.jpg
```
### Step 3: Verify the Collision

Check that the files are different but their hashes are the same:
```
# Check MD5 hashes (Should be IDENTICAL)
md5sum dog_A.jpg dog_B.jpg

# Check SHA1 hashes (Should be DIFFERENT)
sha1sum dog_A.jpg dog_B.jpg
```
# steghide
steghide extract -sf [name of save image]
# wpscan
**Vulnerability Scanning**:
```
wpscan --url TARGET
```

— url: _To determine the url of a website_

**Enumeration of WordPress Components**
Purpose:  
To gather information about WordPress installation- WordPress version, installed plugins, installed themes, and users.
```
wpscan --url https://example.com --enumerate ap,at,cb,dbe,u
```


> ap — _specifies for checking installed vulnerable plugins_  
> at — _specifies for checking installed vulnerable themes  
> _cb — _for checking Config Backups  
> _dbe _— Database Exports_u _— users_

**3> Password Brute-Forcing  
**Purpose:  
Using brute-forcing attack to test weak passwords that are available out for the attackers to attack into the web.

wpscan --url <target> --passwords <wordlist-file> --usernames <username>

**4> WordPress Version Detection  
**Purpose:  
Version detection is very important as if checked and when the version is out-dated then it might be vulnerable and exploitable too.

wpscan --url <target-url> --enumerate v

**5> To Output Results into a file **
Purpose:  
To save scan results for further reporting and analysis

wpscan --url <target-url> --output <output-file> --format <format>

We output the file into any formats like JSON, CLI, XML.

# enum4Linux

The syntax of Enum4Linux is nice and simple: **"enum4linux [options] ip"**

**TAG**            **FUNCTION**

-U             get userlist  
-M             get machine list  
-N             get namelist dump (different from -U and-M)  
-S             get sharelist  
-P             get password policy information  
-G             get group and member list

-a             all of the above (full basic enumeration)

# smbclient

`Syntax: smbclient //[IP]/[SHARE] -U [USERNAME] -p [PORT]`

`Example: smbclient //10.10.10.10/secrets -U Anonymous -p 445`

**SMBClient Commands**

Once inside the share, you can view the available commands by typing "help". The most useful of which are:

- **ls** or **dir**: List files and directories
- **cd [DIR]**: Move to a different directory
- **get [FILE]**: Download the file to your AttackBox

```
smbclient -L 10.10.10.10
```
enumerate smbclient
# telnet

When you are connected via Telnet, your keyboard inputs are sent to the remote server. If the server hangs or you want to leave, your usual Ctrl+C might not work.

1. Press **Ctrl + ]** (Control and the right square bracket).
    
2. This brings up the telnet> prompt.
    
3. Type these commands at that prompt:
    
    - **quit**: Closes telnet and exits to your Linux terminal.
        
    - **close**: Closes the current connection but stays in telnet.
        
    - **status**: Shows if you are connected and to whom.
        
    - **display**: Shows your current operating parameters.

# mysql
 you can connect using `mysql -h 10.80.182.47 -u root -p`.

**Note**: If your `mysql` client returns a `TLS/SSL error`, you are advised to add `--ssl-mode=DISABLED`; therefore your command becomes `mysql -h 10.80.182.47 --ssl-mode=DISABLED -u root -p`

# rpcclient

```
rpcclient -U "" -N 10.80.187.215
```

Once you get a rpcclient $> prompt, run these commands:

- srvinfo: Get OS version and server type.
    
- enumdomusers: List all users on the machine.
    
- getdompwinfo: Get password policy (min length, lockout threshold).
    
- netshareenumall: List all available shares.

# xfreerdp
Run the command. It will open a window on your Windows desktop:
```
# Syntax: xfreerdp /v:TARGET_IP /u:USERNAME /p:PASSWORD /dynamic-resolution
xfreerdp3 /v:10.114.156.93 /u:TCM /p:password123 +dynamic-resolution
```
# burpsuite
**Run Burp Suite from the WSL Terminal:**

```
java -jar /path/to/burpsuite_pro_v2024.x.jar &
```