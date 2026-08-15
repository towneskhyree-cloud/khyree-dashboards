# Dynasty J. CO — Rose Limewash Wallpaper

A seamless, print-ready wallpaper file matched to the pink limewash accent wall
in the Dynasty J. CO suite. Hand it to any print-on-demand wallpaper vendor.

## Files

| File | Size | What it's for |
|---|---|---|
| `assets/limewash-rose-seamless-24in-150dpi.png` | 3600 × 3600 px | **The print file.** Send this one to the vendor. |
| `assets/tiling-proof-2x2.png` | 2000 × 2000 px | Shows the tile repeated 4× — proves there's no seam. |
| `assets/swatch-preview.png` | 1400 × 1400 px | Quick color check on a phone. |
| `assets/detail-crop-actual-size.png` | 1200 × 1200 px | The texture at true printed scale (~8 in × 8 in). |

## Print specs

- **Repeat:** 24 in × 24 in, tiles seamlessly in both directions
- **Resolution:** 150 DPI (the standard most wallpaper printers ask for)
- **Color mode:** RGB — most vendors convert to CMYK themselves; if yours asks
  for CMYK, let them do the conversion so the pink doesn't shift
- **Palette:**
  - Deepest mottling `#BA968F`
  - Base field `#D0AFA7`
  - Chalky bloom `#E8D3CC`

The pattern is generated on a torus, so the left edge matches the right and the
top matches the bottom exactly. Vendors can tile it to any wall height without a
visible seam line, and there is no directional "up" — panels can't be hung upside
down by mistake.

## "No-stick" — two different products

The request was for "no stick" wallpaper, which can mean two things. **The same
print file works for either**; only the material you order changes:

1. **Non-pasted / traditional (unpasted) wallpaper** — no adhesive on the paper
   at all. You paste the wall (or the paper) at install. Best durability and the
   most matte, plaster-like finish, which is what suits this texture. Ask the
   vendor for *unpasted* or *paste-the-wall* stock.
2. **Peel-and-stick / removable** — pressure-sensitive adhesive backing, no paste,
   fully removable. This is what people usually mean by "no glue needed." Good
   for a leased space where the wall has to come back to original. Ask for
   *removable / peel-and-stick* stock.

For a salon suite, peel-and-stick in a **matte** finish is the safer call — it
comes off cleanly at end of lease and matte keeps it reading like real limewash.
Avoid any satin or gloss option; sheen is what makes faux plaster look printed.

## Ordering

Measure the wall's **width × height**, add ~2 in of overage on each dimension,
and give the vendor those numbers plus this file. They'll handle panel splitting.
Order one sample swatch first to confirm the pink against your actual lighting —
the room has both cool white LED strips and a warm panel, and that mix shifts
pink noticeably.

## Regenerating

To tweak color, contrast, or repeat size:

```bash
pip install numpy pillow
python3 generate_limewash.py
```

Key knobs in `generate_limewash.py`:

- `SHADOW` / `MID` / `HIGHLIGHT` — the three-stop color ramp
- `TILE_INCHES` — repeat size (currently 24)
- `DPI` — output resolution (currently 150)
- the contrast pullback in `build()` (`* 0.80`) — lower = flatter, more even wash
- `SEED` — change it for a completely different mottling pattern in the same colors
