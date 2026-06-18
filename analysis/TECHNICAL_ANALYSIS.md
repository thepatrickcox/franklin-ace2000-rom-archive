# Technical Analysis

All numeric claims in this document are reproducible from the binaries in `roms/` and are tabulated in `analysis/DATA_APPENDIX.md`, which is machine-generated. Addresses are given in 6502 memory-map terms; "payload offset" means an offset into a canonical 8 KB image.

## 1. Materials and reconstruction

Eighteen raw reads of four chips were taken across sessions on June 9 and June 11, 2026 (production: 5, P1: 7, P2: 3, P3: 3). Every read is a 32 KB file with the same structure — lower 16 KB 0xFF, upper 16 KB an 8 KB payload repeated twice — which is the electrical signature of an 8 KB payload read under a 27256 device profile (see `PROVENANCE.md` for the device-marking reconciliation). Each read therefore samples every payload byte twice, and the canonical images were produced by per-byte majority vote over all samples: 10 samples per byte for the production chip, 14 for P1, 6 for P2 and P3.

P2 and P3 read identically on every pass and reconstruct with zero ambiguity. The production chip varies by 39-66 bytes between read pairs and P1 by 141-239; after voting, 6 byte positions in the production image and 17 in P1 remain ties (an even split among samples). Every tie is a single-bit ambiguity, and the affected bit is bit 7 or bit 0 in all 23 cases. The complete tie list, with votes, is in the appendix (§4.1). The canonical images resolve ties deterministically to the numerically lower candidate; consumers requiring certainty at those 23 addresses should treat them as one-bit intervals. The tie set is not fixed across sessions: the June 11 read resolved two production-chip positions that had tied on the June 9 data and brought two previously resolved positions to a tie — the expected behavior of cells whose sense margin sits at the read threshold. The appendix additionally annotates each tie with the sister chip's stable reading: at 15 of P1's 17 ties the production chip stably reads the candidate with the differing bit set, independently corroborating P1's fail-low cell behavior.

## 2. Chip identities

### 2.1 Production chip — ACE 2X00 system ROM V5.0, $E000-$FFFF

The image carries the embedded string `ACE 2X00 V5.0` at payload offset 0x18E4. Hardware vectors at the top of the image read NMI=$03FB, RESET=$FA62, IRQ=$FA40, valid only if the payload occupies $E000-$FFFF; the code throughout is consistent with that base. RESET=$FA62 reproduces the address of Apple's own Autostart reset handler — entry-point compatibility extending even to the reset vector.

The code uses CMOS 65C02 opcodes (PHY, PLY, PHX, BRA, STZ, JMP (abs,X)) that do not exist on the NMOS 6502. The firmware therefore requires a 65C02, the processor of the Apple IIe (enhanced)/IIc generation, consistent with the ACE 2000 series' IIe-class design.

The image is the upper half of an Applesoft-compatible BASIC plus a Monitor: the Monitor's hex-digit table `0123456789ABCDEF` sits at offset 0x19AB, the Applesoft floating-point constant region appears near $F0D0 (see §5), and the canonical Monitor entry points are populated (§6).

### 2.2 Beta P1 — the same ROM at revision V5.2, with documented cell degradation

P1's vectors and overall structure match the production chip; 89.48% of bytes are identical. Its version string reads `V5.2` against the production `V5.0`. Two independent phenomena separate the images, and the evidence cleanly distinguishes them.

P1 is a genuinely later revision. Three observations establish this, none producible by chip degradation. First, the version digit: '0' (0x30) versus '2' (0x32) differs in bit 1, and the *set* bit is on P1's side — P1's demonstrated failure mode is bits reading low, which cannot add a set bit. Second, the ROM's entry jump at $E000 is `JMP $F128` in V5.0 and `JMP $F028` in V5.2: the primary entry routine moved one page. Third, the differences cluster: of 708 byte positions where both chips read internally stable yet disagree, 192 fall in $EC00-$EDFF and 92 in $F400-$F5FF — six and three times the background density — with multi-bit XOR patterns characteristic of changed code, not flipped cells.

P1 also has hard-failed cells, concentrated in bit 0. Two semantic anchors prove this beyond argument: P1's hex-digit table reads `0123446789ABCDEF` — a '4' (0x34) where the Monitor's output table forces '5' (0x35) — and its product string reads `ACD` where the product name forces `ACE` (0x44 vs 0x45). Both are bit-0-low errors at positions where the correct value is externally determined.

The two mechanisms cannot be separated at every byte. Of the 862 total differences, 485 have XOR 0x01, and a bit-0 difference is equally consistent with a one-page code relocation (address bytes 0xF1→0xF0) and with a stuck-low cell. The honest statement of P1's status is therefore: revision V5.2 is established; the canonical P1 image is the best 12-sample reconstruction of the physical chip's current contents; byte-exact recovery of V5.2 *as programmed* is not possible from this chip alone, and any future second V5.2 specimen would resolve the residue.

### 2.3 Beta P2 — companion system ROM, $C000-$DFFF

P2 is a different program. Its base address is established by internal evidence rather than vectors (an 8 KB ROM at $C000-$DFFF does not hold the CPU vectors): its diagnostic strings `MAIN MEMORY ERROR - UNABLE TO CONTINUE!` and `AUX MEMORY ERROR - UNABLE TO CONTINUE!` sit at $C48D and $C4B6 under a $C000 base, inside the IIe-style internal-$Cxxx firmware region where such self-test code belongs, and the code reached from the production ROM's boot jump (next section) manipulates IIe banking switches ($C006/$C007, $C00A, $CFFF) with the addressing only a $C000 base makes coherent. The auxiliary-memory diagnostic itself identifies the target machine as IIe-class — a 128 KB machine with an auxiliary bank — matching the ACE 2000 series.

P2 was read with perfect stability and reconstructs with zero ties. Which firmware revision P2 pairs with (V5.0, V5.2, or both) is undetermined; the cross-reference graph (§3) shows it is a working partner of the production V5.0 image, and its own revision marking, if any, has not been identified.

P2 carries the Applesoft BASIC interpreter's core tables in its upper half: the keyword table and the error-message table occupy roughly $D0B5-$D2FF. The keyword table is not stock Applesoft. Franklin removed the five cassette-tape tokens present in Apple's Applesoft II (`SHLOAD`, `RECALL`, `STORE`, `LOAD`, `SAVE`) and inserted a `FKEY` token in the `WAIT`/`DEF` region — a function-key keyword absent from Apple's interpreter. The error-message table is otherwise the familiar Applesoft set (`SYNTAX`, `NEXT WITHOUT FOR`, `RETURN WITHOUT GOSUB`, and the rest). This is a deliberate, byte-level customization of the BASIC interpreter, not a verbatim copy, and it establishes that the companion ROM holds Franklin's own modified Applesoft rather than acting solely as a boot and diagnostic helper.

### 2.4 Beta P3 — floppy-disk controller firmware

P3 contains no CPU vectors (the image's top is zero-fill; 4,967 of 8,192 bytes are zero) and shares no measurable content with any other image in this archive or with any Apple reference ROM. Its identity is fixed by its data: at payload offset 0x0856 it carries the canonical 64-entry 6-and-2 GCR write-translate table (`96 97 9A 9B 9D 9E 9F A6 A7 AB ... FF`) followed by the inverse decode table — the nibble code fundamental to Apple-format 5.25-inch disk encoding — and its code exhibits the unmistakable habits of disk firmware: NOP-sled and countdown timing loops, `LDA $CFFF` to release the shared $C800 expansion-ROM window, and `LDA $C600` boot-chaining through the slot-6 disk address. Code targets concentrate in $C800-$CFFF.

The established statement is that P3 is disk-controller firmware whose code executes at least partly in the $C800-$CFFF expansion window, consistent with the internal drive controller of the ACE 2000-series machines (the ACE 2200 shipped with dual internal 5.25-inch drives). Its complete memory mapping, and the meaning of its sparse layout (payload content occupies scattered spans between 0x0604 and 0x0BE2), are partially characterized; the label "8-6" and the TI date code GHP8441 (week 41, 1984) bound its era.

## 3. The two-ROM architecture

The production ROM's reset path is three instructions long inside its own chip:

    $FA62: 4C FD F7   JMP $F7FD        ; RESET vector target
    $F7FD: 4C FE DE   JMP $DEFE        ; leaves the chip's address space

$DEFE lies in P2's range, and P2 contains at exactly that address a cold-boot orchestrator (full listing in the appendix, §6): it clears processor state, configures the IIe-class ROM/slot banking ($CFFF, $C00A), strobes the annunciators, calls screen and I/O initialization in the $E000 ROM ($FDCE, $FBE2, $FC58), performs the warm/cold-start check (`LDA #$A5 / EOR $03F3 / EOR $03F4` — the power-up-byte convention), and exits either through the boot pointer (`JMP ($002A)`, with `$07F8` slot bookkeeping), back through the reset vector (`JMP ($FFFC)`), or into the system ROM proper (`JMP $E000`).

The interlock is dense in both directions: the production image makes 91 direct absolute JSR/JMP references into $C100-$DFFF, and P2 makes 113 into $E000-$FFFF; the most-called targets ($D43C, $DEB8, $DD67 in one direction; $F2F1 twelve times in the other) disassemble as well-formed routine entries. These are two chips of one firmware. The chance that a single individual's four retained chips would include both halves of the boot path is the central archival fact of this collection.

## 4. The $5EFE correction

A read session predating this archive reported the second boot jump as `JMP $5EFE`, an address that maps to RAM and resolved to nothing — a standing anomaly. The current data closes it. The operand byte at $F7FF reads 0xDE in all ten samples across five reads (appendix §6). 0x5E differs from 0xDE in exactly bit 7, and the production chip's six unresolved weak positions are bit-7 ambiguities in five of six cases. The earlier $5EFE was a single transient bit-7 read error; the instruction is `JMP $DEFE`, and its target is real, present, and disassembles as the machine's boot orchestrator in P2. The correction also illustrates the archive's reconstruction standard: no single read of an aging EPROM is authoritative.

## 5. Similarity to Apple firmware

Each canonical image was compared against the Apple II / II Plus reference set (21 images; hashes in `apple_reference/`) by exhaustive 32-byte and 64-byte sliding-window intersection and by longest-common-substring search (tooling: `tools/compare_apple.py`; full table: appendix §9).

The maximum shared run anywhere is 56 bytes, between the production image at $F0D0 and the Applesoft F0 page at $F0D3 — the floating-point constant table (polynomial coefficients and packed constants for Applesoft's math package). These are numeric values an Applesoft-compatible BASIC must reproduce exactly; they are facts, not expression. The same region accounts for all 25 of the production image's shared 32-byte windows with the Applesoft F0 page. No 64-byte window is shared between any Franklin image and any Apple image. P2's maximum shared run is 33 bytes; P1's is 23; P3 shares nothing at the 16-byte detection threshold.

No Franklin image contains the strings `APPLE`, `APPLESOFT`, any Apple copyright notice, or any attribution text whatsoever (the images' entire human-readable content is the version string, the hex-digit table, and P2's two diagnostic messages). The 1983 litigation record shows Franklin's first-generation ROMs carried exactly such embedded Apple artifacts; their absence here is the byte-level signature of the rewrite.

The shared content that does exist is of a specific legal character. The GCR nibble tables in P3 are fixed by the Disk II hardware encoding; the floating-point constants are fixed by mathematics and the packed numeric format. In copyright terms this is the merger doctrine: where function permits only one expression, identity of bytes carries no implication of copied expression. The byte-identical material in these chips is confined exactly to that category.

## 6. Entry-point compatibility with independent implementation

The production ROM populates Apple's published Monitor entry points at Apple's addresses with code that is behaviorally equivalent and byte-distinct (full table: appendix §8). Representative cases: COUT at $FDED is `JMP ($0036)` — the same indirect-through-CSW dispatch contract as Apple's. BELL at $FF3A is `LDA #$87 / JMP $FDED` where Apple's is `LDA #$87 / JSR $FDED / RTS` — identical effect, different control flow. HOME at $FC58, RDKEY at $FD0C, GETLN at $FD6A, PRBYTE at $FDDA, SETNORM at $FE84 and the others are likewise populated at the canonical addresses with implementations that immediately diverge from Apple's instruction sequences. This is the compatibility contract stated in code: the address surface that third-party software calls is preserved; everything behind it is Franklin's.

## 7. Established facts and open hypotheses

Established by the data in this archive: the four payloads and their hashes; the V5.0 and V5.2 version identities; P1's bit-0 cell degradation (two semantic anchors); the $E000 mapping of PROD/P1 and $C000 mapping of P2; the boot chain $FA62 → $F7FD → $DEFE → ... → $E000 across two chips; the 91/113 cross-reference interlock; the 56-byte maximum Apple overlap and its identity as the float constant table; the absence of any attribution strings; the 65C02 instruction-set requirement; P3's GCR tables and disk-firmware character; the $5EFE correction.

Hypotheses, so labeled: that "12-12" and "8-6" are month-day labels from 1984; P2's revision pairing; P3's complete memory mapping; and per-byte attribution of P1's 485 single-bit-0 differences between revision relink and cell failure.

A question examined and closed negatively: a search of all four images — including every zero-fill and inter-routine gap, in both plain and high-bit ASCII — found no leftover assembler source or developer comments. The only human-readable content is the version string, the Monitor hex-digit table, P2's two memory-error strings, and P2's Applesoft keyword and error tables (section 2.3). This contrasts with the companion ACE 500 firmware, in which another researcher found an assembler source fragment with developer comments left in an unused region; no such remnant survives in this ACE 2000-series set.

A question resolved during the project: the device type of all four chips — 2764-class 8 KB parts — is established by die markings re-inspected June 11, 2026, in agreement with the read structure and the pin-26 contact evidence (see `PROVENANCE.md`).
