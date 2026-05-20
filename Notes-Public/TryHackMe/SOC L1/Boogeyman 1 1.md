Upon checking the latest trends, the initial TTP used for the malicious attachment is attributed to the new threat group named Boogeyman, known for targeting the logistics sector.

- The manual way uses command-line tools such as **cat**, **grep**, **base64**, and **sed.** Analyse the contents manually and build the attachment by decoding the string located at the bottom of the file.

ubuntu@tryhackme:~

```shell-session
ubuntu@tryhackme$ echo # sample command to rebuild the payload, presuming the encoded payload is written in another file, without all line terminators
ubuntu@tryhackme$ cat *PAYLOAD FILE* | base64 -d > Invoice.zip
```

- An alternative and easier way to do this is to double-click the EML file to open it via Thunderbird. The attachment can be saved and extracted accordingly.

Once the payload from the encrypted archive is extracted, use **lnkparse** to extract the information inside the payload. ContextInfo

ubuntu@tryhackme:~

```shell-session
ubuntu@tryhackme$ lnkparse *LNK FILE*
```

Investigation Guide  

With the following discoveries, we should now proceed with analysing the PowerShell logs to uncover the potential impact of the attack:

- Using the previous findings, we can start our analysis by searching the execution of the initial payload in the PowerShell logs.
- Since the given data is JSON, we can parse it in CLI using the `jq` command.
- Note that some logs are redundant and do not contain any critical information; hence can be ignored.

JQ Cheatsheet

﻿**jq** is a lightweight and flexible command-line JSON processor**.** This tool can be used in conjunction with other text-processing commands. 

You may use the following table as a guide in parsing the logs in this task.

Note: You must be familiar with the existing fields in a single log.

|   |   |
|---|---|
|Parse all JSON into beautified output|`cat powershell.json \| jq`|
|Print all values from a specific field without printing the field|`cat powershell.json \| jq '.Field1'`|
|Print all values from a specific field|`cat powershell.json \| jq '{Field1}'`|
|Print values from multiple fields|`cat powershell.json \| jq '{Field1, Field2}'`|
|Sort logs based on their Timestamp|`cat powershell.json \| jq -s -c 'sort_by(.Timestamp) \| .[]'`|
|Sort logs based on their Timestamp and print multiple field values|`cat powershell.json \| jq -s -c 'sort_by(.Timestamp) \| .[] \| {Field}'`|

You may continue learning this tool via its [documentation](https://stedolan.github.io/jq/manual/).