# Level 20
## Connection
~~~
ssh bandit20@bandit.labs.overthewire.org -p2220
password: GbKksEFF4yrVs6il55v6gwY5aVje5f0j
~~~

## Goal
There is a `setuid` binary in the `home` directory that does the following: it makes a connection to `localhost` on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).

*NOTE: Try connecting to your own network daemon to see if it works as you think.*

Commands you may need to solve this level: `ssh`, `nc`, `cat`, `bash`, `screen`, `tmux`, Unix ‘job control’ (`bg`, `fg`, `jobs`, &, `CTRL-Z`, …)

## Solution
We are provided with a setuid ELF:
~~~
bandit20@bandit:~$ file suconnect 
suconnect: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=74c0f6dc184e0412b6dc52e542782f43807268e1, not stripped
~~~

It expects a port number, passed as argument:
~~~
bandit20@bandit:~$ ./suconnect 
Usage: ./suconnect <portnumber>
This program will connect to the given port on localhost using TCP. If it receives the correct password from the other side, the next password is transmitted back.
~~~

Let's first open a socket on port `1234` that will send the password of the current level. Notice that we append `&` at the end to make sure the command will run in the background. We are provided with the PID of this background process (`19945`).
~~~
bandit20@bandit:~$ echo "GbKksEFF4yrVs6il55v6gwY5aVje5f0j" | nc -l -p 1234 &
[1] 19945
~~~

Now, let's tell our program to connect on port `1234`:
~~~
bandit20@bandit:~$ ./suconnect 1234
Read: GbKksEFF4yrVs6il55v6gwY5aVje5f0j
Password matches, sending next password
gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
[1]+  Done                    echo "GbKksEFF4yrVs6il55v6gwY5aVje5f0j" | nc -l -p 1234
~~~~

Notice that the program connected to the port, provided the password, and closed our connection, hence killing the process in the background.

# Flag
~~~
level21:gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
~~~