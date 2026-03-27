import secrets
from sympy import isprime

PRIME_LENGTH = 511
NUM_USERS = 4

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
    print("---------- Generating parameters -----------")
    q,n = generate_safe_prime(PRIME_LENGTH)
    g = generate_g(q,n)
    print("q = ", q)
    print("n = ", n)
    print("g = ", g)
    state: list[tuple[int,int]] = [generate_keypair(g,n) for _ in range(NUM_USERS)]
    for _ in range(NUM_USERS-1):
        new_state: list[tuple[int, int]] = []
        for i in range(NUM_USERS):
            # secret number of that person
            secret_i = state[i][0]
            # public number from previous person
            received_package = state[i - 1][1]
            # X = g^x mod n
            new_package = pow(received_package, secret_i, n)
            new_state.append((secret_i, new_package))
        state = new_state
    print("Generated exchange keys:")
    for i in range(NUM_USERS):
        print(f"User {i}: {state[i][1]}")
    
    first_key = state[0][1]
    all_match = all(user_state[1] == first_key for user_state in state)

    if all_match:
        print("Success, whole group has the same key")
    else:
        print("Something gone wrong")




