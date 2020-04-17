# Level 8
```html
$ curl --user natas8:DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe http://natas8.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas8", "pass": "DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe" };</script></head>
<body>
<h1>natas8</h1>
<div id="content">


<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

We are provided with the source code:
```html
$ curl -s --user natas8:DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe http://natas8.natas.labs.overthewire.org/index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas8", "pass": "<censored>" };</
script></head>
<body>
<h1>natas8</h1>
<div id="content">

<?

$encodedSecret = "3d3d516343746d4d6d6c315669563362";

function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}

if(array_key_exists("submit", $_POST)) {
    if(encodeSecret($_POST['secret']) == $encodedSecret) {
    print "Access granted. The password for natas9 is <censored>";
    } else {
    print "Wrong secret";
    }
}
?>

<form method=post>
Input secret: <input name=secret><br>
<input type=submit name=submit>
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

The PHP script checks that `bin2hex(strrev(base64_encode($_POST["secret"]))) = "3d3d516343746d4d6d6c315669563362"`. Here is a brief description of the PHP functions:
* [bin2hex](https://www.php.net/manual/en/function.bin2hex.php): Convert binary data into hexadecimal representation
* [strrev](https://www.php.net/manual/en/function.strrev.php): Reverse a string
* [base64_encode](https://www.php.net/manual/en/function.base64-encode.php): Encodes data with MIME base64

OK, now let's reverse it:
~~~~
$ echo "3d3d516343746d4d6d6c315669563362" | xxd -r -p | rev | base64 -d
oubWYf2kBq
~~~~

Now, let's submit our password:
~~~~
$ curl -s --user natas8:DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe -d "secret=oubWYf2kBq&submit=1" -X POST http://natas8.natas.labs.overthewire.org/ | html2text 

****** natas8 ******
Access granted. The password for natas9 is W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl
Input secret: [secret              ]
[Submit]
View_sourcecode
~~~~

# Flag
~~~~
natas9:W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl
~~~~
