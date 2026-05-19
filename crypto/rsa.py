#!/usr/bin/env python3
"""RSA from scratch -- pure Python, no libraries. Miller-Rabin, 512-bit keys."""
import random, hashlib

def miller_rabin(n, k=20):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1; d //= 2
    for a in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if a >= n: continue
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1: break
        else: return False
    return True

def gen_prime(bits):
    while True:
        p = random.getrandbits(bits) | (1 << bits-1) | 1
        if miller_rabin(p): return p

def egcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a//b)*y

def modinv(a, m):
    g, x, _ = egcd(a % m, m)
    if g != 1: raise ValueError("No inverse")
    return x % m

def gen_keypair(bits=512):
    e = 65537
    while True:
        p, q = gen_prime(bits//2), gen_prime(bits//2)
        if p == q: continue
        n = p * q; phi = (p-1)*(q-1)
        if egcd(e, phi)[0] == 1:
            return (e, n), (modinv(e, phi), n)

def _pad(msg, nb):
    ps = bytes([random.randint(1,255) for _ in range(nb - len(msg) - 3)])
    return int.from_bytes(b"\x00\x02" + ps + b"\x00" + msg, "big")

def _unpad(m, nb):
    p = m.to_bytes(nb, "big")
    return p[p.index(0, 2) + 1:]

def encrypt(msg, pub):
    e, n = pub; nb = (n.bit_length()+7)//8
    return pow(_pad(msg, nb), e, n)

def decrypt(ct, priv):
    d, n = priv; nb = (n.bit_length()+7)//8
    return _unpad(pow(ct, d, n), nb)

def sign(msg, priv):
    d, n = priv
    return pow(int.from_bytes(hashlib.sha256(msg).digest(),"big"), d, n)

def verify(msg, sig, pub):
    e, n = pub
    return pow(sig, e, n) == int.from_bytes(hashlib.sha256(msg).digest(),"big")

if __name__ == "__main__":
    print("Generating 512-bit RSA keypair...")
    pub, priv = gen_keypair(512)
    msg = b"Hello, terminal-zero!"
    ct = encrypt(msg, pub)
    assert decrypt(ct, priv) == msg
    sig = sign(msg, priv)
    assert verify(msg, sig, pub)
    assert not verify(b"tampered", sig, pub)
    print("encrypt/decrypt OK | sign/verify OK | tamper detection OK")
    print("All RSA tests passed.")
