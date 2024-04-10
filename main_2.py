import os
import secrets
import base64
import time
import platform
from colorama import init, Fore, Style
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import zlib

init()

SUCCESS_COLOR = Fore.GREEN
ERROR_COLOR = Fore.RED
INFO_COLOR = Fore.BLUE + Style.BRIGHT
RESET_COLOR = Style.RESET_ALL

def generate_secure_passphrase(length=256):
    return secrets.token_urlsafe(length)

def generate_key(passphrase, hwid):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.urandom(32) + hwid.encode(),
        iterations=10000000,
        backend=default_backend()
    )
    key = kdf.derive(passphrase.encode())
    return base64.urlsafe_b64encode(key).decode()

def get_hwid():
    system_info = platform.uname()
    hwid = system_info.node + system_info.processor + system_info.machine
    return hwid

def compress_data(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            compressor = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
            while True:
                chunk = f_in.read(1024 * 1024)  # Read 1 MB at a time
                if not chunk:
                    break
                compressed_chunk = compressor.compress(chunk)
                f_out.write(compressed_chunk)
            f_out.write(compressor.flush())

def decompress_data(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
            while True:
                chunk = f_in.read(1024 * 1024)  # Read 1 MB at a time
                if not chunk:
                    break
                decompressed_chunk = decompressor.decompress(chunk)
                f_out.write(decompressed_chunk)
            f_out.write(decompressor.flush())

def encrypt_file(input_folder, output_folder, file_name, key):
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name + ".jxint")
    original_size = 0
    encrypted_size = 0

    cipher = Fernet(key.encode())

    start_time = time.time()

    # Compress and encrypt the file in chunks
    compress_data(input_file_path, output_file_path)

    with open(output_file_path, 'rb') as f:
        while True:
            chunk_en = f.read(1024 * 1024)  # Read 1 MB at a time
            if not chunk_en:
                break
            encrypted_chunk = cipher.encrypt(chunk_en)
            encrypted_size += len(encrypted_chunk)

    end_time = time.time()

    original_size += os.path.getsize(input_file_path)

    print(f"{SUCCESS_COLOR}File '{file_name}' encrypted successfully.")
    print(f"Original size: {original_size} bytes\nEncrypted size: {encrypted_size} bytes")
    print(f"Time taken: {end_time - start_time} seconds{RESET_COLOR}")

def decrypt_file(input_folder, output_folder, file_name, key):
    input_file_path = os.path.join(output_folder, file_name)
    output_file_path = os.path.join(input_folder, file_name[:-6])
    original_size = 0
    decrypted_size = 0

    cipher = Fernet(key.encode())

    start_time = time.time()

    decompress_data(input_file_path, output_file_path)

    with open(output_file_path, 'rb') as f:
        while True:
            chunk_de = f.read(1024 * 1024)  # Read 1 MB at a time
            if not chunk_de:
                break
            dencrypted_chunk = cipher.encrypt(chunk_de)
            decrypted_size += len(dencrypted_chunk)

    end_time = time.time()

    original_size += os.path.getsize(input_file_path)
    decrypted_size += os.path.getsize(output_file_path)

    print(f"{SUCCESS_COLOR}File '{file_name}' decrypted successfully.")
    print(f"Original size: {original_size} bytes\nDecrypted size: {decrypted_size} bytes")
    print(f"Time taken: {end_time - start_time} seconds{RESET_COLOR}")

def get_input_folder():
    folder = input(f"{INFO_COLOR}Enter the input folder path (default: 'input'): {RESET_COLOR}")
    if not folder:
        folder = "input"
    return folder

def get_output_folder():
    folder = input(f"{INFO_COLOR}Enter the output folder path (default: 'output'): {RESET_COLOR}")
    if not folder:
        folder = "output"
    return folder

def perform_encryption(input_folder, output_folder, passphrase, hwid):
    key = generate_key(passphrase, hwid)
    for file_name in os.listdir(input_folder):
        encrypt_file(input_folder, output_folder, file_name, key)
    return key

def perform_decryption(input_folder, output_folder, key, hwid):
    key = generate_key(key, hwid)
    for file_name in os.listdir(output_folder):
        decrypt_file(input_folder, output_folder, file_name, key)

def main():    
    print(f"{INFO_COLOR}Welcome to File Encryption/Decryption Utility!{RESET_COLOR}")
    choice = input(f"{INFO_COLOR}Enter 'E' to encrypt or 'D' to decrypt: {RESET_COLOR}").upper()

    if choice == 'E':
        passphrase = generate_secure_passphrase()
        input_folder = get_input_folder()
        output_folder = get_output_folder()
        hwid = get_hwid()
        key = perform_encryption(input_folder, output_folder, passphrase, hwid)
        print(f"{SUCCESS_COLOR}Encryption key: {key}{RESET_COLOR}")
    elif choice == 'D':
        input_folder = get_input_folder()
        output_folder = get_output_folder()
        hwid = get_hwid()
        key = input(f"{INFO_COLOR}Enter the encryption key: {RESET_COLOR}")
        perform_decryption(input_folder, output_folder, key, hwid)
    else:
        print(f"{ERROR_COLOR}Invalid choice. Please enter 'E' to encrypt or 'D' to decrypt.{RESET_COLOR}")

if __name__ == "__main__":
    main()
