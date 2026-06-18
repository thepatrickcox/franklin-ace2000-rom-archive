# Franklin ACE 2000 Firmware Archive

Four EPROMs from Franklin Computer Corporation (Pennsauken, New Jersey), retained by one person for approximately forty years, dumped and analyzed in June 2026. Together they form a matched, interlocking firmware set for Franklin's ACE 2000 series (introduced October 1985): the post-lawsuit, clean-room generation of Apple II-compatible firmware that Franklin shipped after *Apple Computer, Inc. v. Franklin Computer Corp.*, 714 F.2d 1240 (3d Cir. 1983) — the case that established that object code in ROM is copyrightable.

## Why this matters, in plain terms

In 1982 it was an open legal question whether software burned into a chip could be copyrighted at all. Franklin Computer copied Apple's firmware into its Apple-clone machines and argued in court that a ROM is a machine part, not a writing. In 1983, a federal appeals court disagreed — and that ruling, *Apple v. Franklin*, is a foundation the entire modern software industry stands on. Every software license and every "you can't just copy the binary" assumption traces back to it.

Court opinions about that case are easy to find. What has been almost impossible to find is the engineering aftermath: what a company's programmers actually did, byte by byte, when the law suddenly required them to rewrite everything while staying perfectly compatible. These four chips are that evidence. They show Apple's published function addresses kept exactly in place (so Apple software still runs), all the code behind those addresses rewritten, nothing shared except what mathematics and disk hardware force everyone to share, and not one trace of the embedded Apple text that had convicted the first-generation chips. One chip's startup sequence even jumps mid-boot into a second chip in the set — both halves of the machine's boot path, preserved together.

They survived because a thirteen-year-old who tested these machines kept four chips in a case for forty years, then read them out and published the analysis. The chips prove the engineering; his account (`PERSONAL_ACCOUNT.md`) explains how a kid from a church youth group in New Jersey ended up holding them.

## What is in this archive

| Chip | Canonical image | Identity |
|---|---|---|
| Production, label "©1984-1985 Franklin Computer", marked "1 REV B" in red pen | `roms/canonical/franklin_ace2000_E000_V5.0_production.bin` | ACE 2X00 firmware **V5.0**, system ROM, maps $E000-$FFFF |
| Beta "P1 12-12" | `roms/canonical/franklin_ace2000_E000_V5.2_beta_P1.bin` | ACE 2X00 firmware **V5.2**, a later revision of the same ROM |
| Beta "P2 12-12" | `roms/canonical/franklin_ace2000_C000_beta_P2.bin` | Companion system ROM, maps $C000-$DFFF; contains the cold-boot orchestrator and memory diagnostics |
| Beta "P3 8-6" | `roms/canonical/franklin_ace2000_disk_beta_P3.bin` | Floppy-disk controller firmware; contains the 6-and-2 GCR nibble tables and disk-boot chaining |

Each canonical image is an 8 KB payload reconstructed by majority vote across multiple programmer reads and the device's internal mirror (6 to 14 samples per byte). SHA-256 hashes for canonical images and all eighteen raw reads are in `roms/*/SHA256SUMS`.

## Principal findings

**The chips interlock.** The production ROM's reset path is RESET → $FA62 → `JMP $F7FD` → `JMP $DEFE` — an address outside the chip itself. Beta chip P2 contains, at exactly $DEFE, a 65C02 cold-boot orchestrator that initializes the machine and jumps back to $E000 in the production ROM's space. The two images make 91 and 113 direct absolute JSR/JMP calls into each other's address ranges. One firmware, two chips, both preserved by the same person.

**Two firmware revisions survive.** The production chip carries the embedded string `ACE 2X00 V5.0`; beta P1 carries `V5.2` — a genuinely later revision, established by a bit-set version digit, a relocated entry point (`JMP $F128` vs `JMP $F028`), and code differences clustered in two regions ($EC00-$EDFF: 192 changed bytes; $F400-$F5FF: 93).

**The firmware is an independent implementation.** Across roughly twenty Apple II and II Plus reference ROMs, the longest run of bytes shared with any Apple image is 56 bytes — the Applesoft floating-point constant table, numeric coefficients required for computational compatibility. No 64-byte window is shared anywhere. No Apple copyright string, no `APPLESOFT` string, and no embedded attribution of any kind appears in any of the four chips; the presence of exactly such embedded strings in Franklin's earlier, copied ROMs was central evidence in the 1983 litigation. The firmware preserves Apple's published Monitor entry-point addresses ($FDED COUT, $FC58 HOME, $FF3A BELL, and others) while implementing them with different code — for example, Franklin's BELL is `LDA #$87 / JMP $FDED` where Apple's is `LDA #$87 / JSR $FDED / RTS`: same address, same behavior, different bytes.

**One forty-year-old mystery resolved during this work.** An earlier read of the production chip yielded `JMP $5EFE` at $F7FD, an address that mapped to nothing. Ten independent samples now establish the byte as 0xDE, not 0x5E: the instruction is `JMP $DEFE`, and the earlier value was a single transient bit-7 read error on a chip whose weak cells are demonstrably concentrated in bits 7 and 0.

## Repository layout

    README.md                      this file
    EXECUTIVE_SUMMARY.md           one-page summary of findings
    HISTORY.md                     historical context, with sources
    PROVENANCE.md                  chain of custody and physical description
    PERSONAL_ACCOUNT.md            first-person account by the contributor, 1982-84
    analysis/TECHNICAL_ANALYSIS.md full technical record
    analysis/METHODOLOGY.md        equipment, procedure, reproduction steps
    analysis/DATA_APPENDIX.md      machine-generated tables (do not edit)
    tools/                         the Python tools used; no dependencies
    roms/canonical/                reconstructed 8 KB payloads + SHA256SUMS
    roms/raw_reads/                all 18 original XGpro reads + SHA256SUMS
    chip_photographs/              11 Leica photographs of all four chips (© Patrick Cox 2026)
    provenance_images/             XGpro session screenshots (June 4 and 9, 2026)
    apple_reference/               SHA-256 manifest of the Apple reference set
    LICENSE.md                     MIT (tools), CC BY 4.0 (docs); ROMs excluded
    CITATION.cff                   citation metadata
                                   (Apple images are not redistributed)

## Reproducing the analysis

Every figure in `analysis/DATA_APPENDIX.md` is computed from the binaries by `tools/build_data_appendix.py`. The reconstruction itself is reproducible from the raw reads:

    python3 tools/reconstruct.py out.bin roms/raw_reads/"franklin 1984-1985"*.BIN

See `analysis/METHODOLOGY.md` for the complete procedure, including the device-profile behavior that produces the 32 KB read structure.

The analysis tools have no external dependencies and run entirely on the Python standard library. Clone the repository and run `reconstruct.py` immediately — no `pip install` required.

## Status of the binaries

Franklin Computer Corporation's computer business ended in the late 1980s; the firmware in this archive has had no commercial availability for four decades. The images are published here for preservation and study. The Apple reference ROMs used for comparison are identified by hash only and are not included.
