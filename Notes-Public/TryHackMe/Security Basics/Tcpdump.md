Tcpdump is network capture tool.  It uses libpcap, that is written in C and C++. They we're released for Unix-like systems. They're the backbone for various networking tools today.

Tcpdump can be ran without any arguments, however it's only useful for testing if this command works! First of, you need to know the network interface you want to listen using -i INTERFACE ( where you insert INTERFACE an interface you want to listen to), such as -i eth0. ip address show ( or just ip a s) lists available network interfaces.
![[Pasted image 20251028141837.png]]
Or from example above -i lo or -i ens5.
The list of other basic commands (to have fun with):
- -w FILE, writes the captured packet to a file
- -r FILE, reads existing file
- -c COUNT, limits how much packets you want to capture. If you don't specify the number it will go on until you click Ctrl+C.
- Tcpdump by default resolves IP addresses and ports and prints domain names where possible. To stop it use the -n argument. If you don't want it to also resolve the port numbers, like port 80 with HTTP, then you can use the -nn argument instead.
- To produce more verbose output, -v. To produce even more verbose output, use -vv or -vvv

# Filtering
You can filter by host. You can use src host IP or src host HOST to filter by source host. Or dest host IP or dest host HOST to filter by destination host.

To filter by port, use port NUMBER.

To filter by protocol by specifying the specific protocol, examples include: ip, ip6, tcp, dhcp, ftp and icmp.

Basic logical operators consists of: and, or, not. 
and - For example host example.com and http indicates that the host should be example.com and uses http protocol
or - host example.com or http means that the host should be example.com or http
not - not http filters packets that are not http

The wc flag with piping helps us count the number of packets.


How many packets in `traffic.pcap` use the ICMP protocol?
tcpdump -r traffic.pcap icmp | wc
Answer: 26
What is the IP address of the host that asked for the MAC address of 192.168.124.137?
Search for arp.
192.168.124.148
What hostname (subdomain) appears in the first DNS query?
tcpdump -r traffic.pcap -n -A 'port 53' to inspect DNS queries better and see the hostnames.
mirrors.rockylinux.org

# Advanced Filtering
You can use pcap-filter for advanced filtering and man pcap-filter for help.
Those two flags filters packets that are greater or lesser than:
- greater LENGTH
- less LENGTH
Binary options:
- & - AND logical operator
- | - OR logical operator
- ! - NOT logical operator
Header bytes syntax is: protocol[expr:size], where:
- protocol refers to protocol. For example http, ftp, udp, tcp
- expr indicates the byte offset, where 0 is the first byte
- size indicates a number of bytes that you want to see, which can be 1, 2, 4. The default is 1.
How many packets have only the TCP Reset (RST) flag set?
tcpdump -r traffic.pcap "tcp[ tcpflags] == tcp-rst" | wc
57 
What is the IP address of the host that sent packets larger than 15000 bytes?
tcpdump -r traffic.pcap greater 15000
185.117.80.53

# Displaying packets
Tryhackme selected to cover the following 5 options:
-  -q: Quick output
-  -e: print the link-layer header
-  -A: show packet data in ASCII
-  -xx: show packet data in hex
-  -X show packet data in ASCII and hex
What is the MAC address of the host that sent an ARP request?
52:54:00:7c:d3:5b