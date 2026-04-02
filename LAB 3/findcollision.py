import hashlib

if __name__ == "__main__":
    counter = 1
    found_hashes = {}
    while True:
        x = str(counter).encode("utf-8")
        output_hash = hashlib.sha256(x).hexdigest()
        output_hash = output_hash[:3]
        x = x.decode("utf-8")
        if output_hash in found_hashes:
            print("HASH ALGORITHM - sha256")
            print(f"Collision found in {x} iterations")
            print(f"Shared hash: {output_hash}")
            print(f"The first 12 bits of the hash are identical for '{x}' and '{found_hashes[output_hash]}'")
            break
        else:
            found_hashes[output_hash] = x
            counter += 1