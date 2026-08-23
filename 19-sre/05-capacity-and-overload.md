# Capacity planning and overload

Capacity planning connects forecast demand to the first bottleneck under realistic service levels. Overload control ensures the system degrades deliberately when demand or dependency latency exceeds that capacity.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Define workload units, demand distribution, service-time distribution, concurrency, resource limits, and headroom. Little’s Law relates average concurrency `L`, arrival rate `λ`, and time `W`. Load tests must preserve request mix, data shape, cache state, and dependency behavior.

Admission control, load shedding, bounded queues, priority, and graceful degradation protect critical work. Autoscaling reacts after measurement delay and cannot create downstream capacity or fix an architectural bottleneck.

## See it yourself

At 2,000 requests/s and 200 ms average time, expected concurrency is `2,000 × 0.2 = 400`. Provisioning only 200 concurrent slots guarantees a queue or rejection even if CPU averages seem comfortable.

## Where it shows up

Forecast normal growth, event peaks, failover capacity, and recovery backlog. Track utilization and saturation at the constrained resource. Test at the SLO boundary and with one failure domain absent.

## When it breaks

Coordinated omission hides queued latency, averages hide hot keys, autoscaling oscillates, and retries make offered load exceed user demand. Measure arrivals before retries, completions, rejections, queue age, and bottleneck saturation.

## Practice

Create a closed-form capacity model and test it with a local worker pool. Double service time and remove one-third of workers. Completion means observed saturation matches the model, admission bounds latency, and priority work remains available.

## Check yourself

1. How does service time affect required concurrency?
2. Why is utilization insufficient without saturation?
3. What does coordinated omission hide?
4. Which capacity must remain during a zone failure?

## Sources

### REQUIRED

- [Google SRE: Handling Overload](https://sre.google/sre-book/handling-overload/)

### RECOMMENDED

- [Google SRE: Software Engineering in SRE](https://sre.google/sre-book/software-engineering-in-sre/)

### DEEP DIVE

- [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/)

## Next

[Availability architecture and failure domains](06-availability-engineering.md)
