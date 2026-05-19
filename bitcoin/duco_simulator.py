#!/usr/bin/env python3
"""
Duino-Coin Mining Simulator
Simulates DUCO-S1 SHA1 brute-force protocol offline.
Session: terminal-zero exploration, May 2026
"""
import hashlib, time, json, random, sys

def sha1_hex(data: str) -> str:
    return hashlib.sha1(data.encode()).hexdigest()

def mine_share(last_block_hash: str, difficulty: int):
    """Find nonce where SHA1(last_hash + nonce) == server_expected_hash"""
    rand_nonce = random.randint(1, difficulty * 100)
    expected_hash = sha1_hex(last_block_hash + str(rand_nonce))
    start = time.perf_counter()
    for nonce in range(0, difficulty * 100 + 1):
        if sha1_hex(last_block_hash + str(nonce)) == expected_hash:
            elapsed = time.perf_counter() - start
            return {"nonce": nonce, "expected": rand_nonce, "hash": expected_hash,
                    "attempts": nonce + 1, "ms": round(elapsed * 1000, 3),
                    "khs": round((nonce + 1) / elapsed / 1000, 2), "ok": nonce == rand_nonce}
    return None

def run_benchmark(difficulties=(50, 100, 500, 1000), shares=10):
    results = {}
    for diff in difficulties:
        print(f"\nDifficulty {diff}:")
        last_hash = sha1_hex(f"GENESIS_{time.time()}")
        sess = []
        for i in range(1, shares + 1):
            r = mine_share(last_hash, diff)
            sess.append(r)
            last_hash = sha1_hex(last_hash + str(r["nonce"]))
            print(f"  share {i:>2}: nonce={r['nonce']:>8} attempts={r['attempts']:>9} time={r['ms']:>8.3f}ms rate={r['khs']:>7.2f}kH/s {'PASS' if r['ok'] else 'FAIL'}")
        avg_ms = sum(s["ms"] for s in sess) / shares
        print(f"  avg={avg_ms:.3f}ms  spm={60000/avg_ms:.1f}  avg_khs={sum(s['khs'] for s in sess)/shares:.2f}")
        results[f"d{diff}"] = {"avg_ms": round(avg_ms,3), "spm": round(60000/avg_ms,1), "found": sum(1 for s in sess if s["ok"])}
    return results

if __name__ == "__main__":
    run_benchmark()
