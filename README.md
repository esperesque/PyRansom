This is a ransomware script that encrypts the files on a target's computer. Upon receipt of payment from the victim, a key is provided which can be used to decrypt the files.

When run, the script will generate a random AES key for symmetric key encryption and use this to encrypt files within the files/ folder. Only certain specified file extensions will be targeted to avoid encrypting files that might be very large, such as video files. After encryption, the AES key itself will be encrypted using RSA encryption. A private RSA key from the attacker is required in order to decrypt the AES key and restore the files.

The files/ folder contains a selection of test files that the target would feel very sad to lose access to. The backup/ folder contains identical copies of these test files in case something goes wrong with the encryption.

The following multi-step process can be followed to test the ransomware:

1. Run the generate_rsa.py script in the extras/ folder. This will generate an RSA public key, RSA_PUBLIC_KEY, and an RSA private key, RSA_PRIVATE_KEY. RSA_PUBLIC_KEY should be moved into the root folder and RSA_PRIVATE_KEY should be set aside to be sent to the target upon receipt of payment. This step is carried out by the attacker and in a practical use case the extras/ folder would not be included in the files sent to the victim.

2. Run the ransom.py script in the root folder. This will encrypt all files in the files/ folder with one of the targeted file extensions. The randomly generated AES key will be RSA-encrypted and stored in the file AES_KEY. After encryption is complete, a .html file will open in the user's default web browser and display a message with information on how to transmit payment.

3. Upon receipt of payment, the attacker sends the RSA_PRIVATE_KEY to the victim. The files can now be decrypted by moving the RSA_PRIVATE_KEY file into the root folder and running decrypter.py.

In order to make it easier for the victim to run the ransom script, the PyInstaller package can be used to make executable files with all dependencies bundled (in our case, the PyCryptodome library.) This is not demonstrated here, but has been tested and found to work as intended.
