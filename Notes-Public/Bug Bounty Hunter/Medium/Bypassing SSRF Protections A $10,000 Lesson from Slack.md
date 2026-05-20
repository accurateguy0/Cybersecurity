
[

![Abhishek meena](https://miro.medium.com/v2/resize:fill:32:32/1*g4tYjgpvB52xwZPNMcvefg.png)





](https://medium.com/@Aacle?source=post_page---byline--6cff022a44a6---------------------------------------)

[Abhishek meena](https://medium.com/@Aacle?source=post_page---byline--6cff022a44a6---------------------------------------)

Follow

5 min read

·

Jan 11, 2026

211

2

## How a Simple DNS Rebinding Attack Led to Internal Network Access

Server-Side Request Forgery (SSRF) vulnerabilities remain one of the most critical security issues in modern web applications. Today, I’m breaking down a fascinating SSRF report that earned a researcher $10,000 from Slack’s bug bounty program, and the valuable lessons we can all learn from it.

## The Vulnerability Overview

**Severity:** High  
**Free Read**: [Click](https://medium.com/@Aacle/bypassing-ssrf-protections-a-10-000-lesson-from-slack-6cff022a44a6?sk=11db7e23b85c1147e030b74a5a36d383)

This report demonstrates how an attacker could bypass Slack’s SSRF protections using DNS rebinding techniques to access internal network resources that should have been completely isolated from external access.

## Understanding the Attack Surface

Slack, like many modern applications, needs to fetch external resources — think profile images, link previews, or webhook callbacks. However, allowing a server to make arbitrary HTTP requests opens the door to SSRF attacks, where an attacker tricks the server into making requests to internal resources.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*2_Eww8ZiRWvyWbRqf-jUmw.jpeg)

The typical protection? Blacklisting internal IP ranges like:

- `127.0.0.1` (localhost)
- `10.0.0.0/8` (private network)
- `192.168.0.0/16` (private network)
- `169.254.0.0/16` (link-local addresses)

Slack had implemented these protections. So how did the researcher bypass them?

## The Attack: DNS Rebinding

DNS rebinding is a clever technique that exploits the time gap between when a server validates a URL and when it actually fetches the resource.

## Here’s how it works:

**Step 1: Initial Request**  
The attacker provides a malicious URL to Slack (for example, in a profile picture field or link preview):

https://malicious-domain.com/fetch-me

**Step 2: DNS Resolution (First Check)**  
Slack’s server resolves `malicious-domain.com` and gets back a legitimate public IP address like `1.2.3.4`. The security check passes—this isn't an internal IP!

**Step 3: The Switch**  
Before Slack actually fetches the resource, the attacker’s DNS server changes the resolution for `malicious-domain.com` to point to an internal IP like `127.0.0.1` or `192.168.1.50`.

**Step 4: The Fetch**  
When Slack’s server makes the actual HTTP request (using the cached domain name or re-resolving), it now connects to the internal IP address, completely bypassing the SSRF protections.

## The Technical Details

The researcher likely used a controlled DNS server with an extremely low TTL (Time To Live) value, possibly 0 or 1 second. This ensures that DNS responses aren’t cached for long, allowing rapid switching between external and internal IPs.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*oytlD12J9W3FehPekFI28Q.jpeg)

A simplified timeline might look like this:

T+0s:   Attacker submits URL to Slack  
T+0.1s: Slack validates URL, DNS returns 1.2.3.4 ✓ Passes  
T+0.2s: Attacker's DNS server updates record to 127.0.0.1  
T+0.5s: Slack fetches resource, DNS now returns 127.0.0.1  
T+0.6s: Connection made to localhost—SSRF achieved!

## The Impact

With this SSRF vulnerability, an attacker could potentially:

1. **Access internal services** running on Slack’s infrastructure (databases, admin panels, internal APIs)
2. **Scan the internal network** to map out services and infrastructure
3. **Bypass authentication** on internal services that trust requests from localhost
4. **Exfiltrate sensitive data** from internal endpoints
5. **Perform further attacks** using the Slack server as a pivot point

In cloud environments (AWS, GCP, Azure), this could also lead to accessing instance metadata endpoints, potentially exposing credentials and other sensitive configuration data.

## Why This Bypass Worked

The vulnerability existed because Slack’s SSRF protection had a critical flaw:

**They validated the IP at one point in time but used the domain name at another.**

This race condition is the heart of DNS rebinding attacks. The security check and the actual request weren’t atomic operations using the same resolved IP address.

## The Proper Fix

To defend against DNS rebinding attacks, applications should:

### 1. Resolve Once, Use Everywhere

# Vulnerable approach  
url = get_user_input()  
ip = resolve_dns(url)  
if is_safe_ip(ip):  
    fetch(url)  # May resolve to different IP!  
  
# Secure approach  
url = get_user_input()  
ip = resolve_dns(url)  
if is_safe_ip(ip):  
    fetch_by_ip(ip)  # Use the validated IP directly

### 2. Implement DNS Pinning

Cache the DNS resolution and use the same IP for the entire request lifecycle.

### 3. Validate After Resolution

Even if using the domain name, validate the resolved IP immediately before making the connection.

### 4. Use a Whitelist Approach

Instead of blacklisting internal IPs, whitelist only approved external domains or IP ranges.

### 5. Network Segmentation

Ensure servers that fetch external content have minimal access to internal networks.

### 6. Monitor and Alert

Implement logging for unusual DNS resolution patterns or requests to internal IP ranges.

## Key Takeaways for Bug Bounty Hunters

### 1. Time-Based Vulnerabilities Are Real

Always consider race conditions and time-of-check to time-of-use (TOCTOU) vulnerabilities. What’s validated isn’t always what’s used.

### 2. Test Your Assumptions

Even if a company has SSRF protections, they might not account for advanced techniques like DNS rebinding. Don’t assume protections are comprehensive.

### 3. Understand the Full Request Lifecycle

Map out every step from user input to final request. Vulnerabilities often hide in the gaps between these steps.

### 4. Tools and Services

Services like `1u.ms`, `rebinder.net`, or your own DNS server can facilitate DNS rebinding testing. Always get proper authorization before testing.

### 5. Cloud Metadata is Golden

In cloud environments, SSRF to metadata endpoints (`169.254.169.254`) can be devastating. This should always be on your testing checklist.

## Responsible Disclosure in Action

This report is a perfect example of responsible disclosure:

1. The researcher identified a critical vulnerability
2. They reported it through proper channels (HackerOne)
3. They provided clear reproduction steps
4. Slack validated and fixed the issue
5. Both parties agreed on a fair bounty ($10,000)
6. The report was disclosed publicly after remediation

This collaboration makes the internet safer for everyone.

## Testing for SSRF Vulnerabilities

When hunting for SSRF, look for features that fetch external resources:

- Profile picture uploads (URL-based)
- Link previews and unfurling
- Webhook configurations
- PDF generators that fetch external resources
- Document imports from URLs
- Image processing services
- API integrations
- RSS feed readers

## Conclusion

This $10,000 finding teaches us that security is rarely binary. Even sophisticated companies with dedicated security teams can have subtle vulnerabilities in their defenses. The DNS rebinding technique demonstrates that bypasses often exploit the **timing and implementation details** of security controls rather than their logical intent.

For developers: validate what you use, not just what you receive.

For bug bounty hunters: think creatively about the gap between validation and execution.

For everyone: defense in depth matters. Multiple layers of protection can catch what single controls miss.

## Additional Resources

- **OWASP SSRF Prevention Cheat Sheet**: Essential reading for developers
- **DNS Rebinding Tools**: Research responsibly with proper authorization
- **Cloud Metadata Endpoints**: Understand the risks in AWS, GCP, and Azure
- **HackerOne Disclosed Reports**: A goldmine of real-world vulnerabilities

Happy hunting, and always hack responsibly! 🎯