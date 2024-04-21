from Crypto.PublicKey import RSA

keypair = RSA.generate(1024)
pub_key = keypair.publickey()

with open("RSA_PUBLIC_KEY", "wb") as f:
    f.write(pub_key.exportKey("PEM"))
with open("RSA_PRIVATE_KEY", "wb") as f:
    f.write(keypair.exportKey("PEM"))
