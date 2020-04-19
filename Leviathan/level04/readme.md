# Level 4
## Connection
~~~~
$ ssh leviathan4@leviathan.labs.overthewire.org -p 2223
Password: vuH0coox6m
~~~~

## Solution
~~~~
$ ls -la
total 24
drwxr-xr-x  3 root root       4096 Aug 26  2019 .
drwxr-xr-x 10 root root       4096 Aug 26  2019 ..
-rw-r--r--  1 root root        220 May 15  2017 .bash_logout
-rw-r--r--  1 root root       3526 May 15  2017 .bashrc
-rw-r--r--  1 root root        675 May 15  2017 .profile
dr-xr-x---  2 root leviathan4 4096 Aug 26  2019 .trash
~~~~

When executed, the program displays binary:
~~~~
$ ./bin 
01010100 01101001 01110100 01101000 00110100 01100011 01101111 01101011 01100101 01101001 00001010 
~~~~

That we can easily convert to ASCII:
```python
$ python
>>> a = "01010100 01101001 01110100 01101000 00110100 01100011 01101111 01101011 01100101 01101001 00001010"
>>> ''.join([chr(int(i,2)) for i in a.split(' ')])
'Tith4cokei\n'
```

# Flag
~~~~
leviathan5:Tith4cokei
~~~~