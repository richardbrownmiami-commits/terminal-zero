import urllib.request, json
addr = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
req = urllib.request.Request(f'https://blockstream.info/api/address/{addr}/utxo', headers={'User-Agent':'terminal-zero/1.0'})
utxos = json.loads(urllib.request.urlopen(req, timeout=10).read())
total = sum(u['value'] for u in utxos)
print(f"=== SATOSHI GENESIS ADDRESS UTXOs ===")
print(f"Address: {addr}")
print(f"UTXO count: {len(utxos)}  Total value: {total:,} sat ({total/1e8:.8f} BTC)")
print()
for u in utxos[:8]:
    status = 'confirmed' if u['status']['confirmed'] else 'UNCONFIRMED'
    blk = u['status'].get('block_height','?')
    print(f"  txid:{u['txid'][:20]}... vout:{u['vout']} value:{u['value']:,}sat [{status} blk#{blk}]")
if len(utxos)>8: print(f"  ... and {len(utxos)-8} more")
