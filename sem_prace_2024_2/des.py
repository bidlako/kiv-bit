import random
from tqdm import tqdm


class Des:
    ROUNDS = 16
    BYTE_BLOCK_SIZE = 8

    IP = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    FP = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]

    E = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    S_BOXES = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    P = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]

    PC1 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]

    PC2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def __init__(self, encryption: bool = True):
        self.encryption = encryption

    def __init__(self, encryption: bool = True):
        self.encryption = encryption

    def create_key(self):
        key = random.getrandbits(64)
        return key

    def perform_des(self, input_bytes, key):
        key_bin = self.int_to_bin(key, 64)
        subkeys = self.generate_keys(key_bin)
        result = b''

        assert len(input_bytes) > 0, "Input bytes should not be empty"

        if self.encryption:
            # Pad the input bytes before processing blocks for encryption
            padded_input_bytes = self.pad_data(input_bytes)
        else:
            # No padding needed for decryption
            padded_input_bytes = input_bytes

        for i in tqdm(range(0, len(padded_input_bytes), self.BYTE_BLOCK_SIZE)):
            block = padded_input_bytes[i:i + self.BYTE_BLOCK_SIZE]
            if self.encryption:
                encrypted_block = self.des_encrypt_block(block, subkeys)
                assert len(
                    encrypted_block) == self.BYTE_BLOCK_SIZE, "Encrypted block size should be equal to BYTE_BLOCK_SIZE"
                result += encrypted_block
            else:
                decrypted_block = self.des_decrypt_block(block, subkeys)
                assert len(
                    decrypted_block) == self.BYTE_BLOCK_SIZE, "Decrypted block size should be equal to BYTE_BLOCK_SIZE"
                result += decrypted_block

        if not self.encryption:
            # Remove padding after decryption
            result = self.unpad_data(result)
            assert len(result) > 0, "Decrypted result should not be empty"

        return result

    def des_encrypt_block(self, block, subkeys):
        block_bin = self.bytes_to_bin(block)
        permuted_block = self.apply_permutation(block_bin, self.IP)
        left, right = self.split_halves(permuted_block)

        for i in range(self.ROUNDS):
            left, right = right, self.xor(left, self.f_function(right, subkeys[i]))

        ciphertext_block = self.apply_permutation(self.concat_halves(right, left), self.FP)
        return int(ciphertext_block, 2).to_bytes(self.BYTE_BLOCK_SIZE, byteorder='big')

    def des_decrypt_block(self, block, subkeys):
        block_bin = self.bytes_to_bin(block)
        permuted_block = self.apply_permutation(block_bin, self.IP)
        left, right = self.split_halves(permuted_block)

        for i in range(self.ROUNDS - 1, -1, -1):
            left, right = right, self.xor(left, self.f_function(right, subkeys[i]))

        plaintext_block = self.apply_permutation(self.concat_halves(right, left), self.FP)
        return int(plaintext_block, 2).to_bytes(self.BYTE_BLOCK_SIZE, byteorder='big')

    def f_function(self, right, subkey):
        expanded_right = self.apply_permutation(right, self.E)
        xored = self.xor(expanded_right, subkey)
        sbox_outputs = [self.apply_sbox(xored[i:i + 6], self.S_BOXES[i // 6]) for i in range(0, len(xored), 6)]
        sbox_result = ''.join(sbox_outputs)
        return self.apply_permutation(sbox_result, self.P)

    def generate_keys(self, key):
        permuted_key = self.apply_permutation(key, self.PC1)
        left, right = self.split_halves(permuted_key)
        subkeys = []

        for i in range(self.ROUNDS):
            left = self.left_shift(left, self.SHIFT_TABLE[i])
            right = self.left_shift(right, self.SHIFT_TABLE[i])
            subkey = self.apply_permutation(self.concat_halves(left, right), self.PC2)
            subkeys.append(subkey)

        return subkeys

    def pad_data(self, data):
        padding_length = self.BYTE_BLOCK_SIZE - len(data) % self.BYTE_BLOCK_SIZE
        if padding_length == 0:
            padding_length = self.BYTE_BLOCK_SIZE
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def unpad_data(self, data):
        padding_length = data[-1]
        if padding_length < 1 or padding_length > self.BYTE_BLOCK_SIZE:
            return data
        if data[-padding_length:] != bytes([padding_length] * padding_length):
            return data
        return data[:-padding_length]

    def bytes_to_bin(self, bytes_):
        return ''.join(format(byte, '08b') for byte in bytes_)

    def split_halves(self, binary):
        return binary[:len(binary) // 2], binary[len(binary) // 2:]

    def concat_halves(self, left, right):
        return left + right

    def left_shift(self, binary, shift_amount):
        return binary[shift_amount:] + binary[:shift_amount]

    def apply_permutation(self, binary, permutation_table):
        return ''.join(binary[i - 1] for i in permutation_table)

    def apply_sbox(self, binary, sbox):
        row = int(binary[0] + binary[-1], 2)
        col = int(binary[1:5], 2)
        return bin(sbox[row][col])[2:].zfill(4)

    def xor(self, a, b):
        return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

    def int_to_bin(self, integer, length):
        return bin(integer)[2:].zfill(length)