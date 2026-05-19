import urllib.request, json

# Try to fetch live XMR price
xmr_price = 392.0
try:
    req = urllib.request.Request(
        "https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=usd",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=8) as r:
        data = json.loads(r.read())
    xmr_price = data["monero"]["usd"]
    print(f"Live XMR price: ${xmr_price}")
except Exception as e:
    print(f"CoinGecko failed ({e}), using hardcoded: ${xmr_price}")

# Parameters
block_reward = 0.6          # XMR
network_hashrate = 3.5e9    # H/s (3.5 GH/s)
cpu_hashrate = 500          # H/s (good desktop CPU with RandomX)
blocks_per_day = 720        # ~2 min block time

# Calculations
pool_share = cpu_hashrate / network_hashrate
xmr_per_day = pool_share * block_reward * blocks_per_day
usd_per_day = xmr_per_day * xmr_price
days_to_1_xmr = 1.0 / xmr_per_day if xmr_per_day > 0 else float('inf')

print(f"\n=== Monero CPU Mining Profitability ===")
print(f"XMR Price:         ${xmr_price:,.2f}")
print(f"Block Reward:      {block_reward} XMR")
print(f"Network Hashrate:  {network_hashrate/1e9:.1f} GH/s")
print(f"Your CPU:          {cpu_hashrate} H/s")
print(f"Pool Share:        {pool_share*100:.8f}%")
print(f"XMR/day:           {xmr_per_day:.8f} XMR")
print(f"USD/day:           ${usd_per_day:.6f}")
print(f"Days to 1 XMR:     {days_to_1_xmr:,.0f} days ({days_to_1_xmr/365:.1f} years)")
print(f"\nComparison:")
print(f"  Electricity cost at $0.10/kWh, 65W CPU: ${0.10 * 0.065 * 24:.4f}/day")
print(f"  Net profit/day: ${usd_per_day - (0.10 * 0.065 * 24):.6f}")
