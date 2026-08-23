# Regions, VPCs, and network boundaries

AWS places resources in geographic Regions and fault-isolated Availability Zones, then gives you a software-defined VPC in which to control addressing and routes.

## Why it matters

Availability and data residency depend on placement. Reachability depends on several independent controls; calling a subnet "public" does not make every resource in it reachable.

## How it works

A Region contains multiple Availability Zones. A VPC owns one or more CIDR ranges. Subnets are AZ-scoped slices of those ranges. Route tables decide the next hop; an internet gateway can route public addresses; NAT lets private IPv4 clients initiate internet connections without accepting unsolicited inbound ones.

Security groups are stateful rules attached to network interfaces. Network ACLs are stateless subnet rules and must permit both request and return traffic. DNS names often resolve to changing addresses, so applications should use names rather than pinning IPs.

## Vocabulary

- **route:** destination prefix and next hop
- **security group:** stateful interface firewall
- **endpoint:** private VPC access to a service API

## See it yourself

For one VPC, sketch its CIDRs, subnets, route-table associations, gateways, and security-group edges. A packet reaches an instance only when addressing, route, gateway, firewall, and listening process all agree.

## Where it shows up

Multi-AZ load balancers distribute traffic across failure domains. Private service endpoints keep supported API traffic off public internet paths. Transit gateways connect many VPCs but also enlarge the routing blast radius.

## When it breaks

Overlapping CIDRs prevent clean routing. Missing return routes look like firewall failures. A permissive security group does not repair a process bound only to `127.0.0.1`. One-AZ dependencies defeat a nominally multi-AZ service.

## Practice

Design two private application subnets and two data subnets across two AZs. State exactly how administrators, applications, updates, and AWS APIs are reached.

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
