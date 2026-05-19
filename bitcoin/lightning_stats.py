import urllib.request, json
req = urllib.request.Request('https://mempool.space/api/v1/lightning/statistics/latest', headers={'User-Agent':'terminal-zero/1.0'})
try:
    data = json.loads(urllib.request.urlopen(req, timeout=10).read())
    stats = data.get('latest', data)
    cap_btc = stats.get('total_capacity', 0) / 1e8
    print("=== LIGHTNING NETWORK STATS ===")
    print(f"  Node count      : {stats.get('node_count','?'):,}")
    print(f"  Channel count   : {stats.get('channel_count','?'):,}")
    print(f"  Total capacity  : {cap_btc:.2f} BTC")
    print(f"  Added (24h)     : {stats.get('added','?')}")
    print(f"  Removed (24h)   : {stats.get('removed','?')}")
except Exception as e:
    print(f"ERROR: {e}")
