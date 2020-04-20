# Level 17
## Connection
~~~~
ssh bandit17@bandit.labs.overthewire.org -p2220
password: xLYVMN9WE5zQ5vHacb0sZEVqbrp7nBTn
~~~~

## Goal
There are 2 files in the `home` directory: `passwords.old` and `passwords.new`. The password for the next level is in `passwords.new` and is the only line that has been changed between `passwords.old` and `passwords.new`.

*NOTE: if you have solved this level and see ‘Byebye!’ when trying to log into bandit18, this is related to the next level, bandit19*

Commands you may need to solve this level: `cat`, `grep`, `ls`, `diff`

## Solution
Let's use `diff` to highlight the differences between the 2 password files:
~~~~
bandit17@bandit:~$ diff passwords.old passwords.new 
42c42
< hlbSBPAWJmL6WFDb06gpTx1pPButblOA
---
> kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
~~~~

The only password that is added to `password.new` is `kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd`. Let's see if we can connect using the password:
~~~~
$ ssh bandit18@bandit.labs.overthewire.org -p2220
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit18@bandit.labs.overthewire.org's password: 
Linux bandit 4.18.12 x86_64 GNU/Linux
               
      ,----..            ,----,          .---. 
     /   /   \         ,/   .`|         /. ./|
    /   .     :      ,`   .'  :     .--'.  ' ;
   .   /   ;.  \   ;    ;     /    /__./ \ : |
  .   ;   /  ` ; .'___,/    ,' .--'.  '   \' .
  ;   |  ; \ ; | |    :     | /___/ \ |    ' ' 
  |   :  | ; | ' ;    |.';  ; ;   \  \;      : 
  .   |  ' ' ' : `----'  |  |  \   ;  `      |
  '   ;  \; /  |     '   :  ;   .   \    .\  ; 
   \   \  ',  /      |   |  '    \   \   ' \ |
    ;   :    /       '   :  |     :   '  |--"  
     \   \ .'        ;   |.'       \   \ ;     
  www. `---` ver     '---' he       '---" ire.org     
               
              
Welcome to OverTheWire!

[SNIP]

Byebye !
Connection to bandit.labs.overthewire.org closed.
~~~~

# Flag
~~~~
level18:kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
~~~~