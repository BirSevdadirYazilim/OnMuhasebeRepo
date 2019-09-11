import hashlib

def encryption_h(value1, value2):

	encryption_value = value1 + "-" + value2
	encryption_method = hashlib.md5(encryption_value.encode("utf-8"))
	login_key = encryption_method.hexdigest()

	return login_key