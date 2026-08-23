# Cryptography, key management, and TLS

Cryptography supplies narrow properties under explicit assumptions. Secure systems choose maintained protocols, bind context, manage keys through their lifecycle, and fail closed when verification cannot be completed.

## Why it matters

Incorrect assumptions here create failures that survive ordinary unit tests and emerge under delay, overload, failover, or adversarial behavior. The mechanism matters because it turns an implicit assumption into a contract that can be tested and operated.

## How it works

Authenticated encryption provides confidentiality and integrity; digital signatures provide origin authentication and integrity, not secrecy. Hashes support integrity constructions but plain fast hashes are unsuitable for passwords; use a memory-hard password KDF with salt. Nonces must obey algorithm-specific uniqueness or randomness rules.

TLS authenticates endpoints and protects data in transit. Certificate validation checks chain, hostname, validity, and policy. Modern deployments automate issuance and rotation, prefer TLS 1.3, restrict trust roots, and protect private keys in managed key systems where appropriate.

## See it yourself

For a 96-bit uniformly random nonce, collision probability grows roughly with the square of messages; deterministic counters can guarantee uniqueness per key if never reset. Reusing a nonce in GCM can reveal relationships and undermine authentication, showing that key and nonce state are protocol state.

## Where it shows up

Envelope encryption uses a data key per object and a key-encryption key in a managed system. Record algorithm, key identifier, context, and version so rotation and decryption remain possible.

## When it breaks

Homegrown encryption omits authentication, hostname checks can be disabled, roots can be overbroad, keys can be copied into images, and rotation can make old data unreadable. Test negative verification, expiry, revocation assumptions, and restore with rotated keys.

## Practice

Encrypt and authenticate a local message using a maintained library, then alter ciphertext and associated data. Completion means both changes fail verification, plaintext is never returned on failure, and a written design covers generation, storage, rotation, revocation, and destruction.

## Check yourself

1. Which properties does authenticated encryption provide?
2. Why must TLS validate hostname as well as signature?
3. How does envelope encryption aid rotation?
4. What breaks when a GCM nonce repeats?

## Sources

### REQUIRED

- [NIST SP 800-52 Rev. 2](https://csrc.nist.gov/pubs/sp/800/52/r2/final)

### RECOMMENDED

- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

### DEEP DIVE

- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)

## Next

[Secrets and credential lifecycles](04-secrets-management.md)
