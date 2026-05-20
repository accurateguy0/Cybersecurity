There are two main ways to fix this. The best method depends on which version of Windows you are running.

### Method 1: "Mirrored Mode" (Best for Windows 11)

If you are on **Windows 11 (version 22H2 or newer)**, Microsoft introduced a "Mirrored" networking mode that forces WSL to share the exact same network interface as Windows (including VPNs).[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQG5xecEiXVRdvlbew-YMprU_MiwNR-6IZiovalJkpiPYY0onscPu71bhhPMGnRMC79Hl0sC1LlO4MWyof8Wv2rPp54VX1TeZeBJYDDBKr_unYzWnBxnTn2ZCP8twgC0nD_LFafyzoaXKcFskl2hs5CYi8xb)]

1. **Create/Edit the WSL Config file:**  
    Open PowerShell in Windows and run this command to open the config file in Notepad:
    
    ```
    notepad $env:USERPROFILE\.wslconfig
    ```
    
    (If the file asks to create a new one, say Yes.)
    
2. **Add the Mirrored Networking configuration:**  
    Paste the following into the file:
    ````
    [wsl2]
    networkingMode=mirrored
    dnsTunneling=true
    firewall=true
    autoProxy=true
    ```[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQG5xecEiXVRdvlbew-YMprU_MiwNR-6IZiovalJkpiPYY0onscPu71bhhPMGnRMC79Hl0sC1LlO4MWyof8Wv2rPp54VX1TeZeBJYDDBKr_unYzWnBxnTn2ZCP8twgC0nD_LFafyzoaXKcFskl2hs5CYi8xb)]
    ````
    
3. **Restart WSL:**  
    Save the file, close Notepad, and run this in PowerShell to force a restart:
    
    ```
    wsl --shutdown
    ```
    
1. **Test:** Open Kali and try ping google.com or access an internal corporate site.

### Step 1: Fix the VPN (Move it to Kali)

1. Ensure OpenVPN is **disconnected** on Windows (your ipconfig shows it is currently disconnected, which is good).
    
2. Open your Kali terminal.
    
3. Connect to the VPN here:
    ```
    sudo openvpn /path/to/your/file.ovpn
    ```
    
    (Keep this running in a tab).
    

### Step 2: How to use RDP from Kali

You don't need the Windows Remote Desktop Connection app. Kali has a tool called xfreerdp that works perfectly.

1. Install it (if you haven't already):```
    sudo apt update && sudo apt install freerdp2-x11 -y
    ```
    
2. Run the command. It will open a window on your Windows desktop:
        ```
    # Syntax: xfreerdp /v:TARGET_IP /u:USERNAME /p:PASSWORD /dynamic-resolution
    xfreerdp /v:10.10.10.10 /u:Administrator /p:password123 /dynamic-resolution
    ```
    
    Replace the IP, User, and Pass with the room info.
    

### Step 3: How to use a Browser from Kali

If you need to access a website (like http://10.10.10.10) while the VPN is inside Kali:

1. Just type this in your Kali terminal:
    
    ```
    firefox &
    ```
    
2. A Firefox window will launch. Even though it is running inside Linux, it appears on your Windows screen. This Firefox instance uses the Kali VPN connection, so it can reach the internal TryHackMe sites.
    

---

### Step 4: Now your Payload & SMB work!

Now that the VPN is inside Kali, your original request becomes very easy because **you have a tun0 IP address.**

1. **Get your IP:**
    
    ```
    ip addr show tun0
    # Let's say it is 10.9.1.5
    ```
### How to fix this (The "Clean Slate" Method):

**1. Force-kill all VPN processes:**

```
sudo pkill -9 openvpn
```

**2. Verify the tunnels are gone:**  
Run ip a. You must wait until **both** tun0 and tun1 disappear from the list. If they are still there, your network manager might be restarting them automatically.

**3. Clear the route cache:**

```
sudo ip route flush cache
```

**4. Start the VPN ONE time:**  
Open a fresh terminal and run your OpenVPN command:


```
sudo openvpn your_file.ovpn
```

Wait for "Initialization Sequence Completed".

**5. Verify the route matches the tunnel:**  
Run ip a to see if you have tun0 or tun1. Let's say you have tun0 this time.  
Then run:


```
ip route get 10.114.156.93
```

**Crucial:** The dev in this output **must** match the tun interface that is currently active. If the ip route command says tun0 but ip a shows tun1, the connection will fail.

**6. Try the RDP command again:**

```
xfreerdp3 /u:TCM /p:password123 /v:10.114.156.93 /cert:ignore +dynamic-resolution
```


### 1. Routing Issues (The most common cause)

Even if you are "connected" to the VPN, your computer might not know it should send traffic for the 10.x.x.x range through the VPN tunnel.

- **The Problem:** Your computer is trying to send the ping through your regular home internet instead of the VPN "tunnel."
- **The Fix:** Check your routing table. In your terminal/command prompt, run:
    
    - **Windows:** route print
    - **Mac/Linux:** netstat -nr
    - Look for an entry that points 10.0.0.0 (or your specific subnet) to the VPN interface (often called tun0 or utun). If it's missing, the VPN server isn't "pushing" the routes correctly.
  


The routing table you provided explains exactly why the ping is hanging.

### The Problem: A Routing Mismatch

Your computer only knows how to send a specific range of 10.x.x.x addresses through the VPN (tun0).

Look at this line in your table:

- **Destination:** 10.80.0.0
- **Genmask:** 255.240.0.0 (which is a /12 prefix)
- **Range covered:** This route only covers IPs from **10.80.0.0** to **10.95.255.255**.
    

Your target IP is **10.113.157.107**.  
Since 10.113 is **not** between 10.80 and 10.95, your computer ignores the VPN and sends the traffic to your **Default Gateway** (0.0.0.0 via eth0). Because 10.113.157.107 is a private IP, it cannot be found on the public internet, so the request simply times out.

---

### The Fix: Manually add the route

You need to tell your computer that the 10.113.x.x range belongs to the VPN.

Run the following command in your terminal (you will likely need sudo):
```
sudo ip route add 10.113.157.0/24 dev tun0 via 192.168.128.1
```

**What this command does:**

- 10.113.157.0/24: Tells the computer to look for any IP starting with 10.113.157...
    
- dev tun0: ...on the VPN interface...
    
- via 192.168.128.1: ...using the VPN's gateway.
    

**After running that, try your ping again:**  
ping 10.113.157.107

---

### How to make this permanent

If the manual fix works, you shouldn't have to type it every time. You have two options:

**Option A: Edit your OpenVPN config file (.ovpn)**  
Open your .ovpn file in a text editor and add this line at the bottom:

```
route 10.113.157.0 255.255.255.0
```

Next time you connect, OpenVPN will automatically add the route for you.

**Option B: Fix it on the Server (If you are the admin)**  
The OpenVPN server should be "pushing" this route to all clients. In the server's server.conf, the admin should add:
```
push "route 10.113.157.0 255.255.255.0"
```

**Note:** If you need to access everything in the 10.x.x.x range, you could use a broader mask (like 10.0.0.0/8), but usually, it is safer to only route the specific subnets you need.
