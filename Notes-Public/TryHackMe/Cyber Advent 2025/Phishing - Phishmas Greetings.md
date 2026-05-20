**Social Engineering**

Social engineering in phishing is the art of manipulating people rather than breaking technology. Attackers craft believable stories, emails, calls, or chat messages that exploit emotions (fear, helpfulness, curiosity, urgency) and real-world context to lure the recipients of a message.

Now, read the content of the previous email you had opened. We can spot multiple social engineering techniques:

- **Impersonation:** Is a type of Social Engineering. The attacker is pretending to be McSkidy!
- **Sense of urgency:** We can observe words such as "urgent" and "immediately" to pressure the recipient.
- **Side channel:** The attacker tries to discourage the recipients from reaching McSkidy using his standard communication channels (phone and email address).
- **Malicious intention:** The attacker is trying to trick the user into giving VPN credentials. They can also try to ask for approval of payments, opening malware, or sharing sensitive data.
**Spoofing**

Email spoofing is another way attackers can trick users into thinking they are receiving emails from a legitimate domain.  
The message looks like it came from a trusted sender (the display name and “From:” you see in the preview), but the underlying headers tell a different story. Modern email clients can easily reject spoofing attempts, but because Wareville email protection is down, some spoofing attempts can pass silently!

On `Authentication-Results`, SPF, DKIM, and DMARC are security checks that help confirm if an email really comes from who it says it does:

- **SPF:** Says which servers are allowed to send emails for a domain (like a list of approved senders).
- **DKIM:** Adds a digital signature to prove the message wasn’t changed and really came from that domain.
- **DMARC:** Uses SPF and DKIM to decide what to do if something looks fake (for example, send it to spam or block it).

In short, most phishing attacks aren’t about dropping malware directly; they’re focusing on stealing access.  
Below you can see a diagram of this trending flow:

**![Diagram of the trending phishing flow. A phishing email containing a legitimate sharing application that redirects to a fake login page, or malicious file, or a fake invoice.](https://tryhackme-images.s3.amazonaws.com/user-uploads/68dac5d6d4d4f23175b3296f/room-content/68dac5d6d4d4f23175b3296f-1763985352543.png)**

**Legitimate Applications**

We can see attackers hiding behind trusted services such as Dropbox, Google Drive/Docs, and OneDrive, because those links look legitimate and often pass email filters.  
The most common scenario involves a shared file containing a very attractive proposal, such as a salary raise document from HR or a laptop upgrade.  
Once the user clicks on it, it redirects to a shared document with fake content. The goal is to lure users to access fake login pages to steal credentials or download malicious files.

**Fake Login Pages**

As we learned, credentials are the main goal of attackers nowadays, and fake login pages are their favourite trick for performing this.