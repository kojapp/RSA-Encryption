import random
import string
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP

from create_directory import create_dir


def encrypt_data(data, out_dir, public_key_dir):
    data = data.encode("utf-8")
    create_dir(out_dir)
    file_name = "".join(random.choice(string.ascii_lowercase) for i in range(8))
    file_name += ".bin"
    file_dir = f"{out_dir}/{file_name}"
    file_out = open(file_dir, "wb")

    # find a public key
    try:
        public_key = RSA.import_key(open(public_key_dir).read())
    except FileNotFoundError:
        raise FileNotFoundError("Could not find existing public key.")
    except Exception as error:
        raise Exception(f"An error has occurred: {error}")

    # generate a session key
    session_key = get_random_bytes(16)

    # encrypt the session key with the public key
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    cipher_text, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(component) for component in (enc_session_key, cipher_aes.nonce, tag, cipher_text)]
    print(file_dir)
