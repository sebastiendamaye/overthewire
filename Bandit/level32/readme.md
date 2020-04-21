# Level 32
## Connection
~~~
ssh bandit32@bandit.labs.overthewire.org -p2220
password: 56a9bf19c63d650ce78e6ec0354ee45e
~~~

## Goal
After all this `git` stuff its time for another escape. Good luck!

Commands you may need to solve this level: `sh`, `man`

# Solution
When we connect, we only have access to a customized shell where each command is uppercased:
~~~
WELCOME TO THE UPPERCASE SHELL
>> ls
sh: 1: LS: not found
>> whoami
sh: 1: WHOAMI: not found
>> 
~~~

This shell is probably executed with an executable itself started from `/bin/sh`. With this in mind, we can call the initial shell itself with `$0`. From Bash Manual:
> $0 Expands to the name of the shell or shell script. This is set at shell initialization. 

~~~
>> $0
$ cat /etc/bandit_pass/bandit33
c9c3199ddf4121b10cf581a98d51caee
~~~

Now that we have a shell, we can confirm our assumption. Indeed, a custom shell is defined for the user `bandit32` in `/etc/passwd`:
~~~
$ grep bandit32 /etc/passwd
bandit32:x:11032:11032:bandit level 32:/home/bandit32:/home/bandit32/uppershell
$ file /home/bandit32/uppershell
/home/bandit32/uppershell: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e6a8ed571599ce2bfa8b77145dbfc4eb933c1477, not stripped
~~~

# Flag
~~~
level33:c9c3199ddf4121b10cf581a98d51caee
~~~