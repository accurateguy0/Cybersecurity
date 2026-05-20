## Let's run Snort in Logger Mode

You can use Snort as a sniffer and log the sniffed packets via logger mode. You only need to use the packet logger mode parameters, and Snort does the rest to accomplish this.

Packet logger parameters are explained in the table below;

|   |   |
|---|---|
|**Parameter**|**Description**|
|-l|Logger mode, target **log, and alert** output directory. Default output folder is **/var/log/snort**<br><br>The default action is to dump as tcpdump format in **/var/log/snort**|
|**-K ASCII**|Log packets in ASCII format.|
|-r|Reading option: Review the logged events in Snort.|
|**-n**|Specify the number of packets to be processed or read. Snort will stop after reading the specified number of packets.|

Let's start using each parameter and see the difference between them. Snort needs active traffic on your interface, so we need to generate traffic to see Snort in action.

**Logfile Ownership**

Before generating logs and investigating them, we must remember the Linux file ownership and permissions. There is no need to delve into user types and permissions. The fundamental file ownership rule:

Snort needs superuser (root) rights to sniff the traffic, so once you run Snort with the "sudo" command, the "root" account will own the generated log files. Therefore, you will need "root" rights to investigate the log files. There are two different approaches to analyzing the generated log files:

  
**Elevation of privileges**

- Changing the ownership of files/directories - You can also change the ownership of the file/folder to read it as your user: `sudo chown username file` or `sudo chown username -R directory.` The "-R" parameter enables recursive processing of files and directories.

Logging with parameter "-l"

First, start the Snort instance in packet logger mode; `sudo snort -dev -l.`

Now start ICMP/HTTP traffic with the traffic-generator script.

Once the traffic is generated, Snort will start showing the packets and log them in the target directory. You can configure the default output directory in Snort.config file. However, you can use the "-l" parameter to set a target directory. Identifying the default log directory is useful for continuous monitoring operations, and the "-l" parameter is much more useful for testing purposes.

The `-l`  part of the command creates the logs in the current directory. You will need to use this option to have the logs for each exercise in their folder.  

logging with -l

```shell-session
user@ubuntu$ sudo snort -dev -l.
                             
Running in packet logging mode

        --== Initializing Snort ==--
Initializing Output Plugins!
Log directory = /var/log/snort
pcap DAQ configured to passive.
Acquiring network traffic from "ens33".
Decoding Ethernet

        --== Initialization Complete ==--
...
Commencing packet processing (pid=2679)
WARNING: No preprocessors configured for policy 0.
WARNING: No preprocessors configured for policy 0.
```

Now, let's check the generated log file. **Note that the log file names will be different in your case.  
  
**

Checking the log file

```shell-session
user@ubuntu$ ls.                       
snort.log.1638459842
```

As you can see, it is a single all-in-one log file. It is a binary/tcpdump format log. This is what it looks like in the folder view.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6131132af49360005df01ae3/room-content/157fbfefd174cf32af1de4b2e1d09721.png)

  
Logging with parameter "-K ASCII"

Start the Snort instance in packet logger mode; `sudo snort -dev -K ASCII`

Now run the traffic-generator script as sudo and start ICMP/HTTP traffic. Once the traffic is generated, Snort will start showing the  packets in verbosity mode as follows:

Logging with -K ASCII

```shell-session
user@ubuntu$ sudo snort -dev -K ASCII -l.
                             
Running in packet logging mode

        --== Initializing Snort ==--
Initializing Output Plugins!
Log directory = /var/log/snort
pcap DAQ configured to passive.
Acquiring network traffic from "ens33".
Decoding Ethernet

        --== Initialization Complete ==--
...
Commencing packet processing (pid=2679)
WARNING: No preprocessors configured for policy 0.
WARNING: No preprocessors configured for policy 0.
```

Now, let's check the generated log file.

Checking the log file

```shell-session
user@ubuntu$ ls .
                             
142.250.187.110  192.168.175.129  snort.log.1638459842
```

This is what it looks like in the folder view.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6131132af49360005df01ae3/room-content/ffaf2f3d78769c857afa18a87712dd90.png)

The logs created with the "-K ASCII" parameter are entirely different. There are two folders with IP address names. Let's look into them.  
  

checking the log file

```shell-session
user@ubuntu$ ls ./192.168.175.129/
                             
ICMP_ECHO  UDP:36648-53  UDP:40757-53  UDP:47404-53  UDP:50624-123
```

Once we look closer at the created folders, we can see that the logs are in ASCII and categorised format, so it is possible to read them without using a Snort instance.

This is what it looks like in the folder view.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6131132af49360005df01ae3/room-content/d0ea7902efe8cdae918e26fa70068358.png)

In a nutshell, ASCII mode provides multiple files in a human-readable format, allowing for easy reading of the logs using a text editor. In contrast to the ASCII format, the binary format is not human-readable and requires analysis using Snort or a similar application, such as tcpdump.

Let's compare the ASCII format with the binary format by opening both of them in a text editor. The difference between the binary log file and the ASCII log file is shown below. (Left side: binary format. Right side: ASCII format.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6131132af49360005df01ae3/room-content/5e8487745a7ee4d3d33e67c2967ebaba.png)

Reading generated logs with parameter "-r"

Start the Snort instance in packet reader mode; `sudo snort -r`

reading log files with -r

```shell-session
user@ubuntu$ sudo snort -r snort.log.1638459842
                             
Running in packet dump mode

        --== Initializing Snort ==--
Initializing Output Plugins!
pcap DAQ configured to read-file.
Acquiring network traffic from "snort.log.1638459842".

        --== Initialization Complete ==--
...
Commencing packet processing (pid=3012)
WARNING: No preprocessors configured for policy 0.
12/02-07:44:03.123225 192.168.175.129 -> 142.250.187.110
ICMP TTL:64 TOS:0x0 ID:41900 IpLen:20 DgmLen:84 DF
Type:8  Code:0  ID:1   Seq:49  ECHO
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
WARNING: No preprocessors configured for policy 0.
12/02-07:44:26.169620 192.168.175.129 -> 142.250.187.110
ICMP TTL:64 TOS:0x0 ID:44765 IpLen:20 DgmLen:84 DF
Type:8  Code:0  ID:1   Seq:72  ECHO
===============================================================================
Packet I/O Totals:
   Received:           51
   Analyzed:           51 (100.000%)
    Dropped:            0 (  0.000%)
   Filtered:            0 (  0.000%)
Outstanding:            0 (  0.000%)
   Injected:            0
===============================================================================
Breakdown by protocol (includes rebuilt packets):
...
      Total:           51
===============================================================================
Snort exiting
```

**Note that** Snort can read and handle binary log output (tcpdump and Wireshark can also handle this log format). However, if you create logs with the "-K ASCII" parameter, Snort will not read them. As you can see in the output above, Snort read and displayed the log file, just as it does in sniffer mode.

Opening log file with tcpdump.

Opening the log file with tcpdump

```shell-session
user@ubuntu$ sudo tcpdump -r snort.log.1638459842 -ntc 10
                             
reading from file snort.log.1638459842, link-type EN10MB (Ethernet)
IP 192.168.175.129 > 142.250.187.110: ICMP echo request, id 1, seq 49, length 64
IP 142.250.187.110 > 192.168.175.129: ICMP echo reply, id 1, seq 49, length 64
IP 192.168.175.129 > 142.250.187.110: ICMP echo request, id 1, seq 50, length 64
IP 142.250.187.110 > 192.168.175.129: ICMP echo reply, id 1, seq 50, length 64
IP 192.168.175.129 > 142.250.187.110: ICMP echo request, id 1, seq 51, length 64
IP 142.250.187.110 > 192.168.175.129: ICMP echo reply, id 1, seq 51, length 64
IP 192.168.175.129 > 142.250.187.110: ICMP echo request, id 1, seq 52, length 64
IP 142.250.187.110 > 192.168.175.129: ICMP echo reply, id 1, seq 52, length 64
IP 192.168.175.1.63096 > 239.255.255.250.1900: UDP, length 173
IP 192.168.175.129 > 142.250.187.110: ICMP echo request, id 1, seq 53, length 64
```

Opening the log file with Wireshark.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/6131132af49360005df01ae3/room-content/a4bd8447760481cd2f6f9762a9620a50.png)

The "-r" parameter also allows users to filter the binary log files. You can filter the processed log to see specific packets with the "-r" parameter and Berkeley Packet Filters (BPF). 

- `sudo snort -r logname.log -X`
- `sudo snort -r logname.log icmp`
- `sudo snort -r logname.log tcp`
- `sudo snort -r logname.log 'udp and port 53'`

The output will be the same as the above, but only packets with the chosen protocol will be shown. Additionally, you can specify the number of processes using the "-n" parameter. **The following command will process only the first 10 packets:** `Snort -dvr logname.log -n 10`

Please use the following resources to understand how the BPF works and its use.

- [https://en.wikipedia.org/wiki/Berkeley_Packet_Filter](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter)
- [https://biot.com/capstats/bpf.html](https://biot.com/capstats/bpf.html)
- [https://www.tcpdump.org/manpages/tcpdump.1.html](https://www.tcpdump.org/manpages/tcpdump.1.html)

Now, use the attached VM and navigate to the Task-Exercises/Exercise-Files/TASK-6 folder to answer the questions!

Answer the questions below

Investigate the traffic with the default configuration file with ASCII mode.  

`sudo snort -dev -K ASCII -l .`

Execute the traffic generator script and choose "TASK-6 Exercise". Wait until the traffic ends, then stop the Snort instance. Now analyse the output summary and answer the question.

`sudo ./traffic-generator.sh`

Now, you should have the logs in the current directory. Navigate to folder "145.254.160.237". What is the source port used to connect port 53?

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Action**   | There are several actions for rules. Ensure you understand the functionality and test it thoroughly before creating rules for live systems. The following are the most common actions:<br><br>- alert: Generate an alert and log the packet.<br>- log: Log the packet.<br>- drop: Block and log the packet.<br>- reject: Block the packet, log it, and terminate the packet session.                                                                        |
| **Protocol** | The protocol parameter identifies the type of protocol that was filtered for the rule.<br><br>Note that Snort2 supports only four protocol filters in the rules (IP, TCP, UDP, and ICMP). However, you can detect the application flows using port numbers and options. For instance, if you want to detect FTP traffic, you cannot use the FTP keyword in the protocol field; instead, you can filter FTP traffic by investigating TCP traffic on port 21. |

**IP and Port Numbers**

These parameters identify the source and destination IP addresses, as well as the associated port numbers, filtered for the rule.

|                                  |                                                                                                                                                                                                                                                                                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **IP Filtering**                 | alert icmp 192.168.1.56 any <> any any  (msg: "ICMP Packet From "; sid: 100001; rev:1;)<br><br>This rule will create an alert for each ICMP packet originating from the 192.168.1.56 IP address.                                                                                                                                   |
| **Filter an IP range**           | alert icmp 192.168.1.0/24 any <> any any  (msg: "ICMP Packet Found"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each ICMP packet originating from the 192.168.1.0/24 subnet.                                                                                                                                   |
| **Filter multiple IP ranges**    | alert icmp [192.168.1.0/24, 10.1.1.0/24] any <> any any  (msg: "ICMP Packet Found"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each ICMP packet originating from the 192.168.1.0/24 and 10.1.1.0/24 subnets.                                                                                                   |
| **Exclude IP addresses/ranges.** | The "negation operator" is used to exclude specific addresses and ports. The negation operator is indicated with "!".<br><br>alert icmp !192.168.1.0/24 any <> any any  (msg: "ICMP Packet Found"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each ICMP packet not originating from the 192.168.1.0/24 subnet. |
| **Port Filtering**               | alert tcp any any <> any 21  (msg: "FTP Port 21 Command Activity Detected"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each TCP packet sent to port 21.                                                                                                                                                        |
| **Exclude a specific port**      | alert tcp any any <> any !21  (msg: "Traffic Activity Without FTP Port 21 Command Channel"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each TCP packet not sent to port 21.                                                                                                                                    |
| **Filter a port range (Type 1)** | alert tcp any any <> any 1:1024   (msg: "TCP 1-1024 System Port Activity"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each TCP packet sent to ports between 1 and 1024.                                                                                                                                        |
| **Filter a port range (Type 2)** | alert tcp any any <> any:1024   (msg: "TCP 0-1024 System Port Activity"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each TCP packet sent to ports 1 through 1024.                                                                                                                                              |
| **Filter a port range (Type 3)** | alert tcp any any <> any 1025: (msg: "TCP Non-System Port Activity"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each TCP packet sent to a source port that is higher than or equal to 1025.                                                                                                                    |
| **Filter a port range (Type 4)** | alert tcp any any <> any [21,23] (msg: "FTP and Telnet Port 21-23 Activity Detected"; sid: 100001; rev:1;)<br><br>This rule will create an alert for each TCP packet sent to ports 21 and 23.                                                                                                                                      |
In this section, you manage the IPS mode of Snort. The single-node installation model IPS model works best with "afpacket" mode. You can enable this mode and run Snort in IPS.

|   |   |   |
|---|---|---|
|**TAG NAME**|**INFO**|**EXAMPLE**|
|#config daq|IPS mode selection.|afpacket|
|#config daq_mode|Activating the inline mode|inline|
|#config logdir|Hardcoded default log path.|/var/logs/snort|

Data Acquisition Modules (DAQs) are specialized libraries used for packet I/O, providing flexibility in processing packets. It is possible to select the DAQ type and mode for different purposes.
There are six DAQ modules available in Snort:

- PCAP: Default mode, known as Sniffer mode.
- Afpacket: Inline mode, known as IPS mode.
- Ipq: Inline mode on Linux by using Netfilter. It replaces the snort_inline patch.  
- Nfq: Inline mode on Linux.
- Ipfw: Inline on OpenBSD and FreeBSD by using divert sockets, with the pf and ipfw firewalls.
- Dump: Testing mode of inline and normalisation.