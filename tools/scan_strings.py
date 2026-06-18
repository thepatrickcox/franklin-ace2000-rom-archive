#!/usr/bin/env python3
"""scan_strings.py — Find human-readable content in a ROM image.

Two functions, used to characterize the Franklin payloads:

1. Fragment search: scan the whole image (and, with --gaps, only the
   zero-fill regions) for runs of printable ASCII in both plain and
   high-bit-set encodings, filtering to runs that look like English text
   or 6502 assembler mnemonics. Used to confirm that no leftover assembler
   source or developer comments survive in the ACE 2000-series set.

2. Keyword table: with --tokens, parse a high-bit-terminated token table
   (the Applesoft BASIC keyword list) starting at a given address. Used to
   show that P2's interpreter keyword set is Franklin-customized (cassette
   tokens removed, FKEY added).

Usage:
    python3 scan_strings.py <image.bin> <base_hex> [--gaps] [--minlen N]
    python3 scan_strings.py <image.bin> <base_hex> --tokens <start_hex>
"""
import sys
import re

ASM = re.compile(r'\b(LDA|STA|LDX|LDY|STX|STY|JSR|JMP|RTS|BEQ|BNE|BCC|BCS|'
                 r'INC|DEC|CMP|ORA|AND|EOR|ADC|SBC|TAX|TAY|TXA|TYA|PHA|PLA|'
                 r'CLC|SEC|NOP|BIT|ROL|ROR|ASL|LSR)\b')
ENGLISH = re.compile(r'\b(fix|bug|error|the|and|for|with|byte|page|rom|code|'
                     r'test|version|patch|note|todo|temp|buffer|routine|table|'
                     r'jump|call|init|check|loop)\b', re.I)


def fill_gaps(d, minrun=16):
    gaps, i = [], 0
    while i < len(d):
        if d[i] in (0x00, 0xFF):
            j = i
            while j < len(d) and d[j] == d[i]:
                j += 1
            if j - i >= minrun:
                gaps.append((i, j))
            i = j
        else:
            i += 1
    return gaps


def scan(d, base, minlen, gaps_only):
    regions = fill_gaps(d) if gaps_only else [(0, len(d))]
    for lo, hi in regions:
        seg = d[lo:hi]
        for masked in (False, True):
            chars = []
            for b in seg:
                c = (b & 0x7F) if masked else b
                chars.append(chr(c) if 32 <= c < 127 else '\x00')
            txt = ''.join(chars)
            for m in re.finditer(r'[ -~]{%d,}' % minlen, txt):
                s = m.group()
                asm, eng = ASM.search(s), ENGLISH.search(s)
                low = sum(c.islower() for c in s)
                up = sum(c.isupper() for c in s)
                if asm or eng or (low >= 3 and up >= 2 and ' ' in s and len(s) >= 8):
                    enc = 'masked' if masked else 'plain'
                    tag = f"asm={'Y' if asm else '-'} eng={'Y' if eng else '-'}"
                    print(f"  ${base + lo + m.start():04X} [{enc}] {tag}: {s!r}")


def tokens(d, base, start):
    out, cur, i = [], [], start - base
    while i < len(d):
        b = d[i]
        c = b & 0x7F
        if not (32 <= c < 127):
            break
        cur.append(chr(c))
        if b & 0x80:
            out.append(''.join(cur))
            cur = []
        i += 1
    print(f"Parsed {len(out)} high-bit-terminated tokens from ${start:04X}:")
    print(' | '.join(out))


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    d = open(sys.argv[1], 'rb').read()
    base = int(sys.argv[2], 16)
    if '--tokens' in sys.argv:
        start = int(sys.argv[sys.argv.index('--tokens') + 1], 16)
        tokens(d, base, start)
        return
    minlen = 6
    if '--minlen' in sys.argv:
        minlen = int(sys.argv[sys.argv.index('--minlen') + 1])
    gaps_only = '--gaps' in sys.argv
    print(f"== {sys.argv[1]} (base ${base:04X}) "
          f"{'fill-gaps only' if gaps_only else 'full image'} ==")
    scan(d, base, minlen, gaps_only)


if __name__ == '__main__':
    main()
