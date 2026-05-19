import urllib.request, json
req = urllib.request.Request('https://api.coingecko.com/api/v3/global', headers={'User-Agent':'Mozilla/5.0 terminal-zero/1.0'})
data = json.loads(urllib.request.urlopen(req, timeout=15).read())['data']
dom = data['market_cap_percentage']['btc']
total_mc = data['total_market_cap']['usd']
btc_mc = total_mc * dom / 100
eth_dom = data['market_cap_percentage'].get('eth', 0)
vol_24h = data['total_volume']['usd']
print("=== BITCOIN MARKET DOMINANCE ===")
print(f"  BTC dominance   : {dom:.2f}%")
print(f"  ETH dominance   : {eth_dom:.2f}%")
print(f"  BTC market cap  : ${btc_mc:,.0f}")
print(f"  Total crypto MC : ${total_mc:,.0f}")
print(f"  24h volume      : ${vol_24h:,.0f}")
print(f"  Active coins    : {data.get('active_cryptocurrencies','?'):,}")
