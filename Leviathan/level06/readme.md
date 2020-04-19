# Level 6
## Connection
~~~~
$ ssh leviathan6@leviathan.labs.overthewire.org -p 2223
Password: UgaoFee4li
~~~~

## Solution
There is an executable file (`leviathan6`) in the `home` directory. This executable expects a parameter (a 4 digits password):
~~~~
leviathan6@leviathan:~$ ls -la
total 28
drwxr-xr-x  2 root       root       4096 Aug 26  2019 .
drwxr-xr-x 10 root       root       4096 Aug 26  2019 ..
-rw-r--r--  1 root       root        220 May 15  2017 .bash_logout
-rw-r--r--  1 root       root       3526 May 15  2017 .bashrc
-r-sr-x---  1 leviathan7 leviathan6 7452 Aug 26  2019 leviathan6
-rw-r--r--  1 root       root        675 May 15  2017 .profile
leviathan6@leviathan:~$ ./leviathan6 
usage: ./leviathan6 <4 digit code>
leviathan6@leviathan:~$ ./leviathan6 1234
Wrong
~~~~

Running `ltrace` doesn't reveal the expected password:
~~~~
leviathan6@leviathan:~$ ltrace ./leviathan6 1234
__libc_start_main(0x804853b, 2, 0xffffd784, 0x80485e0 <unfinished ...>
atoi(0xffffd8af, 0, 0xf7e40890, 0x804862b)                      = 1234
puts("Wrong"Wrong
)                                                   = 6
+++ exited (status 0) +++
~~~~

Let's debug the executable with `gdb`.
```asm
leviathan6@leviathan:~$ gdb -q ./leviathan6 
Reading symbols from ./leviathan6...(no debugging symbols found)...done.
(gdb) set disassembly-flavor intel
(gdb) disas main
Dump of assembler code for function main:
   0x0804853b <+0>:	lea    ecx,[esp+0x4]
   0x0804853f <+4>:	and    esp,0xfffffff0
   0x08048542 <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048545 <+10>:	push   ebp
   0x08048546 <+11>:	mov    ebp,esp
   0x08048548 <+13>:	push   ebx
   0x08048549 <+14>:	push   ecx
   0x0804854a <+15>:	sub    esp,0x10
   0x0804854d <+18>:	mov    eax,ecx
   0x0804854f <+20>:	mov    DWORD PTR [ebp-0xc],0x1bd3   ; [ebp-0xc] = 0x1bd3
   0x08048556 <+27>:	cmp    DWORD PTR [eax],0x2
   0x08048559 <+30>:	je     0x804857b <main+64>
   0x0804855b <+32>:	mov    eax,DWORD PTR [eax+0x4]
   0x0804855e <+35>:	mov    eax,DWORD PTR [eax]
   0x08048560 <+37>:	sub    esp,0x8
   0x08048563 <+40>:	push   eax
   0x08048564 <+41>:	push   0x8048660
   0x08048569 <+46>:	call   0x80483b0 <printf@plt>
   0x0804856e <+51>:	add    esp,0x10
   0x08048571 <+54>:	sub    esp,0xc
   0x08048574 <+57>:	push   0xffffffff
   0x08048576 <+59>:	call   0x80483f0 <exit@plt>
   0x0804857b <+64>:	mov    eax,DWORD PTR [eax+0x4]
   0x0804857e <+67>:	add    eax,0x4
   0x08048581 <+70>:	mov    eax,DWORD PTR [eax]
   0x08048583 <+72>:	sub    esp,0xc
   0x08048586 <+75>:	push   eax
   0x08048587 <+76>:	call   0x8048420 <atoi@plt>
   0x0804858c <+81>:	add    esp,0x10
   0x0804858f <+84>:	cmp    eax,DWORD PTR [ebp-0xc]      ; if PIN != value in [ebp-0xc]?
   0x08048592 <+87>:	jne    0x80485bf <main+132>         ; jump to incorrect PIN
   0x08048594 <+89>:	call   0x80483c0 <geteuid@plt>      ; ---- correct PIN
   0x08048599 <+94>:	mov    ebx,eax
   0x0804859b <+96>:	call   0x80483c0 <geteuid@plt>
   0x080485a0 <+101>:	sub    esp,0x8
   0x080485a3 <+104>:	push   ebx
   0x080485a4 <+105>:	push   eax
   0x080485a5 <+106>:	call   0x8048400 <setreuid@plt>
   0x080485aa <+111>:	add    esp,0x10
   0x080485ad <+114>:	sub    esp,0xc
   0x080485b0 <+117>:	push   0x804867a
   0x080485b5 <+122>:	call   0x80483e0 <system@plt>      ; spawn a shell
   0x080485ba <+127>:	add    esp,0x10
   0x080485bd <+130>:	jmp    0x80485cf <main+148>
   0x080485bf <+132>:	sub    esp,0xc                     ; --- incorrect PIN
   0x080485c2 <+135>:	push   0x8048682
   0x080485c7 <+140>:	call   0x80483d0 <puts@plt>
   0x080485cc <+145>:	add    esp,0x10
   0x080485cf <+148>:	mov    eax,0x0
   0x080485d4 <+153>:	lea    esp,[ebp-0x8]
   0x080485d7 <+156>:	pop    ecx
   0x080485d8 <+157>:	pop    ebx
   0x080485d9 <+158>:	pop    ebp
---Type <return> to continue, or q <return> to quit---Quit
(gdb) q
```

At `0x0804854f` we see that `ebp-0xc]` is set to `0x1bd3`. The PIN is compared to this value at `0x0804858f`. The expected PIN is `0x1bd3`, which is equal to `7123`.

Providing the expected password spawns a shell with sufficient rights to read the password file:
~~~~
leviathan6@leviathan:~$ ./leviathan6 7123
$ cat /etc/leviathan_pass/leviathan7
ahy7MaeBo9
~~~~

# Flag
~~~~
leviathan7:ahy7MaeBo9
~~~~