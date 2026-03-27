import secrets
from sympy import isprime

PRIME_LENGTH = 511

def generate_large_prime(bit_length: int = 511) -> int:
    while True:
        candidate = secrets.randbits(bit_length)
        candidate |= 1 << (bit_length - 1) | 1
        if (isprime(candidate)):
            return candidate
        
def generate_safe_prime(bit_length: int = 511) -> tuple[int, int]:
    while True:
        q = generate_large_prime(bit_length)
        n = 2 * q + 1
        if (isprime(n)):
            return q,n

def generate_g(q: int, n: int) -> int:
    while True:
        g = secrets.randbelow(n-2) + 2
        if ((pow(g,2,n) != 1) and (pow(g,q,n) != 1)):
            return g

def generate_keypair(g: int, n: int) -> tuple[int,int]:
    secret_x = secrets.randbelow(n - 3) + 2
    public_x = pow(g, secret_x, n)
    return secret_x, public_x

if __name__ == "__main__":
    q,n = generate_safe_prime(PRIME_LENGTH)
    g = generate_g(q,n)
    print("q = ", q)
    print("n = ", n)
    print("g = ", g)    
    x, X = generate_keypair(g, n)
    y, Y = generate_keypair(g, n)
    a_key = pow(Y, x, n)
    b_key = pow(X, y, n)
    print(f"Person A key: {a_key}")
    print(f"Person B key: {b_key}")




