#!/usr/bin/env python3

import time
import matplotlib.pyplot as plt
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# ──────────────────────────────── Configuration ─────────────────────────────

KEY = get_random_bytes(16)          # 128-bit AES key
FILE_SIZES_MB = [100, 1000, 3000]   # Test file sizes [MB]
CHUNK_SIZE = 1024 * 1024            # 1 MB — single chunk size

MODES = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC,
    "OFB": AES.MODE_OFB,
    "CFB": AES.MODE_CFB,
    "CTR": AES.MODE_CTR,
}

# ─────────────────────────── Helper functions ───────────────────────────────


def _create_cipher(mode_name: str, mode_id: int, iv: bytes) -> AES:
    """Create an AES cipher object with the appropriate parameters for the given mode."""
    if mode_name == "ECB":
        return AES.new(KEY, mode_id)
    if mode_name == "CTR":
        return AES.new(KEY, mode_id, nonce=get_random_bytes(8))
    if mode_name == "CFB":
        return AES.new(KEY, mode_id, iv, segment_size=128)
    # CBC, OFB
    return AES.new(KEY, mode_id, iv)


def warmup(mode_name: str, mode_id: int, rounds: int = 3) -> None:
    for _ in range(rounds):
        iv = get_random_bytes(16)
        c = _create_cipher(mode_name, mode_id, iv)
        c.encrypt(get_random_bytes(CHUNK_SIZE))


def benchmark(size_mb: int, mode_name: str, mode_id: int) -> tuple[float, float]:
    warmup(mode_name, mode_id)

    iv = get_random_bytes(16)

    # --- Cipher initialization ---
    cipher_enc = _create_cipher(mode_name, mode_id, iv)
    # For CTR we need the same nonce
    if mode_name == "CTR":
        cipher_dec = AES.new(KEY, mode_id, nonce=cipher_enc.nonce)
    elif mode_name == "ECB":
        cipher_dec = AES.new(KEY, mode_id)
    elif mode_name == "CFB":
        cipher_dec = AES.new(KEY, mode_id, iv, segment_size=128)
    else:
        cipher_dec = AES.new(KEY, mode_id, iv)

    chunk = get_random_bytes(CHUNK_SIZE)  # 1 MB of random data

    # --- Encryption ---
    t0 = time.perf_counter()
    for _ in range(size_mb):
        cipher_enc.encrypt(chunk)
    t_enc = time.perf_counter() - t0

    # --- Decryption ---
    t0 = time.perf_counter()
    for _ in range(size_mb):
        cipher_dec.decrypt(chunk)
    t_dec = time.perf_counter() - t0

    return t_enc, t_dec


# ──────────────────────────────── Benchmarks ─────────────────────────────────

results = []

for size in FILE_SIZES_MB:
    print(f"▶ Testing file size {size} MB ...")
    for name, mode_id in MODES.items():
        t_enc, t_dec = benchmark(size, name, mode_id)
        throughput_enc = size / t_enc  # MB/s
        throughput_dec = size / t_dec
        results.append({
            "Mode": name,
            "Size [MB]": size,
            "Encryption [s]": round(t_enc, 3),
            "Decryption [s]": round(t_dec, 3),
            "Enc throughput [MB/s]": round(throughput_enc, 1),
            "Dec throughput [MB/s]": round(throughput_dec, 1),
        })
        print(f"   {name:4s}  enc={t_enc:.3f}s  dec={t_dec:.3f}s  "
              f"({throughput_enc:.0f} / {throughput_dec:.0f} MB/s)")

# ─────────────────────────── Results table ───────────────────────────────────

df = pd.DataFrame(results)
print("\n" + "=" * 80)
print(df.to_string(index=False))
print("=" * 80)

# ──────────────────────────── Charts ─────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

for ax, col, title in [
    (axes[0], "Encryption [s]", "Encryption time"),
    (axes[1], "Decryption [s]", "Decryption time"),
]:
    pivot = df.pivot(index="Size [MB]", columns="Mode", values=col)
    pivot = pivot.reindex(FILE_SIZES_MB)
    pivot = pivot[["ECB", "CBC", "OFB", "CFB", "CTR"]]  # fixed order
    pivot.plot(kind="bar", ax=ax, rot=0, width=0.75)

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("Time [s]")
    ax.set_xlabel("File size [MB]")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(title="Mode")

fig.suptitle(
    "AES-128 encryption and decryption time comparison across block cipher modes",
    fontsize=15,
    fontweight="bold",
    y=1.02,
)
plt.tight_layout()
plt.savefig("wykres_wynikow.png", dpi=150, bbox_inches="tight")
print("\n✅ Chart saved as: wykres_wynikow.png")

# ───────────────────────── Interpretation ────────────────────────────────────
#
# ECB — Fastest mode because each block is encrypted/decrypted independently
#        (no dependency on previous blocks). Easy to parallelize.
#        BUT: very insecure! Identical plaintext blocks produce identical
#        ciphertext blocks -> pattern leakage.
#
# CBC — Slightly slower than ECB because encryption is sequential (each block
#        depends on the previous ciphertext). Decryption, however, can be
#        parallelized since it only requires reading the previous ciphertext block.
#
# OFB — Generates a keystream independently of plaintext. Time is similar
#        to CBC/CFB. Encryption and decryption are the same operation.
#
# CFB — With segment_size=128, it behaves similarly to CBC. With the default
#        segment_size=8, it would be much slower (128x more AES calls).
#
# CTR — Counter mode. Often the fastest alongside ECB because the keystream
#        is generated independently of the data — easy to parallelize both
#        encryption and decryption.
#
# General observation: times scale linearly with file size, confirming
# that the computational complexity is O(n) for all modes.