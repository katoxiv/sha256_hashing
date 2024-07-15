import sys
import time
from typing import List, Callable

# SHA-256 constants
K: List[int] = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Initial hash values
H: List[int] = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

def rotr(x: int, n: int) -> int:
    """Perform a right rotation on a 32-bit integer."""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def sha256(message: str) -> str:
    """Compute the SHA-256 hash of a given message."""
    def compress(chunk: bytes) -> None:
        """Compress a 64-byte chunk and update the hash state."""
        w = [int.from_bytes(chunk[i:i+4], 'big') for i in range(0, 64, 4)] + [0] * 48

        for i in range(16, 64):
            s0 = rotr(w[i-15], 7) ^ rotr(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = rotr(w[i-2], 17) ^ rotr(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = H

        for i in range(64):
            S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF
            S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h, g, f, e, d, c, b, a = g, f, e, (d + temp1) & 0xFFFFFFFF, c, b, a, (temp1 + temp2) & 0xFFFFFFFF

        H[:] = [(x + y) & 0xFFFFFFFF for x, y in zip(H, [a, b, c, d, e, f, g, h])]

    message_bytes = bytearray(message.encode('utf-8'))
    length = len(message_bytes) * 8
    message_bytes.append(0x80)
    message_bytes.extend(b'\x00' * ((56 - len(message_bytes) % 64) % 64))
    message_bytes.extend(length.to_bytes(8, 'big'))

    for i in range(0, len(message_bytes), 64):
        compress(message_bytes[i:i+64])

    return ''.join(f'{h:08x}' for h in H)

def benchmark(func: Callable, *args, iterations: int = 1000) -> float:
    """Benchmark a function by running it multiple times and calculating the average execution time."""
    start_time = time.time()
    for _ in range(iterations):
        func(*args)
    end_time = time.time()
    return (end_time - start_time) / iterations

def main() -> None:
    """Main function to handle command-line arguments and execute the appropriate mode."""
    if len(sys.argv) < 2:
        print("Usage: python sha256_script.py <mode> [input]")
        print("Modes: hash, file, benchmark")
        return

    mode = sys.argv[1]

    if mode == "hash":
        if len(sys.argv) != 3:
            print("Usage for hash mode: python sha256_script.py hash <string_to_hash>")
            return
        input_string = sys.argv[2]
        hash_result = sha256(input_string)
        print(f"SHA-256 hash of '{input_string}': {hash_result}")

    elif mode == "file":
        if len(sys.argv) != 3:
            print("Usage for file mode: python sha256_script.py file <path_to_file>")
            return
        file_path = sys.argv[2]
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
            hash_result = sha256(content.decode('utf-8', errors='ignore'))
            print(f"SHA-256 hash of file '{file_path}': {hash_result}")
        except IOError as e:
            print(f"Error reading file: {e}")

    elif mode == "benchmark":
        test_string = "Hello, World!" * 1000
        avg_time = benchmark(sha256, test_string)
        print(f"Average time for SHA-256 computation: {avg_time:.6f} seconds")

    else:
        print("Invalid mode. Choose 'hash', 'file', or 'benchmark'.")

if __name__ == "__main__":
    main()