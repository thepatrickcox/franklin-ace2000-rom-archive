# Provenance

## Chain of custody

The four EPROMs in this archive were retained by Francis Patrick Cox from his time at Franklin Computer Corporation's Pennsauken, New Jersey facility, where he worked as a thirteen-year-old QA tester circa 1982-84. His role was compatibility testing: running commercial Apple-format software from 5¼-inch floppies — games, educational, and business titles — and logging syntax errors and failure conditions. He was introduced to the company through John Applegate, who ran a church youth group in Bordentown, New Jersey; John's brother Bob Applegate was a software engineer at Franklin. Bob Applegate's employment there, from 1982 to 1984 — the same window as Mr. Cox's — is independently corroborated by the published record: he was interviewed as a former Franklin programmer in David Friedman's investigation of the ACE manuals (Ironic Sans, 2023, covered by PC Gamer), and he exhibited "Franklin's Apple II clones and prototypes" at Vintage Computer Festival East 9.1 (2014). The ACE 1000 manual's Ben Franklin chapter cartoons were drawn by an outside illustrator, Frank Williams, per the manual's author Sal Manetta; the manual also includes a cartoon depicting Applegate himself at work on a "Frankenstein" computer. Mr. Cox's recollection of cartoon drawings at Applegate's desk is recorded in `PERSONAL_ACCOUNT.md`. A physical copy of the 1982 ACE 1000 manual remains with the collection.

The chips remained in Mr. Cox's personal possession continuously from the mid-1980s until they were read for this archive in June 2026, stored in a case with other artifacts of the period; the June 2026 reads were the first extraction of their contents. No intermediate custody, transfer, or rework is known or claimed. A first-person account of the work at Franklin during 1982-84, written by Mr. Cox and included at the request of historians, is preserved verbatim in `PERSONAL_ACCOUNT.md`.

## Physical description and label transcription

| Chip | Device marking | Label |
|---|---|---|
| Production | Mitsubishi M5L2764K | Pre-printed: "©1984-1985 Franklin Computer", P/N 02.02764.100, "REV"; "1" before and "B" after the printed "REV" added in red pen, reading "1 REV B" |
| Beta P1 | Mitsubishi M5L2764K | Handwritten: "P1 12-12" |
| Beta P2 | Mitsubishi M5L2764K | Handwritten: "P2 12-12" |
| Beta P3 | Texas Instruments TMS2764JL-25, date code GHP8441 | Handwritten: "P3 8-6" |

Label text is transcribed as written. The "12-12" and "8-6" annotations are plausibly month-day dates from the development period; this interpretation is a hypothesis, not an established fact. The TMS2764JL-25 date code GHP8441 indicates manufacture in week 41 of 1984, which bounds P3's programming date to late 1984 at the earliest and is consistent with development of firmware shipped in machines introduced October 1985.

All four chips were photographed in 2026 (© Patrick Cox 2026); the photographs accompany the collection.

## Reconciling device markings with read behavior

All eighteen reads in `roms/raw_reads/` were taken with the XGpro M5L27256K@DIP28 device profile and are 32 KB files with identical structure: the lower 16 KB reads 0xFF and the upper 16 KB contains an 8 KB payload twice.

This structure is the expected electrical signature of a 2764-class 8 KB device read under a 27256 profile. The 27256 profile drives pin 27 as address line A14 and pin 26 as A13; on a 2764, pin 27 is /PGM and pin 26 is not connected. Addresses with A14 low hold /PGM low and the device returns 0xFF; addresses with A14 high read normally, and the unconnected A13 makes the 8 KB payload appear twice.

All four chips, including the production part, are die-marked 2764, confirmed by physical re-inspection of the packages on June 11, 2026. An earlier working record of the production chip as "M5L27256K" originated from the XGpro device profile embedded in the read filenames, not from the package: XGpro v13.16 offers no Mitsubishi 2764 profile, so the M5L27256K profile was used for all reads. Three independent lines of electrical evidence agree with the markings: the blank lower 16 KB (/PGM held low by the profile's A14), the twice-mirrored 8 KB payload (the 2764's unconnected pin 26 ignoring the profile's A13), and XGpro's pin-contact warning raised on device pin 26 (reported as ZIF pin 38) on every read of every chip, on two different T48 units — pin 26 being bonded A13 on a 27256 and unbonded NC on a 2764 (see `analysis/METHODOLOGY.md`). Franklin's own part number on the production label, 02.02764.100, embeds the device type. The matter is closed: four 2764-class 8 KB EPROMs, each delivering its payload at the top of the address map.

Session records: `provenance_images/` preserves XGpro screenshots of the June 4, 2026 session (showing the superseded checksum 0x005D56DB discussed below) and of the June 9, 2026 archive reads, including the pin-26 warning as raised and acknowledged.

## Read provenance

Reads were performed in Greenville, South Carolina on an XGecu T48 (TL866-3G) programmer under XGpro v13.16, in two sessions. On June 9, 2026: four reads of the production chip, six of P1, and two each of P2 and P3, the counts chosen in response to observed read instability (see `analysis/METHODOLOGY.md`). On June 11, 2026, following the physical re-inspection of the die markings, one additional verification read of each chip — eighteen reads in total. The June 11 reads of P2 and P3 reproduced the June 9 data byte for byte; the June 11 reads of the production chip and P1 fell within the instability ranges already established. The original XGpro output files are preserved byte-for-byte in `roms/raw_reads/` under their original filenames, with SHA-256 hashes in the adjacent `SHA256SUMS`.

A note on superseded data: a read session prior to this archive reported a 32-bit checksum of 0x005D56DB for the production chip and an apparent reset-path jump to $5EFE. Both values are superseded. The production chip's reads vary by 40-66 bytes between passes, so no single-read checksum identifies this chip; the chip's identity is fixed by the canonical voted payload (SHA-256 `2dbc094c...`, in full in `roms/canonical/SHA256SUMS`). The $5EFE value is established by eight consistent samples to have been a transient single-bit read error for $DEFE (see `analysis/TECHNICAL_ANALYSIS.md`, section "The $5EFE correction").
