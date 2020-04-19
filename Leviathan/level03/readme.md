# Level 3
## Connection
~~~~
$ ssh leviathan3@leviathan.labs.overthewire.org -p 2223
Password: Ahdiemoo1j
~~~~

## Solution
### ltrace
When we run the program, we are asked to provide a password:
~~~~
leviathan3@leviathan:~$ ./level3 
Enter the password> oops
bzzzzzzzzap. WRONG
~~~~

Let's use `ltrace` to see the calls to `strcmp`:
~~~~
leviathan3@leviathan:~$ ltrace ./level3 
__libc_start_main(0x8048618, 1, 0xffffd784, 0x80486d0 <unfinished ...>
strcmp("h0no33", "kakaka")                                      = -1
printf("Enter the password> ")                                  = 20
fgets(Enter the password> oops
"oops\n", 256, 0xf7fc55a0)                                = 0xffffd590
strcmp("oops\n", "snlprintf\n")                                 = -1
puts("bzzzzzzzzap. WRONG"bzzzzzzzzap. WRONG
)                                      = 19
+++ exited (status 0) +++
~~~~

OK, the program was expecting the password `snlprintf`:
~~~~
$ ./level3 
Enter the password> snlprintf
[You've got shell]!
$ whoami    <=== from here, we are in the shell that has been spawn by the executable
leviathan4
$ cat /etc/leviathan_pass/leviathan4
vuH0coox6m
~~~~

# Flag
~~~~
leviathan4:vuH0coox6m
~~~~