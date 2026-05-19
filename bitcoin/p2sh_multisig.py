import hashlib
keys = [
    bytes.fromhex('02e577d441d501cace792c02bfe2cc15e59672199e2195770a61fd3288fc9f934f'),
    bytes.fromhex('03b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffdd7d0ff7aa775'),
    bytes.fromhex('02396fa6fabb7c31e6e5283e6f6c1d808a6cde29b0d9d0c6ee88a2f5de4d80fd10'),
]
# Build 2-of-3 multisig redeem script
# OP_2 <len><key1> <len><key2> <len><key3> OP_3 OP_CHECKMULTISIG
script = bytes([0x52])  # OP_2
for k in keys:
    script += bytes([len(k)]) + k
script += bytes([0x53, 0xae])  # OP_3 OP_CHECKMULTISIG
print("=== 2-of-3 P2SH MULTISIG ADDRESS ===")
print(f"Redeem script ({len(script)} bytes):")
print(f"  {script.hex()}")
sha256_hash = hashlib.sha256(script).digest()
ripemd_hash = hashlib.new('ripemd160', sha256_hash).digest()
print(f"SHA256(script)      : {sha256_hash.hex()}")
print(f"HASH160(script)     : {ripemd_hash.hex()}")
# Base58Check with version byte 0x05 (P2SH)
payload = bytes([0x05]) + ripemd_hash
checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
raw = payload + checksum
ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
n = int.from_bytes(raw, 'big'); result = ''
while n: n, r = divmod(n, 58); result = ALPHABET[r] + result
result = ALPHABET[0] * (len(raw) - len(raw.lstrip(b'\x00'))) + result
print(f"P2SH Address        : {result}")
print(f"Starts with '3'     : {result.startswith('3')}")
