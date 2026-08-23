# Architectures and inductive bias

An architecture decides which relationships are easy to learn by encoding assumptions about locality, order, sharing, and symmetry.

## Why it matters

[Deep network training](06-deep-network-training.md) can optimize many functions. Data is finite, so useful structural bias often matters more than adding unconstrained parameters.

## How it works

Convolutions reuse a kernel across positions, encoding translation equivariance and reducing parameters. Receptive field grows with depth, dilation, and stride; padding and pooling change spatial resolution. Recurrent networks reuse a transition through sequence positions, making order explicit but creating long gradient paths. Gated variants regulate state retention.

Attention connects positions dynamically and will be developed in the next module. Graph neural networks aggregate over neighbors, encoding permutation symmetry over neighbor order. In every case, pooling converts structured states into task outputs and can discard location or identity.

Parameter sharing is a claim that the same detector or transition applies in multiple places. Equivariance means transforming input predictably transforms output; invariance means output remains unchanged. Augmentation and architecture should agree with true task symmetries.

## See it yourself

A width-three one-dimensional convolution with kernel `[1,0,-1]` applied to `[0,0,1,1]` detects the same edge wherever it occurs. A dense layer needs separate weights for each location. Shift the input one position and the interior convolution output shifts too.

Add zero padding at the boundary. The response now depends on invented zeros, showing that equivariance is not exact at every boundary.

## Where it shows up

For defect images, convolution uses local shared patterns and preserves spatial maps needed to locate defects. Global pooling may suit image-level classification but destroys exact location. Architecture follows the output contract, not fashion.

## When it breaks

Stride aliases small signals, padding creates edge artifacts, recurrence forgets long context, and pooling removes needed detail. An assumed invariance can be false: horizontally flipping text or medical laterality changes meaning.

Inspect intermediate shapes and receptive fields. Create controlled transformations and compare outputs. If a shift changes classification unexpectedly, distinguish boundary effects, preprocessing, and learned sensitivity with synthetic inputs.

## Practice

**Observe:** calculate a tiny convolution by hand. **Build:** compare a shared kernel with an untied local layer; completion includes parameter counts and shifted-input outputs. **Break:** use an invalid flip augmentation and document the label contradiction.

## Check yourself

1. What does convolution share?
2. How are invariance and equivariance different?
3. Why can global pooling harm localization?
4. Which test exposes a false augmentation assumption?

## Sources

### REQUIRED

- [Deep Learning, convolutional networks](https://www.deeplearningbook.org/contents/convnets.html)

### RECOMMENDED

- [PyTorch convolution documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)

### DEEP DIVE

- [Understanding the Effective Receptive Field in Deep Convolutional Neural Networks](https://arxiv.org/abs/1701.04128)

## Next

Continue to [Systematic ML debugging](08-systematic-ml-debugging.md).
