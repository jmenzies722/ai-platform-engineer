# Addresses, Packets, and Routing

Networks deliver packets between interfaces using layered addresses and forwarding decisions; delivery is not guaranteed by IP alone.

## Why it matters

A service can listen correctly and still be unreachable because a host chooses the wrong route, a subnet lacks a return path, or an MTU drops larger packets. Adding application retries before proving packet direction can amplify load without repairing connectivity. The first decision is where delivery stops between local interface, next hop, and destination prefix.

## How it works

A host places an IP packet toward a next hop selected by a routing table. Routers forward packets toward destination prefixes. Link-layer delivery handles the local hop. TTL or hop limit prevents indefinite loops. Fragmentation and path MTU constrain packet size.

An interface joins a host to a link and has link-layer and network-layer identities. IP packets carry source and destination addresses; the host performs longest-prefix route selection to choose a local delivery, next hop, and egress interface. Neighbor discovery or ARP resolves a next-hop IP to a link-layer destination on the local segment. Routers repeat a forwarding decision while decrementing TTL or hop limit, but they do not provide end-to-end delivery guarantees. Prefixes describe address sets, and a default route is merely the least-specific fallback. The return packet makes its own route decisions, so one-way reachability is possible. Path MTU limits packet size across all hops; fragmentation behavior differs between IPv4 and IPv6. Firewalls and policy routing can add decisions beyond the basic destination table.

## See it yourself

Predict that the route table contains connected prefixes and often a default route, while interface output shows loopback plus one or more network interfaces. Do not assume the interface names or addresses.

```bash
ip route 2>/dev/null || true
ip address show 2>/dev/null | sed -n '1,24p' || true
```

Expected observation: Routes identify reachable prefixes and a preferred next hop or interface. Interface output separates link and IP identities.

Limits of the addresses, packets, and routing observation: These commands do not send an end-to-end probe, reveal every router, or prove a firewall permits application traffic. They display local configuration and route selection inputs.

## Where it shows up

A Kubernetes node reaching a private database still depends on ordinary routing. Pod traffic may be translated or encapsulated, leave through a node interface, traverse cloud route tables, and require a viable return prefix. Comparing route decisions and packet counters at successive owned boundaries is more useful than restarting the pod. The abstraction changes where configuration lives, not the need for bidirectional forwarding.

## When it breaks

“Network unreachable” usually indicates no usable route; timeout permits loss, filtering, wrong return path, or silent service behavior; small packets working while large ones fail suggests MTU trouble. First record source and destination addresses, local route selection, interface state, and whether packets leave and return using a scoped capture or counters. Capture only traffic you own, and avoid treating ICMP filtering as proof that every transport is down.

## Practice

**Build:** complete [Trace a Local HTTP Connection](./lab-local-http.md), then annotate the loopback route and socket endpoints. **Break:** stop the listener to separate routing success from transport refusal; if you own a namespace lab, remove and restore one route. **Explain back:** describe each local forwarding decision without implying routers create application sessions. Success is a layer-by-layer evidence table that identifies the first failed boundary and leaves networking state restored.

## Check yourself

1. What decision does a router make for each packet?
2. Why does knowing an IP address not prove reachability?

## Sources

### REQUIRED

- [RFC 8200: IPv6](https://www.rfc-editor.org/rfc/rfc8200)
- [RFC 791: IPv4](https://www.rfc-editor.org/rfc/rfc791)

### RECOMMENDED

- [ip-route manual](https://man7.org/linux/man-pages/man8/ip-route.8.html)

### DEEP DIVE

- [Computer Networks](https://www.pearson.com/en-us/subject-catalog/p/computer-networks/P200000003188)

## Next

Continue to [TCP, UDP, and Ports](./02-tcp-udp-and-ports.md).
