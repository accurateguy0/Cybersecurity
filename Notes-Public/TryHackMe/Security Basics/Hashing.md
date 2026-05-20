Hashes output are in raw bytes hexadecimal form, then encrypted. (1byte is 2 letters)
Pigeonhole effect states that there are more number of items (pigeons), than pigeonholes;
Hash collision is when the different hashed input gives the same output.
Hashing is important so that data integrity gets protected and password security is safe.
MD5 and SHA1 are considered insecure.
Salting is a random value that is added to the password before it was being hashed.
Websites like [CrackStation](https://crackstation.net/) and [Hashes.com](https://hashes.com/en/decrypt/hash) internally use massive rainbow tables to provide fast password cracking for **hashes without salts**.
Salts can be added at the beginning or at the end of the password. Salts can be public.
We shouldn't encrypt the passwords, because once hackers get the key, they could decrypt all the passwords, unlike hashes.
The encrypted password field contains the hashed passphrase with four components: prefix (algorithm id), options (parameters), salt, and hash. It is saved in the format `$prefix$options$salt$hash`.
MS Windows passwords are hashed using NTLM, a variant of MD4. On MS Windows password hashes are stored in SAM (Security Account Manager). The encrypted password field contains the hashed passphrase with four components: prefix (algorithm id), options (parameters), salt, and hash. It is saved in the format `$prefix$options$salt$hash`.

The encrypted password field contains the hashed passphrase with four components: prefix (algorithm id), options (parameters), salt, and hash. It is saved in the format `$prefix$options$salt$hash`.

You can use Mimikatz and john the ripper to decrypt salted hashes.

HMAC is a type of message authentication code that uses cryptographic hashes function in combination with the secret key to verify authenticity and integrity.
The illustration below should clarify the above steps.

![A visual representation of the HMAC function.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5f04259cf9bf5b57aed2c476/room-content/5f04259cf9bf5b57aed2c476-1725294564965.svg)
Encoding is reversible, hashes aren't. Encryption requires key and authentification to decrypt.