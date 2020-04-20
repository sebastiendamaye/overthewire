# Level 22
## Connection
~~~
ssh bandit22@bandit.labs.overthewire.org -p2220
password: Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
~~~

## Goal
A program is running automatically at regular intervals from `cron`, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

*NOTE: Looking at shell scripts written by other people is a very useful skill. The script for this level is intentionally made easy to read. If you are having problems understanding what it does, try executing it to see the debug information it prints.*

Commands you may need to solve this level: `cron`, `crontab`, `crontab(5)` (use “`man 5 crontab`” to access this)

## Solution
There is a file named `cronjob_bandit23` in the `/etc/cron.d` directory:
~~~
bandit22@bandit:~$ ls -l /etc/cron.d
total 16
-rw-r--r-- 1 root root 189 Jan 25  2017 atop
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit22
-rw-r--r-- 1 root root 122 Oct 16  2018 cronjob_bandit23
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit24
~~~

Let's see what it does:
~~~
bandit22@bandit:~$ cat /etc/cron.d/cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
~~~

OK, it executes a shell script, let's see what this shell script does:
~~~
bandit22@bandit:~$ cat /usr/bin/cronjob_bandit23.sh 
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
~~~

This shell script creates some variables:
* `myname`: set to `$(whoami)`. Will be equal to `bandit23`.
* `mytarget`: corresponds to the MD5 hash of the string "I am user bandit23"

Now, we can access the password:
~~~
bandit22@bandit:~$ cat /tmp/$(echo I am user bandit23 | md5sum | cut -d ' ' -f1)
jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
~~~

Or if you want to access the file directly:
~~~
$ echo "I am user bandit23" | md5sum
8ca319486bfbbc3663ea0fbe81326349  -
$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
~~~

# Flag
~~~
level23:jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
~~~