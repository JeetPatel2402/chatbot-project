import hashlib
password = 'password'
h = hashlib.md5(password.encode())
print(h.hexdigest())
