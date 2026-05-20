Here are some of the most common web servers that you will encounter.

- **[Apache](https://httpd.apache.org/)**: The most popular web server to host simple websites and blogs, most commonly [WordPress](https://wordpress.com/).
- **[Nginx](https://nginx.org/)**: An industry standard for high-performance web apps. Used by companies like [Netflix](https://openconnect.netflix.com/en/appliances/#software), Airbnb, and GitHub.
- **[Internet Information Services](https://www.iis.net/) (IIS)**: A Microsoft-developed web server commonly used in enterprise environments.

the three essential components of any web service: the **application**, the **web server**, and the **host machine**.
**Protecting the Application**

- Secure Coding: Avoid insecure functions, ensure proper handling of errors, and remove sensitive information.
- Input Validation & Sanitization: Validate and sanitize user input to prevent injection attacks.
- Access Control: Restrict access based on user roles.

**Protecting the Web Server**

- Logging: Keep a detailed record of all web requests with access logs.
- Web Application Firewall (WAF): Filter and block harmful traffic based on defined rules.
- Content Delivery Network (CDN): Reduce direct exposure to your server and use integrated WAFs.

**Protecting the Host Machine**

- Least Privilege: Use low-privilege users for services.
- System Hardening: Disable unnecessary services and close unused ports.
- Antivirus: Add endpoint-level protection that blocks known malware.

**Security Tips for All Three Components**

- Strong Authentication: Don't just let anyone access your code, admin panels, or host machine.
- Patch Management: Ensure your app dependencies, web server, and host machine are up to date.
Note that `GET` requests are used to retrieve a resource from the server, like a specific web page.  
`POST` requests are used to submit data to the server, such as login credentials.

**CDNs** store and serve cached content from servers closer to the user to reduce latency. Imagine you have a main server housed in a central location. This main server provides information to edge servers worldwide so your customers can access data more quickly and safely. Aside from speed, CDNs also help in a security sense by acting as a buffer between the user and the origin server.

**Security Benefits**

- IP Masking: Hides the origin server IP address, which makes it harder for attackers to target.
- DDoS Protection: CDNs can absorb a large amount of traffic, making denial-of-service attacks less effective.
- Enforced HTTPS: Encrypted communication via TLS is enforced by default by most CDNs.
- Integrated WAF: Many CDNs, including [Cloudflare CDN](https://www.cloudflare.com/), [Amazon CloudFront](https://aws.amazon.com/cloudfront/) & [Azure Front Door](https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview), integrate web application firewalls.

In essence, CDNs allow web apps to deliver data to customers more efficiently and securely.

![A graphical representation of a Content Delivery Network (CDN) in which the central server distributes data to edge servers around the world, which then distribute data to the users.](https://tryhackme-images.s3.amazonaws.com/user-uploads/616945d482ef350052080da1/room-content/616945d482ef350052080da1-1754461487753.svg)

**Request Methods To Be Aware Of.**

|                    |                                         |                                                |
| ------------------ | --------------------------------------- | ---------------------------------------------- |
| **Request Method** | **Normal Usage**                        | **Possible abuse**                             |
| **GET**            | Retrieve a resource                     | Used for recon or interacting with a web shell |
| **POST**           | Submit data to the server               | Upload or interact with a web shell            |
| **PUT**            | Upload or replace a file on the server  | Upload a web shell                             |
| **DELETE**         | Remove a resource from the server       | Cleanup methods                                |
| **OPTIONS**        | Requests methods that are supported     | Reconaissance                                  |
| **HEAD**           | Similar to GET but only returns headers | To detect files                                |
## Auditd

A native Linux utility that tracks and records events, creating an audit trail. Rules can be created for `auditd`, which determine what is logged in the `audit.log`.
 In the example below, `ausearch` is used to search for any logs matching the `web_shell` rule.

Ausearch Usage for Audit logs

```shell-session
user@tryhackme$ ausearch -k web_shell
time->Wed Jul 23 06:20:36 2025  // A log matching the web_shell rule
"name = /uploads/webshell.php"
"OGID = www-data"
````

malicious bot traffic [makes up 37%](https://www.thalesgroup.com/en/worldwide/defence-and-security/press_release/artificial-intelligence-fuels-rise-hard-detect-bots) of global web traffic.

 [Check out](https://blog.cloudflare.com/new-waf-intelligence-feeds) how Cloudflare maintains curated IP lists, from sources like botnets, VPNs, anonymizers, and malware, based on global threat intelligence.