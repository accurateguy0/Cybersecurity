Nmap offers a list scan with the option `-sL`. This scan only lists the targets to scan without actually scanning them. For example, `nmap -sL 192.168.0.1/24` will list the 256 targets that will be scanned. This option helps confirm the targets before running the actual scan.

`-sn` aims to discover live hosts without attempting to discover the services running on them. This scan might be helpful if you want to discover the devices on a network without causing much noise. However, this won’t tell us which services are running.

It is worth noting that we can have more control over how Nmap discovers live hosts such as `-PS[portlist]`, `-PA[portlist]`, `-PU[portlist]` for TCP SYN, TCP ACK, and UDP discovery via the given ports.
-sV scans the service and version system
-sS scans using the SYN packet, it is the "stealthy" way, because of how it doesn't make the full 3-way-handshake.
-sT is a connection scan that tries to scan every target port. If it's successful, it'll tear down the connection. It's like trying to connect to every target port using telnet.
-sU is a scan for UDP services.
-F is for Fast mode, which scan 100 most common ports. By default Nmap scans 1000 common ports.
-p[range] allows you to specify a range of ports to scan. For example -p 200-300 scans the ports from 200 to 300. -p- scans all ports.
-O OS detection
-Pn scans hosts that appear to be down
-A OS detection, version detection and tracerouting among other additions
Running your scan at its normal speed might trigger an IDS or other security solutions. It is reasonable to control how fast a scan should go. Nmap gives you six timing templates, and the names say it all: paranoid (0), sneaky (1), polite (2), normal (3), aggressive (4), and insane (5). You can pick the timing template by its name or number. For example, you can add `-T0` (or `-T 0`) or `-T paranoid` to opt for the slowest timing.
--min-parallelism <numprobes> and max-parallelism <numprobes>, min and max number of parallel probes
--min-rate <number> and --max-rate <number>, min and max rate (of packets/second)
--host-timeout, max amount of time to wait for a target host response
-oN <filename> - normal output
-oX <filename> - XML output
-oG <filename> - grep -able output (useful for grep and awk)
-oA <basename> - Output in all major formats
Verbosity allows you to observe the scan in real time. To add more verbosity you can use -v, or if you're unsatisfied with the verbosity you can add more like -vv or -vvvv or -v2 -v4. If all that verbosity is still not enough you can add a debugging option. To enable it add -d. The max debugging level output is -d9, so before you use it be ready for thousands of information and debugging line.
It's worth noting that it is best to run Nmap with sudo priviledges so that we can make use of all its features.
