import urllib.request, json

urls = [
    "https://xmrchain.net/api/networkinfo",
    "https://moneroblocks.info/api/get_stats/"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        print(f"Source: {url}")
        print(json.dumps(data, indent=2)[:2000])
        break
    except Exception as e:
        print(f"FAIL {url}: {e}")
