import urllib.request, json, datetime
def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent':'terminal-zero/1.0'})
    return urllib.request.urlopen(req, timeout=10).read()
height = fetch('https://blockstream.info/api/blocks/tip/height').decode().strip()
hash_ = fetch('https://blockstream.info/api/blocks/tip/hash').decode().strip()
block = json.loads(fetch(f'https://blockstream.info/api/block/{hash_}'))
ts = datetime.datetime.utcfromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S UTC')
print(f"=== LATEST BLOCK ===")
print(f"Height    : {height}")
print(f"Hash      : {hash_}")
print(f"Timestamp : {ts}")
print(f"Tx count  : {block['tx_count']:,}")
print(f"Size      : {block['size']:,} bytes  Weight: {block['weight']:,} wu")
