# Lab: Debug DNS, TCP, TLS, and HTTP as Separate Layers

Interrogate one public HTTPS endpoint layer by layer, then inject local name and certificate failures without changing system DNS or trust stores.

## Prerequisites

- Bash, Python 3, `getent`, `curl`, and OpenSSL
- Optional: `dig` for richer DNS evidence
- Outbound access to `example.com`; otherwise substitute an approved endpoint

## Safety

Use only public documentation endpoints you are authorized to query. Keep request rate below one request per second. Do not use `-k`, edit `/etc/hosts`, alter trust stores, or capture unrelated traffic. Stop if a proxy or corporate policy forbids direct probes.

## Setup and baseline

```bash
mkdir -p .work
getent ahosts example.com | tee .work/addresses.txt
curl --max-time 10 --silent --show-error --output /dev/null \
  --write-out 'code=%{http_code} remote=%{remote_ip} tls=%{ssl_verify_result}\n' \
  https://example.com | tee .work/baseline.txt
```

Predict the symptom for name failure, refused TCP, TLS name mismatch, and HTTP 404 before testing.

## Tasks

1. Record resolver configuration without changing it:

   ```bash
   sed -n '1,120p' /etc/resolv.conf | tee .work/resolv-conf.txt
   getent hosts example.com
   ```

2. Inspect the TLS handshake and certificate:

   ```bash
   openssl s_client -connect example.com:443 -servername example.com \
     -verify_return_error </dev/null >.work/tls.txt 2>&1
   openssl s_client -connect example.com:443 -servername example.com \
     </dev/null 2>/dev/null |
     openssl x509 -noout -subject -issuer -dates -ext subjectAltName |
     tee .work/certificate.txt
   ```

3. Make a verbose bounded request and label where DNS, connect, TLS, status, and body occur:

   ```bash
   curl --max-time 10 --verbose --output /dev/null https://example.com \
     2>.work/curl-verbose.txt
   ```

4. Explain why successful DNS does not establish TCP reachability, and why a valid chain does not establish application health.

## Evidence to keep

Keep resolver source, resolved addresses, certificate identity and validity, negotiated protocol, HTTP status, timings, and a layer-by-layer decision table. Record proxy environment variable names, but never their values if they contain credentials.

## Failure injection

Inject three independent failures:

```bash
curl --max-time 3 https://does-not-exist.invalid 2>.work/dns-failure.txt || true
curl --max-time 3 http://127.0.0.1:9 2>.work/connect-failure.txt || true
curl --max-time 5 --resolve wrong.invalid:443:93.184.216.34 \
  https://wrong.invalid 2>.work/tls-failure.txt || true
```

The fixed address may change or be unreachable; the required claim is the observed layer, not a specific error string. Do not suppress certificate verification. For each failure, identify the last completed layer and first failed layer.

## Cleanup

```bash
rm -rf .work
```

No host networking state was modified.

## Rubric

- 2 points: captures a healthy layered baseline
- 3 points: correctly attributes DNS, connect, and TLS failures
- 2 points: validates hostname and certificate dates without bypasses
- 2 points: states the limits of each observation
- 1 point: uses bounded, low-rate probes and cleans artifacts

## Sources

- [DNS concepts, RFC 1034](https://www.rfc-editor.org/rfc/rfc1034)
- [TLS 1.3, RFC 8446](https://www.rfc-editor.org/rfc/rfc8446)
- [HTTP semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [`curl` documentation](https://curl.se/docs/)
