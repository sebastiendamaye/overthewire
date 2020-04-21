# Level 30
## Connection
~~~
ssh bandit30@bandit.labs.overthewire.org -p2220
password: 5b90576bedb2cc04c86a9e924ce42faf
~~~

## Goal
There is a git repository at `ssh://bandit30-git@localhost/home/bandit30-git/repo`. The password for the user `bandit30-git` is the same as for the user `bandit30`.

Clone the repository and find the password for the next level.

Commands you may need to solve this level: `git`

# Solution
## Clone the repo
Clone the repo and read the `README.md` file:
~~~
bandit30@bandit:~$ cd $(mktemp -d)
bandit30@bandit:/tmp/tmp.mpGlN0AcKu$ git clone ssh://bandit30-git@localhost/home/bandit30-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit30/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit30/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit30-git@localhost's password: 
remote: Counting objects: 4, done.
remote: Total 4 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (4/4), done.
bandit30@bandit:/tmp/tmp.mpGlN0AcKu$ cd repo/
bandit30@bandit:/tmp/tmp.mpGlN0AcKu/repo$ ls -la
total 16
drwxr-sr-x 3 bandit30 root 4096 Apr 21 13:37 .
drwx--S--- 3 bandit30 root 4096 Apr 21 13:36 ..
drwxr-sr-x 8 bandit30 root 4096 Apr 21 13:37 .git
-rw-r--r-- 1 bandit30 root   30 Apr 21 13:37 README.md
bandit30@bandit:/tmp/tmp.mpGlN0AcKu/repo$ cat README.md 
just an epmty file... muahaha
~~~

OK, nothing here. I also tested:
* `git grep bandit31` to list all files where the string `bandit31` is listed, but it returned no result 
* `git log -p` (show all commits) doesn't reveal anything else.
* `git branch -a` to list all branches, but there is only the master branch.

## Other git commands?
Trying to play a bit with the git commands, I found that there is a tag named `secret`:
~~~
bandit30@bandit:/tmp/tmp.9v9yncWzKA/repo$ git tag
secret
bandit30@bandit:/tmp/tmp.9v9yncWzKA/repo$ git show secret
47e603bb428404d265f59c42920d81e5
~~~

# Flag
~~~
level31:47e603bb428404d265f59c42920d81e5
~~~
