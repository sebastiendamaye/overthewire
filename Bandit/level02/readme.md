# Level 2
## Connection
ssh bandit2@bandit.labs.overthewire.org -p2220
password: CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
## Goal
The password for the next level is stored in a file called spaces in this filename located in the home directory
## Solution
~~~~
$ ls -ila
total 24
130960 drwxr-xr-x  2 root    root    4096 Oct 16  2018 .
    12 drwxr-xr-x 41 root    root    4096 Oct 16  2018 ..
130961 -rw-r--r--  1 root    root     220 May 15  2017 .bash_logout
130963 -rw-r--r--  1 root    root    3526 May 15  2017 .bashrc
130962 -rw-r--r--  1 root    root     675 May 15  2017 .profile
131187 -rw-r-----  1 bandit3 bandit2   33 Oct 16  2018 spaces in this filename
bandit2@bandit:~$ cat spaces\ in\ this\ filename 
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
~~~~

