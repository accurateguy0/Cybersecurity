On Windows you would usually use a piece of software such as [PuTTY](https://putty.org/). You would then login like this:

![](https://muirlandoracle.co.uk/wp-content/uploads/2020/02/PuTTY-Login-Demo-1.png)
CVE-2019-14287 is a vulnerability found in the Unix Sudo program by a researcher working for Apple: Joe Vennix. Coincidentally, he also found the vulnerability that we'll be covering in the next room of this series. This exploit has since been fixed, but may still be present in older versions of Sudo (versions < 1.8.28), so it's well worth keeping an eye out for!

In this example my user account did not have permission to read the file `/root/root.txt`,so I used sudo to temporarily give myself root privileges, in order to read the file.  

Like many commands on Unix systems, sudo can be configured by editing a configuration file on your system. In this case that file is called `/etc/sudoers`. Editing this file directly is not recommended due to its importance to the OS installation, however, you can safely edit it with the command `sudo visudo`, which checks when you're saving to ensure that there are no misconfigurations.  

The vulnerability we're interested in for this task occurs in a very particular scenario. Say you have a user who you want to grant extra permissions to. You want to let this user execute a program as if they were any other user, but you _don't_ want to let them execute it as root. You might add this line to the sudoers file:

`<user> ALL=(ALL:!root) NOPASSWD: ALL`

Theoretically.

In practice, with vulnerable versions of Sudo you can get around this restriction to execute the programs as root anyway, which is obviously great for privilege escalation!

With the above configuration, using `sudo -u#0 <command>` (the UID of root is always 0) would not work, as we're not allowed to execute commands as root. If we try to execute commands as user 0 we will be given an error. Enter CVE-2019-14287.

Joe Vennix found that if you specify a UID of -1 (or its unsigned equivalent: 4294967295), Sudo would incorrectly read this as being 0 (i.e. root). This means that by specifying a UID of -1 or 4294967295, you can execute a command as root, _despite being explicitly prevented from doing so_. It is worth noting that this will _only_ work if you've been granted non-root sudo permissions for the command, as in the configuration above.

Practically, the application of this is as follows: `sudo -u#-1 <command>`

![](https://muirlandoracle.co.uk/wp-content/uploads/2020/02/capture.png)