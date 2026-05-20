Several methodologies, best practices, and essential techniques are employed to create a coherent timeline and conduct effective log analysis investigations.

Timeline

When conducting log analysis, creating a timeline is a fundamental aspect of understanding the sequence of events within systems, devices, and applications. At a high level, a timeline is a chronological representation of the logged events, ordered based on their occurrence. The ability to visualize a timeline is a powerful tool for contextualizing and comprehending the events that occurred over a specific period.

Within incident response scenarios, timelines play a crucial role in reconstructing security incidents. With an effective timeline, security analysts can trace the sequence of events leading up to an incident, allowing them to identify the initial point of compromise and understand the attacker's tactics, techniques and procedures (TTPs).

Timestamp

In most cases, logs will typically include timestamps that record when an event occurred. With the potential of many distributed devices, applications, and systems generating individual log events across various regions, it's crucial to consider each log's time zone and format. Converting timestamps to a consistent time zone is necessary for accurate log analysis and correlation across different log sources.

Many log monitoring solutions solve this issue through timezone detection and automatic configuration. [Splunk](https://docs.splunk.com/Documentation/Splunk/9.1.0/Search/Abouttimezones), for example, automatically detects and processes time zones when data is indexed and searched. Regardless of how time is specified in individual log events, timestamps are converted to UNIX time and stored in the `_time` field when indexed.

This consistent timestamp can then be converted to a local timezone during visualization, which makes reporting and analysis more efficient. This strategy ensures that analysts can conduct accurate investigations and gain valuable insights from their log data without manual intervention.

Super Timelines

A super timeline, also known as a consolidated timeline, is a powerful concept in log analysis and digital forensics. Super timelines provide a comprehensive view of events across different systems, devices, and applications, allowing analysts to understand the sequence of events holistically. This is particularly useful for investigating security incidents involving multiple components or systems.

Super timelines often include data from previously discussed log sources, such as system logs, application logs, network traffic logs, firewall logs, and more. By combining these disparate sources into a single timeline, analysts can identify correlations and patterns that need to be apparent when analyzing logs individually.

Creating a consolidated timeline with all this information manually would take time and effort. Not only would you have to record timestamps for every file on the system, but you would also need to understand the data storage methods of every application. Fortunately, [Plaso (Python Log2Timeline)](https://github.com/log2timeline/plaso) is an open-source tool created by Kristinn Gudjonsson and many contributors that automates the creation of timelines from various log sources. It's specifically designed for digital forensics and log analysis and can parse and process log data from a wide range of sources to create a unified, chronological timeline.

To learn more about Plaso and its capabilities, visit the [official documentation page here](https://plaso.readthedocs.io/en/latest/).

Data Visualization

Data visualization tools, such as Kibana (of the Elastic Stack) and Splunk, help to convert raw log data into interactive and insightful visual representations through a user interface. Tools like these enable security analysts to understand the indexed data by visualizing patterns and anomalies, often in a graphical view. Multiple visualizations, metrics, and graphic elements can be constructed into a tailored dashboard view, allowing for a comprehensive "single pane of glass" view for log analysis operations.

![An example of a tailored Splunk dashboard for monitoring and performance](https://tryhackme-images.s3.amazonaws.com/user-uploads/6490641ea027b100564fe00a/room-content/caeace06b70e4c6920d32ae0bf22e8f4.png)  

To create effective log visualizations, it's essential first to understand the data (and sources) being collected and define clear objectives for visualization.

For example, suppose the objective is to monitor and detect patterns of increased failed login attempts. In that case, we should look to visualize logs that audit login attempts from an authentication server or user device. A good solution would be to create a line chart that displays the trend of failed login attempts over time. To manage the density of captured data, we can filter the visualization to show the past seven days. That would give us a good starting point to visualize increased failed attempts and spot anomalies.

Log Monitoring and Alerting

In addition to visualization, implementing effective log monitoring and alerting allows security teams to _proactively_ identify threats and immediately respond when an alert is generated.

Many SIEM solutions (like Splunk and the Elastic Stack) allow the creation of custom alerts based on metrics obtained in log events. Events worth creating alerts for may include multiple failed login attempts, privilege escalation, access to sensitive files, or other indicators of potential security breaches. Alerts ensure that security teams are promptly notified of suspicious activities that require immediate attention.

Roles and responsibilities should be defined for escalation and notification procedures during various stages of the incident response process. Escalation procedures ensure that incidents are addressed promptly and that the right personnel are informed at each severity level.

For a hands-on walkthrough on dashboards and alerting within Splunk, it is recommended to check out the [Splunk: Dashboards and Reports](https://tryhackme.com/jr/splunkdashboardsandreports) room!

External Research and Threat Intel

Identifying what may be of interest to us in log analysis is essential. It is challenging to analyze a log if we're not entirely sure what we are looking for.

First, let's understand what threat intelligence is. In summary, threat intelligence are pieces of information that can be attributed to a malicious actor. Examples of threat intelligence include:

- IP Addresses
- File Hashes
- Domains

When analyzing a log file, we can search for the presence of threat intelligence. For example, take this Apache2 web server entry below. We can see that an IP address has tried to access our site's admin panel.

Outputting an Apache2 Access Log

```shell-session
cmnatic@thm cat access.log
54.36.149.64 - - [25/Aug/2023:00:05:36 +0000] "GET /admin HTTP/1.1" 200 8260 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)"
191.96.106.80 - - [25/Aug/2023:00:33:11 +0000] "GET /TryHackMe/rooms/docker-rodeo/dockerregistry/catalog1.png HTTP/1.1" 200 19594 "https://tryhackme.com/" "Mozi>
54.36.148.244 - - [25/Aug/2023:00:34:46 +0000] "GET /TryHackMe/?C=D;O=D HTTP/1.1" 200 5879 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot>
66.249.66.68 - - [25/Aug/2023:00:35:53 +0000] "GET /TryHackMe%20Designs/ HTTP/1.1" 200 5973 "-" "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) 200 19594 "https://tryhackme.com/" "Mozi>
```

Using a threat intelligence feed like [ThreatFox](https://threatfox.abuse.ch/), we can search our log files for known malicious actors' presence.

![Threatfox output, highlighting several indicators of compromise in our log file](https://tryhackme-images.s3.amazonaws.com/user-uploads/6490641ea027b100564fe00a/room-content/c3ad6571c689577d907026d8a75d73c7.png)

  

Using GREP to search a logfile for an IP address

```shell-session
cmnatic@thm grep "54.36.149.64" logfile.txt
54.36.149.64
```

# Common Log File Locations

A crucial aspect of log analysis is understanding where to locate log files generated by various applications and systems. While log file paths can vary due to system configurations, software versions, and custom settings, knowing common log file locations is essential for efficient investigation and threat detection.

- **Web Servers:**
    - **Nginx:**
        - Access Logs: `/var/log/nginx/access.log`
        - Error Logs: `/var/log/nginx/error.log`
    - **Apache:**
        - Access Logs: `/var/log/apache2/access.log`
        - Error Logs: `/var/log/apache2/error.log`

- **Databases:**
    - **MySQL:**
        - Error Logs: `/var/log/mysql/error.log`
    - **PostgreSQL:**
        - Error and Activity Logs: `/var/log/postgresql/postgresql-{version}-main.log`

- **Web Applications:**
    - **PHP:**
        - Error Logs: `/var/log/php/error.log`

- **Operating Systems:**
    - **Linux:**
        - General System Logs: `/var/log/syslog`
        - Authentication Logs: `/var/log/auth.log`

- **Firewalls and IDS/IPS:**
    - **iptables:**
        - Firewall Logs: `/var/log/iptables.log`
    - **Snort:**
        - Snort Logs: `/var/log/snort/`

While these are common log file paths, it's important to note that actual paths may differ based on system configurations, software versions, and custom settings. It's recommended to consult the official documentation or configuration files to verify the correct log file paths to ensure accurate analysis and investigation.

Common Patterns

In a security context, recognizing common patterns and trends in log data is crucial for identifying potential security threats. These "patterns" refer to the identifiable artifacts left behind in logs by threat actors or cyber security incidents. Fortunately, there are some common patterns that, if learned, will improve your detection abilities and allow you to respond efficiently to incidents.

**Abnormal User Behavior**

One of the primary patterns that can be identified is related to unusual or anomalous user behavior. This refers to any actions or activities conducted by users that deviate from their typical or expected behavior.

To effectively detect anomalous user behavior, organizations can employ log analysis solutions that incorporate detection engines and machine learning algorithms to establish normal behavior patterns. Deviations from these patterns or baselines can then be alerted as potential security incidents. Some examples of these solutions include [_Splunk User Behavior Analytics (UBA)_](https://www.splunk.com/en_us/products/user-behavior-analytics.html), _[IBM QRadar UBA](https://www.ibm.com/docs/en/qradar-common?topic=app-qradar-user-behavior-analytics)_, and _[Azure AD Identity Protection](https://learn.microsoft.com/en-us/azure/active-directory/identity-protection/overview-identity-protection)_.

The specific indicators can vary greatly depending on the source, but some examples of this that can be found in log files include:

- **Multiple failed login attempts**
    - Unusually high numbers of failed logins within a short time may indicate a brute-force attack.
- **Unusual login times**
    - Login events outside the user's typical access hours or patterns might signal unauthorized access or compromised accounts.
- **Geographic anomalies**
    - Login events from IP addresses in countries the user does not usually access can indicate potential account compromise or suspicious activity.
    - In addition, simultaneous logins from different geographic locations (or indications of impossible travel) may suggest account sharing or unauthorized access.
- **Frequent password changes**
    - Log events indicating that a user's password has been changed frequently in a short period may suggest an attempt to hide unauthorized access or take over an account.
- **Unusual user-agent strings**
    - In the context of HTTP traffic logs, requests from users with uncommon user-agent strings that deviate from their typical browser may indicate automated attacks or malicious activities.
    - For example, by default, the [Nmap scanner](https://tryhackme.com/room/furthernmap) will log a user agent containing "Nmap Scripting Engine." The [Hydra brute-forcing tool](https://tryhackme.com/room/hydra), by default, will include "(Hydra)" in its user-agent. These indicators can be useful in log files to detect potential malicious activity.

The significance of these anomalies can vary greatly depending on the specific context and the systems in place, so it is essential to fine-tune any automated anomaly detection mechanisms to minimize false positives.

Common Attack Signatures

Identifying common attack signatures in log data is an effective way to detect and quickly respond to threats. Attack signatures contain specific patterns or characteristics left behind by threat actors. They can include malware infections, web-based attacks (SQL injection, cross-site scripting, directory traversal), and more. As this is entirely dependent on the attack surface, some high-level examples include:

SQL Injection

SQL injection attempts to exploit vulnerabilities in web applications that interact with databases. Look for unusual or malformed SQL queries in the application or database logs to identify common SQL injection attack patterns.

Suspicious SQL queries might contain unexpected characters, such as single quotes (`'`), comments (`--`, `#`), union statements (`UNION`), or time-based attacks (`WAITFOR DELAY`, `SLEEP()`). A useful SQLi payload list to reference can be found [here](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection).

In the below example, an SQL injection attempt can be identified by the `' UNION SELECT` section of the `q=` query parameter. The attacker appears to have escaped the SQL query with the single quote and injected a union select statement to retrieve information from the `users` table in the database. Often, this payload may be URL-encoded, requiring an additional processing step to identify it efficiently.

sqli.log

```plaintext
10.10.61.21 - - [2023-08-02 15:27:42] "GET /products.php?q=books' UNION SELECT null, null, username, password, null FROM users-- HTTP/1.1" 200 3122
```

Cross-Site Scripting (XSS)

Exploiting cross-site scripting (XSS) vulnerabilities allow attackers to inject malicious scripts into web pages. To identify common XSS attack patterns, it is often helpful to look for log entries with unexpected or unusual input that includes script tags (`<script>`) and event handlers (`onmouseover`, `onclick`, `onerror`). A useful XSS payload list to reference can be found [here](https://github.com/payloadbox/xss-payload-list).

In the example below, a cross-site scripting attempt can be identified by the `<script>alert(1);</script>` payload inserted into the `search` parameter, which is a common testing method for XSS vulnerabilities.

xss.log

```plaintext
10.10.19.31 - - [2023-08-04 16:12:11] "GET /products.php?search=<script>alert(1);</script> HTTP/1.1" 200 5153
```

Path Traversal

Exploiting path traversal vulnerabilities allows attackers to access files and directories outside a web application's intended directory structure, leading to unauthorized access to sensitive files or code. To identify common traversal attack patterns, look for traversal sequence characters (`../` and `../../`) and indications of access to sensitive files (`/etc/passwd`, `/etc/shadow`). A useful directory traversal payload list to reference can be found [here](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/README.md).

It is important to note, like with the above examples, that directory traversals are often URL encoded (or double URL encoded) to avoid detection by firewalls or monitoring tools. Because of this, `%2E` and `%2F` are useful URL-encoded characters to know as they refer to the `.` and `/` respectively.

In the below example, a directory traversal attempt can be identified by the repeated sequence of `../` characters, indicating that the attacker is attempting to "back out" of the web directory and access the sensitive `/etc/passwd` file on the server.

path-traversal.log

```plaintext
10.10.113.45 - - [2023-08-05 18:17:25] "GET /../../../../../etc/passwd HTTP/1.1" 200 505
```

A log file is processed by a tool which returns an output. What form of analysis is this?
Automated
An analyst opens a log file and searches for events. What form of analysis is this?
Manual

When analyzing collected logs, sometimes the most readily available tool we have is the command line itself. Analyzing logs through the command line provides a quick and powerful way to gain insights into system activities, troubleshoot issues, and detect security incidents, even if we don't have an SIEM system configured.

Many built-in Linux commands allow us to parse and filter relevant information quickly. Viewing log files using the command line is one of the most basic yet essential tasks for conducting log analysis. Several common built-in tools are used for this purpose, offering differing functionalities to read and navigate through log files efficiently.

You can locate the `apache.log` file on the AttackBox under `/root/Rooms/introloganalysis/task6` to follow along with this task. However, it is also attached to this task and available for download.

cat

The `cat` command (short for "concatenate") is a simple utility that reads one or more files and displays its content in the terminal. When used for log files, it prints the entire log content to the screen.

For example, to view the contents of a log file named `apache.log`, you can use the command:

cat Example

```shell-session
user@tryhackme$ cat apache.log        
203.0.113.42 - - [31/Jul/2023:12:34:56 +0000] "GET /index.php HTTP/1.1" 200 1234 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
120.54.86.23 - - [31/Jul/2023:12:34:57 +0000] "GET /contact.php HTTP/1.1" 404 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
185.76.230.45 - - [31/Jul/2023:12:34:58 +0000] "GET /about.php HTTP/1.1" 200 9876 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
201.39.104.77 - - [31/Jul/2023:12:34:59 +0000] "GET /login.php HTTP/1.1" 200 4321 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
...
...
```

Due to its large output, it is typically not the best approach for dealing with long log files.

less

The `less` command is an improvement over `cat` when dealing with larger files. It allows you to view the file's data page by page, providing a more convenient way to read through lengthy logs. When using `less` to open a file, it displays the first page by default, and you can scroll down using the arrow keys or with _Page Up_ and _Page Down_.

For example, to view the same log file using `less`, use the command:

less Example

```shell-session
user@tryhackme$ less apache.log       
...
...
HTTP/1.1" 200 7890 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.350 Safari/5>
P/1.1" 404 4321 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.3>
TTP/1.1" 200 1234 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.90 Safari/537>
P/1.1" 200 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.3>
TTP/1.1" 404 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537>
P/1.1" 200 1234 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Safari/537.3>
TP/1.1" 200 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.90 Safari/537.>
~
~
~
~
(END)
```

You can exit the command's output via the `q` key.

tail

The `tail` command is specifically designed for viewing the end of files and is very useful for seeing a summary of recently generated events in the case of log files. The most common use of `tail` is coupled with the `-f` option, which allows you to "follow" the log file in real-time, as it continuously updates the terminal with new log entries as they are generated and written. This is extremely useful when monitoring logs for live events or real-time system behavior.

By default, `tail` will only display the last ten lines of the file. However, we can change this with the `-n` option and specify the number of lines we want to view.

For example, if we only wanted to print the last five lines of the `apache.log` file and "follow" the logs in real-time, we can use the command:

tail Example

```shell-session
user@tryhackme$ tail -f -n 5 apache.log
176.145.201.99 - - [31/Jul/2023:12:34:24 +0000] "GET /login.php HTTP/1.1" 200 1234 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.90 Safari/537.36"
104.76.29.88 - - [31/Jul/2023:12:34:23 +0000] "GET /index.php HTTP/1.1" 200 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
128.45.76.66 - - [31/Jul/2023:12:34:22 +0000] "GET /contact.php HTTP/1.1" 404 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
76.89.54.221 - - [31/Jul/2023:12:34:21 +0000] "GET /about.php HTTP/1.1" 200 1234 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Safari/537.36"
145.76.33.201 - - [31/Jul/2023:12:34:20 +0000] "GET /login.php HTTP/1.1" 200 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.90 Safari/537.36"
```

Being able to sort, filter, and manipulate log files from the command line is a crucial aspect of performing effective log analysis. Analysts often need to extract specific information, filter out relevant data, aggregate results, and transform logs to uncover insights and identify anomalies.

**Note:** The opposite of the `tail` command is `head`, which allows you to view the _first_ ten lines of a file by default and takes in the same arguments. Feel free to experiment with this as well!

wc

The `wc` (word count) command is a simple but powerful utility that can be quite useful for quick analysis and statistics gathering. The output of `wc` provides information about the number of lines, words, and characters in a log file. This can help security analysts understand the size and volume of log data they are dealing with before diving into a more detailed analysis.

wc Example

```shell-session
user@tryhackme$ wc apache.log     
   70  1562 14305 apache.log
```

After running `wc` on `apache.log`, we can determine that the file contains **70** lines, **1562** individual words (separated by whitespace), and **14305** individual characters.

cut

The `cut` command extracts specific columns (fields) from files based on specified delimiters. This is a handy command for working with log files that have structured or tab-separated data.

If we want to extract all of the IP addresses in the file, we can use the `cut` command to specify a delimiter of a `space` character and only select the first field returned.

cut Example

```shell-session
user@tryhackme$ cut -d ' ' -f 1 apache.log
203.0.113.42
120.54.86.23
185.76.230.45
201.39.104.77
112.76.89.56
211.87.186.35
156.98.34.12
202.176.73.99
122.65.187.55
77.188.103.244
189.76.230.44
153.47.106.221
200.89.134.22
...
...
```

The above command will return a list of every IP address in the log file. Expanding on this, we can change the field number to `-f 7` to extract the URLs and `-f 9` to extract the HTTP status codes.

sort

Sometimes, it's helpful to sort the returned entries chronologically or alphabetically. The `sort` command arranges the data in files in ascending or descending order based on specific criteria. This can be crucial for identifying patterns, trends, or outliers in our log data. It is also common to combine the _output_ of another command (cut, for example) and use it as the _input_ of the sort command using the pipe `|` redirection character.

For example, to sort the list of returned IP addresses from the above `cut` command, we can run:

sort Example

```shell-session
user@tryhackme$ cut -d ' ' -f 1 apache.log | sort -n
76.89.54.221
76.89.54.221
76.89.54.221
76.89.54.221
76.89.54.221
76.89.54.221
77.188.103.244
99.76.122.65
104.76.29.88
104.76.29.88
104.76.29.88
104.76.29.88
104.76.29.88
104.76.29.88
...
...
```

In the above command, we piped the output from `cut` into the `sort` command and added the `-n` option to sort _numerically_. This changed the output to list the IP addresses in ascending order.

If we want to reverse the order, we can add the `-r` option:

sort Example (Reversed)

```shell-session
user@tryhackme$ cut -d ' ' -f 1 apache.log | sort -n -r
221.90.64.76
211.87.186.35
203.78.122.88
203.64.78.90
203.64.78.90
203.64.78.90
203.64.78.90
203.64.78.90
203.64.78.90
203.0.113.42
202.176.73.99
201.39.104.77
200.89.134.22
...
...
```

uniq

The `uniq` command identifies and removes adjacent duplicate lines from sorted input. In the context of log analysis, this can be a useful tool for simplifying data lists (like collected IP addresses), especially when log entries may contain repeated or redundant information. The `uniq` command is often combined with the `sort` command to **sort** the data before removing the duplicate entries.

For example, the output of the `sort` command we ran above contains a few duplicate IP addresses, which is easier to spot when the data is sorted numerically. To remove these repeatedly extracted IPs from the list, we can run:

uniq Example

```shell-session
user@tryhackme$ cut -d ' ' -f 1 apache.log | sort -n -r | uniq
221.90.64.76
211.87.186.35
203.78.122.88
203.64.78.90
203.0.113.42
202.176.73.99
201.39.104.77
200.89.134.22
192.168.45.99
...
...
```

We can also append the `-c` option to output unique lines and prepend the count of occurrences for each line. This can be very useful for quickly determining IP addresses with unusually high traffic.

uniq Example (with count)

```shell-session
user@tryhackme$ cut -d ' ' -f 1 apache.log | sort -n -r | uniq -c
      1 221.90.64.76
      1 211.87.186.35
      1 203.78.122.88
      6 203.64.78.90
      1 203.0.113.42
      1 202.176.73.99
      1 201.39.104.77
      1 200.89.134.22
      1 192.168.45.99
...
...
```

sed

Both `sed` and `awk` are powerful text-processing tools commonly used for log analysis. They are sometimes used interchangeably, but both commands have their use cases and can allow security analysts to manipulate, extract, and transform log data efficiently.

Using the substitute syntax, `sed` can replace specific patterns or strings into log entries. For example, to replace all occurrences of "**31/Jul/2023**" with "**July 31, 2023**" in the `apache.log` file, we can use:

sed Example

```shell-session
user@tryhackme$ sed 's/31\/Jul\/2023/July 31, 2023/g' apache.log
203.0.113.42 - - [July 31, 2023:12:34:56 +0000] "GET /index.php HTTP/1.1" 200 1234 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
120.54.86.23 - - [July 31, 2023:12:34:57 +0000] "GET /contact.php HTTP/1.1" 404 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
...
...
```

Note that the backslash character `\` is required to "escape" the forward slash in our pattern and tell `sed` to treat the forward slash as a literal character. Also, note that the `sed` command _does not_ change the `apache.log` file directly; instead, it only outputs the modified version of the file to the standard output in the command line. If you want to overwrite the file, you can add the `-i` option to edit the file in place or use a redirect operator `>` to save the output to the original or another file.

**Caution:** If you use the `-i` option with `sed`, you risk overwriting the original file and losing valuable data. Ensure to keep a backup copy!

awk

For the `awk` command, a common use case, is conditional actions based on specific field values. For example, to print log entries where the HTTP response code is greater than or equal to `400` (which would indicate HTTP error statuses), we can use the following command:

awk Example

```shell-session
user@tryhackme$ awk '$9 >= 400' apache.log
120.54.86.23 - - [31/Jul/2023:12:34:57 +0000] "GET /contact.php HTTP/1.1" 404 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
156.98.34.12 - - [31/Jul/2023:12:35:02 +0000] "GET /about.php HTTP/1.1" 404 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Safari/537.36"
189.76.230.44 - - [31/Jul/2023:12:35:06 +0000] "GET /about.php HTTP/1.1" 404 1234 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.170 Safari/537.36"
...
...
```

In this case, we're using the `$9` field (which in this log example refers to the HTTP status codes), requiring it to be greater than or equal to `400`.

This only scratches the surface of the power of these commands, and it is highly encouraged to read more about their options and use cases [here](https://www.theunixschool.com/p/awk-sed.html).

grep

The `grep` command is a powerful text search tool widely used on UNIX systems and provides exceptional use cases in log analysis. It allows you to search for specific patterns or regular expressions within files or streams of text. Using `grep` can help analysts quickly identify relevant log entries that match specific criteria, particular resources or keywords, or patterns associated with security incidents.

The most basic usage of `grep` is to search for specific strings within log files. For example, if we are suspicious about any log entries that hit the `/admin.php` webpage on the server, we can `grep` for "admin" to return any relevant results:

grep Example

```shell-session
user@tryhackme$ grep "admin" apache.log
145.76.33.201 - - [31/Jul/2023:12:34:54 +0000] "GET /admin.php HTTP/1.1" 200 4321 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.330 Safari/537.36"
```

Like the `uniq -c` command, we can append the `-c` option to `grep` to count the entries matching the search criteria. For example, because only a single line was returned in the above command, appending `-c` will return "1".

grep Example (with count)

```shell-session
user@tryhackme$ grep -c "admin" apache.log
1
```

If we wanted to know which **line number** in the log file relates to the matched entries, we could add the `-n` option to help quickly locate specific occurrences:

grep Example (line number)

```shell-session
user@tryhackme$ grep -n "admin" apache.log                           
37:145.76.33.201 - - [31/Jul/2023:12:34:54 +0000] "GET /admin.php HTTP/1.1" 200 4321 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.330 Safari/537.36"
```

In this case, the line number **"37"** is prepended to the log entry output.

Lastly, we can **invert** our command using the `-v` option only to select lines that **do not** contain the specified pattern or keyword(s). This can be useful for quickly filtering out unwanted or irrelevant lines from log files. For example, if we're not interested in any log entries that hit the `/index.php` page, we can run the following command to filter it out:

grep Example (inverted)

```shell-session
user@tryhackme$ grep -v "/index.php" apache.log | grep "203.64.78.90"
203.64.78.90 - - [31/Jul/2023:12:35:01 +0000] "GET /about.php HTTP/1.1" 404 4321 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.170 Safari/537.36"
203.64.78.90 - - [31/Jul/2023:12:34:53 +0000] "GET /about.php HTTP/1.1" 200 1234 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.210 Safari/537.36"
203.64.78.90 - - [31/Jul/2023:12:34:46 +0000] "GET /contact.php HTTP/1.1" 200 4321 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.100 Safari/537.36"
203.64.78.90 - - [31/Jul/2023:12:34:32 +0000] "GET /login.php HTTP/1.1" 404 5678 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.330 Safari/537.36"
203.64.78.90 - - [31/Jul/2023:12:34:25 +0000] "GET /about.php HTTP/1.1" 404 4321 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
```

Notice that in the above command, we filtered out the `index.php` page and piped the output into another grep command that only pulled log entries that contained the IP address `203.64.78.90`.

Like with `awk` and `sed`, `grep` is an extremely powerful tool that cannot be fully covered in a single task. It is highly encouraged to read more about it on the official GNU manual page [here](https://www.gnu.org/software/grep/manual/grep.html).

While command-line log analysis offers powerful capabilities, it might only suit some scenarios, especially when dealing with vast and complex log datasets. A dedicated log analysis solution, like the Elastic (ELK) Stack or Splunk, can be more efficient and offer additional log analysis and visualization features. However, the command line remains essential for quick and straightforward log analysis tasks.

Sigma

[Sigma](https://github.com/SigmaHQ/sigma) is a highly flexible open-source tool that describes log events in a structured format. Sigma can be used to find entries in log files using pattern matching. Sigma is used to:

1. Detect events in log files
2. Create SIEM searches
3. Identify threats

Sigma uses the YAML syntax for its rules. This task will demonstrate Sigma being used to detect failed login events in SSH. Please note that writing a Sigma rule is out-of-scope for this room. However, let's break down an example Sigma rule for the scenario listed above:

```yaml
title: Failed SSH Logins
description: Searches sshd logs for failed SSH login attempts
status: experimental
author: CMNatic
logsource: 
    product: linux
    service: sshd

detection:
    selection:
        type: 'sshd'
        a0|contains: 'Failed'
        a1|contains: 'Illegal'
    condition: selection
falsepositives:
    - Users forgetting or mistyping their credentials
level: medium
```

In this Sigma rule:

|   |   |   |
|---|---|---|
|**Key**|**Value**|**Description**|
|title|Failed SSH Logins|This title outlines the purpose of the Sigma rule.|
|description|Searches sshd logs for failed SSH login attempts|This key provides a description that expands on the title.|
|status|experimental|This key explains the status of the rule. For example, "experimental" means that further testing or improvements must be done.|
|author|CMNatic|The person who wrote the rule.|
|logsource|product: linux  <br>service: sshd|Where can the log files that contain the data that we're looking for be found?|
|detection|sshd|This key lists what the Sigma rule is looking to find.|
|a0\|contains|a0\|contains: 'Failed'|In this case, look for all entries with "Failed".|
|a1\|contains|a1\|contains: 'Illegal'|In this case, look for all entries with "Illegal".|
|falsepositives|Users forgetting or mistyping their credentials|List cases where this entry may be present but doesn't necessarily indicate malicious behavior.|

This rule can now be used in SIEM platforms to identify events in the processed logs. If you want to learn more about Sigma, I recommend checking out the [Sigma](https://tryhackme.com/room/sigma) room on TryHackMe.

Yara

[Yara](https://github.com/VirusTotal/yara) is another pattern-matching tool that holds its place in an analyst's arsenal. Yara is a YAML-formatted tool that identifies information based on binary and textual patterns (such as hexadecimal and strings). While it is usually used in malware analysis, Yara is extremely effective in log analysis.

Let's look at this example Yara rule called "IPFinder". This YARA rule uses regex to search for any IPV4 addresses. If the log file we are analyzing contains an IP address, YARA will flag it:

```yaml
rule IPFinder {
    meta:
        author = "CMNatic"
    strings:
        $ip = /([0-9]{1,3}\.){3}[0-9]{1,3}/ wide ascii
 
    condition:
        $ip
}
```

Let's look at the keys that make up this Yara rule:

|   |   |   |
|---|---|---|
|**Key**|**Example**|**Description**|
|rule|IPFinder|This key names the rule.|
|meta|author|This key contains metadata. For example, in this case, it is the name of the rule's author.|
|strings|$ip = /([0-9]{1,3}\.){3}[0-9]{1,3}/ wide ascii|This key contains the values that YARA should look for. In this case, it is using REGEX to look for IPV4 addresses.|
|condition|$ip|If the variable $ip is detected, then the rule should trigger.|

Using YARA to detect a specific IP address

```shell-session
cmnatic@thm:~$ yara ipfinder.yar apache2.txt
IPFinder apache2
```

This YARA rule can be expanded to look for:

- Multiple IP addresses
- IP Addresses based on a range (for example, an ASN or a subnet)
- IP addresses in HEX
- If an IP address lists more than a certain amount (I.e., alert if an IP address is found five times)
- And combined with other rules. For example, if an IP address visits a specific page or does a certain action

If you want to learn more about Yara, check out the [Yara](https://tryhackme.com/room/yara) room on TryHackMe.


Splunk Search Processing Language comprises of multiple functions, operators and commands that are used together to form a simple to complex search and get the desired results from the ingested logs. Main components of SPL are explained below:

﻿**Search Field Operators**  

Splunk field operators are the building blocks used to construct any search query. These field operators are used to filter, remove, and narrow down the search result based on the given criteria. Common field operators are Comparison operators, wildcards, and boolean operators.  

Comparison Operators

﻿These operators are used to compare the values against the fields. Some common comparisons operators are mentioned below:  

|   |   |   |   |
|---|---|---|---|
|**Field Name  <br>**|**Operator  <br>**|**Example**|**Explanation  <br>**|
|**Equal  <br>**|=|UserName=Mark|This operator is used to match values against the field. In this example, it will look for all the events, where the value of the field UserName is equal to Mark.|
|**Not Equal to  <br>**|!=|UserName!=Mark|This operator returns all the events where the UserName value does not match Mark.|
|**Less than  <br>**|<|Age < 10|Showing all the events with the value of Age less than 10.|
|**Less than or Equal to  <br>**|<=|Age <= 10|Showing all the events with the value of Age less than or equal to 10.|
|**Greater than  <br>**|>|Outbound_traffic > 50 MB|This will return all the events where the Outbound traffic value is over 50 MB.|
|**Greater Than or Equal to  <br>**|>=|Outbound_traffic >= 50 MB|This will return all the events where the Outbound traffic value is greater or equal to 50 MB.|

﻿﻿Lets use the comparison operator to display all the event logs from the index "windowslogs", where AccountName is not Equal to "System"

**Search Query:** `index=windowslogs AccountName !=SYSTEM`  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/681a126a98263612b87def7014583ffb.png)  

Boolean Operators

Splunk supports the following Boolean operators, which can be very handy in searching/filtering and narrowing down results.  

|   |   |   |
|---|---|---|
|**Operator  <br>**|**Syntax  <br>**|**Explanation  <br>**|
|**NOT  <br>**|field_A **NOT** value|Ignore the events from the result where field_A contain the specified value.|
|**OR  <br>**|field_A=value1 **OR** field_A=value2|Return all the events in which field_A contains either value1 or value2.|
|**AND  <br>**|field_A=value1 **AND** field_B=value2|Return all the events in which field_A contains value1 and field_B contains value2.|

﻿To understand how boolean operator works in SPL, lets add the condition to show the events from the James account.

**Search Query:** `index=windowslogs AccountName !=SYSTEM **AND** AccountName=James`  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/42c8963dccbd05128f52665c38877f47.png)  

  

Wild Card

Splunk supports wildcards to match the characters in the strings.  

|   |   |   |
|---|---|---|
|**Wildcard symbol**|**Example**|**Explanation**|
|***  <br>**|status=fail*|It will return all the results with values like<br><br>status=failed<br><br>status=failure|

In the events, there are multiple DestinationIPs reported. Let's use the wildcard only to show the **DestinationIP** starting from 172.*

**Search Query:** `index=windowslogs DestinationIp=172.*`  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/5530cae0739755e6a682641f5057b1a5.png)

Our network generates thousands of logs each minute, all ingesting into our SIEM solution. It becomes a daunting task to search for any anomaly without using filters. SPL allows us to use **Filters** to narrow down the result and only show the important events that we are interested in. We can add or remove certain data from the result using filters. The following commands are useful in applying filters to the search results.

**Fields**

|   |   |
|---|---|
|**Command**|**fields**|
|**Explanation  <br>**|Fields command is used to add or remove mentioned fields from the search results. To remove the field, minus sign ( - ) is used before the fieldname and plus ( + ) is used before the fields which we want to display.|
|**Syntax  <br>**|\| fields <field_name1>  <field_name2>|
|**Example**|\| `fields + HostName - EventID`|

Let's use the fields command to only display host, User, and SourceIP fields using the following syntax.  

**Search Query:** `index=windowslogs | fields + host + User + SourceIp`  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/dd77983b5fccf5eacfa73aacbeb7a314.png)  

**Note:** Click on the **More field** to display the fields if some fields are not visible.

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/30b2c651a041bd1c2db77b661dc8cc8e.png)  

**Search**

|   |   |
|---|---|
|**Command**|**search**|
|**Explanation  <br>**|This command is used to search for the raw text while using the chaining command `\|`|
|**Syntax  <br>**|\| search  <search_keyword>|
|**Example**|\| `search "Powershell"`|

Use the search command to show all the events containing the term Powershell. This will return all the events that contain the term "**Powershell**".  

**Search Query:** `index=windowslogs | search Powershell`  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/02d2ece97e7f977e32b4c11fd86e41eb.png)  

**Dedup**

|   |   |
|---|---|
|**Command**|**dedup**|
|**Explanation  <br>**|Dedup is the command used to remove duplicate fields from the search results. We often get the results with various fields getting the same results. These commands remove the duplicates to show the unique values.|
|**Syntax  <br>**|\| dedup <fieldname>|
|**Example**|\| `dedup EventID`|

We can use the dedup command to show the list of unique **EventIDs** from a particular hostname.

**Search Query:** `index=windowslogs | table EventID User Image Hostname | dedup EventID`

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/47bb3fb904c84acdbe7cb89dda535ac1.png)  

**Rename**

|   |   |
|---|---|
|**Command**|**rename**|
|**Explanation  <br>**|It allows us to change the name of the field in the search results. It is useful in a scenario when the field name is generic or log, or it needs to be updated in the output.|
|**Syntax  <br>**|\| rename  <fieldname>|
|**Example**|\| `rename User as Employees`|

Let's rename the User field to Employees using the following search query.

**Search Query**: `index=windowslogs | fields + host + User + SourceIp | rename User as Employees`  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/61e56df15649aa12b4be7c91d8cc91ce.png)

SPL provides various commands to bring structure or order to the search results. These sorting commands like `head`, `tail`, and `sort` can be very useful during logs investigation. These ordering commands are explained below:

Table  

|   |   |
|---|---|
|**Explanation  <br>**|Each event has multiple fields, and not every field is important to display. The Table command allows us to create a table with selective fields as columns.|
|**Syntax  <br>**|\| table <field_name1> <fieldname_2>|
|**Example**|\| `table`  <br><br>\| `head 20` # will return the top 20 events from the result list.|

This search query will create a table with three columns selected and ignore all the remaining columns from the display.  

**Search Query:** `index=windowslogs | table EventID Hostname SourceName`

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/643f5cc127276645eb0fd7fdb339cb29.png)

  

Head

|   |   |
|---|---|
|**Explanation  <br>**|The **head** command returns the first 10 events if no number is specified.|
|**Syntax  <br>**|\| head <number>|
|**Example**|\| `head`   # will return the top 10 events from the result list<br><br>\| `head 20`    # will return the top 20 events from the result list|

The following search query will show the table containing the mentioned fields and display only the top 5 entries.  

**Search Query:** `index=windowslogs |  table _time EventID Hostname SourceName | **head 5**`

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/3a9df7382d1f5e2e3302750dc5016809.png)

Tail

|   |   |
|---|---|
|**Explanation  <br>**|The **Tail** command returns the last 10 events if no number is specified.|
|**Syntax  <br>**|\| tail <number>|
|**Example**|\| `tail` # will return the last 10 events from the result list<br><br>\| `tail 20`   # will return the last 20 events from the result list|

The following search query will show the table containing the mentioned fields and display only 5 entries from the bottom of the list.

**Search Query:** `index=windowslogs |  table _time EventID Hostname SourceName | tail 5`

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/917811648cc95bd3f34c820a473b9c1b.png)

sort  

|   |   |
|---|---|
|**Explanation  <br>**|The **Sort** command allows us to order the fields in ascending or descending order.|
|**Syntax  <br>**|\| `sort` <field_name>|
|**Example**|\| `sort Hostname` # This will sort the result in Ascending order.|

The following search query will sort the results based on the Hostname field.

**Search Query:** `index=windowslogs |  table _time EventID Hostname SourceName | sort Hostname`

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/9589d101b5a07f69fc4771a6c1e54e14.png)  

  

Reverse

|   |   |
|---|---|
|**Explanation  <br>**|The reverse command simply reverses the order of the events.|
|**Syntax  <br>**|\|  reverse|
|**Example**|`<Search Query> \| reverse`|

**Search Query:** `index=windowslogs | table _time EventID Hostname SourceName | reverse`

  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/0de4064ec74ee5f64a399e0a7bed9200.png)

Transformational commands are those commands that change the result into a data structure from the field-value pairs. These commands simply transform specific values for each event into numerical values which can easily be utilized for statistical purposes or turn the results into visualizations. Searches that use these transforming commands are called transforming searches. Some of the most used transforming commands are explained below.

General Transformational Commands  

Top  

|   |   |
|---|---|
|**Command**|**top**|
|**Explanation  <br>**|This command returns frequent values for the top 10 events.|
|**Syntax  <br>**|\| top  <field_name><br><br>\| top limit=6 <field_name>|
|**Example**|`top limit=3 EventID`|

The following command will display the top 7 Image ( representing Processes) captured.

**Search Query:** `index=windowslogs | top limit=7 Image`

  
![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/ffef6c0a6ce0159e6d970de2c32921a3.png)  

**Rare**  

|   |   |
|---|---|
|**Command**|**rare**|
|**Explanation  <br>**|This command does the opposite of top command as it returns the least frequent values or bottom 10 results.|
|**Syntax  <br>**|\| rare <field_name><br><br>\| rare limit=6 <field_name>|
|**Example**|`rare limit=3 EventID`|

The following command will display the rare 7 Image (Processes) captured.

**Search Query:** `index=windowslogs | rare limit=7 Image`  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/8123e0932c169514d9842fbba8f5898c.png)  

**Highlight**

|   |   |
|---|---|
|**Command**|**highlight**|
|**Explanation  <br>**|The highlight command shows the results in raw events mode with fields highlighted.|
|**Syntax  <br>**|highlight      <field_name1>      <field_name2>|
|**Example**|`highlight User, host, EventID, Image`|

The following command will highlight the three mentioned fields in the raw logs  

**Search Query:** `index=windowslogs | highlight User, host, EventID, Image`

  

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/61ad47b204639fa0f75b278bec21abac.gif)  

  

STATS Commands

SPL supports various stats commands that help in calculating statistics on the values. Some common stat commands are:

|   |   |   |   |
|---|---|---|---|
|**Command**|**Explanation**|**Syntax**|**Example**|
|**Average  <br>**|This command is used to calculate the average of the given field.|stats avg(field_name)|stats avg(product_price)|
|**Max  <br>**|It will return the maximum value from the specific field.|stats max(field_name)|stats max(user_age)|
|**Min**|It will return the minimum value from the specific field.|stats min(field_name)|stats min(product_price)|
|**Sum**|It will return the sum of the fields in a specific value.|stats sum(field_name)|stats sum(product_cost)|
|**Count**|The count command returns the number of data occurrences.|stats count(function) AS new_NAME|stats count(source_IP)|

**Splunk Chart Commands**  

These are very important types of transforming commands that are used to present the data in table or visualization form. Most of the chart commands utilize various stat commands.

Chart

|   |   |
|---|---|
|**Command**|**chart**|
|**Explanation  <br>**|The chart command is used to transform the data into tables or visualizations.|
|**Syntax  <br>**|\| chart <function>|
|**Example**|\| `chart count by User`|

**Search Query:** `index=windowslogs | chart count by User`

![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/a954b0a1d37542650df294461d756c61.gif)  

Timechart

|   |   |
|---|---|
|**Command**|**timechart**|
|**Explanation  <br>**|The timechart command returns the time series chart covering the field following the function mentioned. Often combined with STATS commands.|
|**Syntax  <br>**|\| timechart function  <field_name>|
|**Example**|\| `timechart count by Image`|

The following query will display the Image chart based on the time.  

**Search Query:** `index=windowslogs | timechart count by Image`

  
![](https://tryhackme-images.s3.amazonaws.com/user-uploads/5e8dd9a4a45e18443162feab/room-content/bc7f90e4f40be4c047d250d5e3ee44c8.gif)