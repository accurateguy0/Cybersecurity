![Reconnaissance in MITRE ATT&CK Framework](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/61306d87a330ed00419e22e7-1758754650424.png)
Indicators of attack for DNS:
- DNS queries sent to a single external domain, with very high counts compared to the baseline
- long subdomain labels or unusually long full query names
- Unusual response behavior: frequent NXDOMAIN
- queries at regular intervals (beaconing behaviour)
Indicators of attack for FTP:
- use of compromised accounts
- use of non standard ports or tunneling to blend with other traffic
- use legitimate FTP servers to transfer data
- USER and PASS commands
- data channel openings on ephemeral ports (PASV) paired with large payloads
- Large data connections to unusual external IPs, especially outside business hours
- STOR (upload) and RETR ( download) commands: repeated or large transfers
Indicators of attack for HTTP:
- Large amount of HTTP POST requests to external/ unexpected hosts
- HTTP requests to low reputation / rare domains
- Frequent small requests (beaconing) to the same host, followed by large traffic
- Chunked or multipart transfers where multiple requests compose a bigger file
Indicators of attack for ICMP:
- Large frame.len or icmp.payload pings with payloads larger than typical, e.g. 64 bits
- Regular timing: evenly spaced ICMP packets carrying similar-sized payloads
- A single host sending many ICMP echo requests to an external IP
## How adversaries use ICMP for exfiltration

Common techniques:

- ICMP echo (type 8) / reply (type 0) tunneling: attackers place encoded (base64, hex) chunks of files inside ICMP payloads. The remote server collects and decodes them.
- Custom ICMP types/codes: using uncommon ICMP types or non-zero codes to avoid signature-based detections.
- Fragmentation and reassembly: large payloads are split across multiple packets.
- Encryption/obfuscation: Encrypting or encrypting payloads (base64 is common) to look like random data.

Indicators that something may be malicious:

- Persistent ICMP sessions to an external host not used for legitimate monitoring.
- Unusually large ICMP payloads or frequent ICMP with payload > typical ping size.
- ICMP payloads that contain high-entropy data or patterns consistent with base64/hex.
- Bursts of ICMP are immediately followed by no other legitimate application traffic from the same host.
Indicators of attack for ARP spoofing:
- Large amount of ARP traffic 
- Multiple destination MAC for the same gateway IP
- Many ARP requests with `Who has 192.168.1.x? Tell 192.168.1.y` patterns.
- High number of ARP replies without matching requests (gratuitous/ unasked replies)
- Multiple MAC addresses claiming the same IP, indicates impersonification
Indicators of attack for DNS spoofing:
- Unusually short TTLs
- Unsolicited DNS replies
- DNS response from an unexpected source
- Multiple DNS responses for the same query
Indicators of SSL stripping:
- Initial request of https, then the response is http
- redirects/link rewriting to http from https
- certificate errors, although attacker usually tries to hide this, the initial TLS/SSL handshake may fail or display a self-signed certificate if attacker uses a more direct proxying technique
## Show DNS redirect that precedes stripping.

Our hypothesis about SSL stripping is that it is done after the attacker has successfully performed DNS spoofing, sending the victim to the attacker's IP.

We can also identify the user's credentials in plaintext, which confirms that the attacker was able to obtain the victim's credentials. Though there are other SSL stripping indicators as well that we should be looking at.