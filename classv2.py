import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# Generate a new Fernet key
key = Fernet.generate_key()
fernet = Fernet(key)

# Read in the data to be encrypted from the file
with open('C:\Users\hp\Downloads\data.csv', 'rb') as f:
    data = f.read()

# Encrypt the data using the Fernet object
encrypted_data = fernet.encrypt(data)

# Write the encrypted data to a new file
with open('encrypted_datanew.csv', 'wb') as f:
    f.write(encrypted_data)

# Generate an RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Serialize the private key
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Save the serialized private key to a file
with open('private_key.pem', 'wb') as f:
    f.write(private_key_bytes)

# Serialize the public key
public_key_bytes = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the serialized public key to a file
with open('public_key.pem', 'wb') as f:
    f.write(public_key_bytes)

# Read in the serialized public key
with open('public_key.pem', 'rb') as f:
    public_key_bytes = f.read()

# Deserialize the public key
public_key = serialization.load_pem_public_key(
    public_key_bytes,
    backend=default_backend()
)

# Encrypt the Fernet key using the public RSA key
encrypted_key = public_key.encrypt(
    key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save the encrypted key to a file
with open('encrypted_key.bin', 'wb') as f:
    f.write(encrypted_key)

# Read in the serialized private key
with open('private_key.pem', 'rb') as f:
    private_key_bytes = f.read()

# Deserialize the private key
private_key = serialization.load_pem_private_key(
    private_key_bytes,
    password=None,
    backend=default_backend()
)

# Read in the encrypted key
with open('encrypted_key.bin', 'rb') as f:
    encrypted_key = f.read()

# Decrypt the encrypted key using the private RSA key
key = private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Recreate the Fernet object with the decrypted key
fernet = Fernet(key)

# Read in the encrypted data
with open('encrypted_datanew.csv', 'rb') as f:
    encrypted_data = f.read()

# Decrypt the encrypted data using the Fernet object
data = fernet.decrypt(encrypted_data)

# Write the decrypted data to a new file
with open('decrypted_datanew.csv', 'wb') as f:
    f.write(data)


# print(os.getcwd())
# hydaaaaa lsa77777777
