Now that the initial setup and "merge conflicts" are out of the way, updating your repo is much simpler. You have three ways to do this:

### Method 1: The Manual Way (Terminal)

Every time you finish a study session or add new notes, run these three commands in your terminal:

code Bash

```
git add .
git commit -m "Updated my notes"
git push origin main
```

- **git add .** → Gathers all your new files and changes.
- **git commit -m "..."** → Packages them with a descriptive message.
- **git push origin main** → Sends them to GitHub.
### Method 2: The "Obsidian Git" Plugin (Highly Recommended)

Since you are using Obsidian, you don't actually need to use the terminal every time. Most people use the **Obsidian Git** community plugin to automate this.

1. Inside Obsidian, go to **Settings** > **Community Plugins** > **Browse**.
    
2. Search for **"Obsidian Git"** and install it.
    
3. **Features you can enable:**
    
    - **Auto Backup:** Set it to automatically push every 10 or 30 minutes.
        
    - **Pull on Startup:** It will automatically download changes if you edited notes on another computer.
        
    - **Custom Shortcut:** You can set a hotkey (like Cmd + S) to push your notes instantly.