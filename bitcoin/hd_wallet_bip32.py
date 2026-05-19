import hmac, hashlib, struct
# secp256k1 curve parameters
P  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G  = (Gx, Gy)
def modinv(a, m=P): return pow(a, m-2, m)
def point_add(P1, P2):
    if P1 is None: return P2
    if P2 is None: return P1
    x1,y1=P1; x2,y2=P2
    if x1==x2:
        if y1!=y2: return None
        m=(3*x1*x1*modinv(2*y1))%P
    else:
        m=((y2-y1)*modinv(x2-x1))%P
    x3=(m*m-x1-x2)%P; y3=(m*(x1-x3)-y1)%P
    return x3,y3
def point_mul(k,pt):
    res=None; addend=pt
    while k:
        if k&1: res=point_add(res,addend)
        addend=point_add(addend,addend); k>>=1
    return res
def compress_pubkey(pt):
    x,y=pt; prefix=b'\x02' if y%2==0 else b'\x03'
    return prefix+x.to_bytes(32,'big')
def btc_address(pubkey_bytes):
    import hashlib
    sha=hashlib.sha256(pubkey_bytes).digest()
    ripe=hashlib.new('ripemd160',sha).digest()
    payload=b'\x00'+ripe
    chk=hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    raw=payload+chk
    ALPHA='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    n=int.from_bytes(raw,'big'); r=''
    while n: n,rem=divmod(n,58); r=ALPHA[rem]+r
    return ALPHA[0]*(len(raw)-len(raw.lstrip(b'\x00')))+r
# BIP32 test vector 1 seed
SEED = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
I = hmac.new(b'Bitcoin seed', SEED, hashlib.sha512).digest()
master_priv = I[:32]; master_chain = I[32:]
print(f"=== BIP32 HD WALLET (test vector 1) ===")
print(f"Seed           : {SEED.hex()}")
print(f"Master priv    : {master_priv.hex()}")
print(f"Master chain   : {master_chain.hex()}")
# Derive m/44h/0h/0h/0/0
HARD = 0x80000000
path = [(44+HARD),(0+HARD),(0+HARD),0,0]
path_str = "m/44'/0'/0'/0/0"
priv, chain = master_priv, master_chain
for i,idx in enumerate(path):
    pub = compress_pubkey(point_mul(int.from_bytes(priv,'big'), G))
    if idx >= HARD:
        data = b'\x00'+priv+struct.pack('>I',idx)
    else:
        data = pub+struct.pack('>I',idx)
    Ic = hmac.new(chain, data, hashlib.sha512).digest()
    IL_int = int.from_bytes(Ic[:32],'big')
    child_priv_int = (IL_int + int.from_bytes(priv,'big')) % N
    priv = child_priv_int.to_bytes(32,'big')
    chain = Ic[32:]
    step = path_str.split('/')[i+1]
    print(f"  [{step}] priv: {priv.hex()[:16]}...  chain: {chain.hex()[:16]}...")
final_pub = compress_pubkey(point_mul(int.from_bytes(priv,'big'), G))
addr = btc_address(final_pub)
print(f"\nFinal path     : {path_str}")
print(f"Final priv key : {priv.hex()}")
print(f"Final pub key  : {final_pub.hex()}")
print(f"BTC Address    : {addr}")
