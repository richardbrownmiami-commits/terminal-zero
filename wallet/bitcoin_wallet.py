#!/usr/bin/env python3
"""
Bitcoin Wallet Generator
Pure Python stdlib — no pip, no external libraries
secp256k1 elliptic curve from scratch
"""

import os
import hashlib
import struct

# ── secp256k1 curve parameters ──────────────────────────────────────────────
P  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def mod_inv(a, m=P):
    """Extended Euclidean Algorithm modular inverse"""
    if a < 0:
        a = a % m
    g, x, _ = m, 1, 0
    a0 = a
    while a0 != 0:
        q = g // a0
        g, a0 = a0, g - q * a0
        x, _ = _, x - q * _
    return x % m

def point_add(P1, P2):
    """Add two points on secp256k1"""
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2:
        if y1 != y2:
            return None  # point at infinity
        # Point doubling
        lam = (3 * x1 * x1 * mod_inv(2 * y1)) % P
    else:
        lam = ((y2 - y1) * mod_inv(x2 - x1)) % P
    x3 = (lam * lam - x1 - x2) % P
    y3 = (lam * (x1 - x3) - y1) % P
    return (x3, y3)

def scalar_mult(k, point=(Gx, Gy)):
    """Double-and-add scalar multiplication"""
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

# ── Hash helpers ─────────────────────────────────────────────────────────────
def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def ripemd160(data: bytes) -> bytes:
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.digest()

def hash160(data: bytes) -> bytes:
    """SHA256 then RIPEMD160"""
    return ripemd160(sha256(data))

def hash256(data: bytes) -> bytes:
    """Double SHA256"""
    return sha256(sha256(data))

# ── Base58Check ──────────────────────────────────────────────────────────────
BASE58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(data: bytes) -> str:
    n = int.from_bytes(data, 'big')
    result = []
    while n > 0:
        n, r = divmod(n, 58)
        result.append(BASE58_CHARS[r])
    # Leading zero bytes → leading '1's
    for b in data:
        if b == 0:
            result.append('1')
        else:
            break
    return ''.join(reversed(result))

def base58check_encode(version: bytes, payload: bytes) -> str:
    data = version + payload
    checksum = hash256(data)[:4]
    return base58_encode(data + checksum)

# ── Wallet generation ─────────────────────────────────────────────────────────
def generate_wallet():
    # 1. Private key — 32 cryptographically secure random bytes
    while True:
        private_key_bytes = os.urandom(32)
        private_key_int = int.from_bytes(private_key_bytes, 'big')
        if 1 <= private_key_int < N:  # must be in [1, N-1]
            break

    # 2. Public key — secp256k1 scalar multiplication
    pub_point = scalar_mult(private_key_int)
    x, y = pub_point

    # Compressed public key: 02 if y even, 03 if y odd
    prefix = b'\x02' if y % 2 == 0 else b'\x03'
    compressed_pub = prefix + x.to_bytes(32, 'big')

    # 3. Bitcoin address — Hash160 of compressed pubkey + Base58Check
    h160 = hash160(compressed_pub)
    # Mainnet version byte = 0x00
    bitcoin_address = base58check_encode(b'\x00', h160)

    # 4. WIF (Wallet Import Format)
    # Mainnet WIF version = 0x80, + 0x01 suffix for compressed
    wif = base58check_encode(b'\x80', private_key_bytes + b'\x01')

    return {
        'private_key_hex': private_key_bytes.hex(),
        'private_key_int': private_key_int,
        'wif': wif,
        'public_key_compressed': compressed_pub.hex(),
        'public_key_x': x,
        'public_key_y': y,
        'bitcoin_address': bitcoin_address,
        'hash160': h160.hex(),
    }

# ── Verification ──────────────────────────────────────────────────────────────
def verify_wallet(wallet):
    """Basic sanity checks"""
    priv_int = wallet['private_key_int']
    assert 1 <= priv_int < N, "Private key out of range"

    pub_hex = wallet['public_key_compressed']
    assert pub_hex[:2] in ('02', '03'), "Bad compressed pubkey prefix"
    assert len(pub_hex) == 66, "Compressed pubkey must be 33 bytes"

    addr = wallet['bitcoin_address']
    assert addr[0] == '1', "Mainnet address must start with 1"
    assert 25 <= len(addr) <= 34, "Address length out of range"

    wif = wallet['wif']
    assert wif[0] in ('K', 'L'), "Compressed WIF must start with K or L"

    return True

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("  Bitcoin Wallet Generator — Pure Python secp256k1")
    print("  NO external libraries | stdlib only")
    print("=" * 60)
    print()

    wallet = generate_wallet()

    print(f"Private Key (hex)  : {wallet['private_key_hex']}")
    print(f"Private Key (int)  : {wallet['private_key_int']}")
    print()
    print(f"WIF                : {wallet['wif']}")
    print()
    print(f"Public Key (comp.) : {wallet['public_key_compressed']}")
    print(f"  prefix           : {wallet['public_key_compressed'][:2]} ({'even' if wallet['public_key_compressed'][:2] == '02' else 'odd'} y)")
    print(f"  X coord          : {wallet['public_key_x']}")
    print(f"  Y coord          : {wallet['public_key_y']}")
    print()
    print(f"Hash160 (hex)      : {wallet['hash160']}")
    print(f"Bitcoin Address    : {wallet['bitcoin_address']}")
    print()

    # Verify
    try:
        verify_wallet(wallet)
        print("✓ Verification passed — all checks OK")
    except AssertionError as e:
        print(f"✗ Verification FAILED: {e}")

    print()
    print("=" * 60)
    print("  DISCLAIMER: For educational use only.")
    print("  Never share your private key or WIF.")
    print("=" * 60)
