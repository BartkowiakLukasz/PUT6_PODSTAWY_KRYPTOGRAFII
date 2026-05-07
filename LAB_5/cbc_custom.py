#!/usr/bin/env python3
"""
Lab 5 — Task 3
Custom CBC mode implementation using the ECB mode available in pycryptodome.

CBC (Cipher Block Chaining) algorithm:

  Encryption:                      Decryption:
  ┌──────────┐                     ┌──────────┐
  │ Plaintext│                     │Ciphertext│
  │  Block i │                     │  Block i │
  └────┬─────┘                     └────┬─────┘
       │                                │
       ▼                                ▼
  XOR ◄── C_{i-1} (or IV)        AES^{-1}(KEY)
       │                                │
       ▼                                ▼
  AES(KEY)                         XOR ◄── C_{i-1} (or IV)
       │                                │
       ▼                                ▼
  ┌──────────┐                     ┌──────────┐
  │Ciphertext│                     │ Plaintext│
  │  Block i │                     │  Block i │
  └──────────┘                     └──────────┘

  C_0 = IV
  C_i = AES_ECB(P_i XOR C_{i-1})
  P_i = AES_ECB^{-1}(C_i) XOR C_{i-1}
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BS = 16  # AES block size


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings of equal length."""
    return bytes(x ^ y for x, y in zip(a, b))


def cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    """
    Encrypt data in CBC mode implemented manually using AES-ECB.

    Args:
        key: 16/24/32-byte AES key
        iv: 16-byte initialization vector
        plaintext: data to encrypt (length must be a multiple of 16)

    Returns:
        Ciphertext (same length as plaintext)
    """
    assert len(plaintext) % BS == 0, "Plaintext length must be a multiple of 16!"
    assert len(iv) == BS, "IV must be 16 bytes!"

    ecb = AES.new(key, AES.MODE_ECB)
    ciphertext = b""
    prev = iv  # C_0 = IV

    for i in range(0, len(plaintext), BS):
        block = plaintext[i:i + BS]       # P_i
        xored = xor_bytes(block, prev)    # P_i XOR C_{i-1}
        encrypted = ecb.encrypt(xored)    # C_i = AES(P_i XOR C_{i-1})
        ciphertext += encrypted
        prev = encrypted                  # C_{i-1} for the next block

    return ciphertext


def cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypt data in CBC mode implemented manually using AES-ECB.

    Args:
        key: 16/24/32-byte AES key
        iv: 16-byte initialization vector
        ciphertext: encrypted data (length must be a multiple of 16)

    Returns:
        Decrypted plaintext
    """
    assert len(ciphertext) % BS == 0, "Ciphertext length must be a multiple of 16!"
    assert len(iv) == BS, "IV must be 16 bytes!"

    ecb = AES.new(key, AES.MODE_ECB)
    plaintext = b""
    prev = iv  # C_0 = IV

    for i in range(0, len(ciphertext), BS):
        block = ciphertext[i:i + BS]       # C_i
        decrypted = ecb.decrypt(block)     # AES^{-1}(C_i)
        plain = xor_bytes(decrypted, prev) # P_i = AES^{-1}(C_i) XOR C_{i-1}
        plaintext += plain
        prev = block                       # C_i becomes C_{i-1}

    return plaintext


# ═══════════════════════════ VERIFICATION ═══════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("CUSTOM CBC IMPLEMENTATION VERIFICATION")
    print("=" * 60)

    # Test 1: Short message (exactly 1 block)
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    msg = b"Hello, CBC mode!"  # exactly 16 bytes
    assert len(msg) == BS

    my_ct = cbc_encrypt(key, iv, msg)

    lib_enc = AES.new(key, AES.MODE_CBC, iv)
    lib_ct = lib_enc.encrypt(msg)

    assert my_ct == lib_ct, "ERROR: ciphertext does not match!"
    print(f"\nTest 1 (1 block):  PASS")
    print(f"  Plaintext:  {msg}")
    print(f"  My CT:      {my_ct.hex()}")
    print(f"  Lib CT:     {lib_ct.hex()}")

    # Decryption
    my_pt = cbc_decrypt(key, iv, my_ct)
    assert my_pt == msg, "ERROR: decryption does not match!"
    print(f"  Decrypted:  {my_pt}")

    # Test 2: Longer message (5 blocks)
    key2 = get_random_bytes(16)
    iv2 = get_random_bytes(16)
    msg2 = (b"BLOK1___16bajtow"
            b"BLOK2___16bajtow"
            b"BLOK3___16bajtow"
            b"BLOK4___16bajtow"
            b"BLOK5___16bajtow")

    my_ct2 = cbc_encrypt(key2, iv2, msg2)
    lib_ct2 = AES.new(key2, AES.MODE_CBC, iv2).encrypt(msg2)
    assert my_ct2 == lib_ct2, "ERROR: 5-block ciphertext does not match!"

    my_pt2 = cbc_decrypt(key2, iv2, my_ct2)
    assert my_pt2 == msg2, "ERROR: 5-block decryption does not match!"
    print(f"\nTest 2 (5 blocks): PASS")
    print(f"  Plaintext:  {msg2[:32]}...")
    print(f"  My CT:      {my_ct2[:32].hex()}...")
    print(f"  Decrypted:  {my_pt2[:32]}...")

    # Test 3: With PKCS7 padding (message not a multiple of 16)
    key3 = get_random_bytes(16)
    iv3 = get_random_bytes(16)
    msg3 = b"A message of arbitrary length!!"  # 31 bytes
    msg3_padded = pad(msg3, BS)  # PKCS7 padding → 32 bytes

    my_ct3 = cbc_encrypt(key3, iv3, msg3_padded)
    lib_ct3 = AES.new(key3, AES.MODE_CBC, iv3).encrypt(msg3_padded)
    assert my_ct3 == lib_ct3

    my_pt3 = unpad(cbc_decrypt(key3, iv3, my_ct3), BS)
    assert my_pt3 == msg3
    print(f"\nTest 3 (with padding): PASS")
    print(f"  Plaintext:    {msg3} ({len(msg3)} B)")
    print(f"  After padding: {len(msg3_padded)} B")
    print(f"  Decrypted:    {my_pt3}")

    # Test 4: Random data (1 KB)
    key4 = get_random_bytes(16)
    iv4 = get_random_bytes(16)
    msg4 = get_random_bytes(1024)

    my_ct4 = cbc_encrypt(key4, iv4, msg4)
    lib_ct4 = AES.new(key4, AES.MODE_CBC, iv4).encrypt(msg4)
    assert my_ct4 == lib_ct4

    my_pt4 = cbc_decrypt(key4, iv4, my_ct4)
    assert my_pt4 == msg4
    print(f"\nTest 4 (1 KB random data): PASS")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("Custom CBC implementation produces identical results")
    print("to AES.MODE_CBC from the pycryptodome library.")
    print("=" * 60)
