


PUBLIC_KEY_PATH = "public_key.pem"
PRIVATE_KEY_PATH = "private_key.pem"


def load_or_create_public_key():
    if os.path.exists('public_key.pem'):
        with open('public_key.pem', 'rb') as file:
            public_key = file.read()
    else:
        key = RSA.generate(2048)
        public_key = key.publickey().export_key()
        with open('public_key.pem', 'wb') as file:
            file.write(public_key)
    return public_key


def load_or_create_private_key():
    if os.path.exists('private_key.pem'):
        with open('private_key.pem', 'rb') as file:
            private_key = file.read()
    else:
        key = RSA.generate(2048)
        private_key = key.export_key()
        with open('private_key.pem', 'wb') as file:
            file.write(private_key)
    return private_key



