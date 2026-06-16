#!/usr/bin/env python3
"""build_data_appendix.py — Regenerates analysis/DATA_APPENDIX.md from the
binaries in roms/. Every number in the appendix is computed at build time;
nothing is transcribed by hand. Run from the repository root:

    python3 tools/build_data_appendix.py > analysis/DATA_APPENDIX.md
"""
import sys
import os
import glob
import hashlib
import itertools
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dis65c02 import OPS, disassemble

RAW = 'roms/raw_reads'
CAN = 'roms/canonical'

GROUPS = {
    'PROD': sorted(glob.glob(f'{RAW}/franklin 1984-1985*.BIN')
                   + glob.glob(f'{RAW}/1984-1985_labeled*.BIN')),
    'P1':   sorted(glob.glob(f'{RAW}/frankin beta rom P1*.BIN')
                   + glob.glob(f'{RAW}/p1_*.BIN')),
    'P2':   sorted(glob.glob(f'{RAW}/franklin beta rom P2*.BIN')
                   + glob.glob(f'{RAW}/p2_*.BIN')),
    'P3':   sorted(glob.glob(f'{RAW}/Franklin beta rom P3*.BIN')
                   + glob.glob(f'{RAW}/p3_*.BIN')),
}
CANON = {
    'PROD': f'{CAN}/franklin_ace2000_E000_V5.0_production.bin',
    'P1':   f'{CAN}/franklin_ace2000_E000_V5.2_beta_P1.bin',
    'P2':   f'{CAN}/franklin_ace2000_C000_beta_P2.bin',
    'P3':   f'{CAN}/franklin_ace2000_disk_beta_P3.bin',
}
BASE = {'PROD': 0xE000, 'P1': 0xE000, 'P2': 0xC000, 'P3': None}


def sha(d): return hashlib.sha256(d).hexdigest()
def s32(d): return sum(d) & 0xFFFFFFFF


def samples(reads, i):
    return [r[0x4000 + i] for r in reads] + [r[0x6000 + i] for r in reads]


def main():
    P = {n: open(p, 'rb').read() for n, p in CANON.items()}
    R = {n: [open(p, 'rb').read() for p in ps] for n, ps in GROUPS.items()}

    print("# Data Appendix")
    print()
    print("Machine-generated from the binaries in `roms/` by"
          " `tools/build_data_appendix.py`. Regenerate after any change to"
          " the binaries; do not edit by hand.")

    # --- raw read inventory ---
    print("\n## 1. Raw read inventory\n")
    print("| Chip | File | SHA-256 (first 16) | 32-bit sum |")
    print("|---|---|---|---|")
    for n, ps in GROUPS.items():
        for p in ps:
            d = open(p, 'rb').read()
            print(f"| {n} | {os.path.basename(p)} | `{sha(d)[:16]}` | `0x{s32(d):08X}` |")

    # --- read stability ---
    print("\n## 2. Read-to-read stability\n")
    print("Pairwise differing-byte counts across the full 32 KB images.\n")
    for n, reads in R.items():
        if len(reads) == 1:
            continue
        pairs = [f"r{i+1}/r{j+1}={sum(1 for x, y in zip(a, b) if x != y)}"
                 for (i, a), (j, b) in itertools.combinations(enumerate(reads), 2)]
        print(f"* **{n}** ({len(reads)} reads): {', '.join(pairs)}")

    # --- structure ---
    print("\n## 3. 32 KB image structure (all chips)\n")
    print("| Chip | 0x0000-0x3FFF | 0x4000-0x5FFF vs 0x6000-0x7FFF (per read) |")
    print("|---|---|---|")
    for n, reads in R.items():
        d = reads[0]
        ff = d[:0x4000].count(0xFF)
        md = sum(1 for x, y in zip(d[0x4000:0x6000], d[0x6000:0x8000]) if x != y)
        print(f"| {n} | {ff}/16384 bytes 0xFF | {md} differing bytes (read 1) |")

    # --- canonical payloads ---
    print("\n## 4. Canonical 8 KB payloads\n")
    print("| Chip | File | Samples/byte | Ties | SHA-256 |")
    print("|---|---|---|---|---|")
    tie_detail = {}
    for n in P:
        reads = R[n]
        ties = []
        for i in range(8192):
            c = collections.Counter(samples(reads, i))
            top, cnt = c.most_common(1)[0]
            if cnt <= 2 * len(reads) // 2:
                ties.append((i, sorted(c.items())))
        tie_detail[n] = ties
        print(f"| {n} | `{os.path.basename(CANON[n])}` | {2*len(reads)} "
              f"| {len(ties)} | `{sha(P[n])}` |")

    print("\n### 4.1 Unresolved tie positions\n")
    for n, ties in tie_detail.items():
        if not ties:
            continue
        b = BASE[n] or 0
        sister = {'PROD': 'P1', 'P1': 'PROD'}.get(n)
        print(f"**{n}** ({len(ties)}):\n")
        print("| Payload offset | Address | Votes | Canonical | Sister chip (stable?) |")
        print("|---|---|---|---|---|")
        for i, c in ties:
            votes = ' / '.join(f"0x{v:02X}×{k}" for v, k in c)
            addr = f"${b+i:04X}" if BASE[n] else "—"
            note = "—"
            if sister:
                ss = samples(R[sister], i)
                note = (f"0x{ss[0]:02X} (stable)" if len(set(ss)) == 1
                        else "unstable")
            print(f"| 0x{i:04X} | {addr} | {votes} | 0x{P[n][i]:02X} | {note} |")
        print()

    # --- PROD vs P1 ---
    print("## 5. PROD (V5.0) vs P1 (V5.2)\n")
    a, b = P['PROD'], P['P1']
    diffs = [i for i in range(8192) if a[i] != b[i]]
    xh = collections.Counter(a[i] ^ b[i] for i in diffs)
    print(f"Differing bytes: {len(diffs)} of 8192 "
          f"({100*(8192-len(diffs))/8192:.2f}% identical).")
    top = ', '.join(f"0x{x:02X}×{n}" for x, n in xh.most_common(6))
    print(f"XOR histogram (top 6): {top}.")
    stable = []
    for i in diffs:
        if len(set(samples(R['P1'], i))) == 1 and len(set(samples(R['PROD'], i))) == 1:
            stable.append(i)
    print(f"Positions where both chips read internally stable yet differ: "
          f"{len(stable)} of {len(diffs)}.")
    d1 = sum(1 for i in stable if (a[i] ^ b[i]) & a[i] == (a[i] ^ b[i]))
    d2 = sum(1 for i in stable if (a[i] ^ b[i]) & b[i] == (a[i] ^ b[i]))
    print(f"Direction among stable differences: PROD carries the set bits in "
          f"{d1}, P1 in {d2}.")
    buckets = collections.Counter(i // 512 for i in stable)
    print("\nSpatial distribution of stable differences (512-byte buckets, "
          "$E000 base):\n")
    print("| Range | Count |")
    print("|---|---|")
    for k in range(16):
        print(f"| ${0xE000+512*k:04X}-${0xE000+512*k+511:04X} | {buckets.get(k, 0)} |")

    # --- semantic anchors ---
    print("\n### 5.1 Semantic anchor points\n")
    print("Version string region (payload 0x18E0-0x18FA, high bit masked):\n")
    for n in ('PROD', 'P1'):
        t = bytes(x & 0x7F for x in P[n][0x18E0:0x18FA])
        print(f"* {n}: `{t}`")
    print("\nMonitor hex-digit table (payload 0x19AB-0x19BB, high bit masked):\n")
    for n in ('PROD', 'P1'):
        t = bytes(x & 0x7F for x in P[n][0x19AB:0x19BB])
        print(f"* {n}: `{t}`")

    # --- boot chain ---
    print("\n## 6. Boot chain listings\n")
    print("PROD, RESET vector target:\n```")
    for ad, raw, txt in disassemble(P['PROD'], 0xE000, 0xFA62, 1):
        print(f"${ad:04X}: {' '.join(f'{x:02X}' for x in raw):<9} {txt}")
    for ad, raw, txt in disassemble(P['PROD'], 0xE000, 0xF7FD, 1):
        print(f"${ad:04X}: {' '.join(f'{x:02X}' for x in raw):<9} {txt}")
    print("```\n\nP2, boot orchestrator at $DEFE (first 24 instructions):\n```")
    for ad, raw, txt in disassemble(P['P2'], 0xC000, 0xDEFE, 24):
        print(f"${ad:04X}: {' '.join(f'{x:02X}' for x in raw):<9} {txt}")
    print("```")
    rec = []
    for r in R['PROD']:
        rec += [r[0x4000 + 0x17FF], r[0x6000 + 0x17FF]]
    print(f"\nByte $F7FF across all {len(rec)} production-chip samples: "
          f"{' '.join(f'0x{x:02X}' for x in rec)}.")

    # --- cross refs ---
    print("\n## 7. Cross-chip references\n")
    def flow_refs(d, base):
        out, pc = [], 0
        while pc < len(d) - 2:
            o = d[pc]
            if o in OPS:
                mn, mode, ln = OPS[o]
                if ln == 3 and mode in ('abs',) and mn in ('JSR', 'JMP'):
                    out.append((base + pc, mn, d[pc+1] | d[pc+2] << 8))
                pc += ln
            else:
                pc += 1
        return out
    pr = [r for r in flow_refs(P['PROD'], 0xE000) if 0xC100 <= r[2] <= 0xDFFF]
    p2 = [r for r in flow_refs(P['P2'], 0xC000) if 0xE000 <= r[2] <= 0xFFFF]
    print(f"PROD JSR/JMP into $C100-$DFFF: {len(pr)}. "
          f"P2 JSR/JMP into $E000-$FFFF: {len(p2)}.\n")
    print("| Direction | Top targets |")
    print("|---|---|")
    t1 = ', '.join(f"${t:04X}×{n}" for t, n in collections.Counter(
        r[2] for r in pr).most_common(6))
    t2 = ', '.join(f"${t:04X}×{n}" for t, n in collections.Counter(
        r[2] for r in p2).most_common(6))
    print(f"| PROD → P2 space | {t1} |")
    print(f"| P2 → PROD space | {t2} |")

    # --- entry points ---
    print("\n## 8. Apple II Monitor entry points in PROD\n")
    print("| Address | Name | Franklin V5.0 bytes |")
    print("|---|---|---|")
    for addr, name in [(0xF800, 'PLOT'), (0xFB2F, 'INIT'), (0xFC58, 'HOME'),
                       (0xFD0C, 'RDKEY'), (0xFD6A, 'GETLN'), (0xFD8E, 'CROUT'),
                       (0xFDDA, 'PRBYTE'), (0xFDED, 'COUT'), (0xFE84, 'SETNORM'),
                       (0xFE89, 'SETKBD'), (0xFE93, 'SETVID'), (0xFF3A, 'BELL')]:
        line = ' ; '.join(t for _, _, t in disassemble(P['PROD'], 0xE000, addr, 3))
        print(f"| ${addr:04X} | {name} | `{line}` |")

    # --- Apple similarity ---
    print("\n## 9. Similarity vs Apple reference ROMs\n")
    print("Reference set: the 21 Apple II / II Plus ROM images whose SHA-256"
          " hashes are listed in `apple_reference/apple_reference_sha256.txt`"
          " (2 KB each; images not redistributed in this archive).\n")
    apple_dir = os.environ.get('APPLE_ROM_DIR')
    if apple_dir and os.path.isdir(apple_dir):
        def windows(d, w):
            return {d[i:i+w] for i in range(len(d) - w + 1)}
        def lcs(x, y, seed=16):
            pos = {}
            for j in range(len(y) - seed + 1):
                pos.setdefault(y[j:j+seed], []).append(j)
            best = 0
            for i in range(len(x) - seed + 1):
                for j in pos.get(x[i:i+seed], ()):
                    L = seed
                    while i+L < len(x) and j+L < len(y) and x[i+L] == y[j+L]:
                        L += 1
                    best = max(best, L)
            return best
        print("| Franklin | Apple ROM | 32-byte windows | 64-byte windows | LCS |")
        print("|---|---|---|---|---|")
        for n, fd in P.items():
            f32, f64 = windows(fd, 32), windows(fd, 64)
            for path in sorted(glob.glob(os.path.join(apple_dir, '*.bin'))):
                ad = open(path, 'rb').read()
                w32 = len(f32 & windows(ad, 32))
                w64 = len(f64 & windows(ad, 64))
                L = lcs(fd, ad)
                if w32 or L >= 16:
                    print(f"| {n} | {os.path.basename(path)[:52]} "
                          f"| {w32} | {w64} | {L} |")
        print("\nRows with zero 32-byte matches and LCS below 16 are omitted.")
    else:
        print("*(Set APPLE_ROM_DIR to the directory of reference images and"
              " rerun to regenerate this table. The committed appendix was"
              " built with the full reference set present.)*")

    # --- P3 ---
    print("\n## 10. P3 disk firmware data\n")
    d = P['P3']
    print(f"Zero bytes: {d.count(0)} of 8192. 0xFF bytes: {d.count(0xFF)}.\n")
    print("6-and-2 GCR write-translate table at payload 0x0856 (64 bytes):\n```")
    t = d[0x0856:0x0896]
    for k in range(0, 64, 16):
        print(' '.join(f'{x:02X}' for x in t[k:k+16]))
    print("```")


if __name__ == '__main__':
    main()
