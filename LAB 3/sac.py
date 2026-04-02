import hashlib
import secrets

n = 1000
sum_percentage = 0
if __name__ == "__main__":
    for i in range(n):
        random_string = secrets.token_bytes(4)
        original = bytearray(random_string)
        changed = original.copy()
        changed[-1] = changed[-1] ^ 1
        hash1 = hashlib.sha256(original).digest()
        hash2 = hashlib.sha256(changed).digest()
        x = int.from_bytes(hash1, 'big')
        y = int.from_bytes(hash2, 'big')
        bite_diff = (x ^ y).bit_count()
        percentage = bite_diff / 256
        sum_percentage += percentage
    print(f"Average bite diff = {(sum_percentage / n * 100):.2f}% of {n} random strings")