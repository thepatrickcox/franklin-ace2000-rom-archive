# Data Appendix

Machine-generated from the binaries in `roms/` by `tools/build_data_appendix.py`. Regenerate after any change to the binaries; do not edit by hand.

## 1. Raw read inventory

| Chip | File | SHA-256 (first 16) | 32-bit sum |
|---|---|---|---|
| PROD | 1984-1985_labeled_M5L27256K_DIP28.BIN | `3a3008b0c69bbe59` | `0x005EC0D0` |
| PROD | franklin 1984-1985 labeled 1-B  M5L27256K@DIP28.BIN | `d70376343c468932` | `0x005EB4C5` |
| PROD | franklin 1984-1985 labeled 1-B  Read #2 M5L27256K@DIP28.BIN | `1802b3a5ed8058f4` | `0x005EC2D3` |
| PROD | franklin 1984-1985 labeled 1-B  Read #3 M5L27256K@DIP28.BIN | `267fa85d0a526a0f` | `0x005EC6D6` |
| PROD | franklin 1984-1985 labeled 1-B  Read #4 M5L27256K@DIP28.BIN | `b8129f10fbe54726` | `0x005EC758` |
| P1 | frankin beta rom P1 12-12  Read #2 M5L27256K@DIP28.BIN | `82b1cdabe093d5e3` | `0x005EBB11` |
| P1 | frankin beta rom P1 12-12  Read #3 M5L27256K@DIP28.BIN | `fc4409d58f1204ee` | `0x005EB68A` |
| P1 | frankin beta rom P1 12-12  Read #4 M5L27256K@DIP28.BIN | `553154f7b4f3ec15` | `0x005EB68C` |
| P1 | frankin beta rom P1 12-12  Read #5 M5L27256K@DIP28.BIN | `cc3071f1b4ad2b2c` | `0x005EC47E` |
| P1 | frankin beta rom P1 12-12  Read #6 M5L27256K@DIP28.BIN | `06c4a1e6ed467402` | `0x005EC26F` |
| P1 | frankin beta rom P1 12-12 M5L27256K@DIP28.BIN | `ba08ee093cc93988` | `0x005EAD68` |
| P1 | p1_M5L27256K_DIP28.BIN | `fdd9ca5b5ae7269e` | `0x005EBD38` |
| P2 | franklin beta rom P2 12-12 M5L27256K@DIP28.BIN | `ee1e517e027fcd28` | `0x0059D970` |
| P2 | franklin beta rom P2 12-12 Read #2 M5L27256K@DIP28.BIN | `ee1e517e027fcd28` | `0x0059D970` |
| P2 | p2_M5L27256K_DIP28.BIN | `ee1e517e027fcd28` | `0x0059D970` |
| P3 | Franklin beta rom P3 8-6 M5L27256K@DIP28.BIN | `0b045f47c9a8be1d` | `0x004CC984` |
| P3 | Franklin beta rom P3 8-6 Read #2 M5L27256K@DIP28.BIN | `0b045f47c9a8be1d` | `0x004CC984` |
| P3 | p3_M5L27256K_DIP28.BIN | `0b045f47c9a8be1d` | `0x004CC984` |

## 2. Read-to-read stability

Pairwise differing-byte counts across the full 32 KB images.

* **PROD** (5 reads): r1/r2=61, r1/r3=39, r1/r4=46, r1/r5=45, r2/r3=66, r2/r4=65, r2/r5=64, r3/r4=51, r3/r5=40, r4/r5=41
* **P1** (7 reads): r1/r2=152, r1/r3=170, r1/r4=191, r1/r5=182, r1/r6=174, r1/r7=147, r2/r3=150, r2/r4=207, r2/r5=202, r2/r6=180, r2/r7=141, r3/r4=187, r3/r5=184, r3/r6=178, r3/r7=185, r4/r5=143, r4/r6=239, r4/r7=172, r5/r6=232, r5/r7=169, r6/r7=189
* **P2** (3 reads): r1/r2=0, r1/r3=0, r2/r3=0
* **P3** (3 reads): r1/r2=0, r1/r3=0, r2/r3=0

## 3. 32 KB image structure (all chips)

| Chip | 0x0000-0x3FFF | 0x4000-0x5FFF vs 0x6000-0x7FFF (per read) |
|---|---|---|
| PROD | 16384/16384 bytes 0xFF | 24 differing bytes (read 1) |
| P1 | 16384/16384 bytes 0xFF | 58 differing bytes (read 1) |
| P2 | 16384/16384 bytes 0xFF | 0 differing bytes (read 1) |
| P3 | 16384/16384 bytes 0xFF | 0 differing bytes (read 1) |

## 4. Canonical 8 KB payloads

| Chip | File | Samples/byte | Ties | SHA-256 |
|---|---|---|---|---|
| PROD | `franklin_ace2000_E000_V5.0_production.bin` | 10 | 6 | `2dbc094c867bb600d4c0c78ff13db9abe16404a8f4cb6e7fe34a5216e6f6f74d` |
| P1 | `franklin_ace2000_E000_V5.2_beta_P1.bin` | 14 | 17 | `d4469fb66246eb05bc1720411840d97c330ff8688a411e481b3284d927569a3e` |
| P2 | `franklin_ace2000_C000_beta_P2.bin` | 6 | 0 | `fe2046a979f753147bc823d5607aece5ddddf90d589336a28ae91b90b6409662` |
| P3 | `franklin_ace2000_disk_beta_P3.bin` | 6 | 0 | `150a96e13937a93e6fb4ac64b17e30b408f4d306142c16990d398776ac812bb6` |

### 4.1 Unresolved tie positions

**PROD** (6):

| Payload offset | Address | Votes | Canonical | Sister chip (stable?) |
|---|---|---|---|---|
| 0x004C | $E04C | 0x6A×5 / 0xEA×5 | 0x6A | 0xEA (stable) |
| 0x0374 | $E374 | 0x48×5 / 0xC8×5 | 0x48 | 0xC8 (stable) |
| 0x03CC | $E3CC | 0x6A×5 / 0xEA×5 | 0x6A | unstable |
| 0x07CD | $E7CD | 0x25×5 / 0xA5×5 | 0x25 | 0xA5 (stable) |
| 0x1110 | $F110 | 0xB8×5 / 0xB9×5 | 0xB8 | 0xB8 (stable) |
| 0x173D | $F73D | 0x28×5 / 0xA8×5 | 0x28 | 0xA8 (stable) |

**P1** (17):

| Payload offset | Address | Votes | Canonical | Sister chip (stable?) |
|---|---|---|---|---|
| 0x0063 | $E063 | 0x2C×7 / 0x2D×7 | 0x2C | 0x2D (stable) |
| 0x00BC | $E0BC | 0x24×7 / 0xA4×7 | 0x24 | unstable |
| 0x02CC | $E2CC | 0x25×7 / 0xA5×7 | 0x25 | 0xA5 (stable) |
| 0x0453 | $E453 | 0x12×7 / 0x13×7 | 0x12 | 0x13 (stable) |
| 0x046B | $E46B | 0x28×7 / 0xA8×7 | 0x28 | 0xA8 (stable) |
| 0x0703 | $E703 | 0xA0×7 / 0xA1×7 | 0xA0 | 0xA1 (stable) |
| 0x07B5 | $E7B5 | 0x92×7 / 0x93×7 | 0x92 | 0x93 (stable) |
| 0x0CD1 | $ECD1 | 0xEA×7 / 0xEB×7 | 0xEA | 0xEB (stable) |
| 0x0E12 | $EE12 | 0x84×7 / 0x85×7 | 0x84 | 0x24 (stable) |
| 0x0F62 | $EF62 | 0x84×7 / 0x85×7 | 0x84 | 0x85 (stable) |
| 0x1082 | $F082 | 0x88×7 / 0x89×7 | 0x88 | 0x89 (stable) |
| 0x1478 | $F478 | 0x31×7 / 0xB1×7 | 0x31 | 0xB1 (stable) |
| 0x15F1 | $F5F1 | 0xA4×7 / 0xA5×7 | 0xA4 | 0xA5 (stable) |
| 0x1841 | $F841 | 0xF2×7 / 0xF3×7 | 0xF2 | 0xF3 (stable) |
| 0x1DE0 | $FDE0 | 0xFC×7 / 0xFD×7 | 0xFC | 0xFD (stable) |
| 0x1E93 | $FE93 | 0xA8×7 / 0xA9×7 | 0xA8 | 0xA9 (stable) |
| 0x1EE0 | $FEE0 | 0xA4×7 / 0xA5×7 | 0xA4 | 0xA5 (stable) |

## 5. PROD (V5.0) vs P1 (V5.2)

Differing bytes: 862 of 8192 (89.48% identical).
XOR histogram (top 6): 0x01×485, 0x80×31, 0x02×8, 0x60×7, 0x20×7, 0x03×6.
Positions where both chips read internally stable yet differ: 708 of 862.
Direction among stable differences: PROD carries the set bits in 426, P1 in 62.

Spatial distribution of stable differences (512-byte buckets, $E000 base):

| Range | Count |
|---|---|
| $E000-$E1FF | 30 |
| $E200-$E3FF | 32 |
| $E400-$E5FF | 35 |
| $E600-$E7FF | 32 |
| $E800-$E9FF | 30 |
| $EA00-$EBFF | 20 |
| $EC00-$EDFF | 192 |
| $EE00-$EFFF | 61 |
| $F000-$F1FF | 26 |
| $F200-$F3FF | 25 |
| $F400-$F5FF | 92 |
| $F600-$F7FF | 29 |
| $F800-$F9FF | 20 |
| $FA00-$FBFF | 30 |
| $FC00-$FDFF | 44 |
| $FE00-$FFFF | 10 |

### 5.1 Semantic anchor points

Version string region (payload 0x18E0-0x18FA, high bit masked):

* PROD: `b'ACE 2X00 V5.0\x00ERR\x07\x00 \x00\x04$\x05%%'`
* P1: `b'ACD 2X00 V5.2\x00ERR\x06\x00 \x00\x04$\x05%%'`

Monitor hex-digit table (payload 0x19AB-0x19BB, high bit masked):

* PROD: `b'0123456789ABCDEF'`
* P1: `b'0123446789ABCDEF'`

## 6. Boot chain listings

PROD, RESET vector target:
```
$FA62: 4C FD F7  JMP $F7FD
$F7FD: 4C FE DE  JMP $DEFE
```

P2, boot orchestrator at $DEFE (first 24 instructions):
```
$DEFE: A9 00     LDA #$00
$DF00: 48        PHA
$DF01: 28        PLP
$DF02: A2 00     LDX #$00
$DF04: 20 02 FC  JSR $FC02
$DF07: CD FF CF  CMP $CFFF
$DF0A: 8D 0A C0  STA $C00A
$DF0D: A9 FF     LDA #$FF
$DF0F: 8D FB 04  STA $04FB
$DF12: 2C 5B C0  BIT $C05B
$DF15: 2C 5D C0  BIT $C05D
$DF18: 2C 5F C0  BIT $C05F
$DF1B: 2C 59 C0  BIT $C059
$DF1E: 20 CE FD  JSR $FDCE
$DF21: 20 E2 FB  JSR $FBE2
$DF24: A9 A5     LDA #$A5
$DF26: 4D F3 03  EOR $03F3
$DF29: 4D F4 03  EOR $03F4
$DF2C: D0 03     BNE $DF31
$DF2E: 4C 69 DF  JMP $DF69
$DF31: 20 EE C3  JSR $C3EE
$DF34: 20 58 FC  JSR $FC58
$DF37: A2 00     LDX #$00
$DF39: 20 25 FF  JSR $FF25
```

Byte $F7FF across all 10 production-chip samples: 0xDE 0xDE 0xDE 0xDE 0xDE 0xDE 0xDE 0xDE 0xDE 0xDE.

## 7. Cross-chip references

PROD JSR/JMP into $C100-$DFFF: 91. P2 JSR/JMP into $E000-$FFFF: 113.

| Direction | Top targets |
|---|---|
| PROD → P2 space | $DEB8×6, $D412×6, $DD67×6, $DEC0×4, $D91D×4, $D43C×3 |
| P2 → PROD space | $F2F1×12, $F2E5×4, $FC22×3, $F2C5×3, $E07D×3, $FBE2×2 |

## 8. Apple II Monitor entry points in PROD

| Address | Name | Franklin V5.0 bytes |
|---|---|---|
| $F800 | PLOT | `PHA ; JSR $F847 ; JSR $F957` |
| $FB2F | INIT | `JMP $F8BC ; NOP ; NOP` |
| $FC58 | HOME | `NOP ; BIT $2585 ; SEC` |
| $FD0C | RDKEY | `JSR $FA65 ; NOP ; BRA $FD18` |
| $FD6A | GETLN | `LDA $33 ; JSR $FDED ; LDX #$00` |
| $FD8E | CROUT | `JMP $F904 ; BRK ; BRK` |
| $FDDA | PRBYTE | `PHA ; JSR $FD9F ; JSR $FDE3` |
| $FDED | COUT | `JMP ($0036) ; CMP #$A0 ; BCC $FDF6` |
| $FE84 | SETNORM | `LDY #$FF ; STY $32 ; RTS` |
| $FE89 | SETKBD | `LDA #$00 ; BRA $FE9D ; LDA #$FF` |
| $FE93 | SETVID | `LDA #$00 ; JSR $FEAA ; STA $36` |
| $FF3A | BELL | `LDA #$87 ; JMP $FDED ; LDX $46` |

## 9. Similarity vs Apple reference ROMs

Reference set: the 21 Apple II / II Plus ROM images whose SHA-256 hashes are listed in `apple_reference/apple_reference_sha256.txt` (2 KB each; images not redistributed in this archive).

| Franklin | Apple ROM | 32-byte windows | 64-byte windows | LCS |
|---|---|---|---|---|
| PROD | Apple II - 341-0016 - Programmer's Aid #1 - 2716.bin | 0 | 0 | 16 |
| PROD | Apple II plus ROM Pages D8-DF - 341-0012 - Applesoft | 0 | 0 | 19 |
| PROD | Apple II plus ROM Pages E0-E7 - 341-0013 - Applesoft | 0 | 0 | 24 |
| PROD | Apple II plus ROM Pages E8-EF - 341-0014 - Applesoft | 9 | 0 | 40 |
| PROD | Apple II plus ROM Pages F0-F7 - 341-0015 - Applesoft | 25 | 0 | 56 |
| PROD | Apple II+ - 341-0012 - Applesoft BASIC D800 - 2716.b | 0 | 0 | 19 |
| PROD | Apple II+ - 341-0013 - Applesoft BASIC E000 - 2716.b | 0 | 0 | 24 |
| PROD | Apple II+ - 341-0014 - Applesoft BASIC E800 - 2716.b | 9 | 0 | 40 |
| PROD | Apple II+ - 341-0015 - Applesoft BASIC F000 - 2716.b | 25 | 0 | 56 |
| P1 | Apple II - 341-0016 - Programmer's Aid #1 - 2716.bin | 0 | 0 | 16 |
| P1 | Apple II plus ROM Pages D8-DF - 341-0012 - Applesoft | 0 | 0 | 19 |
| P1 | Apple II plus ROM Pages E8-EF - 341-0014 - Applesoft | 0 | 0 | 23 |
| P1 | Apple II plus ROM Pages F0-F7 - 341-0015 - Applesoft | 0 | 0 | 17 |
| P1 | Apple II+ - 341-0012 - Applesoft BASIC D800 - 2716.b | 0 | 0 | 19 |
| P1 | Apple II+ - 341-0014 - Applesoft BASIC E800 - 2716.b | 0 | 0 | 23 |
| P1 | Apple II+ - 341-0015 - Applesoft BASIC F000 - 2716.b | 0 | 0 | 17 |
| P2 | Apple II - 341-0004 - Integer BASIC Monitor F800 - 2 | 0 | 0 | 20 |
| P2 | Apple II plus ROM Pages D0-D7 - 341-0011 - Applesoft | 0 | 0 | 18 |
| P2 | Apple II plus ROM Pages D8-DF - 341-0012 - Applesoft | 2 | 0 | 33 |
| P2 | Apple II plus ROM Pages F8-FF - 341-0020 - Autostart | 0 | 0 | 20 |
| P2 | Apple II+ - 341-0011 - Applesoft BASIC D000 - 2716.b | 0 | 0 | 18 |
| P2 | Apple II+ - 341-0012 - Applesoft BASIC D800 - 2716.b | 2 | 0 | 33 |
| P2 | Apple II+ - 341-0020 - Applesoft BASIC Autostart Mon | 0 | 0 | 20 |
| P2 | Apple II+ - Freeze's Integer BASIC Non-Autostart F80 | 0 | 0 | 20 |
| P2 | Apple II+ - Freeze's Integer BASIC Non-Autostart F80 | 0 | 0 | 20 |

Rows with zero 32-byte matches and LCS below 16 are omitted.

## 10. P3 disk firmware data

Zero bytes: 4967 of 8192. 0xFF bytes: 17.

6-and-2 GCR write-translate table at payload 0x0856 (64 bytes):
```
96 97 9A 9B 9D 9E 9F A6 A7 AB AC AD AE AF B2 B3
B4 B5 B6 B7 B9 BA BB BC BD BE BF CB CD CE CF D3
D6 D7 D9 DA DB DC DD DE DF E5 E6 E7 E9 EA EB EC
ED EE EF F2 F3 F4 F5 F6 F7 F9 FA FB FC FD FE FF
```
