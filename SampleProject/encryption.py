from cryptography.fernet import Fernet
import base64

class CryptKey():
    key = b'RkraUiiGcz3TaZx38QbZl4IlwHldPpMVi-ToENyiaRk='
    #credential = DefaultAzureCredential()
    #client = SecretClient(vault_url='', credential=credential
    #key= client.get_secret("secret_key")
	
    def encrypt_key(self):
        # get the key from settings
        #key = Fernet.generate_key() #this is your "password"
        cipher_suite = Fernet(self.key) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        self.encrypted_key = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return self.encrypted_key 

    def decrypt_key(self,encrypted_text):
        txt = base64.urlsafe_b64decode(encrypted_text)
        cipher_suite = Fernet(self.key)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        return decoded_text

    def encrypt_db(self):
        # get the key from settings
        #key = Fernet.generate_key() #this is your "password"
        cipher_suite = Fernet(self.key) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        self.encrypted_pwd = base64.urlsafe_b64encode(encrypted_text).decode("ascii")            
        return self.encrypted_pwd 

    def decrypt(self,encrypted_text):
        txt = base64.urlsafe_b64decode(encrypted_text)
        cipher_suite = Fernet(self.key)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        return decoded_text


