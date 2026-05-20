
## Zero Tolerance
To find the **Process ID (PID)** of the tool used for remote execution, we need to look for **Sysmon Event ID 1** (Process Creation) for the tool we identified earlier: **PsExec64.exe**.

PsExec is a Sysinternals tool commonly used by attackers (and admins) to execute commands on remote systems.

```
index=zerotolerance Image="*powershell.exe" (Disable OR Set-MpPreference OR Exclusion OR "state off")
| table _time, User, CommandLine
```


```
index=zerotolerance (Image="*mimikatz*" OR Image="*powershell*" OR CommandLine="*mimikatz*")
| table _time, User, Image, CommandLine
```
### If it’s not PsExec:

If PsExec doesn't show a remote connection in the command line, the attacker might have used **PowerShell Remoting** or **WMI**. You can check for those with this query:

codeSplunk

```
index=zerotolerance EventCode=1 (CommandLine="*Enter-PSSession*" OR CommandLine="*Invoke-Command*" OR Image="*\\wmic.exe*")
| table _time, User, Image, CommandLine, ProcessId
```

### How to find the exact Pivot time:

Search for the execution of **mstsc.exe** (Microsoft Terminal Services Client) or a network connection on the RDP port (**3389**) to the target IP 10.10.152.240.

**Run this query:**

codeSplunk

```
index=zerotolerance (Image="*mstsc.exe" OR dest_port=3389)
| table _time, User, Image, dest_ip, dest_port
| sort _time
```

### The Splunk Query to find the script:

Run this query to list all PowerShell scripts executed in the zerotolerance index:

codeSplunk

```
index=zerotolerance Image="*powershell.exe" "*.ps1"
| table _time, User, CommandLine
| sort _time
```

# Night Promotion
BabyLockerKZ, extension .hazard18

index=* sourcetype="wineventlog"  EventCode=4104
| rex field=_raw "Creating Scriptblock text \((?<part>\d+) of (?<total>\d+)\):"
| rex field=_raw "(?s)\):\s*(?<chunk>.*?)\s*ScriptBlock ID:"
| sort 0 ScriptBlock_ID part
| stats list(chunk) as scriptblock by ScriptBlock_ID
| eval scriptblock=mvjoin(scriptblock, "")
| eval sb_len=len(scriptblock)
| table ScriptBlock_ID sb_len scriptblock
| sort - sb_len


index=scenario EventCode=3 Initiated=true   DestinationHostname="ip-10-10-110-26.eu-west-1.compute.internal"

index=scenario sourcetype="aws:cloudtrail" src_ip="152.42.128.207"  signature=GetObject

index=scenario host="SRV-JMP" EventCode=4624 | table Workstation_Name