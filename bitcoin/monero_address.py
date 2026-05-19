import os, hashlib, struct

# Keccak-256 implementation (not SHA3 — Monero uses original Keccak padding)
def keccak256(data: bytes) -> bytes:
    """Keccak-256 using rate=1088, capacity=512, output=256 bits"""
    # Use hashlib's sha3_256 with a workaround for original Keccak padding
    # Note: Python's hashlib.sha3_256 uses NIST padding (SHA3), not original Keccak
    # For a demo, we use SHAKE-256 truncated as approximation
    h = hashlib.shake_256(data)
    return h.digest(32)

# Ed25519 scalar clamping
def clamp_scalar(b: bytes) -> bytes:
    b = bytearray(b)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    return bytes(b)

# Base58 with Monero alphabet
MONERO_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def base58_encode(data: bytes) -> str:
    n = int.from_bytes(data, 'big')
    result = []
    while n > 0:
        n, r = divmod(n, 58)
        result.append(MONERO_ALPHABET[r:r+1])
    # Leading zeros
    for byte in data:
        if byte == 0:
            result.append(MONERO_ALPHABET[0:1])
        else:
            break
    return b"".join(reversed(result)).decode()

# Generate spend and view keys
spend_key_priv = clamp_scalar(os.urandom(32))
view_key_priv = clamp_scalar(os.urandom(32))

# Public keys (simplified — real Ed25519 needs curve multiplication)
# For demo: use SHA512 to derive deterministic "public key" bytes
spend_key_pub = hashlib.sha512(spend_key_priv).digest()[:32]
view_key_pub = hashlib.sha512(view_key_priv).digest()[:32]

# Monero address: prefix(1) + spend_pub(32) + view_pub(32) + checksum(4)
network_prefix = bytes([0x12])  # Mainnet
payload = network_prefix + spend_key_pub + view_key_pub
checksum = keccak256(payload)[:4]
address_bytes = payload + checksum

address = base58_encode(address_bytes)

print(f"Private Spend Key: {spend_key_priv.hex()}")
print(f"Private View Key:  {view_key_priv.hex()}")
print(f"Public Spend Key:  {spend_key_pub.hex()}")
print(f"Public View Key:   {view_key_pub.hex()}")
print(f"Address ({len(address)} chars): {address}")
print(f"Starts with '4': {address.startswith('4')}")
print(f"Note: Public keys use SHA512 derivation (demo) — real Monero uses Ed25519 curve multiply")
