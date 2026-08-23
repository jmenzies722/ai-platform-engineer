# Lab: Trace a Local HTTP Connection

Build a complete network explanation without contacting the public internet. A loopback server lets you inspect addressing, a listening TCP port, one connection, and HTTP evidence safely.

## Start a bounded local server

```bash
lab=$(mktemp -d)
printf 'hello from loopback\n' > "$lab/index.html"
python3 -m http.server 8765 --bind 127.0.0.1 --directory "$lab" >"$lab/server.log" 2>&1 &
pid=$!
printf 'server_pid=%s\n' "$pid"
```

Expected observation: the server runs in the background and writes no terminal output. It is reachable only through IPv4 loopback on this host.

## Inspect the listener

```bash
ss -ltnp 2>/dev/null | sed -n '/127.0.0.1:8765/p'
ip route get 127.0.0.1 2>/dev/null || true
```

Expected observation: a TCP socket listens on `127.0.0.1:8765`; the route is local. Some systems hide process details in `ss`, but address and port should remain visible.

## Send one HTTP request

```bash
python3 - <<'PY'
from http.client import HTTPConnection
c = HTTPConnection('127.0.0.1', 8765, timeout=2)
c.request('GET', '/')
r = c.getresponse()
print(r.status, r.reason)
print(r.read().decode().strip())
c.close()
PY
```

Expected observation: status `200` and the file content appear. Because the client uses an IP literal, this proves no DNS behavior. TCP connected before HTTP returned a status.

Inspect `sed -n '1,8p' "$lab/server.log"`. The request log is application evidence, not a packet trace and not proof that a remote host could connect.

## Controlled failures

Request `/missing` and expect HTTP `404`; the transport still worked. Then stop the server and repeat the original request:

```bash
kill -TERM "$pid"
wait "$pid" || true
python3 - <<'PY'
import socket
try:
    socket.create_connection(('127.0.0.1', 8765), timeout=1)
except OSError as error:
    print(type(error).__name__, error)
PY
```

Expected observation: the stopped listener produces a connection error rather than an HTTP status. This distinguishes transport failure from an application response.

## Explain the layers

Write one sentence each for the loopback address, TCP listening port, established connection, HTTP request, and HTTP response. For every sentence name the command that supports it and one unsupported conclusion.

## Cleanup

```bash
if kill -0 "$pid" 2>/dev/null; then kill -TERM "$pid"; wait "$pid" || true; fi
rm -rf "$lab"
```

Expected observation: `ss -ltn` no longer shows port 8765 and the temporary files are removed.

## Next

Continue to [DNS, HTTP, and TLS](./03-dns-http-and-tls.md).
