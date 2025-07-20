from argon2 import PasswordHasher 

hasher = PasswordHasher()

def hash_password(plain_password):
    hashed_password = hasher.hash(plain_password)
    return hashed_password

def verify_hash(hashed_password,password):
    valid_password = hasher.verify(hashed_password,password)
    return valid_password