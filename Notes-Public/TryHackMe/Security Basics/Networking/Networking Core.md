You don't have to remember IP addresses, unless it's a private, bcs u have DNS attached to it. There are many types of records, for example:
A record - maps A (address) record to an IP or many addresses
AAAA record - same as A, but for IPv6
CNAME - specifies a domain name to another domain
MX Record - specifies the email server that's responsible for handling emails for a domain

To register a domain you have to pay an annual fee yearly or more. You need to disclose the contact information and it's is part of a publicly available WHOIS record. If you don't want it to be public you can go to privacy services ones. You can look up a WHOIS record using a command line 'whois' or search on the web.

HTTP and HTTPS are web protocols, used to retrieve web pages, use ports 80 and 443, more rarely 8080 and 8443. HTTP stands for Hypertext Transfer Protocol and S from HTTPS is Secure. They have 4 common commands:
GET - retrieves specified data
POST - submits new data to the server, such as information or image
PUT - creates, updates, overwrites data
DELETE - deletes specified data

FTP, File Transfer Protocol is a protocol that is faster than HTTP, if given equal circumstances for file transfer. There are example commands like:
USER - input username
PASS - input password
RETR - retrieve file from the FTP server to the client
STOR - store the file to the FTP server from the client

SMTP, Simple Mail Transfer Protocol is a protocol for emails sending. The 4 example commands are:
HELO or EHLO - initiates SMTP session
MAIL FROM - specifies the sender
REPT TO - specifies the recipient
DATA - the message that the sender sent
. - it indicates the end of a message in a line of itself

POP3 (Post Office Protocol version 3), a mail protocol that allows one device to connect to a mail server and communicate with it, then it deletes the email, so that other devices can't access the mail. It listens on port 110, so you can connect to POP3 server using Telnet. Some commands are: 
USER, login credential user
PASS, password cred 
RETR < specified-message-number >,  retrieve a specified message
LIST, lists all messages

IMAP is used when you want to synchronise the emails with different devices.