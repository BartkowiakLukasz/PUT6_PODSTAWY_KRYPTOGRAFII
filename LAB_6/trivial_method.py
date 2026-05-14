import secrets

def trivial_secret_sharing(s, n, k):
    print(f"--- SHARING PHASE ---")
    print(f"Secret: {s}, Number of shares (n): {n}, Space (k): {k}")
    
    shares = []
    random_sum = 0
    
    # 1. Randomly select n-1 values belonging to the set <0; k-1>
    for i in range(n - 1):
        random_share = secrets.randbelow(k)
        shares.append(random_share)
        random_sum += random_share
        print(f"Generated share {i+1}: {random_share}")
        
    # 2. Determine the n-th share: s_n = (s - s_1 - s_2 - ... - s_{n-1}) mod k
    last_share = (s - random_sum) % k
    shares.append(last_share)
    print(f"Calculated share {n}: {last_share}")
    
    return shares

def trivial_secret_reconstruction(shares, k):
    print(f"\n--- RECONSTRUCTION PHASE ---")
    
    shares_sum = sum(shares)
    secret = shares_sum % k
    
    print(f"Gathered shares: {shares}")
    print(f"Sum of shares: {shares_sum}")
    print(f"Reconstructed secret ({shares_sum} mod {k}): {secret}")
    
    return secret

# --- EXECUTION PRESENTATION ---
k = 1000  # number space size 
s = 123   # secret in range 0 to k-1
n = 5     # total number of shares

generated_shares = trivial_secret_sharing(s, n, k)
reconstructed = trivial_secret_reconstruction(generated_shares, k)

# wady
# brak odpornosci na awarie - utrata 1 udzialu uniemozliwia uzyskanie sekretu
# bezpieczenstwo - Jeśli n-1 osób zmówi się, mogą one bardzo łatwo zawęzić pole poszukiwań sekretu do jednej niewiadomej.
# k musi byc wzglednie duze aby uniknac odgadniecia sekretu metoda brute-force
# nie pozwala na ustalenie progu wymaganych udzialow