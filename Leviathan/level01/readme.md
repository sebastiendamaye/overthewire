# Level 1
## Connection
~~~~
$ ssh leviathan1@leviathan.labs.overthewire.org -p 2223
Password: rioGegei8m
~~~~

## Solution
### /etc/leviathan_pass
Let's see if we can dump the password:
~~~~
leviathan1@leviathan:~$ cat /etc/leviathan_pass/leviathan2
cat: /etc/leviathan_pass/leviathan2: Permission denied
~~~~

No luck, let's analyze our `home` directory.

### ./check
There is a an executable file named `check` in our `home` directory:
~~~~
leviathan1@leviathan:~$ ls -la
total 28
drwxr-xr-x  2 root       root       4096 Aug 26  2019 .
drwxr-xr-x 10 root       root       4096 Aug 26  2019 ..
-rw-r--r--  1 root       root        220 May 15  2017 .bash_logout
-rw-r--r--  1 root       root       3526 May 15  2017 .bashrc
-r-sr-x---  1 leviathan2 leviathan1 7452 Aug 26  2019 check
-rw-r--r--  1 root       root        675 May 15  2017 .profile
leviathan1@leviathan:~$ file check 
check: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=c735f6f3a3a94adcad8407cc0fda40496fd765dd, not stripped
~~~~
When we run it, it asks for a password, but we don't have it:
~~~~
leviathan1@leviathan:~$ ./check 
password: password
Wrong password, Good Bye ...
~~~~

The `strings` command reveals interesting strings:
~~~~
secrf
love
/bin/sh
~~~~
I tried both `secrf` and `love` without success. Notice the string `/bin/sh` which may be suspicous.

Let's analyze with `ltrace`:
~~~~
$ ltrace ./check 
__libc_start_main(0x804853b, 1, 0xffffd794, 0x8048610 <unfinished ...>
printf("password: ")                                                                                                              = 10
getchar(1, 0, 0x65766f6c, 0x646f6700password: oops
)                                                                                             = 111
getchar(1, 0, 0x65766f6c, 0x646f6700)                                                                                             = 111
getchar(1, 0, 0x65766f6c, 0x646f6700)                                                                                             = 112
strcmp("oop", "sex")                                                                                                              = -1
puts("Wrong password, Good Bye ..."Wrong password, Good Bye ...
)                                                                                              = 29
+++ exited (status 0) +++
~~~~
We see a call to `strcmp` that compares our password with the expected one (`sex`). OK, let's use it:
~~~~
$ ./check 
password: sex
$ ls <== from here, this is a shell spawned by ./check
check
$ cd /etc/leviathan_pass
$ ls
leviathan0  leviathan1	leviathan2  leviathan3	leviathan4  leviathan5	leviathan6  leviathan7
$ cat leviathan2
ougahZi8Ta
$ 
~~~~
Very nice, the executable was spwaning a shell that allowed us to dump the password.

# Flag
~~~~
leviathan2:ougahZi8Ta
~~~~
