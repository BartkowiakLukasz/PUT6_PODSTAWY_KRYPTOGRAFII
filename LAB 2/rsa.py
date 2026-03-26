import secrets
import math
from sympy import isprime

MIN_VAL = 1000
MAX_VAL = 9999
TEXT = "To jest tajna wiadomosc do zaszyfrowania w Python."


def generate_prime() -> int:
    while True:
        candidate = secrets.randbelow(MAX_VAL - MIN_VAL + 1) + MIN_VAL
        candidate |= 1
        if (isprime(candidate)):
            break
    return candidate

def generate_keys() -> tuple[tuple[int,int],tuple[int,int]]:
    # public keys (e,n)
    p = generate_prime()
    q = generate_prime()
    while (p==q):
        q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = secrets.randbelow(phi - 2) + 2
        if (math.gcd(e, phi) == 1) and isprime(e):
            break
    
    # private key (d,n)
    d = pow(e,-1,phi)
    return (e,n),(d,n)

def encrypt_message(public_key: tuple[int,int], text: str):
    encrypted_message = []
    for m in text:
        c = pow(ord(m), public_key[0], public_key[1])
        encrypted_message.append(c)
    return encrypted_message

def decrypt_message(private_key: tuple[int,int], text: list[int]):
    decrypted_message = ""
    for c in text:
        m = pow(c, private_key[0], private_key[1])
        decrypted_message += chr(m)
    return decrypted_message

def validate_rsa_process(original: str, decrypted: str) -> bool:
    return original == decrypted

if __name__ == "__main__":
    public_key, private_key = generate_keys()
    encrypted_message = encrypt_message(public_key, TEXT)
    print(encrypted_message)
    decrypted_message = decrypt_message(private_key, encrypted_message)
    print(decrypted_message)
    if (validate_rsa_process(TEXT, decrypted_message)):
        print("Decrypted message matches original")
    else:
        print("Decrypted message is different than original!")