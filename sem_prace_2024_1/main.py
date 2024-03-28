import os

STEGANOGRAPHY_IMG = "weber.bmp"
DATA_SOURCE = "validation/"
OUTPUT_DIR = "out/"
DECODED_DIR = "decoded/"

BMP_HEADER_SIZE = 54  # Standard BMP header size for uncompressed images

def is_file_too_big(steganography_img_size, input_file_size):
    """
    Function determines if the input file is about to fit into STEGANOGRAPHY_IMG
    :param steganography_img_size: number of bytes of STEGANOGRAPHY_IMG
    :param input_file_size: number of bytes of an input file
    :return: True if input file fits, False otherwise
    """
    return input_file_size > (steganography_img_size - BMP_HEADER_SIZE) // 8


def hide(input_filepath, output_name):
    """
    This procedure performs steganography with the LSB method
    The part of a filepath is a filename and also a file extension
    :param input_filepath: the file which is about to hide into STEGANOGRAPHY IMG
    :param output_name: path to the encoded img with a hidden file
    """

    # Read all STEGANOGRAPHY_IMG bytes
    with open(STEGANOGRAPHY_IMG, "rb") as f:
        steganography_file_bytes = bytearray(f.read())

    # Read all input file bytes from the input_filepath parameter
    with open(input_filepath, "rb") as f:
        input_file_bytes = f.read()

    if is_file_too_big(len(steganography_file_bytes), len(input_file_bytes)):
        print(f"File {input_filepath} is too big for steganography!")
        return

    resulting_bytes = steganography_file_bytes
    # Perform steganography
    for i in range(len(input_file_bytes)):
        for j in range(8):
            resulting_bytes[BMP_HEADER_SIZE + i * 8 + j] = (resulting_bytes[BMP_HEADER_SIZE + i * 8 + j] & 0xFE) | ((input_file_bytes[i] >> (7 - j)) & 0x01)

    # Write resulting_bytes to the file from the output_name param
    with open(output_name, "wb") as f:
        f.write(resulting_bytes)


def decode(filepath):
    """
    This method decodes a hidden file from a filepath given as parameter and stores it into decoded folder.
    The part of a filepath is a filename and also a file extension
    :param merged_filepath:
    :return:
    """

    # Read all bytes from the filepath
    with open(filepath, "rb") as f:
        merged_file_bytes = bytearray(f.read())

    resulting_bytes = bytearray()
    # Information about filename, extension and size are encoded in a filename
    basename_filepath = os.path.basename(filepath)
    filename_parts = basename_filepath.split("___")
    filename = filename_parts[0]
    extension = filename_parts[1]
    size = int(filename_parts[2])

    # Perform decoding (extract bytes from the merged_file_bytes)
    for i in range(size):
        byte = 0
        for j in range(8):
            byte |= (merged_file_bytes[BMP_HEADER_SIZE + i * 8 + j] & 0x01) << (7 - j)
        resulting_bytes.append(byte)

    filepath = os.path.join(DECODED_DIR, filename+"."+extension)
    # Write resulting_bytes into filepath
    with open(filepath, "wb") as f:
        f.write(resulting_bytes)


if __name__ == '__main__':
    if not os.path.exists(DECODED_DIR):
        os.makedirs(DECODED_DIR)

    # 1. phase hiding (encoding) -- steganography
    if os.path.exists(DATA_SOURCE):
        files = sorted(os.listdir(DATA_SOURCE))
        for file in files:
            filepath = os.path.join(DATA_SOURCE, file)
            print(f"Hiding file {filepath} into {STEGANOGRAPHY_IMG}")
            filename, extension = file.split(".")
            size = os.stat(filepath).st_size
            output_filename = os.path.join(OUTPUT_DIR, filename+"___"+extension+"___"+str(size)+"___"+STEGANOGRAPHY_IMG)
            hide(filepath, output_name=output_filename)

    # 2. phase Decoding
    if os.path.exists(OUTPUT_DIR):
        files = sorted(os.listdir(OUTPUT_DIR))
        for file in files:
            filepath = os.path.join(OUTPUT_DIR, file)
            print(f"Decoding a hidden file from {filepath}")
            decode(filepath)
