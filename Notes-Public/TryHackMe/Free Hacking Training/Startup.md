**We are Spice Hut,** a new startup company that just made it big! We offer a variety of spices and club sandwiches (in case you get hungry), but that is not why you are here. To be truthful, we aren't sure if our developers know what they are doing and our security concerns are rising. We ask that you perform a thorough penetration test and try to own root. Good luck!

I did nmap scan. I have open ports 21, 22 and 80. We can put the payload to ftp server, the payload will be a php file with reverse shell in it. Look for the wireshark file and analyse it, use follow function. You'll get the password for lennie: 

c4ntg3t3n0ughsp1c3

ssh into lennie. read the flag. try sudo -l. Try to see the files with root permissions that are writable and executable and then inject the reverse shell into it then execute the file, before that make sure to have a listener:
```
nc -lvnp [port]
```
