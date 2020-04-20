# Level 21
## Connection
~~~
ssh bandit21@bandit.labs.overthewire.org -p2220
password: gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
~~~

## Goal
A program is running automatically at regular intervals from `cron`, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

Commands you may need to solve this level: `cron`, `crontab`, `crontab(5)` (use “`man 5 crontab`” to access this)

## Solution
First let's list the content of the `cron.d` directory.
~~~
$ ls -l /etc/cron.d/
total 16
-rw-r--r-- 1 root root 189 Jan 25  2017 atop
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit22
-rw-r--r-- 1 root root 122 Oct 16  2018 cronjob_bandit23
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit24
~~~

OK, let's see what cron job is defined in the `cronjob_bandit22` file:
~~~
$ cat /etc/cron.d/cronjob_bandit22 
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
~~~

It seems there is a shell script called, let's see what this looks like:
~~~
$ cat /usr/bin/cronjob_bandit22.sh 
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
~~~

This shell script dumps the password to a temporary file. Let's access the temporary file:
~~~
$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
~~~

# Flag
~~~
level22:Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
~~~