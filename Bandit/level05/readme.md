# Level 5
## Connection
ssh bandit5@bandit.labs.overthewire.org -p2220
password: koReBOKuIDDepwhWk7jZC0RTdopnAYKh
## Goal
The password for the next level is stored in a file somewhere under the inhere directory and has all of the following properties:

    human-readable
    1033 bytes in size
    not executable
## Solution
$ find . -type f -size 1033c ! -executable
./maybehere07/.file2
$ cat ./maybehere07/.file2
DXjZPULLxYr17uwoI01bNLQbtFemEgo7

