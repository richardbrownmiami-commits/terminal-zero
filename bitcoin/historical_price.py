import urllib.request, json, datetime
url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30&interval=daily'
req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 terminal-zero/1.0'})
data = json.loads(urllib.request.urlopen(req, timeout=15).read())
prices = data['prices']
p30d_ts, p30d = prices[0]
pnow_ts, pnow = prices[-1]
pct = (pnow - p30d) / p30d * 100
d30 = datetime.datetime.utcfromtimestamp(p30d_ts/1000).strftime('%Y-%m-%d')
dnow = datetime.datetime.utcfromtimestamp(pnow_ts/1000).strftime('%Y-%m-%d')
print("=== BITCOIN PRICE HISTORY (30 DAYS) ===")
print(f"  30 days ago ({d30}) : ${p30d:>12,.2f}")
print(f"  Today       ({dnow}) : ${pnow:>12,.2f}")
print(f"  Change               : {pct:+.2f}%")
peak = max(prices, key=lambda x: x[1])
low  = min(prices, key=lambda x: x[1])
peak_d = datetime.datetime.utcfromtimestamp(peak[0]/1000).strftime('%Y-%m-%d')
low_d  = datetime.datetime.utcfromtimestamp(low[0]/1000).strftime('%Y-%m-%d')
print(f"  30d high ({peak_d})  : ${peak[1]:>12,.2f}")
print(f"  30d low  ({low_d})   : ${low[1]:>12,.2f}")
