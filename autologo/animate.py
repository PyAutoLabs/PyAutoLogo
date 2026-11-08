"""
Shared frame rendering and GIF writing for the PyAutoGalaxy and PyAutoFit logo
animations, matching the look of ``gifs/pyautolens.gif``:

- 1860 x 924 pixel frames,
- a square region of arc-seconds stretched over the 2:1 frame (the PyAutoLens
  frames were plotted with ``aspect="auto"``),
- the ``jet`` colormap with a linear min-max normalisation and no axes or colorbar,
- 72 frames at 100 ms, with the final frame held for 2.1 s, looping forever.

Like the PyAutoLens frames (cropped out of a 1000 x 1000, 0.025" grid), each frame
is evaluated at 0.025" per pixel over the visible extent and then stretched to the
frame size (bicubic).
"""
import os
from os import path

import numpy as np
from matplotlib import colormaps
from PIL import Image

import autogalaxy as ag

from autologo.strokes import light_profiles_from

FRAME_SHAPE = (924, 1860)  # (height, width) of gifs/pyautolens.gif
N_FRAMES = 72
FRAME_DURATION_MS = 100
FINAL_FRAME_DURATION_MS = 2100
PIXEL_SCALE = 0.025  # arc-seconds, as for the PyAutoLens image-plane grid

repo_path = path.dirname(path.dirname(path.abspath(__file__)))
gif_path = path.join(repo_path, "gifs")
png_path = path.join(repo_path, "pngs")

_grids = {}


def _grid_from(extent, pixel_scale=PIXEL_SCALE):
    """
    Uniform grid covering the square ``extent`` = [x0, x1, y0, y1] (arc-seconds) at
    the PyAutoLens pixel scale with no over-sampling. Sampling at the same resolution
    matters for the look: it sets how much the cuspy Sersic peaks dominate the
    min-max colour scale.
    """
    x0, x1, y0, y1 = extent
    shape = (
        int(round((y1 - y0) / pixel_scale)),
        int(round((x1 - x0) / pixel_scale)),
    )
    key = (tuple(np.round(extent, 6)), shape)

    if key not in _grids:
        grid = ag.Grid2D.uniform(
            shape_native=shape,
            pixel_scales=((y1 - y0) / shape[0], (x1 - x0) / shape[1]),
            origin=((y0 + y1) / 2.0, (x0 + x1) / 2.0),
            over_sample_size=1,
        )
        _grids.clear()
        _grids[key] = grid

    return _grids[key]


def image_from(profiles, extent):
    """
    Image (2D numpy array, y up) over ``extent`` of a galaxy made of ``profiles``,
    which is either a list of light profiles or a list of stroke dictionaries.
    """
    if profiles and isinstance(profiles[0], dict):
        profiles = list(light_profiles_from(profiles, ag.lp).values())

    galaxy = ag.Galaxy(
        redshift=0.5, **{f"light_{i}": profile for i, profile in enumerate(profiles)}
    )
    return np.asarray(galaxy.image_2d_from(grid=_grid_from(extent)).native)


def rgb_from(image, vmax_percentile=100.0):
    """
    Colour an image with ``jet`` (linear, min to max) and upsample it to the frame
    size. ``vmax_percentile`` < 100 saturates the brightest pixels, which stops a
    single cuspy peak from dimming the rest of a frame.
    """
    vmin = image.min()
    vmax = np.percentile(image, vmax_percentile)
    normed = np.clip((image - vmin) / (vmax - vmin), 0.0, 1.0)

    rgb = (colormaps["jet"](normed)[..., :3] * 255).astype(np.uint8)
    return np.asarray(
        Image.fromarray(rgb).resize(
            (FRAME_SHAPE[1], FRAME_SHAPE[0]), resample=Image.BICUBIC
        )
    )


def save_pngs(frames, prefix):
    """Write frames to the (git-ignored) ``pngs/`` folder for inspection."""
    os.makedirs(png_path, exist_ok=True)
    for i, frame in enumerate(frames):
        Image.fromarray(frame).save(path.join(png_path, f"{i}_{prefix}.png"))


def save_gif(frames, filename):
    """
    Write an infinitely looping GIF with the PyAutoLens timing: 100 ms per frame,
    final frame held for 2.1 s. One global palette is shared by all frames so the
    colours do not flicker between frames.
    """
    images = [Image.fromarray(frame) for frame in frames]

    palette_source = Image.fromarray(
        np.concatenate([frames[0], frames[len(frames) // 2], frames[-1]], axis=0)
    ).quantize(colors=256, method=Image.Quantize.MEDIANCUT)

    images = [
        image.quantize(palette=palette_source, dither=Image.Dither.NONE)
        for image in images
    ]

    durations = [FRAME_DURATION_MS] * (len(images) - 1) + [FINAL_FRAME_DURATION_MS]

    out = path.join(gif_path, filename)
    images[0].save(
        out,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=1,
    )
    return out


def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def lerp(a, b, s):
    return (1.0 - s) * np.asarray(a, dtype=float) + s * np.asarray(b, dtype=float)


def lerp_angle(a, b, s):
    """Interpolate ellipse orientations (180 degree periodic) along the shortest path."""
    delta = ((b - a + 90.0) % 180.0) - 90.0
    return a + s * delta
