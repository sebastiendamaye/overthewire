# Level 9
## Connection
ssh bandit9@bandit.labs.overthewire.org -p2220
password: UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
## Goal
The password for the next level is stored in the file data.txt in one of the few human-readable strings, beginning with several ‘=’ characters.
## Solution
$ strings data.txt | grep "==="
2========== the
========== password
========== isa
========== truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk

