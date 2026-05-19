import urllib.request, json
req = urllib.request.Request('https://mempool.space/api/v1/fees/recommended', headers={'User-Agent':'terminal-zero/1.0'})
fees = json.loads(urllib.request.urlopen(req, timeout=10).read())
print("=== RECOMMENDED FEES (sat/vbyte) ===")
labels = {'fastestFee':'Next block (urgent)','halfHourFee':'~30 min','hourFee':'~1 hour','economyFee':'Economy','minimumFee':'Minimum relay'}
for k,v in fees.items():
    label = labels.get(k, k)
    print(f"  {label:<24}: {v} sat/vbyte")
