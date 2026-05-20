Password: 
```
DigitalOceanbluesy123!#a
```
IPv4: 
```
64.226.102.149
```


Follow these steps to get a fresh, working server in 2 minutes:

### 1. The "Clean Slate" (Rebuild)

1. Go to your **DigitalOcean Dashboard**.
2. Click on your Droplet (164.92.200.107).
3. Click **Destroy** on the left menu.
4. Scroll down to **Rebuild**.
5. Select **Ubuntu 24.04 (LTS)**.
6. **Crucial:** Choose **Password** for authentication (unless you are comfortable with SSH keys). Make sure the password is strong but one you can copy/paste easily.
7. Click **Rebuild**.

---

### 2. The "First Login" Rules

Wait 2 minutes for the progress bar to finish. Then, on your **local computer** (the Kali terminal):

1. Type: ssh root@YOUR_IP
2. If it asks "Are you sure you want to continue connecting?", type **yes**.
3. Enter the password you created during the rebuild.

### 3. Once you are IN

Once you successfully see the root@ubuntu:~# prompt, install the tools:

```bash
# Update everything
sudo apt update && sudo apt upgrade -y

# Install Go (Required for the tools in your article)
sudo apt install golang-go -y

# Install one tool to test
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Add the tool to your command path
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc

# Test it
subfinder -h
```

- **if you see the file:** It worked! Go to next Step .
- **If you get an error or it says "Killed":** You must create a **Swap File** right now (extra RAM) or the server will keep crashing.

**Run this to add 2GB of emergency RAM:**

```
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```
### Now, check your RAM again:

Type: free -h
### 4. Repeat for the other tools

Now that Go has updated itself, you can safely install the rest of the tools from Go.

### Alternative: Install "pdtm" (The Faster Way)

To save disk space and time, **do not use go install anymore.** go install builds the program on your server, which takes up massive amounts of disk space for temporary files.

Instead of compiling every tool separately, we will use **pdtm** (ProjectDiscovery Tool Manager). It downloads the tiny pre-built versions of the tools mentioned in your article..

1. **Install pdtm:**
    ```bash
    go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest
    ```
    (If this fails with "No space left," delete more files or check /var/log for big log files.)
    
2. **Use pdtm to install the others (instantly):
    ```bash
    ~/go/bin/pdtm -install-all
    ```
    This will install nuclei, httpx, and katana as pre-built binaries. It uses much less disk space.
#### Update your PATH

You want to be able to type nuclei or httpx from anywhere. Run these lines to make sure your server knows where the tools are:
```bash
echo 'export PATH=$PATH:$HOME/go/bin:$HOME/.pdtm/bin' >> ~/.bashrc
source ~/.bashrc
```
#### Keep the "Essential 6"

From the guide you pasted, these are the tools that do 90% of the work. Let’s make sure they are in your main path and delete the rest.

**The "Must-Haves":**

1. subfinder (Subdomain discovery)
2. httpx (Checking if sites are alive)
3. katana (Crawling for URLs)
4. nuclei (Vulnerability scanning)
5. gau (Finding old/hidden URLs)
6. ffuf (Directory fuzzing/searching)

### Clean up the "Bloat"

pdtm installed about 20 tools. Let's move the 4 you need from pdtm to your main Go folder and delete the rest of the hidden .pdtm folder to save space.

```bash
# Move the ones you need to your main bin folder
cp /root/.pdtm/go/bin/{subfinder,httpx,katana,nuclei} /root/go/bin/

# Delete the pdtm folder (it's about 500MB+ of extra stuff)
rm -rf /root/.pdtm
```

### Install the Missing 2 (Gau and Ffuf)


```bash
# Install GAU
go install github.com/lc/gau/v2/cmd/gau@latest

# Install FFUF
go install github.com/ffuf/ffuf/v2@latest
```

---

### Your "Minimalist" Recon Script

Now, let's create a script that uses **only** these tools, exactly as described in your guide's "Automation Workflow" section, but tuned for your small server.

1. nano recon_lite.sh
2. **Paste this code:**
```bash
#!/bin/bash
# Minimalist Bug Bounty Stack for 512MB VPS
domain=$1
mkdir -p results_$domain

echo "[+] Phase 1: Finding Subdomains (Subfinder)"
subfinder -d $domain -t 10 -silent -o results_$domain/subs.txt

echo "[+] Phase 2: Checking for Live Hosts (httpx)"
cat results_$domain/subs.txt | httpx -t 20 -silent -o results_$domain/live.txt

echo "[+] Phase 3: Fetching Historical URLs (GAU)"
# This finds old pages that might have bugs
cat results_$domain/live.txt | gau --threads 5 >> results_$domain/urls.txt

echo "[+] Phase 4: Crawling for Hidden Links (Katana)"
cat results_$domain/live.txt | katana -d 2 -jc -silent -o results_$domain/katana_urls.txt

echo "[+] Phase 5: Scanning for Vulnerabilities (Nuclei)"
# We focus on High/Critical bugs to save time
nuclei -l results_$domain/live.txt -c 5 -severity critical,high -o results_$domain/bugs.txt

echo "--- HUNT COMPLETE ---"
echo "Check 'results_$domain/bugs.txt' for vulnerabilities!"
```

chmod +x hunt.sh

### 5. The 10GB Survival Strategy

**Do this:**  
If you want to find targets, just download the **one file** you need, use it, and delete it.

```Bash
# Just get the names, don't clone the whole repo
wget https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/main/data/hackerone_data.json

# Extract what you need into a tiny text file
sudo apt install jq -y
cat hackerone_data.json | jq -r '.[].targets.in_scope[] | .asset_identifier' > targets.txt

# NOW DELETE THE BIG JSON FILE IMMEDIATELY
rm hackerone_data.json
```
