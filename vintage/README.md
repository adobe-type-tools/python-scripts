# Python scripts

Various command line scripts no longer in active use.

## Description

### `UFOInstanceGenerator.py`
(Deprecated workflow, but a great starter for interpolation).  
Generate UFO instances from two or more masters, in a one- or two axis MultipleMaster setup. Requires a settings file called `instances`, the contents of which are better described within the script itself.

→ replaced by makeinstancesufo 

---

### `BuildMMFont.py`
Build MM font from bez files.

---

### `copyCFFCharstrings.py`
Copies the CFF charstrings and subroutines from source to destination fonts.

---

### `kernCheck.py`
Performs several (lengthy) checks on the GPOS table `kern` feature in an OpenType font.

This tool will report collisions between kern pairs, or, with the option `-a`, will report any collisions between any pair of glyphs. It will also report when rules in one GPOS table kern feature mask rules in a different subtable of the same lookup.

NOTE: The time needed is related to the square of the number of glyphs. This script will run in a few minutes for a font with 300 glyphs, but can take more than an hour for a font with 3000 glyphs.

---

### `makeinstances.py`
Generates Type 1 font instances (`font.pfa`) from a multiple master Type 1 font file (`mmfont.pfa`) and an `instances` text file.

→ replaced by makeinstancesufo 

---

