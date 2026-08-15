#!/usr/bin/env python3
"""
Generate a seamless, tileable dusty-rose limewash / venetian-plaster texture
matched to the Dynasty J. CO accent wall.

All noise fields are synthesized in the frequency domain on a torus, so the
output tiles perfectly in both directions with no visible seam.

Usage:
    python3 generate_limewash.py
"""

import numpy as np
from PIL import Image

# ---------------------------------------------------------------- parameters

SEED = 20260815

DPI = 150                 # print resolution wallpaper vendors expect
TILE_INCHES = 24          # 24 in x 24 in repeat
N = DPI * TILE_INCHES     # 3600 x 3600 px

# Colors sampled from the reference photo of the pink wall.
SHADOW = np.array([186, 150, 143], dtype=np.float64)     # #BA968F deepest mottling
MID = np.array([208, 175, 167], dtype=np.float64)        # #D0AFA7 base field
HIGHLIGHT = np.array([232, 211, 204], dtype=np.float64)  # #E8D3CC chalky bloom


def periodic_noise(n, beta, rng, aniso=1.0, angle_deg=0.0):
    """Periodic 1/f^beta Gaussian field.

    beta controls the scale: higher = softer, larger blobs.
    aniso > 1 stretches the field along `angle_deg` to fake directional
    trowel/brush work.
    """
    freqs = np.fft.fftfreq(n)
    fx, fy = np.meshgrid(freqs, freqs, indexing="xy")

    theta = np.deg2rad(angle_deg)
    fx_r = fx * np.cos(theta) + fy * np.sin(theta)
    fy_r = -fx * np.sin(theta) + fy * np.cos(theta)

    radial = np.sqrt((fx_r * aniso) ** 2 + fy_r**2)
    radial[0, 0] = 1.0  # avoid divide-by-zero at DC

    spectrum = radial ** (-beta)
    spectrum[0, 0] = 0.0  # drop DC so the field is zero-mean

    white = rng.normal(size=(n, n))
    field = np.real(np.fft.ifft2(np.fft.fft2(white) * spectrum))

    field -= field.mean()
    std = field.std()
    return field / std if std else field


def normalize(a):
    lo, hi = a.min(), a.max()
    return (a - lo) / (hi - lo) if hi > lo else np.zeros_like(a)


def ramp(t, shadow, mid, highlight):
    """Three-stop color ramp: shadow -> mid -> highlight."""
    t = t[..., None]
    lower = shadow + (mid - shadow) * (t / 0.5)
    upper = mid + (highlight - mid) * ((t - 0.5) / 0.5)
    return np.where(t < 0.5, lower, upper)


def build(n, rng):
    # Broad cloudy wash — the big soft light/dark drifts across the wall.
    # Kept deliberately light: heavy low-frequency energy is what makes a
    # repeat readable as a repeat once the wall is papered.
    cloud = periodic_noise(n, beta=2.35, rng=rng)

    # Mid-scale patchiness where the wash pooled and dried unevenly.
    patch = periodic_noise(n, beta=1.70, rng=rng)
    patch_fine = periodic_noise(n, beta=1.25, rng=rng)

    # Cross-hatched trowel strokes, applied in two opposing directions.
    stroke_a = periodic_noise(n, beta=1.55, rng=rng, aniso=7.0, angle_deg=34.0)
    stroke_b = periodic_noise(n, beta=1.55, rng=rng, aniso=7.0, angle_deg=-52.0)

    # Fine mineral tooth of the plaster.
    grain = periodic_noise(n, beta=0.55, rng=rng)

    field = (
        0.70 * cloud
        + 0.60 * patch
        + 0.40 * patch_fine
        + 0.26 * stroke_a
        + 0.20 * stroke_b
        + 0.10 * grain
    )

    t = normalize(field)

    # S-curve: pushes tone toward the mid field and keeps extremes rare, which
    # is how real limewash reads — mostly even, with occasional bloom.
    t = t * t * (3.0 - 2.0 * t)
    t = 0.5 + (t - 0.5) * 0.80  # pull back overall contrast

    rgb = ramp(t, SHADOW, MID, HIGHLIGHT)

    # Limewash shifts slightly warmer where it is lightest.
    warmth = (t - 0.5)[..., None] * np.array([5.0, 1.0, -3.0])
    rgb = rgb + warmth

    # Per-pixel print grain so large flat areas don't band.
    rgb = rgb + rng.normal(scale=1.5, size=rgb.shape)

    return np.clip(rgb, 0, 255).astype(np.uint8)


def main():
    rng = np.random.default_rng(SEED)

    print(f"Synthesizing {N}x{N} px ({TILE_INCHES}in @ {DPI} DPI) tile...")
    tile = build(N, rng)

    img = Image.fromarray(tile, mode="RGB")
    out = "assets/limewash-rose-seamless-24in-150dpi.png"
    img.save(out, dpi=(DPI, DPI), optimize=True)
    print(f"  wrote {out}")

    # 2x2 tiled proof so the seam (or lack of one) is visible at a glance.
    proof_side = 1000
    small = img.resize((proof_side, proof_side), Image.LANCZOS)
    proof = Image.new("RGB", (proof_side * 2, proof_side * 2))
    for x in (0, proof_side):
        for y in (0, proof_side):
            proof.paste(small, (x, y))
    proof.save("assets/tiling-proof-2x2.png", optimize=True)
    print("  wrote assets/tiling-proof-2x2.png")

    # Flat swatch for quick color approval on a phone screen.
    img.resize((1400, 1400), Image.LANCZOS).save(
        "assets/swatch-preview.png", optimize=True
    )
    print("  wrote assets/swatch-preview.png")

    # 1:1 crop — this is the texture at true printed scale (~8in x 8in).
    c = 1200
    off = (N - c) // 2
    img.crop((off, off, off + c, off + c)).save(
        "assets/detail-crop-actual-size.png", optimize=True
    )
    print("  wrote assets/detail-crop-actual-size.png")


if __name__ == "__main__":
    main()
