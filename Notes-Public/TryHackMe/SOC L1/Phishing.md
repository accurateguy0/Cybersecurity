It's only appropriate to start this room by mentioning the man who invented the concept of emails and made the @ symbol famous. The person responsible for the contribution to the way we communicate was Ray Tomlinson. 

The invention of the email dates back to the 1970s for [ARPANET](https://www.britannica.com/topic/ARPANET). Yep, probably before you were born. Definitely, before I was born. :)

The difference between the two is listed below: (credit [AOL](https://help.aol.com/articles/what-is-the-difference-between-pop3-and-imap) -- _[You got mail!](https://www.youtube.com/watch?v=gFBLiHpkcOk)_)

**POP3**

- Emails are downloaded and stored on a single device.
- Sent messages are stored on the single device from which the email was sent.
- Emails can only be accessed from the single device the emails were downloaded to.
- If you want to keep messages on the server, make sure the setting "Keep email on server" is enabled, or all messages are deleted from the server once downloaded to the single device's app or software.

**IMAP**

- Emails are stored on the server and can be downloaded to multiple devices.
- Sent messages are stored on the server.
- Messages can be synced and accessed across multiple devices.

Before ending this room, you should know what **[BEC](https://www.proofpoint.com/us/threat-reference/business-email-compromise)** (Business Email Compromise) means.

  

A BEC is when an adversary gains control of an internal employee's account and then uses the compromised email account to convince other internal employees to perform unauthorized or fraudulent actions.


_Messageheader analyzes SMTP message headers, which help identify the root cause of delivery delays. You can detect misconfigured servers and mail-routing problems_".

**Usage**: Copy and paste the entire email header and run the analysis tool. 

- **Messageheader**: [https://toolbox.googleapps.com/apps/messageheader/analyzeheader](https://toolbox.googleapps.com/apps/messageheader/analyzeheader)

Another tool is called **Message Header Analyzer**. 

- **Message Header Analyzer**: [https://mha.azurewebsites.net/](https://mha.azurewebsites.net/)

Lastly, you can also use [mailheader.org](https://mailheader.org/).

Even though not covered in the previous Phishing rooms, a Message Transfer Agent (MTA) is software that transfers emails between sender and recipient. Read more about MTAs [here](https://csrc.nist.gov/glossary/term/mail_transfer_agent). Since we're on the subject, read about MUAs (Mail User Agent) [here](https://csrc.nist.gov/glossary/term/mail_user_agent).

The tools below can help you analyze information about the sender's IP address:

- IPinfo.io: [https://ipinfo.io/](https://ipinfo.io/)
Per the [site](https://ipinfo.io/), "_With IPinfo, you can pinpoint your users’ locations, customize their experiences, prevent fraud, ensure compliance, and so much more_".

- URLScan.io: [https://urlscan.io/](https://urlscan.io/)[](https://urlscan.io/)

Per the [site](https://urlscan.io/about/), "_urlscan.io is a free service to scan and analyse websites. When a URL is submitted to urlscan.io, an automated process will browse to the URL like a regular user and record the activity that this page navigation creates. This includes the domains and IPs contacted, the resources (JavaScript, CSS, etc) requested from those domains, as well as additional information about the page itself. urlscan.io will take a screenshot of the page, record the DOM content, JavaScript global variables, cookies created by the page, and a myriad of other observations. If the site is targeting the users one of the more than 400 brands tracked by urlscan.io, it will be highlighted as potentially malicious in the scan results_".

Notice that urlscan.io provides a screenshot of the URL. This screenshot is provided, so you don't have to navigate to the URL in question explicitly.

You can use other tools that provide the same functionality and more, such as [URL2PNG](https://www.url2png.com/) and [Wannabrowser](https://www.wannabrowser.net/).

- Talos Reputation Center: [https://talosintelligence.com/reputation](https://talosintelligence.com/reputation)

The same can be accomplished with the assistance of a tool. One tool that can aid us with this task is URL Extractor. 

- URL Extractor: [https://www.convertcsv.com/url-extractor.htm](https://www.convertcsv.com/url-extractor.htm)
You may also use [CyberChef](https://gchq.github.io/CyberChef/) to extract URLs with the Extract URLs recipe.  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5de58e2bfac4a912bcc7a3e9/room-content/a31606afb772b8f87eebf0ff59f00fce.png)

- VirusTotal: [https://www.virustotal.com/gui/](https://www.virustotal.com/gui/)

Per the [site](https://www.virustotal.com/gui/), "Analyze suspicious files and URLs to detect types of malware, automatically share them with the security community."

Another tool/company worth mentioning is [Reversing Labs](https://www.reversinglabs.com/), which also has a [file reputation service](https://register.reversinglabs.com/file_reputation).
 
- [https://www.joesecurity.org/](https://www.joesecurity.org/)[](https://www.joesecurity.org/)

Per the site, "_Joe Sandbox empowers analysts with a large spectrum of product features. Among them: Live Interaction, URL Analysis & AI based Phishing Detection, Yara and Sigma rules support, MITRE ATT&CK matrix, AI based malware detection, Mail Monitor, Threat Hunting & Intelligence, Automated User Behavior, Dynamic VBA/JS/JAR instrumentation, Execution Graphs, Localized Internet Anonymization and many more_".

https://t.co/yuxfZm8KPg?amp=1

The **[SPF Surveyor](https://dmarcian.com/spf-survey/)** tool from dmarcian enables us to gain a visual look at DNS records. It also helps ensure the record uses the correct syntax.
**
Google Admin Toolbox** [**Messageheader**](https://toolbox.googleapps.com/apps/messageheader/) allows you to analyze delivery details using an email's full header. It shows various record results, including SPF.

“DKIM stands for DomainKeys Identified Mail and is used for the authentication of an email that’s being sent. Like SPF, DKIM is an open standard for email authentication that is used for DMARC alignment. A DKIM record exists in the DNS, but it is more complex than SPF. DKIM’s advantage is that it can survive forwarding, which makes it superior to SPF and a foundation for securing your email.”

Dmarcian has some great [resources](https://dmarcian.com/dkim-selectors/) if you wish to learn further about DKIM. You can also check out their [DKIM Record Checker](https://dmarcian.com/dkim-inspector/) and [Validator](https://dmarcian.com/dkim-validator/).

“DMARC, an open source standard, uses a concept called alignment to tie the result of two other open source standards,  SPF (a published list of servers that are authorized to send email on behalf of a domain) and DKIM (a tamper-evident domain seal associated with a piece of email), to the content of an email.”
Here is some [further reading](https://dmarcian.com/what-is-a-dmarc-record/) about DMARC records if you're interested in learning more.

Another great [tool](https://dmarcian.com/domain-checker/) by dmarcian that inspects DMARC, SPF, and DKIM records to identify any issues.

**Secure/Multipurpose Internet Mail Extensions** ([**S/MIME**](https://learn.microsoft.com/en-us/exchange/security-and-compliance/smime-exo/smime-exo)) is a standard protocol for sending digitally signed and encrypted messages.

Response code: Requested action not taken: mailbox name not allowed (553)

## Technical Defenses

Modern email systems employ various technical controls to help detect and block phishing messages before they reach users.

- [**Email Filtering**](https://www.spamhaus.org/resource-hub/ip-domain-reputation/): Provides filtering based on IP and domain reputation, allowing for blocking or quarantining of suspicious messages.
- [**Secure Email Gateways**](https://www.cloudflare.com/learning/email-security/secure-email-gateway-seg/) (SEGs): Scan messages to detect impersonation attempts, spoofing, and other phishing techniques that other filters might miss.
- [**Link Rewriting**](https://learn.microsoft.com/en-us/defender-office-365/safe-links-about): Replaces suspicious or unknown URLs with safe, redirected ones, giving the system time to scan and verify the link.
- [**Sandboxing**](https://learn.microsoft.com/en-us/defender-office-365/safe-attachments-about): Isolates and tests suspicious links or attachments in a secure, virtual environment to check for malicious behavior.

## User-Facing Tools & Training

Even with strong technical defenses in place, some phishing emails will inevitably reach users. Giving users clear visual cues and education is essential.

- **Trust & Warning Indicators**: Modern email platforms display visual cues to help users understand if a message is safe. A banner may read “External Sender,” “Suspicious Link,” or signify that a message is from a trusted organization or sender. 
- **Phishing Reporting**: Easy, in-email reporting options that let users quickly report suspicious messages.
- **User Awareness Training**: Train employees on identifying phishing attempts, social engineering tactics, and safe email practices.
- **Phishing Simulation Exercises**: Run controlled phishing campaigns to test and reinforce employee training.

_Note: Having DMARC, SPF, and DKIM in place is now a requirement from [Google](https://support.google.com/mail/answer/81126?sjid=12081390133285726533-EU) and [Yahoo](https://senders.yahooinc.com/best-practices/)._ _Use our [SPF Record Checker](https://mailtrap.io/free-spf-record-checker/) to verify your SPF syntax and authorized senders, our [DKIM Record Checker](https://mailtrap.io/free-dkim-record-checker/) to confirm your DKIM public key is published correctly, and our [DMARC Record Checker](https://mailtrap.io/free-dmarc-record-checker/) to validate your domain’s DMARC policy and protect against spoofing._

setoolkit - a tool for phishing