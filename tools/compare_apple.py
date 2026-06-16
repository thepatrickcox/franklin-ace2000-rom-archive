#!/usr/bin/env python3
"""compare_apple.py — Byte-level similarity between Franklin payloads and
Apple II reference ROMs.

Method:
  1. 32-byte sliding-window intersection: the count of distinct 32-byte
     sequences present in both images (step 1, exact match).
  2. 64-byte sliding-window intersection: same at 64 bytes.
  3. Longest common substring (LCS): seed 16-byte matches, extend greedily,
     report the single longest contiguous shared run and its offsets.

Interpretation standard used in this archive: shared runs are reported as
raw byte counts with offsets, with the content of the longest run identified
in the analysis documents. No similarity percentage is derived, because
window intersection counts are not commensurable with authorship claims;
the numbers are reported as measured.

Usage:
    python3 compare_apple.py <franklin.bin> <apple_rom_dir>
"""
import sys
import os
import glob


def windows(d, w):
    return {d[i:i+w] for i in range(len(d) - w + 1)}


def longest_common(a, b, seed=16):
    pos = {}
    for j in range(len(b) - seed + 1):
        pos.setdefault(b[j:j+seed], []).append(j)
    best = (0, -1, -1)
    for i in range(len(a) - seed + 1):
        s = a[i:i+seed]
        if s in pos:
            for j in pos[s]:
                L = seed
                while i + L < len(a) and j + L < len(b) and a[i+L] == b[j+L]:
                    L += 1
                if L > best[0]:
                    best = (L, i, j)
    return best


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    fd = open(sys.argv[1], 'rb').read()
    f32, f64 = windows(fd, 32), windows(fd, 64)
    print(f"{'Apple reference ROM':<62} {'w32':>5} {'w64':>5} {'LCS':>5}")
    overall = (0, '', -1, -1)
    for path in sorted(glob.glob(os.path.join(sys.argv[2], '*.bin'))):
        ad = open(path, 'rb').read()
        name = os.path.basename(path)
        s32 = len(f32 & windows(ad, 32))
        s64 = len(f64 & windows(ad, 64))
        L, i, j = longest_common(fd, ad)
        print(f"{name[:62]:<62} {s32:>5} {s64:>5} {L:>5}")
        if L > overall[0]:
            overall = (L, name, i, j)
    L, name, i, j = overall
    if L:
        print(f"\nLongest shared run overall: {L} bytes")
        print(f"  Franklin offset 0x{i:04X} vs {name} offset 0x{j:04X}")
        print(f"  bytes: {fd[i:i+min(L,64)].hex()}")


if __name__ == '__main__':
    main()
