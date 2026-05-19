import urllib.request, json

# Use a well-known address with a manageable UTXO count
# 1CounterpartyXXXXXXXXXXXXXXXUWLpVr is the Counterparty burn address (~1 UTXO)
# We try genesis first; if >500 UTXOs fall back to a simpler address
ADDRESSES = [
    ('Counterparty burn', '1CounterpartyXXXXXXXXXXXXXXXUWLpVr'),
    ('Satoshi genesis',   '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'),
]

def fetch_utxos(addr):
    url = f'https://mempool.space/api/address/{addr}/utxo'
    req = urllib.request.Request(url, headers={'User-Agent': 'terminal-zero/1.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        body = e.read(200).decode()
        return None, f'HTTP {e.code}: {body}'
    except Exception as ex:
        return None, str(ex)

for label, addr in ADDRESSES:
    print(f'=== {label.upper()} UTXOs (mempool.space) ===')
    print(f'Address : {addr}')
    utxos, err = fetch_utxos(addr)
    if err:
        print(f'Error   : {err}')
        print()
        continue
    total = sum(u['value'] for u in utxos)
    print(f'UTXO count : {len(utxos)}')
    print(f'Total value: {total:,} sat  ({total / 1e8:.8f} BTC)')
    print()
    for u in utxos[:8]:
        status = 'confirmed' if u['status']['confirmed'] else 'UNCONFIRMED'
        blk = u['status'].get('block_height', '?')
        print(f"  txid:{u['txid'][:20]}...  vout:{u['vout']}  value:{u['value']:,} sat  [{status} blk#{blk}]")
    if len(utxos) > 8:
        print(f'  ... and {len(utxos) - 8} more')
    print()
    break  # success — stop after first working address
