# SHA-256 Script Documentation

## Overview

This script implements the SHA-256 (Secure Hash Algorithm 256-bit) cryptographic hash function. It provides functionality to compute SHA-256 hashes for strings and files, as well as a benchmarking feature to measure performance.

## Features

1. Compute SHA-256 hash for input strings
2. Compute SHA-256 hash for file contents
3. Benchmark SHA-256 computation performance

## Usage

The script can be run from the command line with the following syntax:

```
python sha256_script.py <mode> [input]
```

### Modes

1. `hash`: Compute the SHA-256 hash of a given string
2. `file`: Compute the SHA-256 hash of a file's contents
3. `benchmark`: Measure the average execution time of the SHA-256 function

### Examples

1. Hash a string:
   ```
   python sha256_script.py hash "Hello, World!"
   ```

2. Hash a file:
   ```
   python sha256_script.py file path/to/your/file.txt
   ```

3. Run benchmark:
   ```
   python sha256_script.py benchmark
   ```

## Implementation Details

### Main Components

1. `sha256(message: str) -> str`: Core function that computes the SHA-256 hash of a given message.
2. `compress(chunk: bytes) -> None`: Internal function used by `sha256()` to process 64-byte chunks of the message.
3. `rotr(x: int, n: int) -> int`: Utility function to perform right rotation on 32-bit integers.
4. `benchmark(func: Callable, *args, iterations: int = 1000) -> float`: Function to measure the average execution time of a given function.
5. `main() -> None`: Entry point of the script, handles command-line arguments and executes the appropriate mode.

### SHA-256 Algorithm Implementation

The `sha256()` function implements the SHA-256 algorithm as follows:

1. Pad the input message to ensure its length is a multiple of 512 bits.
2. Split the padded message into 64-byte (512-bit) chunks.
3. For each chunk:
   a. Prepare the message schedule (expand the chunk into 64 32-bit words).
   b. Initialize the eight working variables with the current hash value.
   c. Perform the main hash computation loop (64 rounds).
   d. Compute the new hash value by adding the compressed chunk to the previous hash value.
4. Produce the final hash by concatenating the resulting eight 32-bit words.

## Performance Considerations

- The script uses bitwise operations and modular arithmetic to ensure efficient computation.
- The `benchmark()` function can be used to measure and compare the performance of the SHA-256 implementation across different systems or after code modifications.

## Limitations and Potential Improvements

- The current implementation reads entire files into memory, which may not be suitable for very large files. A streaming approach could be implemented for better memory efficiency.
- The script currently handles Unicode strings by encoding them as UTF-8. This behavior might not be suitable for all use cases and could be made configurable.
- Error handling could be improved, especially for file operations and invalid inputs.
- The implementation is not optimized for parallel processing. For better performance on multi-core systems, parallel processing of independent chunks could be considered.

## Security Considerations

- This implementation is for educational and non-critical use only. For security-sensitive applications, it is recommended to use well-vetted cryptographic libraries.
- The script does not implement any protection against timing attacks or other side-channel attacks.

## Dependencies

The script uses only Python standard library modules:

- `sys`: For command-line argument handling
- `time`: For performance benchmarking
- `typing`: For type hinting (Python 3.5+)

