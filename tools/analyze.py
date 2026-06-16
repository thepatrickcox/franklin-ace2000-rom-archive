#!/usr/bin/env python3
"""analyze.py — Structural analysis of the canonical Franklin payloads.

Reports, for a given 8 KB payload and base address:
  * 6502/65C02 hardware vectors (NMI/RESET/IRQ) read from the top of image
  * High-bit-masked ASCII strings
  * All absolute JSR/JMP references, bucketed by target page, to expose
    cross-chip calls between the $C000 ROM and the $E000 ROM
  * Bytes at canonical Apple II Monitor entry points (for the E000 image)

Usage:
    python3 analyze.py <payload.bin> <base_hex>
Example:
    python3 analyze.py franklin_ace2000_C000_beta_P2.bin C000
"""
import sys
import collections
from dis65c02 import OPS, disassemble


def masked_strings(data, minlen=5):
    out, cur, start = [], [], 0
    for i, b in enumerate(data):
        c = b & 0x7F
        if 0x20 <= c < 0x7F:
            if not cur:
                start = i
            cur.append(chr(c))
        else:
            if len(cur) >= minlen:
                out.append((start, ''.join(cur)))
            cur = []
    if len(cur) >= minlen:
        out.append((start, ''.join(cur)))
    return out


def abs_refs(data, base):
    refs, pc = [], 0
    while pc < len(data) - 2:
        o = data[pc]
        if o in OPS:
            mn, mode, ln = OPS[o]
            if ln == 3 and mode in ('abs', 'ind', 'iax', 'abx', 'aby'):
                refs.append((base + pc, mn, data[pc+1] | data[pc+2] << 8))
            pc += ln
        else:
            pc += 1
    return refs


APPLE_MONITOR_ENTRY_POINTS = [
    (0xF800, 'PLOT'), (0xFB2F, 'INIT'), (0xFC58, 'HOME'), (0xFD0C, 'RDKEY'),
    (0xFD6A, 'GETLN'), (0xFD8E, 'CROUT'), (0xFDDA, 'PRBYTE'), (0xFDED, 'COUT'),
    (0xFE84, 'SETNORM'), (0xFE89, 'SETKBD'), (0xFE93, 'SETVID'), (0xFF3A, 'BELL'),
]


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    data = open(sys.argv[1], 'rb').read()
    base = int(sys.argv[2], 16)

    print(f"== {sys.argv[1]} (base ${base:04X}) ==")
    if base + len(data) == 0x10000:
        nmi = data[-6] | data[-5] << 8
        rst = data[-4] | data[-3] << 8
        irq = data[-2] | data[-1] << 8
        print(f"Vectors: NMI=${nmi:04X} RESET=${rst:04X} IRQ=${irq:04X}")

    print("\nMasked ASCII strings (len >= 8):")
    for off, s in masked_strings(data, 8):
        print(f"  ${base+off:04X}: {s!r}")

    refs = abs_refs(data, base)
    flow = [r for r in refs if r[1] in ('JSR', 'JMP')]
    pages = collections.Counter(t >> 12 for _, _, t in flow)
    print("\nJSR/JMP target distribution by 4 KB page:")
    for pg in sorted(pages):
        print(f"  ${pg:X}xxx: {pages[pg]}")

    lo, hi = base, base + len(data)
    external = [r for r in flow if not (lo <= r[2] < hi) and r[2] >= 0xC000]
    print(f"\nJSR/JMP to ROM space outside this image: {len(external)}")
    top = collections.Counter(f"${t:04X}" for _, _, t in external).most_common(12)
    for tgt, n in top:
        print(f"  {tgt}: {n}")

    if base == 0xE000:
        print("\nApple II Monitor canonical entry points:")
        for addr, name in APPLE_MONITOR_ENTRY_POINTS:
            line = ' ; '.join(t for _, _, t in disassemble(data, base, addr, 3))
            print(f"  ${addr:04X} {name:<8}: {line}")


if __name__ == '__main__':
    main()
