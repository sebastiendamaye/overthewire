# Level 3
## Connection
~~~~
ssh bandit3@bandit.labs.overthewire.org -p2220
password: UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
~~~~
## Goal
The password for the next level is stored in a hidden file in the inhere directory.
## Solution
~~~~
$ ls -ila
total 24
131004 drwxr-xr-x  3 root root 4096 Oct 16  2018 .
    12 drwxr-xr-x 41 root root 4096 Oct 16  2018 ..
131005 -rw-r--r--  1 root root  220 May 15  2017 .bash_logout
131007 -rw-r--r--  1 root root 3526 May 15  2017 .bashrc
131296 drwxr-xr-x  2 root root 4096 Oct 16  2018 inhere
131006 -rw-r--r--  1 root root  675 May 15  2017 .profile
bandit3@bandit:~$ cd inhere/
bandit3@bandit:~/inhere$ ls
bandit3@bandit:~/inhere$ ls -ila
total 12
131296 drwxr-xr-x 2 root    root    4096 Oct 16  2018 .
131004 drwxr-xr-x 3 root    root    4096 Oct 16  2018 ..
131302 -rw-r----- 1 bandit4 bandit3   33 Oct 16  2018 .hidden
bandit3@bandit:~/inhere$ cat .hidden 
pIwrPrtPN36QITSp3EQaw936yaFoFgAB
~~~~
