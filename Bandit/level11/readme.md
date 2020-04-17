# Level 11
## Connection
ssh bandit11@bandit.labs.overthewire.org -p2220
password: IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
## Goal
The password for the next level is stored in the file data.txt, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions
## Solution
$ cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
The password is 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu

