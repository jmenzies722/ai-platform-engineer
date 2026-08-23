# Kernels, precision, and performance

Kernel performance is governed by useful work, memory traffic, launch overhead, and numerical representation.

## Why it matters

Optimization without measurement can make code less accurate and no faster.

## How it works

Arithmetic intensity is operations per byte moved. A roofline compares this intensity with memory bandwidth and compute limits. Fusion reduces intermediate writes and launches. Lower precision improves throughput and memory use, but accumulation, scaling, and sensitive operations may require wider types. Profilers distinguish host delay, copies, kernel time, stalls, and synchronization.

The attainable rate is bounded by the smaller of peak compute and bandwidth times arithmetic intensity. Fusion raises intensity only when it actually avoids traffic; it can also increase register pressure and reduce occupancy. Reduced precision changes range and spacing as well as storage. Quantization needs a scale and zero point or codebook, and calibration data determines which values receive resolution.

## See it yourself

For `c=a+b` on FP32 vectors, each element performs one addition and moves roughly 12 bytes, about 0.083 operations per byte. A square \(n\times n\) matrix multiply performs about \(2n^3\) operations while ideally moving \(12n^2\) bytes, intensity near \(n/6\). At \(n=1024\), reuse can make compute the limit. This calculation predicts why fusion helps elementwise chains more than already tiled matrix multiplication.

## Where it shows up

In quantized model serving, int8 weights reduce memory bandwidth and footprint, but activation outliers can dominate one scale and damage rare cases. Teams therefore benchmark both kernel latency and task slices against an accuracy tolerance. A faster kernel that forces dequantization between every layer can lose the expected end-to-end gain.

## When it breaks

Overflow, underflow, quantization error, hidden synchronization, and tiny shapes defeat expected gains. First profile an end-to-end trace and compare output error against a trusted higher-precision baseline. Non-finite values suggest range failure; slice-specific drift suggests calibration; gaps between kernels suggest launch or synchronization overhead.

## Practice

**Build:** calculate a roofline bound, profile the operation, and state whether evidence supports compute or bandwidth limitation. **Break:** lower precision until a known numerical test fails and fuse until register pressure hurts occupancy. **Explain back:** defend one optimization with both latency and correctness measurements.

## Check yourself

1. What does fusion save?
2. Why use wider accumulation?
3. What does a roofline not capture?

## Sources

### REQUIRED

- [Nsight Compute documentation](https://docs.nvidia.com/nsight-compute/)

### RECOMMENDED

- [PyTorch numerical accuracy](https://docs.pytorch.org/docs/stable/notes/numerical_accuracy.html)

### DEEP DIVE

- [Roofline model](https://doi.org/10.1145/1498765.1498785)

## Next

Continue to [Multi-GPU communication](03-multi-gpu-communication.md).
