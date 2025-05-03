from cryptography.fernet import Fernet, InvalidToken
import pickle as pkl

path ="private/encryption/cookie_key.key"
key = pkl.load(open(path, "rb"))

#key = Fernet.generate_key() # Uncomment this line and run the file to generate a new key if needed

fernet = Fernet(key)

def encrypt_message(message: str) -> str:
    """
    Encrypts a message using Fernet symmetric encryption.
    
    Args:
        message (str): The message to encrypt.
        
    Returns:
        str: The encrypted message as a base64-encoded string.
    """
    encoded_message = message.encode()
    encrypted_message = fernet.encrypt(encoded_message)
    return encrypted_message.decode()

def decrypt_message(encrypted_message: str) -> str:
    """
    Decrypts a message using Fernet symmetric encryption.
    
    Args:
        encrypted_message (str): The encrypted message to decrypt.
        
    Returns:
        str: The decrypted message, or None if decryption fails.
    """
    decoded_encrypted_message = encrypted_message.encode()
    try:
        decrypted_message = fernet.decrypt(decoded_encrypted_message)
        return decrypted_message.decode()
    except InvalidToken:
        #print("Decryption failed: Invalid token")
        return None