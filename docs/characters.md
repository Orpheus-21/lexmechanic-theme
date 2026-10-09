# Characters of the embedded fonts

This file lists which characters the fonts Volume Tc and Volume Tc Sans have. A character that a font lacks is drawn with the next font of the font stack. The text stack ends with Georgia, Times New Roman, Noto Serif, and a serif font. The interface stack ends with Verdana, Noto Sans, and a sans-serif font. The two Noto fonts cover Greek, Cyrillic, and more Latin letters, if they are installed. A line of text can then have glyphs of two styles.

These 15 characters were not in the fonts that came with the theme: – — … • × ÷ ° ± ² ³ ½ å Å → ←. `scripts/extend_fonts.py` draws them from outlines that the fonts have, such as the hyphen, the period, and the digits. The dashes, the dots, and the signs are plain shapes of the weight of the font. They are not the work of the type designer.

The tables come from `scripts/font_coverage.py`. Run `python3 scripts/font_coverage.py --write` to make them again.

## Volume Tc, normal

* Characters: 189
* Layout features: GPOS: kern

| Block | Characters | Of |
|---|---|---|
| Basic Latin | 95 | 95 |
| Latin 1 Supplement | 73 | 96 |
| Latin Extended A and B | 4 | 336 |
| General Punctuation | 8 | 112 |
| Arrows | 2 | 112 |
| Mathematical Operators | 1 | 256 |

Common characters that the font lacks:

* `§` section sign (U+00A7)
* `✓` check mark (U+2713)
* `✔` heavy check mark (U+2714)

## Volume Tc, italic

* Characters: 189
* Layout features: GPOS: kern

| Block | Characters | Of |
|---|---|---|
| Basic Latin | 95 | 95 |
| Latin 1 Supplement | 74 | 96 |
| Latin Extended A and B | 4 | 336 |
| General Punctuation | 8 | 112 |
| Arrows | 2 | 112 |

Common characters that the font lacks:

* `§` section sign (U+00A7)
* `✓` check mark (U+2713)
* `✔` heavy check mark (U+2714)

## Volume Tc Sans, normal

* Characters: 190
* Layout features: GPOS: kern

| Block | Characters | Of |
|---|---|---|
| Basic Latin | 95 | 95 |
| Latin 1 Supplement | 75 | 96 |
| Latin Extended A and B | 4 | 336 |
| General Punctuation | 8 | 112 |
| Arrows | 2 | 112 |

Common characters that the font lacks:

* `§` section sign (U+00A7)
* `✓` check mark (U+2713)
* `✔` heavy check mark (U+2714)

## Test line

Put this line in a note, and look at which glyphs differ in style:

```
— – … • × ÷ ° ± ² ³ ½ § å Å → ← ✓ ✔ ‘ ’ “ ” € ™
```
