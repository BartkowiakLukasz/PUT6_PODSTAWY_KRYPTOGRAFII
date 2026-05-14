import secrets

def shamir_share(s, n, t, p):
    print("--- SHARING PHASE (Shamir) ---")
    print(f"Secret (s): {s}, Shares (n): {n}, Threshold (t): {t}, Prime (p): {p}")
    
    if not (p > s and p > n):
        raise ValueError("Prime p must be greater than both s and n!")
        
    # 2. Randomly select t-1 numbers a_1, a_2, ..., a_{t-1}
    # a_0 is our secret s
    coefficients = [s] + [secrets.randbelow(p - 1) + 1 for _ in range(t - 1)]
    
    polynomial_str = f"{s}"
    for i in range(1, t):
        polynomial_str += f" + {coefficients[i]}*x^{i}"
    print(f"Generated polynomial f(x): {polynomial_str} (mod {p})")
    
    shares = []
    for x in range(1, n + 1):
        y = sum((coefficients[j] * (x ** j)) for j in range(t)) % p
        shares.append((x, y)) # (i, s_i)
        print(f"Generated share for x={x}: (x={x}, y={y})")
        
    return shares

def shamir_reconstruct(shares_t, p):
    print("\n--- RECONSTRUCTION PHASE (Shamir) ---")
    print(f"Shares used for reconstruction: {shares_t}")
    
    secret = 0
    t = len(shares_t)
    
    for i in range(t):
        xi, yi = shares_t[i]
        
        numerator = 1
        denominator = 1
        
        for j in range(t):
            if i != j:
                xj, yj = shares_t[j]
                numerator = (numerator * (-xj)) % p
                denominator = (denominator * (xi - xj)) % p
                
        denominator_inverse = pow(denominator, -1, p)
        
        l_i = (yi * numerator * denominator_inverse) % p
        secret = (secret + l_i) % p
        
    print(f"Reconstructed secret: {secret}")
    return secret

total_shares = 6   # n
threshold = 3      # t
secret_value = 42  # s [0, p-1]
prime_number = 101 # p ( p > s v p > n )

generated_shares = shamir_share(
    secret_value, 
    total_shares, 
    threshold, 
    prime_number
)

secure_random = secrets.SystemRandom()
selected_shares = secure_random.sample(generated_shares, threshold)

reconstructed_shamir = shamir_reconstruct(selected_shares, prime_number)

#wady
# zlozonosc obliczeniowa
# Konieczne jest wygenerowanie dużej, losowej liczby pierwszej p spełniającej warunek p > s oraz p > n
# Ryzyko "oszusta": Bez dodatkowych mechanizmów weryfikacji,
# jeden uczestnik może podać błędny udział i uniemożliwić poprawne odtworzenie sekretu przez grupę.