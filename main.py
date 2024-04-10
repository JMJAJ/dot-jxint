import os
import secrets
import base64
import zlib
import lzma
import time
import ctypes
import platform
from colorama import init, Fore, Style
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

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

def check_debugger():
    kernel32 = ctypes.windll.kernel32
    return kernel32.IsDebuggerPresent()

def compress_data(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        data = f_in.read()
        compressed_data = zlib.compress(data)
        with lzma.open(output_file, 'wb') as f_out:
            f_out.write(compressed_data)

def decompress_data(input_file, output_file):
    with lzma.open(input_file, 'rb') as f_in:
        compressed_data = f_in.read()
        data = zlib.decompress(compressed_data)
        with open(output_file, 'wb') as f_out:
            f_out.write(data)

def encrypt_file(input_folder, output_folder, file_name, key):
    input_file_path = os.path.join(input_folder, file_name)
    output_file_path = os.path.join(output_folder, file_name + ".jxint")
    original_size = 0
    encrypted_size = 0

    cipher = Fernet(key.encode())

    start_time = time.time()

    compress_data(input_file_path, output_file_path)

    with open(output_file_path, 'rb') as f:
        data = f.read()

    encrypted_data = cipher.encrypt(data)

    with open(output_file_path, 'wb') as f:
        f.write(encrypted_data)

    end_time = time.time()

    original_size += os.path.getsize(input_file_path)
    encrypted_size += os.path.getsize(output_file_path)

    print(f"{SUCCESS_COLOR}File '{file_name}' encrypted successfully.")
    print(f"Original size: {original_size} bytes, Encrypted size: {encrypted_size} bytes")
    print(f"Time taken: {end_time - start_time} seconds{RESET_COLOR}")

def decrypt_file(input_folder, output_folder, file_name, key):
    input_file_path = os.path.join(output_folder, file_name)
    output_file_path = os.path.join(input_folder, file_name[:-6])
    original_size = 0
    decrypted_size = 0

    cipher = Fernet(key.encode())

    start_time = time.time()

    with open(input_file_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    with open(input_file_path + ".tmp", 'wb') as f:
        f.write(decrypted_data)

    decompress_data(input_file_path + ".tmp", output_file_path)

    os.remove(input_file_path + ".tmp")

    end_time = time.time()

    original_size += os.path.getsize(input_file_path)
    decrypted_size += os.path.getsize(output_file_path)

    print(f"{SUCCESS_COLOR}File '{file_name}' decrypted successfully.")
    print(f"Original size: {original_size} bytes, Decrypted size: {decrypted_size} bytes")
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

def perform_decryption(input_folder, output_folder, key):
    for file_name in os.listdir(output_folder):
        decrypt_file(input_folder, output_folder, file_name, key)

def main():
    if check_debugger():
        print(f"{ERROR_COLOR}Debugger detected. Exiting.{RESET_COLOR}")
        return
    
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
        key = input(f"{INFO_COLOR}Enter the encryption key: {RESET_COLOR}")
        perform_decryption(input_folder, output_folder, key)
    else:
        print(f"{ERROR_COLOR}Invalid choice. Please enter 'E' to encrypt or 'D' to decrypt.{RESET_COLOR}")

if __name__ == "__main__":
    main()