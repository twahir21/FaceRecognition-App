import csv
from cryptography.fernet import Fernet

# Initialize the cryptography key
key = b'TkaKvFAWzRtmjOnIis5XK31UOK61C02Z2cSMvN_efjM='
cipher_suite = Fernet(key)

def encrypt_data(data):
    encrypted_data = []
    for entry in data:
        username, password, email = entry
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        encrypted_email = cipher_suite.encrypt(email.encode()).decode()
        encrypted_data.append((username, encrypted_password, encrypted_email))
    return encrypted_data

def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for entry in data:
            writer.writerow(entry)

# Dummy data
dummy_data = [
    ("user1", "password1", "user1@example.com"),
    ("user2", "password2", "user2@example.com"),
    ("user3", "password3", "user3@example.com")
]

# Encrypt the dummy data
encrypted_data = encrypt_data(dummy_data)

# Save encrypted data to CSV
save_data_to_csv(encrypted_data, "encrypt.csv")

print("Data encrypted and saved to 'encrypt.csv' file.")
