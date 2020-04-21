# Level 29
## Connection
~~~
ssh bandit29@bandit.labs.overthewire.org -p2220
password: bbc96594b4e001778eee9975372716b2
~~~

## Goal
There is a git repository at `ssh://bandit29-git@localhost/home/bandit29-git/repo`. The password for the user `bandit29-git` is the same as for the user `bandit29`.

Clone the repository and find the password for the next level.

Commands you may need to solve this level: `git`

## Solution
### Clone the repo
Let's create a temporary directory and clone the repo:
~~~
bandit29@bandit:~$ cd $(mktemp -d)
bandit29@bandit:/tmp/tmp.FPMjeahbLH$ git clone ssh://bandit29-git@localhost/home/bandit29-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit29/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit29/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password: 
remote: Counting objects: 16, done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 16 (delta 2), reused 0 (delta 0)
Receiving objects: 100% (16/16), done.
Resolving deltas: 100% (2/2), done.
~~~

### Master branch
The `README.md` file doesn't show the password:
~~~
bandit29@bandit:/tmp/tmp.cWuhyvHD1F/repo$ git grep bandit30
README.md:Some notes for bandit30 of bandit.
README.md:- username: bandit30
bandit29@bandit:/tmp/tmp.FPMjeahbLH$ cd repo/
bandit29@bandit:/tmp/tmp.FPMjeahbLH/repo$ cat README.md 
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>
~~~

Even with `git log -p` (list all commits), we are not able to see the password:
~~~
bandit29@bandit:/tmp/tmp.cWuhyvHD1F/repo$ git log -p
commit 84abedc104bbc0c65cb9eb74eb1d3057753e70f8
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    fix username

diff --git a/README.md b/README.md
index 2da2f39..1af21d3 100644
--- a/README.md
+++ b/README.md
@@ -3,6 +3,6 @@ Some notes for bandit30 of bandit.
 
 ## credentials
 
-- username: bandit29
+- username: bandit30
 - password: <no passwords in production!>
 

commit 9b19e7d8c1aadf4edcc5b15ba8107329ad6c5650
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    initial commit of README.md

diff --git a/README.md b/README.md
new file mode 100644
index 0000000..2da2f39
--- /dev/null
+++ b/README.md
@@ -0,0 +1,8 @@
+# Bandit Notes
+Some notes for bandit30 of bandit.
+
+## credentials
+
+- username: bandit29
+- password: <no passwords in production!>
+
~~~

### Other branch?
~~~
bandit29@bandit:/tmp/tmp.cWuhyvHD1F/repo$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
~~~

It seems we have a `dev` branch:
~~~
bandit29@bandit:/tmp/tmp.cWuhyvHD1F/repo$ git show remotes/origin/dev
commit 33ce2e95d9c5d6fb0a40e5ee9a2926903646b4e3
Author: Morla Porla <morla@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    add data needed for development

diff --git a/README.md b/README.md
index 1af21d3..39b87a8 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for bandit30 of bandit.
 ## credentials
 
 - username: bandit30
-- password: <no passwords in production!>
+- password: 5b90576bedb2cc04c86a9e924ce42faf
~~~

# Flag
~~~
level30:5b90576bedb2cc04c86a9e924ce42faf
~~~