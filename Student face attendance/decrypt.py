import csv
from cryptography.fernet import Fernet

# Initialize the cryptography key
key = b'TkaKvFAWzRtmjOnIis5XK31UOK61C02Z2cSMvN_efjM='
cipher_suite = Fernet(key)

def decrypt_data(data):
    decrypted_data = []
    for entry in data:
        username, encrypted_password, encrypted_email = entry
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        decrypted_email = cipher_suite.decrypt(encrypted_email.encode()).decode()
        decrypted_data.append((username, decrypted_password, decrypted_email))
    return decrypted_data

def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for entry in data:
            writer.writerow(entry)

# Load encrypted data from CSV
encrypted_data = []
with open("encrypt.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        encrypted_data.append(row)

# Decrypt the encrypted data
decrypted_data = decrypt_data(encrypted_data)

# Save decrypted data to CSV
save_data_to_csv(decrypted_data, "decrypt.csv")

print("Data decrypted and saved to 'decrypt.csv' file.")
