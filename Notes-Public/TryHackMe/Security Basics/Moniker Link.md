 [CVE-2024-21413](https://www.cve.org/CVERecord?id=CVE-2024-21413)
 The ! special character was used to bypass Outlook's "Protected View"
 We use file:// Moniker Link type in the hyperlink.
## YARA
A [Yara rule](https://github.com/Neo23x0/signature-base/blob/master/yara/expl_outlook_cve_2024_21413.yar) has been created by [Florian Roth](https://twitter.com/cyb3rops/status/1758792873254744344) to detect emails containing the `file:\\` element in the Moniker Link.

## Wireshark

Additionally, the SMB request from the victim to the client can be seen in a packet capture with a truncated netNTLMv2 hash.