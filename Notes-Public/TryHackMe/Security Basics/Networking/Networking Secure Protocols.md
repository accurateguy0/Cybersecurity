For a server that needs to be identified itself, TLS needs to be signed, for a fee, but https://letsencrypt.org/, lets you sign a certificate for free. You need to install the signed certificate in order to validate it. You should not validate the self signed certificates

HTTPS is basically HTTP over TLS. You need to establish a TCP three-way handshake first, then have TLS handshake later. POP3S, IMAPS, SMTPS is basically the same as HTTPS, they go through TLS, just like HTTP goes through TCP.\

SSH (secure shell) is an encrypted counterpart of telnet, that provides security. Nowadays when you connect to a server with ssh you likely will use open source library OpenSSH.

SFTP stands for SSH File Transfer Protocol, it's part of SSH suite and it shares the same port 22. Not to be confused with FTPS, which is File Transfer Protocol Secure that uses port 990. FTPS commands are not the same as FTP, they're more Unix-like. Just like other secure protocols mentioned above FTPS need proper TLS certificate to run.

VPNs are used to maintain "privacy". When the VPN server connection is made, internet traffic goes through the VPN tunnel and is seen from outside as a VPN server, so if you're connected to a VPN in Japan, then the website will configure you to this particular country and access to restricted content.