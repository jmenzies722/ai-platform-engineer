# Quantization and quality control

Quantization exchanges numerical resolution and range for lower memory traffic, smaller footprints, and potentially faster kernels.

## Why it matters

A smaller model is not automatically faster, and average benchmark quality can hide severe regressions on rare or safety-critical slices.

## How it works

Uniform quantization maps real value \(x\) to an integer using scale \(s\) and optional zero point \(z\), approximately \(q=\mathrm{round}(x/s)+z\). Granularity may be tensor, channel, or group. Post-training quantization uses calibration; quantization-aware training exposes the model to simulated error. Weight-only methods save weight bandwidth, while activation and KV-cache quantization address other memory.

End-to-end gain requires kernels that consume the representation without repeated dequantization. Evaluate footprint, load time, prefill and decode latency, throughput, energy, and accuracy against an immutable higher-precision baseline.

## See it yourself

Values from -1 to 1 with symmetric int8 scale \(1/127\) resolve increments near 0.00787. A single outlier of 100 changes scale to \(100/127\), so ordinary values receive coarse resolution. Per-channel scales can isolate the outlier. This proves calibration distribution affects error.

## Where it shows up

A release matrix tests model digest, quantizer, calibration digest, runtime, hardware, and representative shapes. Quality gates include aggregate tasks, long context, languages, tool formatting, calibration error, and high-consequence slices.

## When it breaks

Outliers saturate, accumulators overflow, unsupported operators fall back, memory savings vanish in workspaces, and calibration data leaks or drifts. Compare layer errors, saturation rates, fallback events, kernel traces, and slice metrics. Roll back the artifact, not merely a configuration flag, because scales are model state.

## Practice

**Observe:** quantize a skewed vector globally and per channel. **Build:** define a release scorecard with quality guardrails. **Break:** calibrate on an unrepresentative slice and force one operator fallback. Completion requires finding both the quality and latency regression.

## Check yourself

1. Why can int4 weights produce no speedup?
2. Which artifact makes quantization reproducible?
3. When is average task accuracy an unsafe gate?

## Sources

### REQUIRED

- [PyTorch quantization documentation](https://docs.pytorch.org/docs/stable/quantization.html)

### RECOMMENDED

- [ONNX Runtime quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)

### DEEP DIVE

- [GPTQ](https://arxiv.org/abs/2210.17323)

## Next

Continue to [Advanced serving topologies](07-routing-autoscaling-and-overload.md).
