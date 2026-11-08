"""
Make ``gifs/pyautogalaxy.gif``: a spiral galaxy that unwinds into "PyAuto Galaxy".

Every letter stroke of the final logo starts life as a knot of light on one of the
two arms of a logarithmic spiral galaxy, with a bright Sersic bulge and an
exponential disk underneath. The galaxy rotates while the knots peel off the arms
and slide, turn and stretch into their letter strokes; the bulge and disk fade as
the text forms, and the view zooms in from +-5.5" to the +-4" framing of the
PyAutoLens logo.

Run from the repository root:

    python -m autologo.make_pyautogalaxy
"""
import numpy as np

import autogalaxy as ag

from autologo import animate
from autologo.strokes import GALAXY_STROKES, PYAUTO_STROKES, light_profiles_from

TARGET_STROKES = PYAUTO_STROKES + GALAXY_STROKES

# Frames are stretched x2 horizontally (square extent on a 2:1 frame). Compressing
# the galaxy by 0.8 in x makes it look like an inclined disk (1.6:1 on screen) whose
# footprint matches the text it turns into.
X_SQUASH = 0.8

EXTENT_START = 5.5
EXTENT_FINAL = 4.0

ARM_TURNS = 1.15  # turns of each spiral arm
ARM_R_INNER = 0.45
ARM_R_OUTER = 3.6
ROTATION_DEGREES = 110.0  # clockwise turn over the animation (arms trail)


def _spiral_point(u, arm, rotation):
    """(y, x) and on-screen tangent angle of position ``u`` in [0, 1] along an arm."""
    theta_max = 2.0 * np.pi * ARM_TURNS
    b = np.log(ARM_R_OUTER / ARM_R_INNER) / theta_max

    def position(u):
        # ``u`` is the fraction of arm length (arc length ~ r on a log spiral), so
        # knots are spread evenly along the arm rather than bunched at the centre.
        r = ARM_R_INNER + u * (ARM_R_OUTER - ARM_R_INNER)
        theta = np.log(r / ARM_R_INNER) / b
        phi = theta + np.pi * arm - np.radians(rotation)
        return np.array([r * np.sin(phi), X_SQUASH * r * np.cos(phi)])

    p = position(u)
    dp = position(u + 1e-3) - position(u - 1e-3)
    angle = np.degrees(np.arctan2(dp[0], dp[1])) % 180.0
    return p, angle


def _spiral_assignment(strokes):
    """
    Map each target stroke to a place on the spiral: strokes nearest the middle of
    the logo sit on the inner arms, the outermost letters on the arm tips, so the
    galaxy appears to unwind into the text.
    """
    centres = np.array([s["centre"] for s in strokes], dtype=float)
    middle = centres.mean(axis=0)
    distance = np.hypot(centres[:, 0] - middle[0], (centres[:, 1] - middle[1]) / 2.0)
    order = np.argsort(distance)

    n_per_arm = int(np.ceil(len(strokes) / 2))
    rng = np.random.default_rng(42)

    assignment = {}
    for rank, index in enumerate(order):
        arm = rank % 2
        u = (rank // 2 + 0.5) / n_per_arm
        u = float(np.clip(u + rng.normal(0.0, 0.01), 0.0, 1.0))
        assignment[index] = (u, arm)
    return assignment


def _galaxy_component_profiles(fade):
    """Bulge and disk of the spiral, dimmed by ``fade`` (1 = full, 0 = gone)."""
    if fade <= 0.0:
        return []
    # Same squash as the arms, so the bulge and disk share the disk's inclination.
    ell_comps = ag.convert.ell_comps_from(axis_ratio=X_SQUASH, angle=90.0)
    return [
        ag.lp.Sersic(
            centre=(0.0, 0.0),
            ell_comps=ell_comps,
            intensity=6.0 * fade,
            effective_radius=0.8,
            sersic_index=1.5,
        ),
        ag.lp.Exponential(
            centre=(0.0, 0.0),
            ell_comps=ell_comps,
            intensity=0.25 * fade,
            effective_radius=2.6,
        ),
    ]


def frame_profiles(i, n_frames=animate.N_FRAMES):
    """Light profiles, extent and colour-scale percentile of frame ``i``."""
    t = i / (n_frames - 1)
    s = animate.smoothstep((t - 0.18) / 0.72)  # morph progress: 0 = galaxy, 1 = text
    rotation = ROTATION_DEGREES * t

    assignment = _spiral_assignment(TARGET_STROKES)

    strokes = []
    for index, target in enumerate(TARGET_STROKES):
        if s >= 1.0:
            strokes.append(target)
            continue

        u, arm = assignment[index]
        start_centre, start_angle = _spiral_point(u, arm, rotation)

        target_q = 1.0 if target["axis_ratio"] is None else target["axis_ratio"]
        target_angle = 0.0 if target["angle"] is None else target["angle"]

        # Knots are brighter and more compact towards the galaxy centre.
        start_radius = 0.55 + 0.5 * u

        strokes.append(
            dict(
                centre=tuple(animate.lerp(start_centre, target["centre"], s)),
                axis_ratio=float(animate.lerp(0.3, target_q, s)),
                angle=float(animate.lerp_angle(start_angle, target_angle, s)),
                intensity=float(animate.lerp(0.45 - 0.15 * u, target["intensity"], s)),
                effective_radius=float(
                    animate.lerp(start_radius, target["effective_radius"], s)
                ),
                sersic_index=target["sersic_index"],
            )
        )

    profiles = list(
        light_profiles_from(strokes, ag.lp).values()
    ) + _galaxy_component_profiles(fade=1.0 - s)

    half_width = float(animate.lerp(EXTENT_START, EXTENT_FINAL, s))
    extent = [-half_width, half_width, -half_width, half_width]

    # While the galaxy is visible its bulge peak would set the colour scale, so the
    # brightest pixels are saturated; this relaxes to a plain min-max by the end.
    vmax_percentile = float(animate.lerp(99.95, 100.0, s))

    return profiles, extent, vmax_percentile


def make(n_frames=animate.N_FRAMES, write_pngs=False):
    frames = []
    for i in range(n_frames):
        profiles, extent, vmax_percentile = frame_profiles(i, n_frames)
        image = animate.image_from(profiles, extent)
        frames.append(animate.rgb_from(image, vmax_percentile=vmax_percentile))
        print(f"pyautogalaxy frame {i + 1}/{n_frames}")

    if write_pngs:
        animate.save_pngs(frames, "autogalaxy")

    return animate.save_gif(frames, "pyautogalaxy.gif")


if __name__ == "__main__":
    print(make(write_pngs=True))
