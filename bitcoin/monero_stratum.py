import socket, json, time

host = "gulf.moneroocean.stream"
port = 10128

login_msg = json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "login",
    "params": {
        "login": "44AFFq5kSiGBoZ4NMDwYtN18obc8AemS33DBLWs3H7otXft3XjrpDtQGv7SqSsaBYBb98uNbr2VBBEt7f2wfn3RVGQBEP3A",
        "pass": "x",
        "agent": "test/1.0"
    }
}) + "\n"

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(15)
    print(f"Connecting to {host}:{port}...")
    s.connect((host, port))
    print("Connected!")
    s.sendall(login_msg.encode())
    print("Login sent. Waiting for response...")
    
    data = b""
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
            if b"\n" in data:
                break
        except socket.timeout:
            break
    
    s.close()
    
    if data:
        print(f"Raw response ({len(data)} bytes):")
        print(data.decode(errors='replace')[:2000])
        # Parse job structure
        resp = json.loads(data.decode().strip())
        if "result" in resp and resp["result"]:
            job = resp["result"].get("job", {})
            print(f"\nJob fields: {list(job.keys())}")
            print(f"Blob length: {len(job.get('blob',''))} chars")
            print(f"Target: {job.get('target','N/A')}")
            print(f"Algorithm: {job.get('algo','N/A')}")
    else:
        print("No response received")
except Exception as e:
    print(f"Error: {e}")
