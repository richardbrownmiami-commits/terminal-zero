import hashlib, time, struct, os

def randomx_simulate(seed: bytes, input_data: bytes) -> bytes:
    # Step 1: Blake2b key derivation
    key = hashlib.blake2b(seed, digest_size=32).digest()
    # Step 2: Initialize 64-byte state
    state = bytearray(hashlib.blake2b(input_data, key=key, digest_size=64).digest())
    # Step 3: 64 iterations of XOR + rotation (simulating RandomX program execution)
    for i in range(64):
        rot = i % 8
        for j in range(64):
            state[j] ^= state[(j + i) % 64]
            state[j] = ((state[j] << rot) | (state[j] >> (8 - rot))) & 0xFF
    # Step 4: Final Blake2b hash
    return hashlib.blake2b(bytes(state), digest_size=32).digest()

seed = b"RandomX seed 2026"
test_input = os.urandom(76)  # 76-byte block header like Bitcoin

# Single hash
result = randomx_simulate(seed, test_input)
print(f"Input (hex):  {test_input.hex()[:32]}...")
print(f"Output hash:  {result.hex()}")

# Benchmark
count = 0
start = time.time()
while time.time() - start < 2.0:
    randomx_simulate(seed, os.urandom(76))
    count += 1
elapsed = time.time() - start
print(f"Benchmark: {count} hashes in {elapsed:.2f}s = {count/elapsed:.1f} H/s")
print(f"Note: Real RandomX uses AES-NI + 2MB scratchpad; this is a simulation")
