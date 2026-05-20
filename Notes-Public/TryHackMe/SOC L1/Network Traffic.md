## Transport
 **Session hijacking** can be detected by analyzing the **sequence numbers** included in the header. If the sequence numbers are suddenly far apart, further investigation is warranted. The output below shows a series of packets captured with Wireshark. 

```json
No.     Time        Source          Destination     Protocol Length  Info
1       0.000000    192.168.1.45    172.217.22.14   TCP      74      51432 → 80 [SYN] Seq=0 Win=64240 Len=0 MSS=1460
2       0.000120    172.217.22.14   192.168.1.45    TCP      74      80 → 51432 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1460
3       0.000220    192.168.1.45    172.217.22.14   TCP      66      51432 → 80 [ACK] Seq=1 Ack=1 Win=64240 Len=0
4       0.010500    192.168.1.45    172.217.22.14   TCP      1514    51432 → 80 [PSH, ACK] Seq=1 Ack=1 Win=64240 Len=1460
5       0.010620    172.217.22.14   192.168.1.45    TCP      66      80 → 51432 [ACK] Seq=1 Ack=1461 Win=65535 Len=0
6       0.020100    192.168.99.200  172.217.22.14   TCP      74      51432 → 80 [PSH, ACK] Seq=34567232 Ack=1 Win=64240 Len=20  
```

- The first 3 lines show a normal TCP 3-way handshake
- Lines 4 and 5 show legitimate data transfer
- Line 6 shows a packet from another source trying to inject itself into the session. Note the massive jump in the sequence number

## Internet
The fields that are most often logged are the source and destination IP and TTL. This is sufficient for most use cases. But, if we want to, for example, detect fragmentation attacks, we will need to inspect the fragment offset and total length fields as well. There are different variations of a fragmentation attack. For example, an attacker can create tiny fragments to evade the IDS or mess up the reassembly of fragments by using overlapping byte ranges. The offset in line 3 (highlighted in yellow) overlaps with the one in line 2. This means that the complete packet can be reassembled one way or another. Attackers can use this technique to bypass an IDS, for example.

```json
No.   Time       Source        Destination   Protocol Length Info
1     0.000000   203.0.113.45  192.168.1.10  UDP      1514    Fragmented IP protocol (UDP) (id=0x1a2b) [MF] Offset=0, Len=1480
2     0.000015   203.0.113.45  192.168.1.10  UDP      1514    Fragmented IP protocol (UDP) (id=0x1a2b) [MF] Offset=1480, Len=1480
3     0.000030   203.0.113.45  192.168.1.10  UDP       600    Fragmented IP protocol (UDP) (id=0x1a2b) Offset=1480, Len=64   <-- Overlap
4     0.000045   192.168.1.10  203.0.113.45  ICMP      98     Destination unreachable (Fragment reassembly time exceeded)
```
## Link
Once the internet layer finishes encapsulation, the IP packet is sent to the link layer. The link layer adds its header as well, containing more addressing information. Most logs will display the source and destination MAC addresses. For certain types of attacks, for example, ARP poisoning or spoofing, the information in the logs won't be sufficient. For these types of attacks, we need the full packet and context. What you, for example, can't see in a log is when the MAC address appears from multiple interfaces or when many gratuitous ARP packets are sent out with conflicting MAC addresses. The example below shows a packet capture detailing an ARP poisoning attack. The host with IP 192.168.1.200 is replying to each ARP request with the same MAC.

```json
No.   Time       Source           Destination      Protocol Length Info
1     0.000000   192.168.1.1      Broadcast        ARP      60     Who has 192.168.1.10? Tell 192.168.1.1
2     0.000025   192.168.1.10     192.168.1.1      ARP      60     192.168.1.10 is at 00:11:22:33:44:55
3     1.002010   192.168.1.200    192.168.1.1      ARP      60     192.168.1.10 is at aa:bb:cc:dd:ee:ff  <-- Attacker spoof
4     1.002015   192.168.1.200    192.168.1.10     ARP      60     192.168.1.1 is at aa:bb:cc:dd:ee:ff  <-- Attacker spoof
5     1.100000   192.168.1.10     172.217.22.14    TCP      74     54433 → 80 [SYN] Seq=0 Win=64240 Len=0
6     1.100120   192.168.1.200    172.217.22.14    TCP      74     54433 → 80 [SYN] Seq=0 Win=64240 Len=0  <-- Relayed via attacker
```



In the previous task, we discussed what we can observe theoretically based on the TCP/IP stack. Practically, it is more helpful to focus on specific sources and flows. A corporate network typically has some predetermined network flows and sources. We can group the sources into two categories:

- Intermediary
- Endpoint

The flows we can also group into two categories:

- North-South: Traffic that exits or enters the LAN and passes the firewall
- East-West: Traffic that stays within the LAN (including LAN that extends to the cloud)

**North-South Traffic**  
NS traffic is often monitored closely as it flows from the LAN to the WAN and vice versa. The most well-known services in this category are client-server protocols like HTTPS, DNS, SSH, VPN, SMTP, RDP, and many more. Each of these protocols has two streams: ingress (inbound) and egress (outbound). All of this traffic passes the firewall in one way or another. Configuring firewall rules and logging properly are key to visibility.

**East-West Traffic**  
EW traffic stays within the corporate LAN, so it is often monitored less. However, it is important to keep track of these flows. When the network is compromised, an attacker will often exploit different services internally to move laterally within the network. As we see below, there are many services within this category. Click on each category to see which services it contains.

Directory, Authentication & Identity Services

- Kerberos / LDAP: Authentication/queries to Active Directory
- RADIUS / TACACS+: Network access control
- Certificate Authority issuing internal certifications

File shares & print services

- SMB/CIFS: Accessing network drives
- IPP/LPD: Printing over the network

Router, switching, and infrastructure services

- DHCP traffic between hosts and the DHCP server
- ARP broadcast messages
- Internal DNS
- Routing protocol messages

Application Communication

- Database Connections: SQL over TCP
- Microservices APIs: REST or gRPC calls between services

Backup & Replication

- File Replication: Between data centers or to backup servers
- Database Replication: MySQL binlog replication, PostgreSQL streaming, and more

Monitoring & Management

- SNMP: Device health metrics
- Syslog: Centralized logging
- NetFlow/IPFIX: Traffic flow telemetry
- Other endpoint logs sent to a central logging server

## Flow Examples

Let's have a visual look at some of the network flows mentioned above.

**HTTPS**  
There are different variations of HTTPS network traffic flows. Let's examine a flow where the web proxy does TLS inspection:  
A host requests a website; this request is sent to the NGFW, which includes a web proxy. The web proxy will act as the web server and simultaneously establish a new TCP session with the actual web server and forward the clients' requests. When the web proxy receives the answer from the web server, it inspects its contents and then forwards it to the host if deemed safe. To summarize, we have two sessions, one between the client and the proxy and the other between the proxy and the web server. From the client's point of view, it has established a session with the web server.

![HTTPS Network Flow](https://tryhackme-images.s3.amazonaws.com/user-uploads/66c44fd9733427ea1181ad58/room-content/66c44fd9733427ea1181ad58-1760459431334.svg)

**External DNS**  
DNS traffic within a corporate network starts when a host sends a DNS query. The host sends the query to the internal DNS server on port 53, which will then act on behalf of the host. First, it will check if it has an answer to the query in its cache; if not, it will send the query via the router, through the firewall, to the configured DNS servers. The answer will then follow the same path to the internal DNS server, which will then forward it to the host. The network diagram below shows a simplified flow.

![DNS Network Flow](https://tryhackme-images.s3.amazonaws.com/user-uploads/66c44fd9733427ea1181ad58/room-content/66c44fd9733427ea1181ad58-1760460288845.svg)

**SMB with Kerberos**  
When a host opens a share to, for example, \\FILESERVER\MARKETING, an SMB session is set up. First, authentication is done via Kerberos. When a user logged in on the host, it **authenticated** with the Key Distribution Center on the Domain Controller and received a Ticket Granting Ticket to request **"service authentication tickets"**. Now, the host requests a service ticket using the Ticket Granting Ticket it received earlier. The host then uses this ticket to establish the SMB connection. Once the SMB session is set up, the host can access the share. Below we see a simplified network diagram of the flow.

![HTTPS Flow](https://tryhackme-images.s3.amazonaws.com/user-uploads/66c44fd9733427ea1181ad58/room-content/66c44fd9733427ea1181ad58-1760459778270.svg)

Answer the questions below

Which category of devices generates the most traffic in a network?

Submit

Before an SMB session can be established, which service needs to be contacted first for authentication?

Submit

What does TLS stand for?

Submit

Task 5How Can We Observe Network Traffic?

Task 6Conclusion

## How likely are you to recommend this room to others?

12345678910

Submit now

[

![User avatar](https://tryhackme.com/static/svg/avatar.fab1b29e.svg "Echo")

](https://tryhackme.com/echo)

[](https://tryhackme.com/legal/terms-of-use)