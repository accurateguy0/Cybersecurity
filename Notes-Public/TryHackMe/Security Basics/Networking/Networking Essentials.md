### UDP

UDP (User Datagram Protocol) allows us to reach a specific process on this target host. UDP is a simple connectionless protocol that operates at the transport layer, i.e., layer 4. Being connectionless means that it does not need to establish a connection.
### TCP

TCP (Transmission Control Protocol) is a connection-oriented transport protocol. It uses various mechanisms to ensure reliable data delivery sent by the different processes on the networked hosts. A TCP connection is established using what’s called a three-way handshake. Two flags are used: SYN (Synchronise) and ACK (Acknowledgment). The packets are sent as follows:

1. SYN Packet: The client initiates the connection by sending a SYN packet to the server. This packet contains the client’s randomly chosen initial sequence number.
2. SYN-ACK Packet: The server responds to the SYN packet with a SYN-ACK packet, which adds the initial sequence number randomly chosen by the server.
3. ACK Packet: The three-way handshake is completed as the client sends an ACK packet to acknowledge the reception of the SYN-ACK packet.
Encapsulation is a  concept of adding header to each layer to the packet:
- **Application data**: It all starts when the user inputs the data they want to send into the application, then it adds application protocol
- **Transport protocol segment or datagram**: adds the header information and creates the TCP **segment** (or UDP **datagram**). 
- **Network packet**: adds an IP header to the received TCP segment or UDP datagram. 
- **Data link frame**: The Ethernet or WiFi receives the IP packet and adds the proper header and trailer, creating a **frame**.

![Application data is encapsulated within a TCP segment or UDP datagram, which in turn is encapsulated within an IP packet. The IP packet is encapsulated within a data link frame.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1719849061418.svg)

 DHCP is an application-level protocol that relies on UDP; the server listens on UDP port 67, and the client sends from UDP port 68. Your smartphone and laptop are configured to use DHCP by default.
 DHCP follows four steps: Discover, Offer, Request, and Acknowledge (DORA):

1. **DHCP Discover**: The client broadcasts a DHCPDISCOVER message seeking the local DHCP server if one exists.
2. **DHCP Offer**: The server responds with a DHCPOFFER message with an IP address available for the client to accept.
3. **DHCP Request**: The client responds with a DHCPREQUEST message to indicate that it has accepted the offered IP.
4. **DHCP Acknowledge**: The server responds with a DHCPACK message to confirm that the offered IP address is now assigned to this client.

Address Resolution Protocol (ARP) makes it possible to find the MAC address of another device on the Ethernet.  The ARP Request is sent from the MAC address of the requester to the broadcast MAC address, `ff:ff:ff:ff:ff:ff` as shown in the first packet. The ARP Reply arrived shortly afterwards, and the host with the IP address `192.168.66.1` responded with its MAC address.

ARP is considered layer 2 because it deals with MAC addresses. Others would argue that it is part of layer 3 because it supports IP operations. What is essential to know is that ARP allows the translation from layer 3 addressing to layer 2 addressing.

ICMP is used for network diagnostics and error correction.  The two commands that use ICMP are: ping and traceroute.
Ping is a command that sends a echo request to check if the target is alive. The target would typically reply with ICMP respond message, tho it may not always be the case.
Traceroute is a command that checks the routing from your host to the target. The internet protocol has a field TTL that indicates maximum time before the packet is dropped by a router. When it's dropped by a router, the response would be with ICMP Time Exceeded message, tho most routers wouldn't reveal their IP address, unless it's an ISP. The rest would send a public IP, which then we can use to discover the domain name and geographical location, otherwise the packet is blocked entirely by the firewall.

You need proper routing to for example, establish a mobile to a web server. Some of the protocols are:
OSPF( Open Shortest Path First)
EIGRP (Enhanced Interior Gateway Routing Protocol) is a proprietary cisco routing protocol combines different algorithms. It chooses the best routes based on bandwidth and available networks.
BGF
RIP (Routing Information Protocol) a simple routing protocol that bases on calculating minimal amount of hops and amount of networks they can reach

The solution to IP depletion is NAT ( Network Address Translation). As the name suggests, it translates from private IP to public and vice versa. NAT-supporting routers maintains a table that translates network address between internal and external networks.