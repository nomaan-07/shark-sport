import bcrypt

def hasho(password):
    hash_admin_pw = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return hash_admin_pw

print(hasho("1234"))
