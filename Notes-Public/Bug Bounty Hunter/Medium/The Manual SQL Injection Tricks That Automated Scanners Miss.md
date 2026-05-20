

> Automated scanners miss critical bugs. Here is how to find them using the “Break & Repair” method.

We all do it.

We find a parameter, run `sqlmap`, and wait. If the terminal says "No vulnerabilities found," we move on.

**But scanners are dumb.** They miss context. They get blocked by basic filters. They don’t understand _logic_.

In a brilliant NahamCon session, security expert [Tib3rius](https://x.com/0xTib3rius) broke down how to find SQL Injection (SQLi) manually.

Here is the entire methodology, stripped down to the essentials.

FREE Link : [Here](https://medium.com/@Aacle/the-manual-sql-injection-tricks-that-automated-scanners-miss-a5eac6d74f38?sk=9d80c2f588dfaa4268e56c1b9edcad28)

## Part 1: The “Break & Repair” Method

Stop guessing random payloads. Use science.

The goal isn’t to hack the database immediately. The goal is to see if the database is **listening** to you.

The Logic:

If you can break the page on purpose, and then fix it on purpose, you have full control.

**The 5-Step Workflow:**

1. **Find an Entry Point:** Look for URLs with IDs (`id=1`), search bars, or login forms.
2. **Establish a Baseline:**

- Type a valid ID (`id=1`). Does the page load? **Yes.**
- Type a fake ID (`id=9999`). Does it give a 404? **Yes.**

**3. The “Break”:** Add a single quote (`'`) to the valid ID.

- _Input:_ `id=1'`
- _Result:_ Did you get a 500 Error or a blank page? **Good. You broke the syntax.**

**4. The “Repair”:** Add a comment character to “fix” the quote you just added.

- _Input:_ `id=1' -- -`
- _Result:_ Did the page go back to normal?

**5. Confirmation:** If the page broke on step 3 and worked on step 4, **you have found a vulnerability.**

## Part 2: Syntax Traps (And How to Fix Them)

You found the bug. Now, how do you keep the query working?

### 1. The Trailing Space Trap

You might use `--` to comment out the rest of a query.

- **The Problem:** Many databases require a _space_ after the dashes. If the web server trims whitespace, your attack fails.
- **The Fix:** Use `-- -`.
- That extra dash at the end forces the database to respect the space in the middle.

### 2. When Comments Fail

Sometimes, commenting out the code breaks the website (e.g., if the query needs a closing footer).

- **The Fix:** Don’t delete the code. Just make it mathematically true.
- **Payload:** `' AND '1'='1`
- This keeps the structure intact while letting you inject commands.

## Part 3: Fingerprinting (What Database is This?)

Don’t guess. Ask the database what language it speaks.

Try these payloads one by one. The first one that returns a **200 OK** (normal page) tells you the technology.

![](https://miro.medium.com/v2/resize:fit:371/1*iKp9eU3MPh6plksONcndJw.png)

## Part 4: Stealing Data (The Exploitation)

Now for the fun part. Getting the data out.

### 1. The UNION Attack

You want to join your data with the website’s data.

- **Problem:** The website only shows the first result (the real article).
- **Solution:** Make the first result “False.”
- **How:** Change `id=1` to `id=-1`.
- **Result:** The site finds nothing for ID -1, so it displays _your_ data instead.

### 2. Finding the Column Count

You can’t use UNION unless you know how many columns are in the table.

- **Don’t do this:** `ORDER BY 1`, `ORDER BY 2`, `ORDER BY 3`... (Too slow).
- **Do this (Binary Search):**
- Try `ORDER BY 10`. Error?
- Try `ORDER BY 5`. Works?
- Then the answer is between 5 and 10.
- You find the limit in seconds, not minutes.

### 3. The Login Bypass

Trying to bypass a login page?

- **Classic Payload:** `' OR 1=1 --`
- **The Risk:** This might return _every user in the database_, confusing the app.
- **The Fix:** `' OR 1=1 LIMIT 1 --`
- This forces the database to log you in as the **first** user only (usually the Admin).

## Part 5: Blind Injection (When the Database is Silent)

Sometimes the database won’t show you text. It only says “Yes” (Page loads) or “No” (Error).

**Don’t guess passwords letter by letter.**

- _Is the first letter ‘a’? No._
- _Is it ‘b’? No._
- _(26 requests later…)_

Use Math (Binary Search).

Convert the password character to a number (ASCII).

- _Is the value greater than 100?_ **Yes.** (You just eliminated 100 options).
- _Is it greater than 110?_ **No.**
- _Okay, it’s between 100 and 110._

You can guess any character in about **7 requests** using this method.

## The Takeaway

SQLmap is a hammer. You are a surgeon.

Automated tools are great for dumping data _after_ you find the hole. But to find the hole in the first place?

**Use your brain.**

1. Break the query.
2. Repair the query.
3. Inject your code.