# Level 25
## Connection
~~~
ssh bandit25@bandit.labs.overthewire.org -p2220
password: uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
~~~

## Goal
Logging in to bandit26 from bandit25 should be fairly easy… The shell for user bandit26 is not `/bin/bash`, but something else. Find out what it is, how it works and how to break out of it.

Commands you may need to solve this level: `ssh`, `cat`, `more`, `vi`, `ls`, `id`, `pwd`

## Solution
We find a file named `bandit26.sshkey` in our `home` directory:
~~~
bandit25@bandit:~$ ls -lh
total 4.0K
-r-------- 1 bandit25 bandit25 1.7K Oct 16  2018 bandit26.sshkey
~~~

This is obviously a SSH key:
~~~
bandit25@bandit:~$ cat bandit26.sshkey 
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApis2AuoooEqeYWamtwX2k5z9uU1Afl2F8VyXQqbv/LTrIwdW
pTfaeRHXzr0Y0a5Oe3GB/+W2+PReif+bPZlzTY1XFwpk+DiHk1kmL0moEW8HJuT9
/5XbnpjSzn0eEAfFax2OcopjrzVqdBJQerkj0puv3UXY07AskgkyD5XepwGAlJOG
xZsMq1oZqQ0W29aBtfykuGie2bxroRjuAPrYM4o3MMmtlNE5fC4G9Ihq0eq73MDi
1ze6d2jIGce873qxn308BA2qhRPJNEbnPev5gI+5tU+UxebW8KLbk0EhoXB953Ix
3lgOIrT9Y6skRjsMSFmC6WN/O7ovu8QzGqxdywIDAQABAoIBAAaXoETtVT9GtpHW
qLaKHgYtLEO1tOFOhInWyolyZgL4inuRRva3CIvVEWK6TcnDyIlNL4MfcerehwGi
il4fQFvLR7E6UFcopvhJiSJHIcvPQ9FfNFR3dYcNOQ/IFvE73bEqMwSISPwiel6w
e1DjF3C7jHaS1s9PJfWFN982aublL/yLbJP+ou3ifdljS7QzjWZA8NRiMwmBGPIh
Yq8weR3jIVQl3ndEYxO7Cr/wXXebZwlP6CPZb67rBy0jg+366mxQbDZIwZYEaUME
zY5izFclr/kKj4s7NTRkC76Yx+rTNP5+BX+JT+rgz5aoQq8ghMw43NYwxjXym/MX
c8X8g0ECgYEA1crBUAR1gSkM+5mGjjoFLJKrFP+IhUHFh25qGI4Dcxxh1f3M53le
wF1rkp5SJnHRFm9IW3gM1JoF0PQxI5aXHRGHphwPeKnsQ/xQBRWCeYpqTme9amJV
tD3aDHkpIhYxkNxqol5gDCAt6tdFSxqPaNfdfsfaAOXiKGrQESUjIBcCgYEAxvmI
2ROJsBXaiM4Iyg9hUpjZIn8TW2UlH76pojFG6/KBd1NcnW3fu0ZUU790wAu7QbbU
i7pieeqCqSYcZsmkhnOvbdx54A6NNCR2btc+si6pDOe1jdsGdXISDRHFb9QxjZCj
6xzWMNvb5n1yUb9w9nfN1PZzATfUsOV+Fy8CbG0CgYEAifkTLwfhqZyLk2huTSWm
pzB0ltWfDpj22MNqVzR3h3d+sHLeJVjPzIe9396rF8KGdNsWsGlWpnJMZKDjgZsz
JQBmMc6UMYRARVP1dIKANN4eY0FSHfEebHcqXLho0mXOUTXe37DWfZza5V9Oify3
JquBd8uUptW1Ue41H4t/ErsCgYEArc5FYtF1QXIlfcDz3oUGz16itUZpgzlb71nd
1cbTm8EupCwWR5I1j+IEQU+JTUQyI1nwWcnKwZI+5kBbKNJUu/mLsRyY/UXYxEZh
ibrNklm94373kV1US/0DlZUDcQba7jz9Yp/C3dT/RlwoIw5mP3UxQCizFspNKOSe
euPeaxUCgYEAntklXwBbokgdDup/u/3ms5Lb/bm22zDOCg2HrlWQCqKEkWkAO6R5
/Wwyqhp/wTl8VXjxWo+W+DmewGdPHGQQ5fFdqgpuQpGUq24YZS8m66v5ANBwd76t
IZdtF5HXs2S5CADTwniUS5mX1HO9l5gUkk+h0cH5JnPtsMCnAUM+BRY=
-----END RSA PRIVATE KEY-----
~~~

Let's save it to our machine ([`bandit26.sshkey`](files/bandit26.sshkey)) and connect to the next level
~~~
$ chmod 600 bandit26.sshkey
$ ssh -i bandit26.sshkey bandit26@bandit.labs.overthewire.org -p2220
~~~

Let's test:
~~~
$ ssh -i bandit26.sshkey bandit26@bandit.labs.overthewire.org -p2220
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

[SNIP]
  _                     _ _ _   ___   __  
 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \ 
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/ 
Connection to bandit.labs.overthewire.org closed.
~~~

It seems to work but the connection is automatically closed. As we were told in the instructions that bandit26 uses a different shell, let's check:

~~~
$ cat /etc/passwd | grep "bandit2[5|6]"
bandit25:x:11025:11025:bandit level 25:/home/bandit25:/bin/bash
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
$ cat /usr/bin/showtext
#!/bin/sh

export TERM=linux

more ~/text.txt
exit 0
~~~

OK, now we know why the connection is automatically closed (`exit 0`). But just before, a banner is shown (`/home/bandit26/text.txt`) using the `more` command.

Now there is a trick here... When we connect, the `more` command will display the banner. This banner is an ASCII art displaying "bandit26", which is only 6 lines height. If the `more` command is able to display all the text on your screen, it will exit. However, if the size of the screen does not allow the entire text to be displayed, it will wait and you can scroll the text.

~~~
  _                     _ _ _   ___   __
 | |                   | (_) | |__ \ / /
 | |__   __ _ _ __   __| |_| |_   ) / /_
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/

~~~

Let's resize our window so that it will display only 2 or 3 lines and connect:

!["more1"](files/more1.png)

Now, you can enter into visual mode pressing the `v` key. Below is the extract from `man more`:
~~~
 v         Start up an editor at current  line.   The  editor  is
           taken from the environment variable VISUAL if defined,
           or EDITOR if VISUAL is not defined, or defaults to  vi
           if neither VISUAL nor EDITOR is defined.
~~~

And now, we are editing the banner in `vi`. The great thing is that within `vi`, we can open a new file:
~~~
:e [file] - Opens a file, where [file] is the name of the file you want opened
~~~

Let's try to access our password file: `:e /etc/bandit_pass/bandit26`:

!["more2"](files/more2.png)

# Flag
~~~
bandit26:5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z
~~~
