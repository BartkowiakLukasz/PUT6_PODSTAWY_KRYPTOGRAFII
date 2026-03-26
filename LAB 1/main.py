import secrets
import math
from sympy import isprime

DEFAULT_PRIME_BIT_LENGTH = 512

def generate_large_prime_3_mod_4(bit_length: int) -> int:
    while True:
        candidate = secrets.randbits(bit_length)
        
        # Ensure the number is exactly 'bit_length' bits long (set MSB)
        # and ensure it is odd (set LSB)
        candidate |= (1 << (bit_length - 1)) | 1
        
        if candidate % 4 == 3:
            if isprime(candidate):
                return candidate

def generate_bbs(num_bits: int, prime_bit_length: int = DEFAULT_PRIME_BIT_LENGTH) -> tuple[list[int], int, int, int, int]:
    p = generate_large_prime_3_mod_4(prime_bit_length)
    q = generate_large_prime_3_mod_4(prime_bit_length)
    while (p == q):
        q = generate_large_prime_3_mod_4(prime_bit_length)
    N = p * q
    
    # gcd(x, N) == 1
    x = secrets.randbelow(N - 2) + 2
    while math.gcd(x, N) != 1:
        x = secrets.randbelow(N - 2) + 2
        
    # x0 - initial value
    x_curr = pow(x, 2, N)
    
    bits = []
    
    for _ in range(num_bits):
        # x_{i+1} = x_i^2 mod N
        x_curr = pow(x_curr, 2, N)
        
        # The output bit (LSB)
        bit = x_curr & 1
        bits.append(bit)
        
    return bits, N, p, q, x


def monobit_test(bits: list[int]) -> bool:
    """
    FIPS 140-2 Monobit Test.
    Counts the number of 1s in the 20,000-bit sequence.
    Passed if the count is between 9,725 and 10,275.
    """
    count_ones = sum(bits)
    passed = 9725 < count_ones < 10275
    
    print("--- Monobit Test ---")
    print(f"Number of 1s: {count_ones}")
    print(f"Result: {'PASSED' if passed else 'FAILED'}\n")
    return passed

def poker_test(bits: list[int]) -> bool:
    """
    FIPS 140-2 Poker Test.
    Divides the sequence into 5,000 contiguous 4-bit segments.
    Counts the occurrences of each of the 16 possible 4-bit values.
    Calculates the X statistic. Passed if 2.16 < X < 46.17.
    """
    frequencies = {i: 0 for i in range(16)}
    
    for i in range(0, len(bits), 4):
        chunk = bits[i:i+4]
        # Convert list of 4 bits to an integer (0-15)
        val = (chunk[0] << 3) | (chunk[1] << 2) | (chunk[2] << 1) | chunk[3]
        frequencies[val] += 1
        
    sum_sq = sum(f ** 2 for f in frequencies.values())
    
    # X = (16 / 5000) * sum(f^2) - 5000
    x_statistic = (16.0 / 5000.0) * sum_sq - 5000.0
    passed = 2.16 < x_statistic < 46.17
    
    print("--- Poker Test ---")
    print(f"X Statistic: {x_statistic:.4f}")
    print(f"Result: {'PASSED' if passed else 'FAILED'}\n")
    return passed

def runs_test(bits: list[int]) -> bool:
    """
    FIPS 140-2 Runs Test.
    Counts the number of runs (consecutive identical bits) of lengths 1 to 6+.
    Checks if the counts fall within the required intervals.
    """
    # Required intervals for runs of length 1, 2, 3, 4, 5, and 6+
    intervals = {
        1: (2315, 2685),
        2: (1114, 1386),
        3: (527, 723),
        4: (240, 384),
        5: (103, 209),
        6: (103, 209) # 6 and greater
    }
    
    # Dictionaries to count runs of 0s and 1s
    runs_0 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    runs_1 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    
    current_run_len = 1
    for i in range(1, len(bits)):
        if bits[i] == bits[i-1]:
            current_run_len += 1
        else:
            length_key = min(current_run_len, 6)
            if bits[i-1] == 0:
                runs_0[length_key] += 1
            else:
                runs_1[length_key] += 1
            current_run_len = 1
            
    # Count the very last run
    length_key = min(current_run_len, 6)
    if bits[-1] == 0:
        runs_0[length_key] += 1
    else:
        runs_1[length_key] += 1

    passed = True
    print("--- Runs Test ---")
    for length in range(1, 7):
        min_val, max_val = intervals[length]
        label = str(length) if length < 6 else "6+"
        
        pass_0 = min_val < runs_0[length] < max_val
        pass_1 = min_val < runs_1[length] < max_val
        
        print(f"Length {label}: 0s={runs_0[length]}, 1s={runs_1[length]} | Required: ({min_val}, {max_val})")
        if not (pass_0 and pass_1):
            passed = False
            
    print(f"Result: {'PASSED' if passed else 'FAILED'}\n")
    return passed

def long_run_test(bits: list[int]) -> bool:
    """
    FIPS 140-2 Long Run Test.
    Checks if there are any runs of length 26 or more.
    Passed if no such run exists.
    """
    max_run = 0
    current_run_len = 1
    
    for i in range(1, len(bits)):
        if bits[i] == bits[i-1]:
            current_run_len += 1
            if current_run_len > max_run:
                max_run = current_run_len
        else:
            current_run_len = 1
            
    passed = max_run < 26
    
    print("--- Long Run Test ---")
    print(f"Longest run length: {max_run}")
    print(f"Result: {'PASSED' if passed else 'FAILED'}\n")
    return passed

def run_all_tests(bits):
    print("========================================")
    print("     FIPS 140-2 RANDOMNESS TESTS")
    print("========================================\n")
    
    if len(bits) != 20000:
        print(f"WARNING: The FIPS 140-2 tests require exactly 20,000 bits. Provided sequence has {len(bits)} bits.\n")
        
    t1 = monobit_test(bits)
    t2 = poker_test(bits)
    t3 = runs_test(bits)
    t4 = long_run_test(bits)
    
    all_passed = t1 and t2 and t3 and t4
    print("========================================")
    print(f"OVERALL RESULT: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("========================================")

if __name__ == "__main__":
    num_bits_to_generate = 20000
    
    print("Generating sequence, please wait (this might take a few seconds due to large primes)...\n")
    generated_bits, n_val, p_val, q_val, x_val = generate_bbs(num_bits_to_generate, DEFAULT_PRIME_BIT_LENGTH)

    print(f"Generated prime numbers: \np = {p_val} \nq = {q_val}\n")
    print(f"Blum integer (N = p*q): N = {n_val}\n")
    print(f"Random seed (x): x = {x_val}")
    print(f"(Is it coprime with N? {'Yes' if math.gcd(x_val, n_val) == 1 else 'No'})\n")
    print(f"Generated a sequence of {len(generated_bits)} bits.")
    print(f"First 50 bits of the sequence: {''.join(map(str, generated_bits[:50]))}\n")
    
    run_all_tests(generated_bits)