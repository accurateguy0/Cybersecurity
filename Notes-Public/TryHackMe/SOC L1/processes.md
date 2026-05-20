`net.exe` is ==a legitimate Windows command-line utility for managing network resources, users, and services==
`robocopy.exe` is ==a command-line utility for Windows that provides robust file and directory copying and replication capabilities==, including the ability to handle interruptions and copy security information.

`nslookup.exe` is ==a command-line tool in Windows for querying the [Domain Name System (DNS)](https://www.google.com/search?q=Domain+Name+System+%28DNS%29&oq=nslookup.exe&gs_lcrp=EgRlZGdlKgkIABBFGDkYgAQyCQgAEEUYORiABDIGCAEQABgeMgYIAhAAGB4yBggDEAAYHjIGCAQQABgeMgYIBRAAGB4yBggGEAAYHjIGCAcQABge0gEIMzU2M2owajGoAgCwAgA&sourceid=chrome&ie=UTF-8&mstk=AUtExfCgGbK6Jdy5-ol4n5ldksd4Ne5LF-5FHeeBMlfJQm21IOAgGMU07r_wl-hDPYybKPsO_v0lwrL0AlnqlJi6FHGH6Qnq97QbYx_3isiXheiXrXjbI_ItsvSwiQVT4UcztUznv9rNajGcAourpvY7e9MSijpxSYR56IkP6Yv7zpX-vshEwO4hxMzLNOI9_gK2zytgDUI34dqB-5nl7gAGT7Zp195B64T67i0Zbo6wqgRvnxChqc7ewwznH8FZOJMh03GOFkSPisff8GBgwFij1ZLo&csui=3&ved=2ahUKEwjpq-24qPmQAxUlSvEDHXnjML0QgK4QegQIARAC) to troubleshoot and get information about domain names, IP addresses, and DNS records==.

`taskhostw.exe KEYROAMING` is ==a valid Windows process related to the Certificate Services Client and its task for key roaming==, often seen when a certificate is being handled or a related background task is running. The legitimacy of the process can be verified by checking if the `taskhostw.exe` file is located in `C:\Windows\System32`, which is the correct location for the legitimate executable.

A dynamic link library (DLL) is **a collection of one or more functions or variables in an executable module that is executable or accessible from a separate application module**. In an application without DLLs, all external function and variable references are resolved statically at bind time.

`taskhostw.exe` with the argument `keyroaming` indicates a legitimate Windows background task, likely related to the `Microsoft\Windows\CertificateServicesClient` scheduled task, which is responsible for managing certificates.

**`WUDFHost.exe`**, which is the Windows User Mode Driver Framework Host Process. The `WUDFHost.exe` is an essential and legitimate Windows process used to run drivers in user mode, protecting the kernel. Its service is started and managed by the Windows Service Control Manager, which is `services.exe` (PID 3648).

**Windows Service Control Manager (`services.exe`)** legitimately launching the **Windows Modules Installer service (`TrustedInstaller.exe`)**

`TrustedInstaller.exe` is ==the executable file for the Windows Modules Installer service==, which is a legitimate and essential part of Windows that manages Windows updates and other optional components. It is responsible for installing, modifying, and removing system updates and components, and is located in `C:\Windows\servicing\`. While it's a core system file, high CPU usage during updates can be a common issue.

taskhostw.exe is a legitimate Windows process that acts as a host for running DLL-based services, while NGCKeyPregen is related to the Windows Hello feature for managing security keys.

## Full Packet Capture

In task three, we discussed what a full packet looks like. Now, we want to know how to capture and inspect those packets. To do this, we have two options:

- Install a physical network tap
- Configure port mirroring

**Network Tap**  
A network tap is a physical device you place inline in your network. These devices create a copy of all the network traffic that passes without affecting performance. That copied data is then forwarded to a packet capture box, IDS, or other system using the dedicated monitoring port. It is interesting to know that a TAP operates only on the link layer of the TCP-IP model; it does not need a MAC or IP address, because it copies the electrical/light signals and sends them to its monitoring port. This way, there is no added delay to the network. The image below shows an example of a network TAP.

![Network TAP](https://tryhackme-images.s3.amazonaws.com/user-uploads/66c44fd9733427ea1181ad58/room-content/66c44fd9733427ea1181ad58-1760027292073.png)**Port Mirroring**  
Port mirroring is a software approach to copying packets from one port on an intermediary device to another that is attached to, for example, an IDS, packet capture box, or other systems. Each vendor has its own name. Cisco, for example, calls it SPAN. On the terminal below, we can see how to configure SPAN on a Cisco device. In this example, the packets going through `fastEthernet0/1` are duplicated and sent to `fastEthernet0/2`.

```json
Switch(config)# monitor session 1 source interface fastEthernet0/1
Switch(config)# monitor session 1 destination interface fastEthernet0/2
```

The image below shows what this would look like. The WIN-001 sends packets through the switch to communicate with the server. When the packet arrives at the switch, it gets duplicated and is also sent to the monitoring device.

![SPAN diagram](https://tryhackme-images.s3.amazonaws.com/user-uploads/66c44fd9733427ea1181ad58/room-content/66c44fd9733427ea1181ad58-1760354092835.png)
**Best Practices**  
When doing full packet capture, we need to take some things into account:

- Placement: Depending on which traffic we want to capture, we need to place the TAP or configure the mirror in the right place
- Duration: Full packet capture will require a proportionate amount of storage. If you capture traffic on a 1 Gbps line for a whole day, we would need an average of 10.8 TB of storage space. Imagine the amount of storage we need on 10Gb or 40Gb lines
- Mirror vs TAP: Physical taps offer close to zero performance reduction. Mirroring can impact performance when a huge amount of traffic passes through the mirrored port

## Network Statistics

Another great way to find anomalies in your network is to gather metadata about the data flowing through the network, such as counting the number of DNS requests that a host sends out. A few protocols facilitate this. We will briefly discuss two of them: NetFlow and IPFIX.

**NetFlow** is a protocol developed by Cisco that collects metadata about traffic flowing in a network. It is a great way to detect things like C2 traffic, data exfiltration, and lateral movement. The image below shows a sample of NetFlow output. As we can see, the sample does not contain individual packets but metadata about the flow of packets going from the source IP 12.1.1.1 to the destination IP 13.1.1.2.  
![NetFlow data example](https://tryhackme-images.s3.amazonaws.com/user-uploads/66c44fd9733427ea1181ad58/room-content/66c44fd9733427ea1181ad58-1760027513334.png)

**The Internet Protocol Flow Information Export protocol (IPFIX)** can be considered as the successor to NetFlow. NetFlow was initially a proprietary protocol from Cisco. This means that the protocol was designed for Cisco systems only. Only from NetFlow v9 on did Cisco include templating, so other vendors could adapt it to their devices. In collaboration with Cisco and other vendors, the IETF created IPFIX and released it as a vendor-neutral standard. It offers features similar to NetFlow, but includes more flexibility in configuring which fields to capture.