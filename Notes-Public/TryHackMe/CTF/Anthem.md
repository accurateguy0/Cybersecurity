## Flag 1 + 2:[](https://krauss-it.com/posts/CTF-try-hack-me-anthem/#flag-1--2)

**hint: Inspect the webpages**

            `|   |   | |---|---| ||<h2 class="blog-description"><br>        Welcome to our blog<br>    </h2><br>            <nav class="menu" role="nav"><br>        <ul><br>            <li><a href="/blog/categories">Categories</a></li><br>            <li><a href="/blog/tags">Tags</a></li><br>            <li><br>                <div class="articulate-search"><br>        <form method="get" action="/blog/search"><br>            <input type="text" name="term" placeholder="Search...                                                           THM{G!T_G00D}" /><br>            <button type="submit" class="fa fa-search fa"></button><br>        </form><br>    </div><br>            </li><br>        </ul><br>    </nav><br><br>        </header><br><br>        <br><br>    <main class="content" role="main"><br><br>        <article class="post"><br><br>            <header>|`

We know we search for `THM`flags, thats why we can use `curl` to search for the word `THM` in other pages.

    `|   |   | |---|---| ||─$ curl http://10.10.211.67/archive/we-are-hiring/ \|grep THM                                                                                                                                                                              <br>    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current<br>                                    Dload  Upload   Total   Spent    Left  Speed<br>    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0<meta content="THM{L0L_WH0_US3S_M3T4}" property="og:description" /><br>            <input type="text" name="term" placeholder="Search...                                                           THM{G!T_G00D}" /><br>    100  6200  100  6200    0     0   7932      0 --:--:-- --:--:-- --:--:--  7928|`

Nice, we found already two flags:

`THM{G!T_G00D}` (flag 2) `THM{L0L_WH0_US3S_M3T4}` (flag 1)

## Flag 3:[](https://krauss-it.com/posts/CTF-try-hack-me-anthem/#flag-3)

**hint: Profile**

I ran a `gobuster` seach before to find some hidden directories.

`|   |   | |---|---| ||─$ gobuster -u 10.10.211.67 -w ~/Downloads/common.txt dir<br>===============================================================<br>Gobuster v3.6<br>by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)<br>===============================================================<br>[+] Url:                     http://10.10.211.67<br>[+] Method:                  GET<br>[+] Threads:                 10<br>[+] Wordlist:                /home/admin/Downloads/common.txt<br>[+] Negative Status codes:   404<br>[+] User Agent:              gobuster/3.6<br>[+] Timeout:                 10s<br>===============================================================<br>Starting gobuster in directory enumeration mode<br>===============================================================<br>/Archive              (Status: 301) [Size: 118] [--> /]<br>/Blog                 (Status: 200) [Size: 5394]<br>/RSS                  (Status: 200) [Size: 1873]<br>/Search               (Status: 200) [Size: 3468]<br>/SiteMap              (Status: 200) [Size: 1041]<br>/archive              (Status: 301) [Size: 123] [--> /blog/]<br>/authors              (Status: 200) [Size: 4115]<br>Progress: 339 / 1943 (17.45%)[ERROR] Get "http://10.10.211.67/aux": context deadline exceeded (Client.Timeout exceeded while awaiting headers)<br>/blog                 (Status: 200) [Size: 5394]<br>/categories           (Status: 200) [Size: 3541]<br>Progress: 896 / 1943 (46.11%)^C<br>[!] Keyboard interrupt detected, terminating.<br>Progress: 896 / 1943 (46.11%)<br>===============================================================<br>Finished<br>===============================================================|`

I think `authors` looks promising. When we use the browser for checking /authors we find the next flag under `webpage`.

Flag 3: `THM{L0L_WH0_D15}`

## Flag 4:[](https://krauss-it.com/posts/CTF-try-hack-me-anthem/#flag-4)

**Hint: Have we all inspected all the pages yet?**

For the last flag I used `curl` and searched every directory of the webpage with `THM`. I found it.

`|   |   | |---|---| ||curl http://10.10.211.67/archive/a-cheers-to-our-it-department  \|grep THM<br>  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current<br>                                 Dload  Upload   Total   Spent    Left  Speed<br>100  6260  100  6260    0     0   8264      0 --:--:-- --:--:-- --:--:--  8258<br><meta content="THM{AN0TH3R_M3TA}" property="og:description" /><br>        <input type="text" name="term" placeholder="Search...|`    

Flag 4: `THM{AN0TH3R_M3TA}`

We have all our flags now.

SG UmbracoIsTheBest!