# Level 1
## Connection
ssh bandit1@bandit.labs.overthewire.org -p2220
password: boJ9jbbUNNfktd78OOpsqOltutMc3MY1
## Goal
The password for the next level is stored in a file called - located in the home directory
## Solution
There is a file named "-"
~~~~
$ ls -lab
total 24
-rw-r-----  1 bandit2 bandit1   33 Oct 16  2018 -
drwxr-xr-x  2 root    root    4096 Oct 16  2018 .
drwxr-xr-x 41 root    root    4096 Oct 16  2018 ..
-rw-r--r--  1 root    root     220 May 15  2017 .bash_logout
-rw-r--r--  1 root    root    3526 May 15  2017 .bashrc
-rw-r--r--  1 root    root     675 May 15  2017 .profile
~~~~
To read it:
~~~~
$ cat ./-
CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
~~~~

