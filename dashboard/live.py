#!/usr/bin/env python3
"""Live terminal dashboard -- pure Python stdlib. BTC, weather, HN, arXiv."""
import urllib.request, json, xml.etree.ElementTree as ET
from datetime import datetime

WMO = {0:"Clear",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",45:"Fog",
       51:"Light drizzle",61:"Slight rain",63:"Rain",65:"Heavy rain",
       71:"Snow",73:"Moderate snow",80:"Showers",95:"Thunderstorm",99:"Heavy thunderstorm"}

def fetch(url, t=8):
    req = urllib.request.Request(url, headers={"User-Agent":"terminal-zero/1.0"})
    with urllib.request.urlopen(req, timeout=t) as r: return r.read()

def btc():
    try:
        d = json.loads(fetch("https://api.coinbase.com/v2/prices/BTC-USD/spot"))
        return f"${float(d['data']['amount']):,.2f}"
    except Exception as e: return f"unavailable ({e})"

def weather():
    try:
        url = ("https://api.open-meteo.com/v1/forecast"
               "?latitude=24.8607&longitude=67.0011&current=temperature_2m,weathercode")
        d = json.loads(fetch(url))["current"]
        return f"{d['temperature_2m']}C  {WMO.get(d['weathercode'], str(d['weathercode']))}"
    except Exception as e: return f"unavailable ({e})"

def hn():
    try:
        ids = json.loads(fetch("https://hacker-news.firebaseio.com/v0/topstories.json"))[:3]
        return [(json.loads(fetch(f"https://hacker-news.firebaseio.com/v0/item/{i}.json"))
                 .get("title","?")) for i in ids]
    except Exception as e: return [f"unavailable ({e})"]

def arxiv():
    try:
        xml = fetch("http://export.arxiv.org/api/query?search_query=cat:cs.AI"
                    "&sortBy=submittedDate&sortOrder=descending&max_results=1").decode()
        ns = {"a":"http://www.w3.org/2005/Atom"}
        entry = ET.fromstring(xml).find("a:entry", ns)
        title = entry.find("a:title", ns).text.strip().replace("\n"," ")
        date  = entry.find("a:published", ns).text[:10]
        return f"{title} ({date})"
    except Exception as e: return f"unavailable ({e})"

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 60)
    print(f"  terminal-zero DASHBOARD  |  {now}")
    print("=" * 60)
    print(f"\n  BTC/USD     {btc()}")
    print(f"\n  Karachi     {weather()}")
    print("\n  HN Top 3")
    for i, t in enumerate(hn(), 1): print(f"    {i}. {t[:55]}")
    print("\n  arXiv cs.AI")
    print(f"    {arxiv()[:80]}")
    print("=" * 60)
