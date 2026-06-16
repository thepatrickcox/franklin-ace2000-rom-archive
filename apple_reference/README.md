# Apple reference ROM set

The similarity analysis in `analysis/` compares the Franklin images against
21 Apple II and Apple II Plus reference ROM images (2 KB each: Integer BASIC,
Applesoft BASIC, Monitor, Autostart Monitor, Programmer's Aid, and character
generator/video ROMs). Apple's firmware is not redistributed in this archive.
The exact files used are identified by SHA-256 in
`apple_reference_sha256.txt`; an independently obtained set matching those
hashes reproduces the comparison tables via:

    APPLE_ROM_DIR=<dir> python3 tools/build_data_appendix.py
