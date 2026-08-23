# Regions, VPCs, and network boundaries

AWS places resources in geographic Regions and fault-isolated Availability Zones, then gives you a software-defined VPC in which to control addressing and routes.

## Why it matters

Availability and data residency depend on placement. Reachability depends on several independent controls; calling a subnet "public" does not make every resource in it reachable.

## How it works

A Region contains multiple Availability Zones. A VPC owns one or more CIDR ranges. Subnets are AZ-scoped slices of those ranges. Route tables decide the next hop; an internet gateway can route public addresses; NAT lets private IPv4 clients initiate internet connections without accepting unsolicited inbound ones.

Security groups are stateful rules attached to network interfaces. Network ACLs are stateless subnet rules and must permit both request and return traffic. DNS names often resolve to changing addresses, so applications should use names rather than pinning IPs.

A subnet is conventionally public when its associated route table reaches an internet gateway and a workload has a public address; reachability still requires security controls and a listener. NAT gateways translate outbound IPv4 flows but do not provide inbound publication, and one NAT per AZ avoids cross-AZ dependency and transfer at additional cost. Gateway and interface VPC endpoints provide private routes or interfaces to supported service APIs, with endpoint and service policies adding authorization layers.

VPC peering is non-transitive. Transit Gateway centralizes routing across many networks, while PrivateLink exposes a service without general routed connectivity. Choose address space before connection: overlapping CIDRs make routing and future acquisition integration difficult. Flow Logs record accepted or rejected metadata at supported interfaces, not packet contents or application success.

## Vocabulary

- **route:** destination prefix and next hop
- **security group:** stateful interface firewall
- **endpoint:** private VPC access to a service API

## See it yourself

For one VPC, sketch its CIDRs, subnets, route-table associations, gateways, endpoints, and security-group edges. Predict the forward and return path for one client connection. A packet reaches an instance only when DNS, addressing, route, gateway or translation, network ACL, security group, and listening process agree. Use Reachability Analyzer or Flow Logs when approved, but treat them as network evidence rather than proof of application correctness.

## Where it shows up

Multi-AZ load balancers distribute traffic across failure domains, private service endpoints keep supported API traffic off public internet paths, and egress proxies make destinations and policy observable. Transit gateways connect many VPCs but also enlarge the routing blast radius. Production diagrams should show DNS authority, ingress, egress, inspection, shared services, route ownership, and every AZ-specific dependency.

## When it breaks

Overlapping CIDRs prevent clean routing. Missing return routes look like firewall failures. Stateless ACL ephemeral-port mistakes drop replies. A permissive security group does not repair a process bound only to `127.0.0.1`. MTU or path fragmentation can break large requests while pings work. DNS and endpoint policy failures can resemble routing problems. One-AZ NAT, endpoint, or data dependencies defeat nominally multi-AZ compute.

Debug from name resolution through each hop and back. Record source and destination addresses, protocol and port, route selection, translation, rule decisions, listener, TLS result, and request ID. Change one layer at a time; opening every rule destroys diagnostic and security evidence.

## Practice

**Observe:** map a real or sample VPC and trace one successful and one denied flow in both directions with cited evidence.

**Build:** design private application and data subnets across at least two AZs. State exactly how users, administrators, applications, updates, DNS, and AWS APIs are reached and price the egress design.

**Break safely:** remove one sandbox route or security-group rule and predict the symptom. Completion means route, firewall, listener, and application failures can be distinguished without using an allow-all rule.

## Check yourself

1. What properties make a subnet conventionally public?
2. Why can a network ACL drop reply traffic that a security group permits?

## Sources

### REQUIRED
- [Amazon VPC concepts](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)

### RECOMMENDED
- [AWS Availability Zones](https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-availability-zones.html)

### DEEP DIVE
- [AWS VPC security best practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)

## Next

[Compute, storage, and managed data](03-compute-storage-data.md)
