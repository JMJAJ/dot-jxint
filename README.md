# File Encryption/Decryption Utility (.jxint File Extension)

This Python script provides functionality for encrypting and decrypting files using a passphrase-based encryption scheme. It supports various compression methods and utilizes the Fernet symmetric encryption algorithm for securing data. It's for educational purposes only.

## Features

- **Encryption:** Encrypt files using a passphrase and hardware ID.
- **Decryption:** Decrypt previously encrypted files using the encryption key.
- **Compression:** Supports multiple compression methods including Brotli, zlib, gzip, lzma, bz2, lz4, and snappy.
- **Debugger Check:** Detects if a debugger is present and exits if detected. (Dont mind this lmao, I just saw it somewhere so I copypaste)

## Requirements

- Python 3.x
- colorama (for colored output)
- cryptography (for encryption)
- brotli (for Brotli compression, Version 1)
- lz4 (for LZ4 compression, Version 1)
- python-snappy (for Snappy compression, Version 1)
- zlib (for compression, Version 2)
- lzma (for compression, Version 2)

## Usage

### Encryption

To encrypt files, run the script and choose 'E'. Follow the prompts to specify the input and output folders. The script will generate a secure passphrase and encryption key, encrypt each file in the input folder, and output the encrypted files to the specified output folder. The encryption key will be displayed upon completion.

### Decryption

To decrypt files, run the script and choose 'D'. Provide the input and output folders as well as the encryption key when prompted. The script will decrypt each file in the input folder using the provided key and output the decrypted files to the specified output folder.

### Notes

- Ensure that the input folder contains files to be encrypted/decrypted.
- Make sure to keep the encryption key secure as it is required for decryption.
- Compression method can be specified in the code (Version 1) or modified as needed (Version 2).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The script utilizes the cryptography library for encryption and decryption.
- Compression methods are provided by various Python libraries such as brotli, lz4, and python-snappy (Version 1).
- Compression functionality in Version 2 is provided by the zlib and lzma libraries.
- Debugger detection functionality is based on ctypes library.

