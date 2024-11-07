from cryptography.fernet import Fernet

# Generate a random key
key = Fernet.generate_key()
print(key.decode())
