# Level 8
## Connection
ssh bandit8@bandit.labs.overthewire.org -p2220
password: cvX2JJa4CFALtqS87jk27qwqGhBM9plV
## Goal
The password for the next level is stored in the file data.txt and is the only line of text that occurs only once
## Solution
$ sort data.txt | uniq -u 
UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR

