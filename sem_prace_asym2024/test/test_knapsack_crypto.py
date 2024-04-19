import os
import shutil
import unittest


class TestKnapsack(unittest.TestCase):
    def setUp(self):
        self.validation_folder = "../validation/"
        self.out_folder = "../out/"
        self.decoded_folder = "../decoded/"

    def test_encrypt_decrypt_files(self):

        # Check if the decoded files match the original files
        for filename in os.listdir(self.validation_folder):
            with open(os.path.join(self.validation_folder, filename), "rb") as original_file:
                original_content = original_file.read()
            with open(os.path.join(self.decoded_folder, filename), "rb") as decoded_file:
                decoded_content = decoded_file.read()
            self.assertEqual(original_content, decoded_content,
                             f"Decoded file {filename} does not match the original file.")
