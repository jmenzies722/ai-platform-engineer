# Bits, Bytes, and Representation

Computers store patterns of bits; meaning comes from the representation and the operation interpreting those bits.

## Why it matters

A protocol field containing the bytes `00 10` can mean sixteen, 4096, two characters, or part of a floating-point value depending on width, byte order, and schema. Production corruption often begins when two components agree on bytes but not meaning. Representation choices therefore belong in interfaces, migrations, and test vectors rather than in undocumented assumptions.

## How it works

Binary positional notation encodes integers. Fixed-width unsigned arithmetic wraps modulo a power of two; signed integers commonly use two’s complement. Text encodings map characters to code points and bytes. Floating-point represents a finite set of approximations, not all real numbers.

A bit has two states; positional binary gives each position a power-of-two weight. Fixed width bounds the representable set, so unsigned arithmetic is modular and signed two’s-complement uses the top bit’s weight to extend negative values. Endianness specifies byte order for multi-byte quantities, not bit order inside ordinary notation. Unicode assigns code points, while UTF-8 encodes those points into one to four bytes; characters perceived by a user can contain multiple code points. IEEE 754 floating point stores sign, exponent, and significand, providing finite precision, signed zeros, infinities, and NaNs. Parsing is the boundary that attaches one of these meanings to bytes. Serialization must specify width, order, encoding, and invalid-input behavior so the inverse operation is well defined.

## See it yourself

Predict that thirteen appears as `0b1101` and two big-endian bytes, that `é` has one Python code point but two UTF-8 bytes, and that `0.1 + 0.2` is not printed as exact decimal 0.3.

```bash
python3 - <<'PY2'
n = 13
print(bin(n), n.to_bytes(2, 'big'))
text = 'é'
print(text.encode('utf-8'), len(text), len(text.encode('utf-8')))
print(0.1 + 0.2)
PY2
```

Expected observation: One character can occupy multiple UTF-8 bytes, and decimal fractions may not have exact binary floating-point representations.

Limits of the bits, bytes, and representation observation: The output does not explain every Unicode grapheme, prove a language’s integer storage width, or imply floating-point arithmetic is random. Python integers are arbitrary precision, and its displayed float is a shortest useful decimal representation of a binary value.

## Where it shows up

Database and API boundaries expose representation mismatches sharply. Storing money as binary floating point can accumulate rounding that violates accounting rules; storing it as integer minor units or a specified decimal type makes rounding policy explicit. Likewise, truncating UTF-8 by bytes can split an encoded code point and produce invalid text. Schema constraints and round-trip fixtures catch these failures before values cross services.

## When it breaks

Mojibake suggests decoding with the wrong character encoding; swapped magnitudes suggest endian disagreement; values that jump at a width boundary suggest overflow or truncation; small numerical drift suggests finite precision or unstable calculation. First preserve the original bytes in hexadecimal alongside the declared schema and decoder settings. Re-encoding a rendered string loses evidence and can compound corruption.

## Practice

**Build:** define a four-byte message containing a big-endian unsigned length and UTF-8 payload, with encode and decode functions. **Break:** decode the length as little-endian and truncate a multi-byte character, capturing both failure modes. **Explain back:** separate value, code point, byte sequence, width, and interpretation. Success is a set of round-trip tests plus fixed hexadecimal vectors that another implementation could consume.

## Check yourself

1. Why is a byte pattern meaningless without a representation?
2. Why can `len(text)` differ from encoded byte length?

## Sources

### REQUIRED

- [Unicode Standard](https://www.unicode.org/versions/latest/)

### RECOMMENDED

- [IEEE 754 overview](https://standards.ieee.org/ieee/754/6210/)

### DEEP DIVE

- [Computer Systems: A Programmer’s Perspective](https://csapp.cs.cmu.edu/)

## Next

Continue to [Instructions, CPU, and Memory](./02-instructions-cpu-and-memory.md).
