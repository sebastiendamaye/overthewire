# Level 18
## Connection
~~~~
ssh bandit18@bandit.labs.overthewire.org -p2220
password: kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
~~~~

## Goal
The password for the next level is stored in a file `readme` in the `home` directory. Unfortunately, someone has modified `.bashrc` to log you out when you log in with SSH.

## Solution
When we connect via SSH, we are immediately disconnected because of these lines added at the end of the `.bashrc` file:
~~~~
echo 'Byebye !'
exit 0
~~~~

However, we can still get the `readme` file:
~~~~
$ ssh bandit18@bandit.labs.overthewire.org -p2220 cat readme
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit18@bandit.labs.overthewire.org's password: 
IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
~~~~

# Flag
~~~~
level19:IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
~~~~