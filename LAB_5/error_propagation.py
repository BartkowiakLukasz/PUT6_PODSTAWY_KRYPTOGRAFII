#!/usr/bin/env python3
"""
Lab 5 — Task 2
Error propagation analysis in 5 AES-128 block cipher modes.

Scenario:
  1. Encrypt a message consisting of 5 blocks (80 bytes) in each mode.
  2. Introduce a 1-bit error in the 2nd ciphertext block (bit flip).
  3. Decrypt the corrupted ciphertext.
  4. Compare with the original — visualize which blocks/bits are damaged.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY = get_random_bytes(16)
IV = get_random_bytes(16)
BS = 16  # AES block size in bytes
NB = 5   # number of blocks
PLAINTEXT = (b"BLOK1___16bajtow"
             b"BLOK2___16bajtow"
             b"BLOK3___16bajtow"
             b"BLOK4___16bajtow"
             b"BLOK5___16bajtow")
assert len(PLAINTEXT) == NB * BS

ERR_BYTE = BS + 3  # byte 19 (4th byte of block 2)

MODES = {"ECB": AES.MODE_ECB, "CBC": AES.MODE_CBC,
         "OFB": AES.MODE_OFB, "CFB": AES.MODE_CFB, "CTR": AES.MODE_CTR}


def mk(name, mid, nonce=None):
    """Create an AES cipher for the given mode."""
    if name == "ECB": return AES.new(KEY, mid)
    if name == "CTR": return AES.new(KEY, mid, nonce=nonce or get_random_bytes(8))
    if name == "CFB": return AES.new(KEY, mid, IV, segment_size=128)
    return AES.new(KEY, mid, IV)


def flip(data, idx, bit=0):
    """Flip a single bit in the data at the given byte index."""
    a = bytearray(data); a[idx] ^= (1 << bit); return bytes(a)


def diff_bits(a, b):
    """Count the number of differing bits between two byte strings."""
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


# ──────── Analysis ────────

all_res = {}
print("=" * 70)
print("ERROR PROPAGATION — 1-bit flip in ciphertext block 2")
print("=" * 70)

for name, mid in MODES.items():
    enc = mk(name, mid)
    nonce = getattr(enc, "nonce", None)
    ct = enc.encrypt(PLAINTEXT)

    ct_bad = flip(ct, ERR_BYTE)

    dec_ok = mk(name, mid, nonce)
    assert dec_ok.decrypt(ct) == PLAINTEXT

    dec_bad = mk(name, mid, nonce)
    pt_bad = dec_bad.decrypt(ct_bad)

    blocks = []
    for i in range(NB):
        s, e = i * BS, (i + 1) * BS
        d = diff_bits(PLAINTEXT[s:e], pt_bad[s:e])
        blocks.append({"block": i + 1, "diff": d, "bad": d > 0})
    all_res[name] = blocks

    dmg = [str(b["block"]) for b in blocks if b["bad"]]
    tot = sum(b["diff"] for b in blocks)
    print(f"\n{name:4s}: damaged blocks={','.join(dmg) or '-'}  "
          f"changed bits={tot}")
    for b in blocks:
        st = f"X {b['diff']:3d}b" if b["bad"] else "  OK"
        print(f"       Block {b['block']}: {st}")

# ──────── Summary table ────────

desc = {"ECB": "Entire block 2 randomized; rest OK",
        "CBC": "Block 2 randomized + 1 bit in block 3",
        "OFB": "Only 1 bit in block 2 (stream cipher)",
        "CFB": "1 bit in block 2 + block 3 randomized",
        "CTR": "Only 1 bit in block 2 (stream cipher)"}

print("\n" + "=" * 70)
print(f"{'Mode':<6}{'Damaged':<15}{'Bits':<10}{'Description'}")
print("-" * 70)
for name, bks in all_res.items():
    dmg = [str(b["block"]) for b in bks if b["bad"]]
    tot = sum(b["diff"] for b in bks)
    print(f"{name:<6}{','.join(dmg) or '-':<15}{tot:<10}{desc[name]}")

# ──────── Visualization ────────

fig, axes = plt.subplots(len(MODES), 1, figsize=(10, 8), sharex=True)
COL = {True: "#e74c3c", False: "#2ecc71"}

for ax, (name, bks) in zip(axes, all_res.items()):
    for b in bks:
        c = COL[b["bad"]]
        r = mpatches.FancyBboxPatch((b["block"] - 0.4, 0.1), 0.8, 0.8,
            boxstyle="round,pad=0.05", facecolor=c, edgecolor="white", lw=2)
        ax.add_patch(r)
        lb = f'{b["diff"]}b' if b["bad"] else "OK"
        ax.text(b["block"], 0.5, lb, ha="center", va="center",
                fontsize=11, fontweight="bold", color="white")
    ax.set_xlim(0.3, NB + 0.7); ax.set_ylim(0, 1)
    ax.set_ylabel(name, fontsize=12, fontweight="bold", rotation=0,
                  labelpad=40, va="center")
    ax.set_yticks([]); ax.set_xticks(range(1, NB + 1))
    ax.set_xticklabels([f"Block {i}" for i in range(1, NB + 1)])
    ax.set_facecolor("#f8f9fa")

axes[-1].set_xlabel("Plaintext blocks after decryption", fontsize=12)
fig.suptitle("1-bit error propagation in ciphertext (block 2)\n"
             "GREEN = OK  |  RED = damaged (bit count)",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("propagacja_bledow.png", dpi=150, bbox_inches="tight")
print(f"\n✅ Chart saved as: propagacja_bledow.png")

# ──────── Interpretation ────────
#
# ECB: Each block is encrypted/decrypted independently.
#      An error in one ciphertext block randomizes ONLY that block (~64 bits
#      changed, ~50% of the 128-bit block). All other blocks are untouched.
#
# CBC: Decrypting block N requires AES^{-1}(C_N) XOR C_{N-1}. Therefore:
#      - The corrupted block (2) → entirely randomized (~63 bits)
#      - The next block (3) → only 1 bit changed (XOR with corrupted block)
#      - All further blocks → untouched.
#
# OFB: The keystream is generated INDEPENDENTLY of the ciphertext (depends
#      only on key and IV). Ciphertext is XOR'd with the keystream.
#      Flipping 1 bit in ciphertext → exactly 1 bit flipped in plaintext.
#
# CFB: With segment_size=128: the keystream for block N+1 depends on the
#      ciphertext of block N. Therefore:
#      - Block 2 → only 1 bit changed (direct XOR)
#      - Block 3 → randomized (~68 bits, because the keystream was generated
#        from the corrupted ciphertext block)
#      - All further blocks → untouched.
#
# CTR: The keystream is generated from a counter (nonce + counter), INDEPENDENTLY
#      of the ciphertext. Like OFB: 1 bit changed in ciphertext = 1 bit changed
#      in plaintext. Most resilient to error propagation.
#
# CONCLUSION:
# - Stream-like modes (OFB, CTR) → minimal propagation (1 bit → 1 bit).
# - CBC, CFB → limited propagation (affects 1-2 blocks).
# - ECB → propagation limited to the corrupted block, but the entire block is randomized.
# - NONE of the modes causes the ENTIRE message to become unreadable.
