The TBFC is very wary since the last series of attacks by the underlings of King Malhare. They are on full alert for anything happening. But they are getting restless; it is too quiet. Sir Elfo of the TBFC takes the initiative and proposes to hunt for Command and Control traffic using the meticulously collected network traffic. A majority of the TBFC elves object, we don't have the time to go through so much network traffic! Sir Elfo chuckles, don't fret, for I have a powerful tool to assist us! I present to you RITA, Real Intelligence Threat Analytics. We just need to convert our PCAP file to Zeek logs, and RITA will do the rest! Anyone can do it, just follow today's tasks.

## The Magic of RITA

Real Intelligence Threat Analytics (RITA) is an open-source framework created by Active Countermeasures. Its core functionality is to detect command and control (C2) communication by analyzing network traffic captures and logs. Its primary features are:

- C2 beacon detection
- DNS tunneling detection
- Long connection detection
- Data exfiltration detection
- Checking threat intel feeds
- Score connections by severity
- Show the number of hosts communicating with a specific external IP
- Shows the datetime when the external host was first seen on the network
## The Magic of RITA

Real Intelligence Threat Analytics (RITA) is an open-source framework created by Active Countermeasures. Its core functionality is to detect command and control (C2) communication by analyzing network traffic captures and logs. Its primary features are:

- C2 beacon detection
- DNS tunneling detection
- Long connection detection
- Data exfiltration detection
- Checking threat intel feeds
- Score connections by severity
- Show the number of hosts communicating with a specific external IP
- Shows the datetime when the external host was first seen on the network

A SPAN port (sometimes called a mirror port) is a software feature built into a switch or router that creates a copy of selected packets passing through the device and sends them to a designated SPAN port. Using software, the administrator can easily configure or change what data is to be monitored. Since the primary purpose of a switch or router is to forward production packets, SPAN data is given a lower priority on the device. The SPAN also uses a single egress port to aggregate multiple links, so it is easily oversubscribed.

RITA only accepts network traffic input as **Zeek** logs. **Zeek** is an open-source **network security monitoring (NSM)** tool. Zeek is not a firewall or IPS/IDS; it does not use signatures or specific rules to take an action. It simply observes network traffic via configured SPAN ports (used to copy traffic from one port to another for monitoring), physical network taps, or imported packet captures in the PCAP format.

The `pcaps` directory contains example PCAPs of real-life incidents collected from Bradly Duncan's [blog](https://malware-traffic-analysis.net/). He has a wonderful collection of malware-related PCAPs that cover real-world threats.

 You can find more info at https://docs.zeek.org/en/master/logs/index.html if you want a detailed description.
The `zeek_logs` directory contains Zeek logs. These were created by parsing a PCAP file. Let's parse a PCAP ourselves and look at the output Zeek logs. We will use the `zeek readpcap <pcapfile> <outputdirectory>` command.

cd /home/ubuntu/zeek_logs/asyncrat/ && ls

 As seen in the terminal, a lot of output is produced. The terminal output was redacted in the example below to keep it tidy.

RITA walkthrough

```shell-session
ubuntu@tryhackme$ rita import --logs ~/zeek_logs/asyncrat/ --database asyncrat
```

Now that RITA has parsed and analyzed our data, we can view the results by entering the command `rita view <database-name>`

The terminal window shows three elements: the search bar, the results pane, and a details pane.

**Search bar**  
To search, we need to enter a forward slash (/). We can then enter our search term and narrow down the results. The search utility supports the use of search fields. When we enter `?` while in search mode, we can see an overview of the search fields, alongside some examples. The image below shows the help for the search utility. To exit the help page, enter `?` again. Enter the escape key ("esc") to exit the search functionality.

![RITA - Search help](https://tryhackme-images.s3.amazonaws.com/user-uploads/66c44fd9733427ea1181ad58/room-content/66c44fd9733427ea1181ad58-1761301233135.png)

**Results pane**  
The results pane includes information for each entry that can quickly help us recognize potential threats. The following columns are included:

- **Severity**: A score calculated based on the results of threat modifiers (discussed below)
- **Source and destination** IP/FQDN
- **Beacon** likelihood
- **Duration** of the connection: Long connections can be indicators of compromise. Most application layer protocols are stateless and close the connection quickly after exchanging data (exceptions are SSH, RDP, and VNC).
- **Subdomains**: Connections to subdomains with the same domain name. If there are many subdomains, it could indicate the use of a C2 beacon or other techniques for data exfiltration.
- **Threat intel**: lists any matches on threat intel feeds

We can see two interesting findings: an FQDN pointing to `sunshine-bizrate-inc-software[.]trycloudflare[.]com` and an IP `91[.]134[.]150[.]150`. Move the keyboard arrows to select the first entry. You should then see detailed information in the right pane.

![RITA - Details](https://tryhackme-images.s3.amazonaws.com/user-uploads/66c44fd9733427ea1181ad58/room-content/66c44fd9733427ea1181ad58-1761301302504.png)
**Details pane**  
Apart from the Source and Destination, we have two information categories: Threat Modifiers and Connection info. Let's have a closer look at these categories:

_Threat Modifiers_  
These are criteria to determine the severity and likelihood of a potential threat. The following modifiers are available:

- **MIME type/URI mismatch:** Flags connections where the MIME type reported in the HTTP header doesn't match the URI. This can indicate an attacker is trying to trick the browser or a security tool.
- **Rare signature:** Points to unusual patterns that attackers might overlook, such as a unique user agent string that is not seen in any other connections on the network.
- **Prevalence:** Analyzes the number of internal hosts communicating with a specific external host. A low percentage of internal hosts communicating with an external one can be suspicious.
- **First Seen:** Checks the date an external host was first observed on the network. A new host on the network is more likely to be a potential threat.
- **Missing host header:** Identifies HTTP connections that are missing the host header, which is often an oversight by attackers or a sign of a misconfigured system.
- **Large amount of outgoing data**: Flags connections that send a very large amount of data out from the network.
- **No direct connections:** Flags connections that don't have any direct connections, which can be a sign of a more complex or hidden command and control communication.