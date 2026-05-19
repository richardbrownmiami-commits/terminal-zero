#!/usr/bin/env python3
"""SHA-3/Keccak-256 from scratch -- pure Python. Full permutation, test vectors."""
import hashlib

RC = [
    0x0000000000000001,0x0000000000008082,0x800000000000808A,0x8000000080008000,
    0x000000000000808B,0x0000000080000001,0x8000000080008081,0x8000000000008009,
    0x000000000000008A,0x0000000000000088,0x0000000080008009,0x000000008000000A,
    0x000000008000808B,0x800000000000008B,0x8000000000008089,0x8000000000008003,
    0x8000000000008002,0x8000000000000080,0x000000000000800A,0x800000008000000A,
    0x8000000080008081,0x8000000000008080,0x0000000080000001,0x8000000080008008,
]
RHO = [1,3,6,10,15,21,28,36,45,55,2,14,27,41,56,8,25,43,62,18,39,61,20,44]
PI  = [10,7,11,17,18,3,5,16,8,21,24,4,15,23,19,13,12,2,20,14,22,9,6,1]

def rotl64(x, n):
    return ((x << n) | (x >> (64-n))) & 0xFFFFFFFFFFFFFFFF

def keccak_f(A):
    for rc in RC:
        C = [A[x]^A[x+5]^A[x+10]^A[x+15]^A[x+20] for x in range(5)]
        D = [C[(x-1)%5]^rotl64(C[(x+1)%5],1) for x in range(5)]
        A = [A[x]^D[x%5] for x in range(25)]
        B = [0]*25; B[0] = A[0]; last = A[1]
        for i in range(24):
            B[PI[i]] = rotl64(last, RHO[i]); last = A[PI[i]]
        A = [B[x]^(~B[(x//5)*5+(x+1)%5] & B[(x//5)*5+(x+2)%5]) for x in range(25)]
        A[0] ^= rc
    return A

def sha3_256(data: bytes) -> str:
    rate = 136  # 1088 bits / 8
    msg = bytearray(data)
    msg.append(0x06)
    while len(msg) % rate != rate - 1: msg.append(0x00)
    msg.append(0x80)
    state = [0]*25
    for blk in range(0, len(msg), rate):
        block = msg[blk:blk+rate]
        for i in range(rate//8):
            state[i] ^= int.from_bytes(block[i*8:(i+1)*8], "little")
        state = keccak_f(state)
    out = bytearray()
    for i in range(4): out += state[i].to_bytes(8, "little")
    return bytes(out).hex()

if __name__ == "__main__":
    tests = [b"", b"abc", b"Hello, terminal-zero!", b"The quick brown fox jumps over the lazy dog"]
    print("SHA-3/256 vs hashlib:\n")
    for t in tests:
        expected = hashlib.sha3_256(t).hexdigest()
        got = sha3_256(t)
        status = "PASS" if got == expected else "FAIL"
        print(f"  [{status}] {t[:40]!r}")
        if got != expected:
            print(f"    exp: {expected}")
            print(f"    got: {got}")
    print("\nDone.")
