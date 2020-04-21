# Level 28
## Connection
~~~
ssh bandit28@bandit.labs.overthewire.org -p2220
password: 0ef186ac70e04ea33b4c1853d2526fa2
~~~

## Goal
There is a git repository at `ssh://bandit28-git@localhost/home/bandit28-git/repo`. The password for the user `bandit28-git` is the same as for the user `bandit28`.

Clone the repository and find the password for the next level.

Commands you may need to solve this level: `git`

## Solution
Let's create a temporary directory and clone the git repo:
~~~
bandit28@bandit:~$ cd $(mktemp -d)
bandit28@bandit:/tmp/tmp.nX7Jc9DIaL$ git clone ssh://bandit28-git@localhost/home/bandit28-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit28/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit28/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit28-git@localhost's password: 
remote: Counting objects: 9, done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0)
Receiving objects: 100% (9/9), done.
Resolving deltas: 100% (2/2), done.
bandit28@bandit:/tmp/tmp.nX7Jc9DIaL$ ls -la
total 305928
drwx--S--- 3 bandit28 root      4096 Apr 21 10:35 .
drwxrws-wt 1 root     root 313204736 Apr 21 10:35 ..
drwxr-sr-x 3 bandit28 root      4096 Apr 21 10:35 repo
bandit28@bandit:/tmp/tmp.nX7Jc9DIaL$ cd repo/
bandit28@bandit:/tmp/tmp.nX7Jc9DIaL/repo$ ls -la
total 16
drwxr-sr-x 3 bandit28 root 4096 Apr 21 10:35 .
drwx--S--- 3 bandit28 root 4096 Apr 21 10:35 ..
drwxr-sr-x 8 bandit28 root 4096 Apr 21 10:35 .git
-rw-r--r-- 1 bandit28 root  111 Apr 21 10:35 README.md
~~~

Let's see what the README tells us:
~~~
bandit28@bandit:/tmp/tmp.nX7Jc9DIaL/repo$ cat README.md 
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx
~~~

The `show` option will highlight log messages and textual diff for the last `commit` operation:
~~~
bandit28@bandit:/tmp/tmp.nX7Jc9DIaL/repo$ git show
commit 073c27c130e6ee407e12faad1dd3848a110c4f95
Author: Morla Porla <morla@overthewire.org>
Date:   Tue Oct 16 14:00:39 2018 +0200

    fix info leak

diff --git a/README.md b/README.md
index 3f7cee8..5c6457b 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for level29 of bandit.
 ## credentials
 
 - username: bandit29
-- password: bbc96594b4e001778eee9975372716b2
+- password: xxxxxxxxxx
~~~

It shows that the password was in clear and has been replaced by 'xxxxxxxxxx'. Hopefully, the old password still appears.

# Flag
~~~
level29:bbc96594b4e001778eee9975372716b2
~~~