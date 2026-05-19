# terminal-zero

Zero dependencies. Terminal-first. Everything from scratch.

Built with: Clang-18 + Python 3.12 + Bun 1.3.10 — no npm, no pip, no install.

## Structure

| Folder | What is inside |
|--------|----------------|
| `crypto/` | RSA, SHA-3/Keccak-256 |
| `interpreters/` | LISP interpreter |
| `dashboard/` | Live terminal dashboard: BTC, weather, HN, arXiv |

## Run anything

```bash
python3 crypto/rsa.py
python3 crypto/sha3.py
python3 dashboard/live.py
python3 interpreters/lisp.py
```

## Philosophy

Every file is self-contained. No dependencies. No internet required (except dashboard).
Read the code, understand the concept, run it.
