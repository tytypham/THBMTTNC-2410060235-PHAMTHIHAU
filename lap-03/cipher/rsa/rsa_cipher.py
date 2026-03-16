import rsa
import os

class RSACipher:
    def __init__(self):
        # Đường dẫn lưu keys tương ứng với cấu trúc bài tập
        self.path = "cipher/rsa/keys/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def generate_keys(self):
        (pubkey, privkey) = rsa.newkeys(1024)
        with open(self.path + "publicKey.pem", "wb") as f:
            f.write(pubkey.save_pkcs1())
        with open(self.path + "privateKey.pem", "wb") as f:
            f.write(privkey.save_pkcs1())

    def load_keys(self):
        with open(self.path + "publicKey.pem", "rb") as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read())
        with open(self.path + "privateKey.pem", "rb") as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read())
        return privkey, pubkey

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('utf-8'), key)

    def decrypt(self, ciphertext, key):
        return rsa.decrypt(ciphertext, key).decode('utf-8')

    def sign(self, message, key):
        return rsa.sign(message.encode('utf-8'), key, 'SHA-1')

    def verify(self, message, signature, key):
        try:
            rsa.verify(message.encode('utf-8'), signature, key)
            return True
        except:
            return False