# Level 27
## Connection
~~~
ssh bandit27@bandit.labs.overthewire.org -p2220
password: 3ba3118a22e93127a4ed485be72ef5ea
~~~

## Goal
There is a git repository at `ssh://bandit27-git@localhost/home/bandit27-git/repo`. The password for the user `bandit27-git` is the same as for the user `bandit27`.

Clone the repository and find the password for the next level.

Commands you may need to solve this level: `git`

## Solution
Let's create a temporary directory and clone the git repo in it:
~~~
bandit27@bandit:~$ cd $(mktemp -d)
bandit27@bandit:/tmp/tmp.8KxZOP21yP$ git clone ssh://bandit27-git@localhost/home/bandit27-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit27/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit27/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password: 
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (3/3), done.
~~~

The repo contains a `README` text file that contains the password:
~~~
bandit27@bandit:/tmp/tmp.8KxZOP21yP$ ls -la
total 305928
drwx--S--- 3 bandit27 root      4096 Apr 21 10:29 .
drwxrws-wt 1 root     root 313204736 Apr 21 10:29 ..
drwxr-sr-x 3 bandit27 root      4096 Apr 21 10:29 repo
bandit27@bandit:/tmp/tmp.8KxZOP21yP$ cd repo/
bandit27@bandit:/tmp/tmp.8KxZOP21yP/repo$ ls -la
total 16
drwxr-sr-x 3 bandit27 root 4096 Apr 21 10:29 .
drwx--S--- 3 bandit27 root 4096 Apr 21 10:29 ..
drwxr-sr-x 8 bandit27 root 4096 Apr 21 10:29 .git
-rw-r--r-- 1 bandit27 root   68 Apr 21 10:29 README
bandit27@bandit:/tmp/tmp.8KxZOP21yP/repo$ cat README 
The password to the next level is: 0ef186ac70e04ea33b4c1853d2526fa2
~~~

# Flag
~~~
level28:0ef186ac70e04ea33b4c1853d2526fa2
~~~