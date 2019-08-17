from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP


def decrypt_data(file_dir, private_key_dir):
    file_in = open(file_dir, "rb")
    private_key = RSA.import_key(open(private_key_dir).read())

    encrypted_session_key, nonce, tag, cipher_text = \
        [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

    # decrypt the session key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(encrypted_session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(cipher_text, tag)

    print(data.decode("utf-8"))


if __name__ == "__main__":
    decrypt_data("./h/ymzpqcxg.bin", "./generated_keys/private.pem")