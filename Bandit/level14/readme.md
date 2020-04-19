# Level 14
## Connection
~~~~
ssh bandit14@bandit.labs.overthewire.org -p2220
password: 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
~~~~

## Goal
The password for the next level can be retrieved by submitting the password of the current level to port `30000` on `localhost`.

* Commands you may need to solve this level: `ssh`, `telnet`, `nc`, `openssl`, `s_client`, `nmap`
* Helpful Reading Material:
  * [How the Internet works in 5 minutes (YouTube)](https://www.youtube.com/watch?v=7_LPdttKXPc) (Not completely accurate, but good enough for beginners)
  * [IP Addresses](http://computer.howstuffworks.com/web-server5.htm)
  * [IP Address on Wikipedia](https://en.wikipedia.org/wiki/IP_address)
  * [Localhost on Wikipedia](https://en.wikipedia.org/wiki/Localhost)
  * [Ports](http://computer.howstuffworks.com/web-server8.htm)
  * [Port (computer networking) on Wikipedia](https://en.wikipedia.org/wiki/Port_(computer_networking))

## Solution
First connect to the server and check that port `30000` is open:
~~~~
bandit14@bandit:~$ nmap -p 30000 127.0.0.1

Starting Nmap 7.40 ( https://nmap.org ) at 2020-04-19 20:26 CEST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00017s latency).
PORT      STATE SERVICE
30000/tcp open  ndmps

Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
~~~~

OK, let's send our password:
~~~~
bandit14@bandit:~$ echo "4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e" | nc localhost 30000
Correct!
BfMYroe26WYalil77FoDi9qh59eK5xNr
~~~~

# Flag
~~~~
level15:BfMYroe26WYalil77FoDi9qh59eK5xNr
~~~~