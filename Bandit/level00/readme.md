# Level 0
## Connection
~~~~
ssh bandit0@bandit.labs.overthewire.org -p2220
password: bandit0
~~~~
## Goal
The password for the next level is stored in a file called readme located in the home directory. Use this password to log into bandit1 using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.
## Solution
~~~~
$ cat readme 
boJ9jbbUNNfktd78OOpsqOltutMc3MY1
~~~~
