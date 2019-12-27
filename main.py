from hashlib import sha1
import random
import string
import os


class STHS:
    def __init__(self, hash_function=sha1, random_size=1, data_size=1):
        self.hash_function = hash_function
        self.random_size = random_size
        self.data_size = data_size
        self.random_pool = string.ascii_letters + string.digits + string.punctuation + ' '
        self.hash_prefix_size = 6
    
    def encrypt(self, password, data):
        encrypted = ""
        for chunk in data:
            data_to_hash = password
            for x in range(self.random_size):
                data_to_hash += random.choice(self.random_pool)
            data_to_hash += chunk
            hash_value = self.hash_function(data_to_hash.encode())
            prefix = hash_value.hexdigest()[:self.hash_prefix_size]
            encrypted += prefix
        return encrypted

    def decrypt(self, password, data):
        decrypted = ""
        for chunk in [data[i:i+self.hash_prefix_size] for i in range(0, len(data), self.hash_prefix_size)]:
            guess = ""
            while guess != chunk:
                guess = password
                for x in range(self.random_size+1):
                    guess += random.choice(self.random_pool)
                value = guess[-self.data_size:]
                hash_value = self.hash_function(guess.encode())
                guess = hash_value.hexdigest()[:self.hash_prefix_size]
            decrypted += value
        return decrypted

if __name__ == "__main__":
    password = "password123"
    secret_message = "the code to the computer is 'B4dStewI5N3VrEN!ce'"
    crypto = STHS()
    encrypted_message = crypto.encrypt(password, secret_message)
    print(encrypted_message)
    clear_text = crypto.decrypt(password, encrypted_message)
    print(clear_text)
