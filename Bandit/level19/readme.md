# Level 19
## Connection
~~~~
ssh bandit19@bandit.labs.overthewire.org -p2220
password: IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
~~~~

## Goal
To gain access to the next level, you should use the `setuid` binary in the `home` directory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (`/etc/bandit_pass`), after you have used the `setuid` binary.

Helpful Reading Material: [setuid on Wikipedia](https://en.wikipedia.org/wiki/Setuid)

## Solution
We can see that `bandit20-do` is a setuid ELF:
~~~~
bandit19@bandit:~$ file bandit20-do 
bandit20-do: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=8e941f24b8c5cd0af67b22b724c57e1ab92a92a1, not stripped
~~~~

As it is owned by `bandit20`, we should be able to run commands as `bandit20` and hopefully access the password.
~~~~
bandit19@bandit:~$ ls -l
total 8
-rwsr-x--- 1 bandit20 bandit19 7296 Oct 16  2018 bandit20-do
~~~~

Let's see how the binary works:
~~~~
bandit19@bandit:~$ ./bandit20-do 
Run a command as another user.
  Example: ./bandit20-do id
~~~~

OK, the executable expects a command to be passed as argument. Let's see if we can confirm our assumption:
~~~~
bandit19@bandit:~$ whoami 
bandit19
bandit19@bandit:~$ ./bandit20-do id
uid=11019(bandit19) gid=11019(bandit19) euid=11020(bandit20) groups=11019(bandit19)
bandit19@bandit:~$ ./bandit20-do whoami
bandit20
~~~~

That's great. Now let's access the password file:
~~~~
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
~~~~

# Flag
~~~~
level20:GbKksEFF4yrVs6il55v6gwY5aVje5f0j
~~~~