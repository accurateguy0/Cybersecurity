The full term, Insecure Direct Object Reference, sounds fancy, but it doesn’t really describe what’s going wrong. The “Direct Object Reference” part just means that a system uses an ID (like `/user/1`) to point to something. That’s not the problem. The real issue is that the system doesn’t check whether the person making the request is allowed to access it.

A lot of people try to “fix” IDORs by hiding or encoding IDs. For example, changing `/user/1` to `/user/ea21f09b2`. That might make it look harder to guess, but if the server still isn’t checking permissions, it’s just as insecure. The vulnerability isn’t about how the object is referenced, it’s about missing authorization checks.

To understand the root cause of IDOR, it is important to understand the basic principles of authentication and authorization:

- **Authentication:** The process by which you verify who you are. For example, supplying your username and password.
- **Authorization:** The process by which the web application verifies your permissions. For example, are you allowed to visit the admin page of a web application, or are you allowed to make a payment using a specific account?
## It's Deterministic, Obviously Reproducible

Sometimes you have to dig quite deep for IDOR. Sometimes IDOR is not as clear. Sometimes the IDOR stems from the actual algorithm being used. In this last case, let's take a look at our vouchers. While the values may look random, we need to investigate what algorithm was used to generate them. Their format looks like a UUID, so let's use a website such as [UUID Decoder](https://www.uuidtools.com/decode) to try to understand what UUID format was used. Copy one of the vouchers to the website for decoding, and you should see something like this:

![UUID decoder tool](https://tryhackme-images.s3.amazonaws.com/user-uploads/6093e17fa004d20049b6933e/room-content/6093e17fa004d20049b6933e-1759961699555.png)

While these look completely random, we can see that the UUID version 1 was used. The issue with UUID 1 is that if we know the exact date when the code was generated, we can recover the UUID. For example, suppose we knew the elves always generated vouchers between 20:00 - 21:00. In that case, we can create UUIDs for that entire time period (3600 UUIDs since we have 60 minutes, and 60 seconds in a minute), which we could use in a brute force attack to aim to recover a valid voucher and get more gifts.