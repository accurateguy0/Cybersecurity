Let's examine the tools we will focus on in this room. These tools are the basic ones used for initial investigations. See the list below.

|**Tool**|**Investigative Value**|
|---|---|
|Procmon|A helpful tool for tracking system activity, especially regarding malware research, troubleshooting, and forensic investigations.|
|Process Explorer|Allows you to see the Process of the Parent-child relationship, DLLs loaded, and its path.|
|HxD|Malicious files can be examined or altered via hex editing.|
|Wireshark|Observing and investigating network traffic to look for unusual activity.|
|CFF Explorer|Can generate file hashes for integrity verification, authenticate the source of system files, and validate their validity.|
|PEStudio|Static analysis or studying executable file properties without running the files.|
|FLOSS|Extracts and de-obfuscates all strings from malware programs using advanced static analysis techniques.|
## HxD

HxD is a quick and flexible hex editor for editing files, memory, and drives of any capacity. It can be applied to forensic investigation, data recovery, debugging, and exact manipulation of binary data. Important features include viewing file and memory contents, editing, searching, and comparing hex data. Let's look at how the tool works.

![The image shows the hex value of a file](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e6bbe59a46ee9407fd65bbe/room-content/5e6bbe59a46ee9407fd65bbe-1727170785692.png)

This HxD hex editor snapshot shows the binary file **possible_medusa.txt**. The hex data on the left indicates the file's contents in hexadecimal, and the ASCII interpretation appears on the right. Interestingly, the file starts with **4D 5A (Little Endian)**, indicating it is executable.
## PEStudio

Static analysis, or studying executable file properties without running the files, is done with PEstudio. This feature is beneficial in several situations. PEstudio offers a variety of information about a file without putting users in danger of execution, which aids in identifying executables that seem suspect or harmful.

So, how does it work? Let's look at the image below.

![this image shows information about the certain file that you wish to examine.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e6bbe59a46ee9407fd65bbe/room-content/5e6bbe59a46ee9407fd65bbe-1727170785666.png)

This example shows the examination of an executable file, PSexec.exe ( **not in the VM; this is a pure example only**), using PEstudio 9.22, a static malware analysis tool. The file has a dual purpose—legitimate for system administrators but potentially exploited by hackers for remote access.

The file's **entropy value of 6.596** indicates a remote chance of packing or encryption, which is typical of dangerous software. **Version 2.34** of this 32-bit console-based application allows it to run programs remotely, a feature frequently used to migrate laterally during attacks. The file is assembled using **Visual C++ 8**.

The dual-use nature of **PsExec**, typically legitimate but suspicious in compromised environments, combined with **low to medium indicators** and moderately high entropy, makes its presence on a system concerning, especially if remote code execution is not expected. Its use in **post-exploitation phases** warrants further investigation to determine if it’s being misused maliciously.****

$$\mathbf{RijndaelManaged}$$
$$\mathbf{042c6b16f932b7d83d864033b4c9bf27}$$