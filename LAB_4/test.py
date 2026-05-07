import hashlib
import time
import statistics
import matplotlib.pyplot as plt
import numpy as np
HASHES = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']

SIZES = {
    "10 KB": 10 * 1024,
    "100 KB": 100 * 1024,
    "1 MB": 1 * 1024 * 1024,
    "10 MB": 10 * 1024 * 1024,
}

def hash_speed_test(algorithms, sizes, iterations=50):
    dummy_payload = b"A" * 1024 * 1024  # 1 MB
    for _ in range(50):
        hashlib.md5(dummy_payload).digest()

    results = {}
    for algo in algorithms:
        results[algo] = {}
        for size_label, size_bytes in sizes.items():
            results[algo][size_label] = {'times': []}
            payload = b"A" * size_bytes

            for _ in range(iterations):
                start_time = time.perf_counter()
                hashlib.new(algo, payload).digest()
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                results[algo][size_label]['times'].append(elapsed_time)

            results[algo][size_label]['mean'] = statistics.mean(results[algo][size_label]['times'])
            payload_size_mb = size_bytes / (1024 * 1024)
            if results[algo][size_label]['mean'] > 0:
                results[algo][size_label]['throughput_mbps'] = payload_size_mb / results[algo][size_label]['mean']
            else:
                results[algo][size_label]['throughput_mbps'] = 0

    return results

def plot_results(results, algorithms, sizes):
    """
    Plots the hashing speed comparison results.

    Args:
        results (dict): The results from hash_speed_test().
        algorithms (list): List of algorithms.
        sizes (dict): Dict of sizes.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(sizes))
    width = 0.8 / len(algorithms)
    positions = np.arange(len(sizes))

    for i, algo in enumerate(algorithms):
        y = [results[algo][size_label]['throughput_mbps'] for size_label in sizes]
        ax.bar(positions + i * width, y, width, label=algo, alpha=0.7)

    ax.set_xlabel('Payload Size')
    ax.set_ylabel('Throughput (MB/s)')
    ax.set_title('Hashing Speed Comparison')
    ax.set_xticks(positions + width * (len(algorithms) - 1) / 2)
    ax.set_xticklabels(sizes.keys())
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    fig.tight_layout()
    plt.savefig("hash_speed_comparison.png")
    plt.show()

if __name__ == "__main__":
    results = hash_speed_test(HASHES, SIZES)
    plot_results(results, HASHES, SIZES)
