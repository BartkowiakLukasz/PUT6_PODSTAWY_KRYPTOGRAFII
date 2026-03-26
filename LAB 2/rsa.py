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

def encrypt_message(public_key: tuple[int,int], private_key: tuple[int,int], text: str):
    for m in text:
        print(m, end=" ")

if __name__ == "__main__":
    public_key, private_key = generate_keys()
    encrypt_message(public_key, private_key, TEXT)