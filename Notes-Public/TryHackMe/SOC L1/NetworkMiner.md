## Operating Modes

There are two main operating modes:

- **Sniffer Mode**: Although it has a sniffing feature, it is not intended to use as a sniffer. The sniffier feature is available only on Windows. However, the rest of the features are available in Windows and Linux OS. Based on experience, the sniffing feature is not as reliable as other features. Therefore we suggest not using this tool as a primary sniffer. Even the official description of the tool mentions that this tool is a "Network Forensics Analysis Tool", but it can be used as a "sniffer". In other words, it is a Network Forensic Analysis Tool with but has a sniffer feature, but it is not a dedicated sniffer like Wireshark and tcpdump. 

- **Packet Parsing/Processing**: NetworkMiner can parse traffic captures to have a quick overview and information on the investigated capture. This operation mode is mainly suggested to grab the "low hanging fruit" before diving into a deeper investigation.
The best practice is to record the traffic for offline analysis, quickly overview the pcap with NetworkMiner and go deep with Wireshark for further investigation.

|   |   |   |
|---|---|---|
|**Feature**|**NetworkMiner**|**Wireshark**|
|Purpose|Quick overview, traffic mapping, and data extraction|In-Depth analysis|
|GUI|✅|✅|
|Sniffing|✅|✅|
|Handling PCAPS|✅|✅|
|OS Fingerprinting|✅|❌|
|Parameter/Keyword Discovery|✅|Manual|
|Credential Discovery|✅|✅|
|File Extraction|✅|✅|
|Filtering Options|Limited|✅|
|Packet Decoding|Limited|✅|
|Protocol Analysis|❌|✅|
|Payload Analysis|❌|✅|
|Statistical Analysis|❌|✅|
|Cross-Platform Support|✅|✅|
|Host Categorisation|✅|❌|
|Ease of Management|✅|✅|
## Mac Address Processing

NetworkMiner versions after version 2 can process MAC address specific correlation as shown in the picture below. This option will help you identify if there is a MAC Address conflict. This feature is not available before version 2.