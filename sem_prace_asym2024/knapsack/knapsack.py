import os
import random
import sys


class Knapsack:
    def __init__(self, n):
        self.n = n
        self.private_key, self.q, self.r = self.generate_private_key()
        self.public_key = self.generate_public_key()
        self.save_parameters()

    def generate_private_key(self):
        superincreasing_sequence = []
        total = 0
        for i in range(self.n):
            if i == 0:
                value = random.randint(2 ** 100, 2 ** 400)
            else:
                value = random.randint(total + 1, 2 * total)
            superincreasing_sequence.append(value)
            total += value

        q = random.randint(total + 1, 2 * total)
        r = random.randint(2, q - 1)
        while self.gcd(r, q) != 1:
            r = random.randint(2, q - 1)

        return superincreasing_sequence, q, r

    def generate_public_key(self):
        return [(num * self.r) % self.q for num in self.private_key]

    def save_parameters(self):
        with open("../p.txt", "w") as file:
            file.write(str(self.r))
        with open("../q.txt", "w") as file:
            file.write(str(self.q))
        with open("../private_key.txt", "w") as file:
            file.write(",".join(map(str, self.private_key)))
        with open("../public_key.txt", "w") as file:
            file.write(",".join(map(str, self.public_key)))

    def encrypt(self, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        padded_binary_message = binary_message.zfill(self.n)
        encrypted = sum(bit * key for bit, key in zip(map(int, padded_binary_message), self.public_key))
        return encrypted

    def decrypt(self, encrypted):
        s = self.modinv(self.r, self.q)
        decrypted = (encrypted * s) % self.q

        binary_message = ''
        for num in reversed(self.private_key):
            if num <= decrypted:
                binary_message = '1' + binary_message
                decrypted -= num
            else:
                binary_message = '0' + binary_message

        padding_size = (8 - len(binary_message) % 8) % 8
        binary_message = binary_message.zfill(len(binary_message) + padding_size)

        hex_message = ''
        for i in range(0, len(binary_message), 8):
            hex_message += '{:02x}'.format(int(binary_message[i:i + 8], 2))

        return hex_message, padding_size

    @staticmethod
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def modinv(a, m):
        g, x, y = Knapsack.egcd(a, m)
        if g != 1:
            raise Exception('Modular inverse does not exist')
        else:
            return x % m

    @staticmethod
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = Knapsack.egcd(b % a, a)
            return (g, x - (b // a) * y, y)


def encrypt_files():
    knapsack = Knapsack(n=250)

    validation_folder = "validation/"
    out_folder = "out/"

    # Create the "out/" directory if it doesn't exist
    os.makedirs(out_folder, exist_ok=True)

    for filename in os.listdir(validation_folder):
        file_path = os.path.join(validation_folder, filename)

        with open(file_path, "rb") as file:
            content = file.read()

        encrypted_blocks = []
        for i in range(0, len(content), 31):
            block = content[i:i + 31]
            encrypted_block = knapsack.encrypt(block.hex())
            encrypted_blocks.append(str(encrypted_block))

        padding_size = 250 - (len(content) % 250)
        output_filename = f"{padding_size}_{filename}.kna"

        with open(os.path.join(out_folder, output_filename), "w") as file:
            file.write("\n".join(encrypted_blocks))


def decrypt_files():
    knapsack = Knapsack(n=250)

    out_folder = "out/"
    decoded_folder = "decoded/"

    # Create the "decoded/" directory if it doesn't exist
    os.makedirs(decoded_folder, exist_ok=True)

    for filename in os.listdir(out_folder):
        if filename.endswith(".kna"):
            with open(os.path.join(out_folder, filename), "r") as file:
                encrypted_blocks = file.read().split("\n")

            padding_size = int(filename.split("_")[0])
            original_filename = filename[len(str(padding_size)) + 1:-4]

            decrypted_content = b""
            for encrypted_block in encrypted_blocks:
                decrypted_block, _ = knapsack.decrypt(int(encrypted_block))
                decrypted_content += bytes.fromhex(decrypted_block)

            decrypted_content = decrypted_content[:-padding_size]

            with open(os.path.join(decoded_folder, original_filename), "wb") as file:
                file.write(decrypted_content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python knapsack.py [-e|-d]")
        sys.exit(1)

    if sys.argv[1] == "-e":
        encrypt_files()
    elif sys.argv[1] == "-d":
        decrypt_files()
    else:
        print("Invalid parameter. Use -e for encryption or -d for decryption.")
        sys.exit(1)
