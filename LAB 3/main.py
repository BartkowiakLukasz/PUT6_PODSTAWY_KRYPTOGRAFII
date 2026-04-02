import hashlib
import time
if __name__ == "__main__":
   #print(hashlib.algorithms_available())
    HASHES = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']
    results = []
    print(HASHES)
    txt = "Kot".encode('utf-8')
    for name in HASHES:
       start = time.perf_counter()
       algorithm = hashlib.new(name)
       algorithm.update(txt)
       algorithm_hex = algorithm.hexdigest()
       end = time.perf_counter()
       total_time = (end - start) * 10**6
       print(f"HASH of {name}: {algorithm_hex}")
       print(f"Total time: {total_time} mu, len = {len(algorithm_hex)}")
       results.append((name, total_time, len(algorithm_hex))) 
    fastest = min(results, key= lambda x: x[1])
    print(f"The fastest algorithm: {fastest[0]}, {fastest[1]} mu")
    slowest = max(results, key = lambda x : x[1])
    print(f"The slowest algorithm: {slowest[0]}, {slowest[1]} mu")
    shortest = min(results, key = lambda x : x[2])
    print(f"The shortest output: {shortest[0]}, {shortest[2]}")
    longest = max(results, key = lambda x : x[2])
    print(f"The longest output: {longest[0]}, {longest[2]}")
    