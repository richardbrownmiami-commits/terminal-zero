import urllib.request, json
req = urllib.request.Request('https://mempool.space/api/mempool', headers={'User-Agent':'terminal-zero/1.0'})
r1 = json.loads(urllib.request.urlopen(req, timeout=10).read())
print(f"=== MEMPOOL STATS ===")
print(f"Count: {r1['count']:,}  vsize: {r1['vsize']:,} vbytes  total_fee: {r1['total_fee']:,} sat")
req2 = urllib.request.Request('https://mempool.space/api/mempool/recent', headers={'User-Agent':'terminal-zero/1.0'})
r2 = sorted(json.loads(urllib.request.urlopen(req2, timeout=10).read()), key=lambda x: x.get('fee',0), reverse=True)
print("\n=== TOP 5 BY FEE ===")
for tx in r2[:5]:
    fee=tx.get('fee',0); vs=tx.get('vsize',0)
    print(f"  {tx['txid'][:20]}... fee:{fee:,} sat vsize:{vs}vb rate:{fee/vs:.1f}sat/vb" if vs else f"  {tx['txid'][:20]}... fee:{fee:,} sat")
