Microsoft Intune is one of the most widely used Mobile Device Management (MDM) platforms in the enterprise. It is a powerful tool in the hands of IT and security teams, but it can also become a weapon for attackers, as proven by the recent wiper attack on Stryker.

Microsoft Intune is a cloud-based Mobile Device Management platform. It lets your organization audit how Windows, Linux, MacOS, and mobile devices are used across your environment and remotely control their password policy, disk encryption, OS settings, application allowlist, and much more. Other popular MDM vendors you might have heard of are Jamf, JumpCloud, Atera, and Manage Engine.

## Wiper Attack on Stryker

In the wrong hands, the Intune console can become a fully-featured Command & Control server, or a weapon for mass destruction of corporate data. On March 11, 2026, the threat actors [allegedly compromised(opens in new tab)](https://www.bleepingcomputer.com/news/security/stryker-attack-wiped-tens-of-thousands-of-devices-no-malware-needed/) an administrative M365 account of Stryker, a US-based medtech giant, and issued a remote wipe Intune command across nearly 80,000 enrolled devices. Within hours, data was erased, causing a major disruption to Stryker's operations.

**Intune Bulk Device Actions**

Intune supports bulk actions across enrolled devices: restart, rename, and wipe, among them. With administrative access to the Intune console, any user can issue a wipe command against the selected devices, across all platforms except Linux. The moment the agent receives the command, it immediately resets the device to factory settings, erasing local data. This exact functionality was weaponized to destroy data across nearly 80,000 devices.

![Microsoft Intune admin center "Bulk device action" screen with one Windows device selected, illustrating how a factory reset could be remotely triggered across multiple devices.](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1773866275644.png)

_Devices > Bulk device action > Wipe_

![Windows screen showing the "Resetting this PC" message after being wiped via Intune.](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1773858132728.png)

## Monitoring Remote Wipes

First of all, remember that there is no sense in building SIEM rules like "Mass Device Wipe via Intune", because by the time your SOC triages the alert, the wipe will already finish (there is no documented way of aborting the Intune command). Still, let's see a timeline of events leading to wiper attacks:

**Intune Login**

The first stage is to detect logins to the Intune portal. At a minimum, you should alert on logins of Intune administrators from unmanaged devices, suspicious IPs, or outside of working hours. Regular Entra ID sign-in logs record every Intune login with **appDisplayName** set to "**Microsoft Intune portal extension**".

An advanced adversary can also use Intune via Graph API instead of a web browser. You can detect it whenever someone consents to the app with **DeviceManagementManagedDevices.*** or **DeviceManagementConfiguration.*** OAuth permissions ([Mandiant example(opens in new tab)](https://cloud.google.com/blog/topics/threat-intelligence/abusing-intune-permissions-entra-id-environments)). But for this room, let's focus on the more common attack path, Intune access via a web browser.

|Splunk query to detect Intune logins from unmanaged devices|
|---|
|```c<br>index=intune sourcetype=azure:aad:signin appDisplayName=*Intune* deviceDetail.displayName=""<br>\| rename deviceDetail.* as dvc.*<br>\| table _time appDisplayName ipAddress dvc.isManaged dvc.isCompliant dvc.displayName user<br>```|

**Wipe Command**

Unfortunately, the next and final point where you can catch Intune abuse is already the remote wipe. Whenever a user initiates a remote command, you see the corresponding logs in **Tenant admin** > **Audit logs** Intune panel in real time. Note that, unlike in Entra ID and M365, you can't ingest Intune logs directly into SIEM. You'd need to use the Graph API or route the logs through Azure Event Hub ([Documentation(opens in new tab)](https://learn.microsoft.com/en-us/intune/intune-service/fundamentals/monitor-audit-logs)).

![Intune Tenant Admin audit logs showing a successful "wipe ManagedDevice" action initiated via the Microsoft Intune portal extension, with full activity details including actor UPN and correlation ID.](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1773866140825.png)
|Splunk query to detect remote wiper (Note that the sourcetype is custom)|
|---|
|```c<br>index=intune sourcetype="o365:graph:intune" wipe<br>\| eval deviceid=mvindex('resources{}.modifiedProperties{}.newValue', 0)<br>\| table _time activityType actor.userPrincipalName deviceid<br>```|

d66b71f3-a644-4392-89b2-d97ba5612356

## Intune Platform Scripts

Remote wipe is not the only weapon available to an attacker with Intune access. The platform also allows administrators to deploy custom scripts (**Platform scripts**), such as PowerShell, and execute them under the context of the logged-in user or the local SYSTEM account. The Platform scripts feature lets IT administrators push one-time commands in bulk, useful for tasks that aren't covered by built-in templates and configuration policies:

![Intune Windows "Scripts and remediations" panel showing one assigned PowerShell platform script named "ad-dns-fix".](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1773878042128.png)

The Platform scripts feature might also be interesting for threat actors, as it is easy to write a PowerShell data stealer or deploy it on all devices. Check out [this(opens in new tab)](https://sansorg.egnyte.com/dl/6crjWkYYJcdx) SANS presentation for a deep dive and a real-world attack example. Also, note that there are **no safeguards** against malicious commands and **no email notification** to the IT team, so vigilant log monitoring is the way to go!

**SIEM Artifacts**

Script lifecycle consists of four stages: Script is **created** in the Intune console, **assigned** to the selected devices, **executed** on the devices (not logged), and **deleted** from Intune by IT at some point. You can see these stages in SIEM by starting from this query: `activityType=*DeviceManagementScript*`.

![Splunk query of Intune logs showing a user creating, assigning, and deleting a PowerShell device management script across multiple target devices.](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1773878042135.png)

The image above shows that some script was deleted, another one was created instead, and then assigned to two targets. Note that some target IDs are unique to your environment (e.g. group ID or host ID), while others are well-known. For example, `adadadad-808e-44e2-905a-0b7873a8a531` ID means `All Devices`. You can always try googling or retrohunting the IDs to find the readable name of the targets.

| Splunk query to detect platform scripts (Note that the sourcetype is custom)                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ```index=intune sourcetype="o365:graph:intune" activityType=*DeviceManagementScript*<br>\| eval action=mvindex(split(activityType, " "), 0)<br>\| eval script='resources{}.resourceId'<br>\| eval target=mvindex('resources{}.modifiedProperties{}.newValue', 0)<br>\| eval target=if(action="assignDeviceManagementScript", target, "N/A")<br>\| table _time actor.userPrincipalName action script target``` |
**Host Artifacts**

As mentioned in Task 2, all MDMs are agent-based, regardless of how the marketing frames it. On Windows, Intune executes Platform Scripts through a process tree below, which can be monitored via Security event 4688, or better, Sysmon event 1.

After execution, the script is automatically removed from the staging directory, but traces remain in debug logs. Execution output and metadata are written to the local Intune logfile, specifically **AgentExecutor.log** under **C:\ProgramData\Microsoft\IntuneManagementExtension\Logs**. From a forensic standpoint, this file is extremely valuable, as it captures:

|                              |                                                                                           |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| Time of the script execution | In my attempts, the delay between script creation and execution was approx. 30 minutes.   |
| Duration of the script run   | You will see separate events once the script is deployed, starts, and finishes execution. |
| Plaintext output or error    | See the screenshot below; there was no error in the script, and the output is "SECRET"    |
|                              |                                                                                           |
## Intune App Deployment

A more advanced attack scenario would be to package malware inside an app and compile it into the **.intunewin** format using a [Microsoft tool(opens in new tab)](https://github.com/Microsoft/Microsoft-Win32-Content-Prep-Tool), or classic **.dmg**/**.pkg** for MacOS. Intune can then be used to deploy the compiled application on the selected devices with the highest privileges, even if the app isn't signed by a trusted authority. For threat actors, this opens a whole range of possibilities: from ransomware and cryptocurrency miner deployment to data exfiltration at scale. 

|Splunk query to detect application events (Note that the sourcetype is custom)|
|---|
|```c<br>index=intune sourcetype="o365:graph:intune" activityType=*MobileApp*<br>```|
## Lessons Learned (Stryker Case)

The wiper attack covered in Task 4 was devastating in impact yet trivial to execute. All the attackers needed were valid credentials for a single Stryker employee with administrative access to the Intune portal. While unconfirmed, Internet users have already [found(opens in new tab)](https://www.reddit.com/r/cybersecurity/comments/1rwssna/forensics_on_the_stryker_breach_possibly/) compromised Stryker admin credentials in the wild, making it believable that the adversaries simply used the credentials via AiTM phishing or from infostealer dumps. 

## Protecting Admin Accounts

The first line of defense against a mass wipe event is controlling access to privileged accounts: Global Administrators, Intune Administrators, and any other role that grants wipe permissions. You have already learned how to monitor admin accounts in the [Entra ID monitoring](https://tryhackme.com/room/entraidmonitoring) room, but let's revisit the key suggestions:

- Use **Conditional Access** to prevent logins from unexpected devices and countries
- Use **Identity Protection** to alert on risky sign-ins, or auto-disable high-risk accounts
- Use Entra ID sign-in and audit logs to alert on **unreal travels** and other anomalies  
      
    
- Have **less than 5** Global Administrators, no matter the company size
- For all privileged accounts, enforce **passkeys** or **hardware MFA**
- Use Privileged Identity Management ([PIM(opens in new tab)](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure)) for administrative tasks
## Intune Security Features

No matter how mature your SOC is, incidents happen, and accounts get compromised. A single control is never enough. To limit the impact when a breach does occur, you should prefer custom Intune roles over Intune's default ones - default roles are broad, and that breadth might be abused by an attacker. Consider the following company structure:

- **The security team** (4 people) runs a remote wipe on stolen devices around once a year
- **The global IT** (6 people) occasionally uses Intune platform scripts, around once a month
- **The EU helpdesk** (10 people) often installs apps and changes policies across EU-based devices
- **The US helpdesk** (10 people) has the same workflow, but works exclusively with US-based devices

Each of these tasks requires a distinct set of Intune privileges, so companies often take the path of least resistance, assigning the Intune Administrator role to every IT and helpdesk member. As a result, they maintain 30 accounts, each capable of initiating a mass wipe. A far more secure alternative is to define four custom roles:

1. **Security**: Allowed to wipe devices
2. **Global IT**: Allowed to run platform scripts
3. **Helpdesk Operator**: Allowed to install apps
4. **Helpdesk Admin**: Installs apps and changes policies

**Scope Tags**

Privileges can be reduced further through scope tags, an Intune feature that labels specific resources and restricts access based on those labels. In our scenario, since the EU helpdesk operates exclusively with EU-based hosts and the US helpdesk with US-based ones, workstations can be tagged by region. The **Helpdesk Operator** and **Helpdesk Admin** roles are then split into four groups: EU and US variants of each, each scoped to only the assets they need to manage.

**Multi Admin Approval**

Lastly, for rare and critical operations such as platform scripts and remote wipes, you can set up multi admin approval. In our scenario, it might be a good idea for the IT team to approve device wipes, and for the Security team to approve platform scripts. Just make sure there is only one or two Global Admins who can edit the approval policies, not the whole IT!