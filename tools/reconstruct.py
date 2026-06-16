#!/usr/bin/env python3
"""reconstruct.py — Rebuild canonical 8 KB payloads from raw XGpro reads.

Every Franklin chip in this archive was read with the XGpro M5L27256K@DIP28
device profile, producing 32 KB files with a fixed structure:

    0x0000-0x3FFF : 0xFF fill   (device /PGM pin driven low by profile's A14)
    0x4000-0x5FFF : payload     (mirror copy 1; profile's A13 not connected)
    0x6000-0x7FFF : payload     (mirror copy 2, identical by hardware)

The true device payload is therefore 8 KB, and every raw read supplies two
samples of each payload byte. With N raw reads of a chip, each byte position
has 2N samples. This script majority-votes all samples per position and
reports any position where no value wins an absolute majority (a "tie").
Tie positions are emitted to stdout and must be resolved by documentation,
never silently.

Usage:
    python3 reconstruct.py out.bin read1.bin [read2.bin ...]

Reproduces (given the raw_reads in this archive):
    PROD  5 reads -> 10 samples/byte ->  6 ties
    P1    7 reads -> 14 samples/byte -> 17 ties
    P2    3 reads ->  6 samples/byte ->  0 ties
    P3    3 reads ->  6 samples/byte ->  0 ties
"""
import sys
import hashlib
import collections

PAYLOAD = 8192
MIRROR_OFFSETS = (0x4000, 0x6000)


def reconstruct(read_paths):
    reads = [open(p, 'rb').read() for p in read_paths]
    for p, r in zip(read_paths, reads):
        if len(r) != 32768:
            raise SystemExit(f"{p}: expected 32768 bytes, got {len(r)}")
        if r[:0x4000].count(0xFF) != 0x4000:
            print(f"WARNING: {p}: lower 16 KB is not all 0xFF", file=sys.stderr)
    out = bytearray(PAYLOAD)
    ties = []
    for i in range(PAYLOAD):
        samples = [r[off + i] for r in reads for off in MIRROR_OFFSETS]
        counts = collections.Counter(samples)
        value, n = counts.most_common(1)[0]
        if n <= len(samples) // 2:
            # No absolute majority: deterministic tie-break, lowest
            # top-voted candidate. Ties are reported and documented;
            # the chosen byte is a flagged placeholder, not a finding.
            top = max(counts.values())
            value = min(v for v, k in counts.items() if k == top)
            ties.append((i, sorted(counts.items())))
        out[i] = value
    return bytes(out), ties


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    out_path, read_paths = sys.argv[1], sys.argv[2:]
    payload, ties = reconstruct(read_paths)
    open(out_path, 'wb').write(payload)
    print(f"{out_path}: {len(payload)} bytes, "
          f"{2*len(read_paths)} samples/byte, {len(ties)} unresolved ties")
    print(f"SHA-256: {hashlib.sha256(payload).hexdigest()}")
    for pos, counts in ties:
        votes = ', '.join(f"0x{v:02X}x{n}" for v, n in counts)
        print(f"  TIE at payload 0x{pos:04X}: {votes}")


if __name__ == '__main__':
    main()
