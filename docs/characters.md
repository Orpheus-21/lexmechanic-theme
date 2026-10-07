# Characters of the embedded fonts

This file lists which characters the fonts Volume Tc and Volume Tc Sans have. A character that a font lacks is drawn with the next font of the font stack. The text stack ends with Georgia, Times New Roman, and a serif font. The interface stack ends with Verdana and a sans-serif font. A line of text can then have glyphs of two styles.

The tables come from `scripts/font_coverage.py`. Run `python3 scripts/font_coverage.py --write` to make them again.

## Volume Tc, normal

* Characters: 174
* Layout features: GPOS: kern

| Block | Characters | Of |
|---|---|---|
| Basic Latin | 95 | 95 |
| Latin 1 Supplement | 64 | 96 |
| Latin Extended A and B | 4 | 336 |
| General Punctuation | 4 | 112 |
| Mathematical Operators | 1 | 256 |

Common characters that the font lacks:

* `—` em dash (U+2014)
* `–` en dash (U+2013)
* `…` ellipsis (U+2026)
* `•` bullet (U+2022)
* `×` multiplication sign (U+00D7)
* `÷` division sign (U+00F7)
* `°` degree sign (U+00B0)
* `±` plus or minus sign (U+00B1)
* `²` superscript two (U+00B2)
* `³` superscript three (U+00B3)
* `½` one half (U+00BD)
* `§` section sign (U+00A7)
* `å` a with ring (U+00E5)
* `Å` A with ring (U+00C5)
* `→` right arrow (U+2192)
* `←` left arrow (U+2190)
* `✓` check mark (U+2713)
* `✔` heavy check mark (U+2714)

## Volume Tc, italic

* Characters: 174
* Layout features: GPOS: kern

| Block | Characters | Of |
|---|---|---|
| Basic Latin | 95 | 95 |
| Latin 1 Supplement | 65 | 96 |
| Latin Extended A and B | 4 | 336 |
| General Punctuation | 4 | 112 |

Common characters that the font lacks:

* `—` em dash (U+2014)
* `–` en dash (U+2013)
* `…` ellipsis (U+2026)
* `•` bullet (U+2022)
* `×` multiplication sign (U+00D7)
* `÷` division sign (U+00F7)
* `°` degree sign (U+00B0)
* `±` plus or minus sign (U+00B1)
* `²` superscript two (U+00B2)
* `³` superscript three (U+00B3)
* `½` one half (U+00BD)
* `§` section sign (U+00A7)
* `å` a with ring (U+00E5)
* `Å` A with ring (U+00C5)
* `→` right arrow (U+2192)
* `←` left arrow (U+2190)
* `✓` check mark (U+2713)
* `✔` heavy check mark (U+2714)

## Volume Tc Sans, normal

* Characters: 175
* Layout features: GPOS: kern

| Block | Characters | Of |
|---|---|---|
| Basic Latin | 95 | 95 |
| Latin 1 Supplement | 66 | 96 |
| Latin Extended A and B | 4 | 336 |
| General Punctuation | 4 | 112 |

Common characters that the font lacks:

* `—` em dash (U+2014)
* `–` en dash (U+2013)
* `…` ellipsis (U+2026)
* `•` bullet (U+2022)
* `×` multiplication sign (U+00D7)
* `÷` division sign (U+00F7)
* `°` degree sign (U+00B0)
* `±` plus or minus sign (U+00B1)
* `²` superscript two (U+00B2)
* `³` superscript three (U+00B3)
* `½` one half (U+00BD)
* `§` section sign (U+00A7)
* `å` a with ring (U+00E5)
* `Å` A with ring (U+00C5)
* `→` right arrow (U+2192)
* `←` left arrow (U+2190)
* `✓` check mark (U+2713)
* `✔` heavy check mark (U+2714)

## Test line

Put this line in a note, and look at which glyphs differ in style:

```
— – … • × ÷ ° ± ² ³ ½ § å Å → ← ✓ ✔ ‘ ’ “ ” € ™
```
