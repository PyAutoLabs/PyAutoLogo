"""
Letter strokes shared by the PyAutoLens, PyAutoGalaxy and PyAutoFit logo animations.

Every letter of a logo is drawn by a handful of elongated Sersic light profiles
("strokes"). A stroke is stored as a plain dictionary so the same definitions can
be turned into light profiles of either `autolens` or `autogalaxy` (whose `lp`
modules are identical), and so the animation scripts can interpolate them.

Keys of a stroke dictionary:

- ``centre``: (y, x) in arc-seconds.
- ``axis_ratio`` / ``angle``: ellipticity (angle counter-clockwise from +x, degrees).
  Both are ``None`` for a spherical stroke (``SersicSph``).
- ``intensity``, ``effective_radius``, ``sersic_index``: as for ``lp.Sersic``.

The "PyAuto" row is exactly the top row of the original PyAutoLens source galaxy
(``light_0`` ... ``light_19`` in ``png_maker.py``).
"""
import numpy as np


def _stroke(centre, axis_ratio, angle, intensity, effective_radius, sersic_index=2.5):
    return dict(
        centre=centre,
        axis_ratio=axis_ratio,
        angle=angle,
        intensity=intensity,
        effective_radius=effective_radius,
        sersic_index=sersic_index,
    )


PYAUTO_STROKES = [
    _stroke((1.5, -3), 0.2, 110.0, 0.6, 1.0),
    _stroke((1, -2.8), 0.2, 110.0, 0.6, 1.0),
    _stroke((1.8, -2.7), 0.3, -15.0, 0.5, 1.1),
    _stroke((1.5, -2.6), 0.3, 35.0, 0.5, 1.1),
    _stroke((1.0, -2.0), 0.25, -35.0, 0.5, 1.2),
    _stroke((1.1, -1.7), 0.2, 70.0, 0.5, 1.2),
    _stroke((0.7, -1.85), 0.2, 70.0, 0.5, 1.2),
    _stroke((0.9, -1), 0.2, 75.0, 0.4, 1.5),
    _stroke((1.6, -0.8), 0.2, 75.0, 0.4, 1.3),
    _stroke((0.9, -0.3), 0.2, 115.0, 0.4, 1.5),
    _stroke((1.6, -0.6), 0.2, 115.0, 0.4, 1.3),
    _stroke((1.2, -0.7), 0.15, 0, 0.4, 1.3),
    _stroke((1.1, 0.2), 0.15, 100, 0.5, 1),
    _stroke((0.8, 0.5), 0.25, -10, 0.4, 1.1),
    _stroke((1.0, 0.7), 0.15, 90, 0.5, 1.4),
    _stroke((1.0, 1.3), 0.15, 100, 0.5, 1.1),
    _stroke((1.5, 1.1), 0.15, 100, 0.5, 1.1),
    _stroke((1.3, 1.45), 0.2, 10, 0.5, 0.7),
    _stroke((0.9, 2.2), None, None, 0.4, 6, 2.4),
    _stroke((0.9, 2.2), None, None, 0.3, 1.1, 1.4),
]


def light_profiles_from(strokes, lp, start_index=0):
    """
    Turn stroke dictionaries into ``{"light_<i>": profile}`` keyword arguments for
    ``Galaxy``, using the ``lp`` module of ``autolens`` or ``autogalaxy``.
    """
    import autogalaxy as ag

    profiles = {}

    for i, stroke in enumerate(strokes):
        if stroke["axis_ratio"] is None:
            profile = lp.SersicSph(
                centre=tuple(stroke["centre"]),
                intensity=stroke["intensity"],
                effective_radius=stroke["effective_radius"],
                sersic_index=stroke["sersic_index"],
            )
        else:
            profile = lp.Sersic(
                centre=tuple(stroke["centre"]),
                ell_comps=ag.convert.ell_comps_from(
                    axis_ratio=stroke["axis_ratio"], angle=stroke["angle"]
                ),
                intensity=stroke["intensity"],
                effective_radius=stroke["effective_radius"],
                sersic_index=stroke["sersic_index"],
            )
        profiles[f"light_{start_index + i}"] = profile

    return profiles


"""
New words are written as polylines and converted to strokes: each straight segment
is split into short pieces, each one an elongated Sersic centred on the piece,
aligned with the segment and with an effective radius proportional to its length.
Letters are defined in a local frame (y up, x right, baseline at y=0) and then
placed along a row.
"""

# Row geometry matched to the "Lens" row of the PyAutoLens logo.
BASELINE = -2.0
X_HEIGHT = 0.75
CAP_HEIGHT = 1.35

MAX_PIECE_LENGTH = 0.35
SEGMENT_RADIUS_FACTOR = 2.4


def _arc(centre, radii, angle_start, angle_end, n_segments):
    """Polyline points of an elliptical arc; angles in degrees, counter-clockwise."""
    angles = np.radians(np.linspace(angle_start, angle_end, n_segments + 1))
    return [
        (centre[0] + radii[0] * np.sin(a), centre[1] + radii[1] * np.cos(a))
        for a in angles
    ]


def _letter_polylines(letter):
    """Polylines (lists of (y, x) points) and dots for one letter, plus its width."""
    h = X_HEIGHT
    H = CAP_HEIGHT

    if letter == "G":
        bowl = _arc((H / 2, 0.45), (H / 2, 0.45), 40.0, 360.0, 7)
        bar = [(H * 0.45, 0.9), (H * 0.45, 0.5)]
        return [bowl, bar], [], 0.9
    if letter == "a":
        bowl = _arc((h / 2, 0.32), (h / 2, 0.32), 0.0, 360.0, 6)
        stem = [(h, 0.64), (0.0, 0.66)]
        return [bowl, stem], [], 0.7
    if letter == "l":
        return [[(H, 0.1), (0.0, 0.1)]], [], 0.2
    if letter == "x":
        # Four half-diagonals, so no two stroke centres sit on the crossing.
        c = (h / 2, 0.3)
        return [
            [(h, 0.0), c],
            [(h, 0.6), c],
            [(0.0, 0.0), c],
            [(0.0, 0.6), c],
        ], [], 0.6
    if letter == "y":
        return [[(h, 0.0), (0.05, 0.32)], [(h, 0.65), (-0.6, 0.1)]], [], 0.65
    if letter == "F":
        return [
            [(0.0, 0.0), (H, 0.0)],
            [(H, 0.0), (H, 0.7)],
            [(H * 0.52, 0.0), (H * 0.52, 0.55)],
        ], [], 0.7
    if letter == "i":
        return [[(0.0, 0.1), (h, 0.1)]], [(h + 0.35, 0.1)], 0.2
    if letter == "t":
        return [[(H * 0.85, 0.25), (0.0, 0.25)], [(h, 0.0), (h, 0.6)]], [], 0.6

    raise ValueError(f"No stroke definition for letter {letter!r}")


def _segment_strokes(p0, p1, intensity, axis_ratio):
    """
    Strokes drawing the straight segment p0 -> p1. Long segments are split into
    pieces no longer than ``MAX_PIECE_LENGTH`` so brightness is even along the line,
    mirroring how the PyAutoLens letters use pairs of overlapping strokes.
    """
    dy, dx = p1[0] - p0[0], p1[1] - p0[1]
    length = float(np.hypot(dy, dx))
    n_pieces = max(1, int(np.ceil(length / MAX_PIECE_LENGTH)))
    piece_length = length / n_pieces
    angle = float(np.degrees(np.arctan2(dy, dx))) % 180.0

    # Frames stretch x by 2 (square extent on a 2:1 frame), so horizontal strokes
    # are shortened to keep their on-screen length in proportion.
    radius_factor = SEGMENT_RADIUS_FACTOR * (1.0 - 0.45 * abs(np.cos(np.radians(angle))))

    strokes = []
    for i in range(n_pieces):
        f = (i + 0.5) / n_pieces
        strokes.append(
            _stroke(
                centre=(p0[0] + f * dy, p0[1] + f * dx),
                axis_ratio=axis_ratio,
                angle=angle,
                intensity=intensity,
                effective_radius=radius_factor * piece_length,
            )
        )
    return strokes


def word_strokes(
    word, x_start, baseline=BASELINE, spacing=0.22, intensity=0.4, axis_ratio=0.15
):
    """Strokes spelling ``word`` along a row starting at ``x_start``."""
    strokes = []
    x = x_start

    for letter in word:
        polylines, dots, width = _letter_polylines(letter)

        for polyline in polylines:
            points = [(baseline + y, x + px) for (y, px) in polyline]
            for p0, p1 in zip(points[:-1], points[1:]):
                strokes += _segment_strokes(p0, p1, intensity, axis_ratio)

        for (y, px) in dots:
            strokes.append(
                _stroke((baseline + y, x + px), None, None, intensity, 0.4)
            )

        x += width + spacing

    return strokes


def word_width(word, spacing=0.22):
    widths = [_letter_polylines(letter)[2] for letter in word]
    return sum(widths) + spacing * (len(widths) - 1)


def centred_word_strokes(word, x_centre=-0.2, **kwargs):
    """Strokes for ``word`` centred horizontally on ``x_centre`` (the "Lens" row centre)."""
    return word_strokes(word, x_start=x_centre - word_width(word) / 2.0, **kwargs)


GALAXY_STROKES = centred_word_strokes("Galaxy")
FIT_STROKES = centred_word_strokes("Fit")
