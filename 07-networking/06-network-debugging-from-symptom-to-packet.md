# Network Debugging from Symptom to Packet

Network debugging is the disciplined search for the first boundary where expected evidence stops.

## Why it matters

“The network is slow” can describe resolver delay, a dropped SYN, retransmission, TLS verification, proxy queueing, server work, or a response body consumed slowly by the client. Restarting components changes evidence and may temporarily hide the fault. A useful investigation starts with a timestamped transaction, decomposes its latency, and narrows one boundary at a time.

## How it works

Begin with the application’s exact source context, destination name, operation, deadline, and error. Resolve the name as that application does. Ask the kernel which route and source address it would choose. Confirm local listener or connection state. Probe the actual transport and protocol with bounded deadlines. Only then capture packets at interfaces you own.

Packet capture records observed frames, not universal truth. A host capture can be distorted by checksum, segmentation, or receive offload: the kernel may expose large synthetic segments or checksums that hardware will later fill. A capture on one side cannot prove the other side received a frame. Sequence and acknowledgment behavior can support a loss hypothesis, but application logs are needed to establish processing. Time synchronization and shared request identifiers connect evidence across hosts.

Latency should be split into resolver, connect, TLS, time to first byte, and body transfer when the client exposes those phases. Deadlines form a budget. A retry policy consumes more budget and load, and must account for whether the operation may already have happened. Use `ping` only as an ICMP reachability and timing observation; many systems filter it while allowing application traffic. `traceroute` reveals selected hop responses, not a guaranteed symmetric route.

## See it yourself

Start the server, predict one successful connect and one refusal after shutdown, then preserve timings and clean up.

```bash
python3 -m http.server 8765 --bind 127.0.0.1 >/tmp/net-debug.log 2>&1 &
pid=$!
curl --silent --output /dev/null --max-time 2 \
  --write-out 'connect=%{time_connect} first_byte=%{time_starttransfer} total=%{time_total}\n' \
  http://127.0.0.1:8765/
ss -tnp 2>/dev/null | sed -n '1,12p'
kill "$pid"; wait "$pid" 2>/dev/null || true
curl --silent --show-error --max-time 1 http://127.0.0.1:8765/ >/dev/null || true
rm -f /tmp/net-debug.log
```

Expected observation: the first request reports separate local timing phases; after shutdown, the same endpoint usually fails immediately with refusal rather than returning HTTP.

Limits of the observation: loopback excludes routers, physical links, DNS, and TLS. Fast local values are instrumentation examples, not production baselines, and `ss` may miss a short-lived connection.

## Where it shows up

Suppose one region reports intermittent 504s. Client metrics show normal DNS and connect time but long time to first byte. The edge log identifies one backend pool; load-balancer telemetry shows queue growth; packet traces show established streams without retransmission; application profiles show a saturated worker pool. The evidence moves the incident from “network” to admission control without denying that network boundaries were tested.

## When it breaks

No route is a local routing decision; refusal usually proves reachability to an active reject or closed port; connect timeout permits loss or missing return traffic; reset indicates an endpoint or intermediary aborted state; repeated retransmissions suggest loss or a nonresponsive receiver; long first-byte time with clean transport suggests queueing or application work. Verify clocks, endpoint tuples, capture location, and offload before interpreting packets. Capture the smallest filter and duration that answer the question, protect payload data, and remove capture files after use.

## Practice

**Build:** complete the module lab and produce a six-column timeline: observer, timestamp, layer, expected event, actual evidence, and limit. **Break:** create refusal, application delay, malformed HTTP, and an unresolvable name without touching shared infrastructure. **Explain back:** state the first failed boundary and two alternative hypotheses still compatible with the evidence. Success means another engineer can reproduce the diagnosis and cleanup from your notes.

## Check yourself

1. Why can a packet capture on the sender not prove receipt by the peer application?
2. Which latency phase would you investigate first when connect is fast but time to first byte is slow?

## Sources

### REQUIRED

- [Linux packet capture manual](https://man7.org/linux/man-pages/man7/packet.7.html)
- [tcpdump manual](https://www.tcpdump.org/manpages/tcpdump.1.html)

### RECOMMENDED

- [Wireshark User’s Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- [ss manual](https://man7.org/linux/man-pages/man8/ss.8.html)

### DEEP DIVE

- [The TCP/IP Guide](http://www.tcpipguide.com/free/index.htm)

## Next

Continue to [Databases](../08-databases/README.md).
