## Internal SOC vs MSSP

Not every organization has the expertise to operate a SOC on its own and relies on a Managed Security Services Provider (MSSP), a company that delivers outsourced security services, most commonly SOC, to its clients. Working at MSSP is typically high-pressure, but it is also a good option to quickstart your career.

## Human As Attack Vectors

As threats evolve, staying informed about the latest attack trends is key to your success in the SOC. Here are a few great sites to follow:

- Krebs on Security - [https://krebsonsecurity.com](https://krebsonsecurity.com/)
- The Hacker News -  [https://thehackernews.com](https://thehackernews.com/)
- BleepingComputer - [https://www.bleepingcomputer.com](https://www.bleepingcomputer.com/)

## System as Attack Vectors
Even though SOC analysts don't typically manage systems directly, understanding the common attacks and defenses, and sharing them with the IT department, is a key to broadening your cyber security perspective. If you want to grow quickly and be a strong team player, stay updated on the latest threats and always share the news with others!

- [The DFIR Report: How Real Intrusions Happen](https://thedfirreport.com/)
- [CISA: Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [BleepingComputer: Latest Supply Chain Attacks](https://www.bleepingcomputer.com/tag/supply-chain-attack/)
- [CheckPoint: Interactive Live Cyber Threat Map](https://threatmap.checkpoint.com/)

## Communication Cases

- **You need to escalate an urgent, critical alert, but L2 is unavailable and does not respond for 30 minutes.**  
    Ensure you know where to find emergency contacts. First, try to call L2, then L3, and finally your manager.
    
- **The alert about Slack/Teams account compromise requires you to validate the login with the affected user.**  
    Do not contact the user through the breached chat - use alternative contact methods like a phone call.
    
- **You receive an overwhelming number of alerts during a short period of time, some of which are critical.**  
    Prioritise the alerts according to the workflow, but inform your L2 on shift about the situation.
    
- **After a few days, you realise that you misclassified the alert and likely missed a malicious action.**  
    Immediately reach out to your L2 explaining your concerns. Threat actors can be silent for weeks before impact.
    
- **You can not complete the alert triage since the SIEM logs are not parsed correctly or are not searchable.**  
    Do not skip the alert - investigate what you can and report the issue to your L2 on shift or SOC engineer.

**Sources of Identities**

| Solution         | Examples               | Description                                                           |
| ---------------- | ---------------------- | --------------------------------------------------------------------- |
| Active Directory | On-prem AD, Entra ID   | AD itself is an identity database, and it is commonly used by SOC     |
| SSO Providers    | Okta, Google Workspace | Cloud alternative for AD, an easy way to manage and search the users  |
| HR Systems       | BambooHR, SAP, HiBob   | Limited to employees only, but usually provides full employee data    |
| Custom Solution  | CSV or Excel Sheets    | It is common for IT or security teams to maintain their own solutions |
**Sources of Assets**

|Solution|Examples|Description|
|---|---|---|
|Active Directory|On-prem AD, Entra ID|AD is not only an identity but also a solid asset inventory database|
|SIEM or EDR|Elastic, CrowdStrike|Some SIEM or EDR agents collect information about the monitored hosts|
|MDM Solution|MS Intune, Jamf MDM|A dedicated class of solutions created to list and manage assets|
|Custom Solution|CSV or Excel Sheets|Same as with the identity inventory, custom solutions are common|

## SOC Workbooks

**SOC workbook**, also called playbook, runbook, or workflow, is a structured document that defines the steps required to investigate and remediate specific threats efficiently and consistently. Since L1 analysts are considered junior specialists and are not expected to triage every possible attack scenario perfectly, senior analysts often prepare workbooks to support their less experienced teammates. L1 analysts are recommended and sometimes even required to triage the alerts precisely according to workbooks to avoid mistakes and streamline the analysis.

## Workbook Example

**Unusual Login Location Workbook**

_![The flowchart showing the process from receiving a login alert through identity enrichment via BambooHR, Threat Intel usage, investigation using Splunk and escalation stages. It includes IP analysis, user behaviour checks, and conditions for escalating to L2 or closing alerts based on actions preceding or following the login](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1743455620681.svg)_

Next, remember that an alert by itself will not stop the breach, and it is important to timely receive the alert, triage it, and respond to the attack before the attackers achieve their goals. The requirements to ensure a quick detection and remediation of the threat are commonly grouped into a **Service Level Agreement (SLA)** - a document signed between the internal SOC team and its company management, or by the managed SOC provider (MSSP) and its customers. The agreement usually requires quick threat detection (measured by **MTTD**), timely alert acknowledgement by L1 analysts (measured by **MTTA**), and finally, prompt response to the threat, like isolating the device or securing the breached account (measured by **MTTR**):

![Metrics timeline showing a typical threat timeline, where first we measure MTTD, then MTTA, and finally MTTR](https://tryhackme-images.s3.amazonaws.com/user-uploads/678ecc92c80aa206339f0f23/room-content/678ecc92c80aa206339f0f23-1746642255233.svg)

## Reference Table

Note that different teams might have different definitions or formulas for the SOC metrics, depending on what they want to measure. For this and the following tasks, please use the illustration above and the reference table below to answer the questions.

| Metric                          | Common SLA | Description                                                              |
| ------------------------------- | ---------- | ------------------------------------------------------------------------ |
| SOC Team Availability           | 24/7       | Working schedule of the SOC team, often Monday-Friday (8/5) or 24/7 mode |
| Mean Time to Detect (MTTD)      | 5 minutes  | Average time between the attack and its detection by SOC tools           |
| Mean Time to Acknowledge (MTTA) | 10 minutes | Average time for L1 analysts to start triage of the new alert            |
| Mean Time to Respond (MTTR)     | 60 minutes | Average time taken by SOC to actually stop the breach from spreading     |