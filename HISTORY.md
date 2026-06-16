# Historical Context

## Franklin Computer Corporation and the Apple II clone market

Franklin Computer Corporation of Pennsauken, New Jersey entered the personal computer market in early 1982 with the ACE 100, followed in March 1982 by the ACE 1000 — close copies of the Apple II and Apple II Plus. Compatibility was the entire commercial premise: the Apple II's value lay in its software library, and a clone that ran that library at a lower price had an immediate market.

Franklin achieved compatibility the direct way. Its first-generation machines shipped with Apple's operating firmware copied into Franklin ROMs. Fourteen Apple programs, stored as object code in ROM, became the subject of *Apple Computer, Inc. v. Franklin Computer Corp.*

## The litigation

Apple sued in the Eastern District of Pennsylvania in 1982. The district court denied Apple's motion for a preliminary injunction on July 30, 1982, expressing doubt that programs in object code and ROM were copyrightable at all. The court record preserved two details that matter to this archive. First, Franklin did not seriously dispute the copying; identical embedded artifacts — including Apple attribution strings present in Franklin's chips — made the copying demonstrable at the byte level. Second, the court recorded that Franklin had "made no attempt to rewrite any of the programs prior to the lawsuit except for Copy," while Apple introduced evidence that rewriting was feasible and that compatible third-party implementations existed.

The Third Circuit heard argument on March 17, 1983 and reversed on August 30, 1983 (714 F.2d 1240, opinion by Judge Sloviter, joined by Judges Hunter and Higginbotham), holding that object code, including operating-system code fixed in ROM, is protectable as a literary work under the Copyright Act of 1976. Rehearing en banc was denied September 23, 1983; the Supreme Court dismissed certiorari on January 4, 1984 (464 U.S. 1033). The decision is a foundational case in software copyright law.

Franklin settled, ultimately paying Apple $2.5 million, with residual disputes running through 1985. The company filed for Chapter 11 reorganization in June 1984, cutting its workforce from roughly 275 to just over 100.

## The second generation: rewrite or die

What the law now required, the ACE 2000 series delivered. Starting in October 1985, Franklin shipped a second generation of Apple-compatible machines — the ACE 2000 series, based on the Apple IIe, and the ACE 500, based on the Apple IIc — with firmware that had to be functionally compatible with Apple's while being independently written. The ACE 2200 model featured a detached keyboard and dual internal 5.25-inch floppy drives.

The chips in this archive are that firmware. The technical analysis documents the result of the rewrite in byte-level detail: Apple's published entry-point addresses preserved exactly, because the software library calls them; the code behind those addresses implemented differently; the only shared content a 56-byte table of floating-point constants whose values are fixed by mathematics; and not one Apple attribution string anywhere in 32 KB of Franklin firmware — the precise artifact class that had condemned the first generation now conspicuously absent. The firmware targets the 65C02, the CMOS processor of the IIe/IIc era, and its companion ROM performs auxiliary-memory diagnostics ("AUX MEMORY ERROR"), both consistent with the IIe-class ACE 2000 hardware.

Franklin's computer business did not survive the decade; the company found durable success from 1986 onward in handheld electronic references, beginning with the Spelling Ace. The ACE 2000-series firmware thus represents a short, terminal chapter: the engineering Franklin performed because the law left no alternative, in the first years in which American law required it of anyone.

## Why these particular chips matter

Surviving Franklin ACE 2000-series firmware is scarce; surviving *development* firmware is scarcer. This archive contains a production chip (V5.0, factory label "©1984-1985 Franklin Computer") alongside three hand-labeled engineering chips, one of which carries a *later* revision (V5.2) than the production part — evidence of continued firmware development — and two of which are the production ROM's working partners: the companion system ROM whose code the production chip jumps into on every reset, and the disk controller firmware for the machines' internal drives. The set was preserved not by an institution but by a teenager who tested these machines and kept four chips for forty years.

## Sources

Apple Computer, Inc. v. Franklin Computer Corp., 714 F.2d 1240 (3d Cir. 1983); cert. dismissed, 464 U.S. 1033 (1984). Procedural dates and the quoted finding on Franklin's rewriting are from the published opinion. Corporate chronology (ACE 100/1000 release timing, Chapter 11 filing and workforce reduction, ACE 2000-series introduction in October 1985, ACE 2200 configuration, settlement amount, and the post-1985 transition to electronic references) follows standard published company histories of Franklin Computer Corporation / Franklin Electronic Publishers. All claims about the chips themselves are original findings of this archive, documented in `analysis/`.
