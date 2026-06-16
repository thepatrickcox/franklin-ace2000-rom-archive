# Methodology

## Equipment

Reads were performed on an XGecu T48 (TL866-3G) universal programmer running XGpro v13.16, using the M5L27256K@DIP28 device profile for all four chips. Analysis was performed with the Python tools in `tools/` (standard library only, Python 3.8+).

## Read procedure

Each chip was read repeatedly without removal between consecutive passes: five passes for the production chip, seven for P1, three each for P2 and P3, across sessions on June 9 and June 11, 2026. The pass counts were escalated in response to observed instability — P2 and P3 produced bit-identical reads immediately, while the production chip and P1 produced no two identical reads, so additional passes were taken to support statistical reconstruction. Every XGpro output file is preserved unmodified in `roms/raw_reads/`.

## Why the 32 KB reads contain an 8 KB payload twice

The 27256 profile drives DIP-28 pin 27 as address A14 and pin 26 as A13. On 2764-class 8 KB devices, pin 27 is /PGM and pin 26 is not connected. Under the profile, addresses 0x0000-0x3FFF hold /PGM low and the device returns 0xFF; addresses 0x4000-0x7FFF read normally with A13 floating, so the 8 KB array appears at both 0x4000-0x5FFF and 0x6000-0x7FFF. A genuine 27256 programmed with an 8 KB image duplicated in its upper half produces an identical dump; die markings distinguish the cases (see `PROVENANCE.md`). The payload is taken from the upper 16 KB; the two copies are treated as independent samples of each byte.

## The pin-26 contact warning

Every read of every chip produced the XGpro warning "Bad Pin: ZIF38 - PIN#26," reproduced on a second T48 unit. This is expected behavior, not a fault, and it is diagnostic. A DIP-28 device sits top-justified in the ZIF-40 socket, so device pins 15-28 occupy ZIF pins 27-40 and ZIF pin 38 is device pin 26 — the one pin whose function differs between the device families involved: A13 (bonded) on a 27256, NC (unbonded) on a 2764. XGpro's pin-contact test senses the protection network behind each pin and flags an unbonded pin as bad. Reading 2764-class silicon under a 27256 profile therefore necessarily produces this exact warning on this exact pin. The warning was acknowledged ("ignore to Continue") on each read; A13 is not required, and the payload reads out completely, with the mirroring documented above. Screenshots of the warning and of the read sessions are preserved in `provenance_images/`.

## Reconstruction by majority vote

For each payload position i, the sample set is {read r at 0x4000+i, read r at 0x6000+i, for every read r}. The canonical byte is the majority value. A position with no absolute majority is recorded as a tie and listed in the data appendix; the canonical file takes the numerically lower candidate, and the tie list is the authoritative statement of uncertainty. This procedure is implemented in `tools/reconstruct.py` and regenerating any canonical image from the raw reads reproduces its published SHA-256.

Sampling depth per byte: production 10, P1 14, P2 and P3 6. Outcomes: P2 and P3 zero ties; production 6; P1 17. All 23 ties are single-bit (bit 7 or bit 0) ambiguities. The tie set shifts between sessions — added reads resolve some ties and expose others — which is the expected signature of threshold-marginal cells; the published tables reflect all eighteen reads.

## Error-mode characterization

Read-noise analysis (differences between same-chip reads) shows the unstable chips err in both directions — bits reading high and reading low — concentrated in bits 7 and 0; this is marginal sensing, not simple charge loss, and it motivates multi-read voting rather than trusting any single pass. Independently, P1 exhibits *stable* wrong bits (cells that read the same wrong value on all 12 samples), proven at two positions where the correct value is semantically forced: the Monitor hex-digit table and the product-name string, both failing bit-0-low. Stable-wrong cells cannot be detected by re-reading the same chip; they were caught here only because a second specimen of nearly identical firmware (the production chip) and semantic anchors existed. The methodological consequence is stated in the technical analysis: P1's image is the best reconstruction of the chip's current contents, with a documented residue of positions where revision differences and cell failure cannot be distinguished per-byte.

## Disassembly

`tools/dis65c02.py` implements the full WDC 65C02 instruction set. The NMOS-only subset was insufficient: the firmware uses PHY/PLY/PHX/PLX, BRA, STZ, TRB/TSB, BIT immediate and JMP (abs,X), and these opcodes appear in load-bearing positions (the boot orchestrator uses STZ and BRA). Linear-sweep classification is used only for statistical purposes (operand-versus-opcode diff classification) and is acknowledged as approximate across data regions; all load-bearing disassembly in the documents is from verified code entry points.

## Similarity measurement

`tools/compare_apple.py` computes, for each Franklin/Apple image pair: the number of distinct 32-byte sequences present in both images, the same at 64 bytes, and the single longest contiguous shared run (16-byte seed, greedy extension). Exact-match windowing at these sizes is insensitive to alignment and detects any verbatim copying of code-sized fragments; the 64-byte null result across all pairs is the headline negative. No similarity percentage is reported anywhere in this archive, because no defensible normalization exists; counts and offsets are reported as measured. Character-generator and video ROMs in the reference set participate in the comparison and match nothing, as expected for bitmap content.

## Reproduction

From the repository root: reconstruct any canonical image with `tools/reconstruct.py` over the corresponding raw reads and compare hashes against `roms/canonical/SHA256SUMS`; regenerate every figure with `APPLE_ROM_DIR=<path-to-reference-set> python3 tools/build_data_appendix.py > analysis/DATA_APPENDIX.md`; inspect any address with `tools/dis65c02.py <image> <base> <addr>`; rerun the similarity study with `tools/compare_apple.py <image> <apple-rom-dir>`. The Apple reference images are not redistributed; the manifest in `apple_reference/` identifies the exact files by SHA-256.
