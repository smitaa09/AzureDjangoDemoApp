import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class CryptKey():

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()


    def decrypt(self, encrypted_text):
        enc = base64.b64decode(encrypted_text)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_GCM, iv)
        decrypted_text = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    
    
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


  
