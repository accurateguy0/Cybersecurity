**The Problem:** Your Chrome browser is running inside the **WSL Kali Linux environment**, but your **Burp Suite application is running on the Windows host machine.**

Chrome in WSL is trying to connect to 127.0.0.1:8080. In the WSL context, 127.0.0.1 refers to the **WSL instance itself**, NOT the Windows host machine. Since Burp Suite is running on Windows, the connection **fails** with ERR_PROXY_CONNECTION_FAILED.

### The Solution: Use the Windows Host IP Address in WSL

You need to tell Chrome inside WSL to connect to the **IP address that Windows uses to communicate with the WSL network.** This is usually the **Gateway IP** for the WSL virtual network.

1. **Find the Windows Host IP Address as Seen by WSL:**  
    In your **WSL Kali Terminal**, run the route command again (or look at the output you provided earlier):
    
    codeBash
    
    ```
    ip route show
    ```
    
    Look for the line starting with default:
    
    codeCode
    
    ```
    default via 172.17.144.1 dev eth0 proto kernel 
    # The IP you want is 172.17.144.1 in this example!
    ```
    
    The IP address after default via is the IP address of the **Windows host machine** from the perspective of your WSL instance.
    
2. **Update FoxyProxy in Chrome:**
    
    - Go to the **FoxyProxy Options** in Chrome.
        
    - Edit your BurpSuite THM profile.
        
    - Change the **Proxy Server IP Address** from 127.0.0.1 to the **IP address you found in Step 1** (e.g., 172.17.144.1).
        
    - Keep the **Port** as 8080.
        
    - Save the changes.
        
3. **Activate and Test:**
    
    - Activate the BurpSuite THM profile in FoxyProxy.
        
    - Try browsing to any website (like http://neverssl.com).
        

If this configuration is correct, Chrome in WSL will route traffic to the Windows host at that IP address, where Burp Suite will be listening on port 8080, and the connection should succeed!

This site can’t be reached  
neverssl.com took too long to respond.  
Try:

Checking the connection  
Checking the proxy and the firewall  
ERR_TIMED_OUT

Model 10:47 AM

You are very close! The error has changed from ERR_PROXY_CONNECTION_FAILED (meaning "I couldn't even talk to the proxy") to **ERR_TIMED_OUT** (meaning "I talked to the proxy, but the proxy couldn't reach the final destination").

This means:

1. Chrome in WSL **successfully reached** Burp Suite on your Windows host at the IP you set (e.g., 172.17.144.1:8080). **Success!**
    
2. Burp Suite received the request for neverssl.com and tried to forward it.
    
3. The traffic forwarded by Burp **failed to reach the outside internet or the TryHackMe network**.
    

### The Final Hurdle: VPN Routing from Windows

When you are using the TryHackMe VPN connection **inside WSL**, that connection is only active within the **WSL network namespace**. When Burp Suite on the **Windows Host** forwards the request, it does so **outside** the VPN tunnel.

**Your Windows Host machine is NOT connected to the TryHackMe VPN.** Therefore, it has no route to reach TryHackMe IPs (10.x.x.x) or to correctly handle traffic being routed through the WSL VPN tunnel.

### Solution: Use the In-Browser Connection or Connect VPN on Windows

Since you are relying on the VPN connection inside WSL, Burp Suite running outside of it cannot utilize that connection.

You have two choices to fix this:

#### Option A: Use TryHackMe's Web Access (Recommended and Easiest)

This completely bypasses the need for local networking between WSL and Windows.

1. **Stop the OpenVPN connection** in your WSL terminal (use sudo pkill -f openvpn).
    
2. Go to the **TryHackMe room page** in your **Windows Chrome** browser (the one where Burp Suite is running).
    
3. Click the **"Access the Machine"** button or use the built-in **Web Terminal/VNC**.
    
4. **Burp Suite is not needed** in this case unless you are trying to intercept the web traffic between your Windows browser and the THM web interface, which is usually unnecessary for basic room interaction.
    

#### Option B: Connect the VPN on the Windows Host

If you must use Burp Suite on Windows to intercept traffic from an application on Windows (like the Chrome instance on Windows, not WSL):

1. **Download the .ovpn file** onto your Windows machine.
    
2. **Install OpenVPN Client for Windows** on your Windows host.
    
3. **Connect the VPN** using the Windows OpenVPN client.
    
4. **Configure FoxyProxy in your Windows Chrome** to point to 127.0.0.1:8080.
    
5. Now, the traffic from Windows Chrome will go through Burp Suite, and Burp Suite will be correctly connected to the TryHackMe network.