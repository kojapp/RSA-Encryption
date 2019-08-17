from Cryptodome.PublicKey import RSA
from create_directory import create_dir
from constants import KEYS_DIR, NEW_PRIVATE_KEY, NEW_PUBLIC_KEY


def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    create_dir(KEYS_DIR)

    # export private key
    encryption_key_file = open(NEW_PRIVATE_KEY, "wb")
    encryption_key_file.write(private_key)

    # export public key
    encryption_key_file = open(NEW_PUBLIC_KEY, "wb")
    encryption_key_file.write(public_key)

    encryption_key_file.close()
