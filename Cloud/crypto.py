from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

def CreateRSAKeys():
    code = 'nooneknows'
    # Generate a 2048-bit RSA key
    key = RSA.generate(2048)
    encrypted_key = key.exportKey(passphrase=code, pkcs=8, protection="scryptAndAES128-CBC")
    # Generate private key
    with open('my_private_rsa_key.bin', 'wb') as f:
        f.write(encrypted_key)
    # Generating a public key
    with open('my_rsa_public.pem', 'wb') as f:
        f.write(key.publickey().exportKey())

def Encrypt(filename):         
    data = ''
    # Binary read-only open file, read file data
    with open(filename, 'rb') as f:
        data = f.read()
    with open(filename, 'wb') as out_file:
        # Recipient key - public key
        recipient_key = RSA.import_key(open('my_rsa_public.pem').read())
        #a 16-byte session key
        session_key = get_random_bytes(16)
        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        out_file.write(cipher_rsa.encrypt(session_key))
        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
       
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        out_file.write(cipher_aes.nonce)
        out_file.write(tag)
        out_file.write(ciphertext)
def Descrypt(filename):
    code = 'nooneknows'
    with open(filename, 'rb') as fobj:
        # Import private key
        private_key = RSA.import_key(open('my_private_rsa_key.bin').read(), passphrase=code)
        # Session key, random number, message authentication code, confidential data
        enc_session_key, nonce, tag, ciphertext = [ fobj.read(x) 
                                                    for x in (private_key.size_in_bytes(), 
                                                    16, 16, -1) ]
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        # Decrypt
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    with open(filename, 'wb') as wobj:
        wobj.write(data)


CreateRSAKeys()
#Encrypt('dataset.csv')
#Descrypt('dataset.csv')
