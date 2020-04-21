# Level 31
## Connection
~~~
ssh bandit31@bandit.labs.overthewire.org -p2220
password: 47e603bb428404d265f59c42920d81e5
~~~

## Goal
There is a git repository at `ssh://bandit31-git@localhost/home/bandit31-git/repo`. The password for the user `bandit31-git` is the same as for the user `bandit31`.

Clone the repository and find the password for the next level.

Commands you may need to solve this level: `git`

# Solution
## Clone the repo
~~~
bandit31@bandit:~$ cd $(mktemp -d)
bandit31@bandit:/tmp/tmp.tK7zzRhbsa$ git clone ssh://bandit31-git@localhost/home/bandit31-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit31/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password: 
remote: Counting objects: 4, done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (4/4), done.
~~~

The `README.md` file seems to indicate that we have to push a file `key.txt`.
~~~
bandit31@bandit:/tmp/tmp.tK7zzRhbsa$ cd repo/
bandit31@bandit:/tmp/tmp.tK7zzRhbsa/repo$ ls -la
total 20
drwxr-sr-x 3 bandit31 root 4096 Apr 21 14:30 .
drwx--S--- 3 bandit31 root 4096 Apr 21 14:30 ..
drwxr-sr-x 8 bandit31 root 4096 Apr 21 14:30 .git
-rw-r--r-- 1 bandit31 root    6 Apr 21 14:30 .gitignore
-rw-r--r-- 1 bandit31 root  147 Apr 21 14:30 README.md
bandit31@bandit:/tmp/tmp.tK7zzRhbsa/repo$ cat README.md 
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
~~~

## Remove the .gitignore file
According to the `.gitignore` file `*.txt` files are not synchronized. Let's first remove the file and create the file with the expected content.
~~~
bandit31@bandit:/tmp/tmp.tK7zzRhbsa/repo$ rm .gitignore
~~~

## Push the key
Now, let's create our key, commit our change, and push it.
~~~
bandit31@bandit:/tmp/tmp.tK7zzRhbsa/repo$ echo -n "May I come in?" > key.txt
bandit31@bandit:/tmp/tmp.tK7zzRhbsa/repo$ git add key.txt 
bandit31@bandit:/tmp/tmp.tK7zzRhbsa/repo$ git commit -m "Adding key.txt"
[master 1bf132b] Adding key.txt
 1 file changed, 1 insertion(+)
 create mode 100644 key.txt
bandit31@bandit:/tmp/tmp.tK7zzRhbsa/repo$ git push
Could not create directory '/home/bandit31/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password: 
Counting objects: 3, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 324 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
remote: ### Attempting to validate files... ####
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
remote: Well done! Here is the password for the next level:
remote: 56a9bf19c63d650ce78e6ec0354ee45e
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
To ssh://localhost/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://bandit31-git@localhost/home/bandit31-git/repo'
~~~

# Flag
~~~
level32:56a9bf19c63d650ce78e6ec0354ee45e
~~~