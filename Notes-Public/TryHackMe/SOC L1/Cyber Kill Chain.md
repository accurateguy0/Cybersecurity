**Reconnaissance** is the research and planning phase of an attack against a system or victim. Adversaries use this phase to gather information about their target to inform their next steps. This information can include infrastructure details, employee data, business processes, and exposed technologies. Reconnaissance is often passive and undetected.

Poor recon typically leads to sloppy attacks, while well informed adversaries can create highly targeted, believable payloads that increase their chances of success.

A valuable piece of recon is **OSINT** (Open-Source Intelligence). With OSINT, adversaries gather insights about their target through publicly available information. 
## Reconnaissance Types

- **Passive Recon:** This involves having no direct interaction with the target. This may include WHOIS lookups, social media scraping, or reviewing breach data.
- **Active Recon:** This involves direct contact with the target with activities such as social engineering, port scanning, banner grabbing, or probing for open services.

Let's look at it from the attacker's perspective, who initially doesn't know what company he wants to attack.
**Email harvesting** is the process of obtaining email addresses from public, paid, or free services. An attacker can use email-address harvesting for a phishing attack (a type of social-engineering attack used to steal sensitive data, including login credentials and credit card numbers). The attacker will have a big arsenal of tools available for reconnaissance purposes. Here are some of them:

- [theHarvester](https://github.com/laramies/theHarvester): other than gathering emails, this tool is also capable of gathering names, subdomains, IPs, and URLs using multiple public data sources.
- [Hunter.io](https://hunter.io/): this is an email hunting tool that will let you obtain contact information associated with the domain.
- [OSINT Framework](https://osintframework.com/): OSINT Framework provides the collection of OSINT tools based on various categories.

# Weaponisation
Most attackers usually use automated tools to generate the malware or refer to the [DarkWeb](https://www.kaspersky.com/resource-center/threats/deep-web) to purchase the malware. More sophisticated actors or nation-sponsored APT (Advanced Persistent Threat Groups) would write their custom malware to make the malware sample unique and evade detection on the target.
In the Weaponization phase, the attacker can adopt the following tactics:

- Create an infected Microsoft Office document containing a malicious macros or VBA (Visual Basic for Applications) scripts.
- Create a malicious payload or a very sophisticated worm, implant it on USB drives, and then distribute them in public.
- Set up Command and Control (C2) infrastructure for executing the commands on the victim's machine or deliver more payloads.
- Infect the victim's host with a backdoor, which would provide a way to access the computer system, and bypass the security mechanisms.
- Tailoring phishing templates or OAuth-consent apps to look legitimate and dupe the victim.

# Delivery
is when Megatron decides to choose the method for transmitting the payload or the malware onto the target environment. There are plenty of options to choose from: 

- Phishing email: after conducting the reconnaissance and determining the targets for the attack, the malicious actor could craft a malicious email that would target either a specific person (spear phishing attack) or multiple people in the company. The email would contain a malicious link or email attachment that would result into a compromise.
    
- USB drops offer the attacker a physical delivery medium into public places like coffee shops, car parks, or on the street. An attacker might decide to conduct a sophisticated USB Drop Attack by printing the company's logo on the USB drives and mailing them to the company while pretending to be a customer sending the USB devices as a gift.
    
- Watering hole attacks are targeted and designed to aim at a specific group of people by compromising the website they are usually visiting, redirecting them to a malicious website of the attacker's choice or creation. Victims would unintentionally download malware or a malicious application to their computer, resulting in a drive-by download. An example can be a malicious pop-up asking to download a fake Browser extension.
# Exploitation
Exploitation is the moment the attacker's code executes on the target, taking advantage of a known vulnerability. In this phase, Megatron can opt to utilise a number of key techniques to gain access:

- Malicious macro execution: This may have been delivered through a phishing email, that would execute ransomware when the victim opens it.
- Zero-day exploits: These leverages on unknown and unpatched flaws in a system. These exploits leave no opportunity for detection at the beginning.
- Known CVEs: The attacker can choose to exploit unpatched public vulnerabilities found on the target environment.

After gaining access to the system, the malicious actor could exploit software, system, or server-based vulnerabilities to escalate the privileges or move laterally through the network. 

Signs of exploitation to look out for include:

- Unexpected process spawns.
- Registry changes or new services created.
- Suspicious command-line arguments found in system logs.
# Installation
A backdoor is also known as an access point. Once the attacker gets access to the system, he would want to reconnect back to the system if he loses the connection to it or if he got detected and got the initial access removed. Or if the system is later patched, they will no longer have access to it. That is when the attacker needs to install a **[persistent backdoor](https://www.offensive-security.com/metasploit-unleashed/persistent-backdoors/).** A persistent backdoor will let the attacker access the system he compromised in the past.

The persistence can be achieved through:

- Installing a **web shell** on the webserver. A web shell is a malicious script written in web development programming languages such as ASP, PHP, or JSP used by an attacker to maintain access to the compromised system. Because of the web shell simplicity and file formatting (.php, .asp, .aspx, .jsp, etc.) can be difficult to detect and might be classified as benign. You may check out this great article released by [Microsoft](https://www.microsoft.com/security/blog/2021/02/11/web-shell-attacks-continue-to-rise/) on various web shell attacks.
- Installing a backdoor on the victim's machine. For example, the attacker can use [Meterpreter](https://www.offensive-security.com/metasploit-unleashed/meterpreter-backdoor/) to install a backdoor on the victim's machine. Meterpreter is a Metasploit Framework payload that gives an interactive shell from which an attacker can interact with the victim's machine remotely and execute the malicious code.
- Creating or modifying Windows services. This technique is known as [T1543.003](https://attack.mitre.org/techniques/T1543/003/) on MITRE ATT&CK (MITRE ATT&CK® is a knowledge base of adversary tactics and techniques based on real-world scenarios). An attacker can create or modify the Windows services to execute the malicious scripts or payloads regularly as a part of the persistence. An attacker can use the tools like **ssc.exe** (sc.exe lets you Create, Start, Stop, Query, or Delete any Windows Service) and [Reg](https://attack.mitre.org/software/S0075/) to modify service configurations. The attacker can also **[masquerade](https://attack.mitre.org/techniques/T1036/)** the malicious payload by using a service name that is known to be related to the Operating System or legitimate software.
- Adding the entry to the "run keys" for the malicious payload in the Registry or the Startup Folder. By doing that, the payload will execute each time the user logs in to the computer. According to MITRE ATT&CK, there is a startup folder location for individual user accounts and a system-wide startup folder that will be checked no matter what user account logs in

In this phase, the attacker can also use the **[Timestomping](https://attack.mitre.org/techniques/T1070/006/)** technique to avoid detection by the forensic investigator and also to make the malware appear as a part of a legitimate program. The timestomping technique lets an attacker modify the file's timestamps, including to modify, access, create and change times.
# Command & Control
After getting persistence and executing the malware on the victim's machine, Megatron opens up the C2 (Command and Control) channel through the malware to remotely control and manipulate the victim. This term is also known as **C&C or C2 Beaconing** as a type of malicious communication between a C&C server and malware on the infected host. The infected host will consistently communicate with the C2 server; that is also where the beaconing term came from.
# Exfiltration
