# Level 10
## Connection
~~~~
ssh bandit10@bandit.labs.overthewire.org -p2220
password: truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
~~~~
## Goal
The password for the next level is stored in the file data.txt, which contains base64 encoded data
## Solution
~~~~
$ cat data.txt | base64 -d
The password is IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
~~~~
