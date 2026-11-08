"""
Make ``gifs/pyautofit.gif``: a model fit converging on "PyAuto Fit".

The logo is treated as a model to be fitted: every letter stroke is a PyAutoFit
``af.Model`` of a Sersic light profile whose free parameters (centre, elliptical
components, effective radius) have broad uniform priors over the field. The first
frame is a draw from those priors (``instance_from_unit_vector`` on a random unit
cube point, as a nested sampler starts), so it is a scatter of randomly placed,
randomly shaped blobs.

Each later frame shows the current model of a simulated search: every parameter
moves towards its true value along an exponentially shrinking path with random
jitter, like a sampler's live points contracting onto the posterior peak. Strokes
converge at different rates, so letters lock into place one by one, until the last
frames show the exact "PyAuto Fit" logo (the maximum likelihood model).

The search is simulated (no likelihood is evaluated); the priors, parameterisation
and prior-cube draws are PyAutoFit's.

Run from the repository root:

    python -m autologo.make_pyautofit
"""
import numpy as np

import autofit as af
import autogalaxy as ag

from autologo import animate
from autologo.strokes import FIT_STROKES, PYAUTO_STROKES, light_profiles_from

TARGET_STROKES = PYAUTO_STROKES + FIT_STROKES

SEED = 3

PRIOR_CENTRE_Y = (-3.0, 3.0)
PRIOR_CENTRE_X = (-3.5, 3.5)
PRIOR_ELL_COMPS = (-0.6, 0.6)
PRIOR_EFFECTIVE_RADIUS = (0.3, 2.5)

CONVERGED_FRAMES = 8  # frames at the end showing the exact logo


def stroke_model_from(stroke):
    """An ``af.Model`` of one stroke: free geometry, intensity and index fixed."""
    if stroke["axis_ratio"] is None:
        model = af.Model(ag.lp.SersicSph)
    else:
        model = af.Model(ag.lp.Sersic)
        model.ell_comps.ell_comps_0 = af.UniformPrior(*PRIOR_ELL_COMPS)
        model.ell_comps.ell_comps_1 = af.UniformPrior(*PRIOR_ELL_COMPS)

    model.centre.centre_0 = af.UniformPrior(*PRIOR_CENTRE_Y)
    model.centre.centre_1 = af.UniformPrior(*PRIOR_CENTRE_X)
    model.effective_radius = af.UniformPrior(*PRIOR_EFFECTIVE_RADIUS)
    model.intensity = stroke["intensity"]
    model.sersic_index = stroke["sersic_index"]
    return model


def _vector_from(profile):
    """Free parameters of a profile: (centre_0, centre_1, [ell_comps_0, ell_comps_1,] effective_radius)."""
    vector = list(profile.centre)
    if not isinstance(profile, ag.lp.SersicSph):
        vector += list(profile.ell_comps)
    vector.append(profile.effective_radius)
    return np.array(vector, dtype=float)


def _profile_from(vector, truth):
    """Inverse of ``_vector_from``, taking the fixed parameters from ``truth``."""
    centre = (float(vector[0]), float(vector[1]))
    if isinstance(truth, ag.lp.SersicSph):
        return ag.lp.SersicSph(
            centre=centre,
            intensity=truth.intensity,
            effective_radius=float(vector[2]),
            sersic_index=truth.sersic_index,
        )
    return ag.lp.Sersic(
        centre=centre,
        ell_comps=(float(vector[2]), float(vector[3])),
        intensity=truth.intensity,
        effective_radius=float(vector[4]),
        sersic_index=truth.sersic_index,
    )


# Jitter (arc-seconds or ellipticity units) of each free parameter type.
JITTER = {"centre": 0.25, "ell_comps": 0.08, "effective_radius": 0.15}


def _search_path(n_frames):
    """
    For every stroke, the parameter vectors of the simulated search at each frame,
    from a prior draw (frame 0) to the true values (last ``CONVERGED_FRAMES``).
    """
    rng = np.random.default_rng(SEED)

    true_profiles = list(light_profiles_from(TARGET_STROKES, ag.lp).values())
    models = [stroke_model_from(stroke) for stroke in TARGET_STROKES]

    n_search = n_frames - CONVERGED_FRAMES
    steps = np.arange(n_search) / (n_search - 1)

    paths = []
    for model, truth in zip(models, true_profiles):
        start = model.instance_from_unit_vector(
            unit_vector=list(rng.uniform(0.05, 0.95, model.prior_count))
        )
        start_vector = _vector_from(start)
        true_vector = _vector_from(truth)

        # Convergence rate varies per stroke, so the letters lock in one by one.
        rate = rng.uniform(2.0, 6.0)
        remaining = np.exp(-rate * steps)
        remaining = (remaining - remaining[-1]) / (1.0 - remaining[-1])

        jitter_scale = np.array(
            [JITTER["centre"]] * 2
            + [JITTER["ell_comps"]] * (len(true_vector) - 3)
            + [JITTER["effective_radius"]]
        )
        jitter = rng.normal(size=(n_search, len(true_vector))) * jitter_scale
        jitter *= remaining[:, None] * (1.0 - remaining[:, None]) * 4.0

        path = (
            true_vector
            + remaining[:, None] * (start_vector - true_vector)
            + jitter
        )
        path[:, -1] = np.abs(path[:, -1])  # effective radius stays positive
        paths.append((truth, path))

    return paths, true_profiles


def frames_profiles(n_frames=animate.N_FRAMES):
    """Light profiles of every frame."""
    paths, true_profiles = _search_path(n_frames)

    frames = []
    for i in range(n_frames - CONVERGED_FRAMES):
        frames.append(
            [_profile_from(path[i], truth) for truth, path in paths]
        )
    frames += [true_profiles] * CONVERGED_FRAMES
    return frames


EXTENT = [-4.0, 4.0, -4.0, 4.0]


def make(n_frames=animate.N_FRAMES, write_pngs=False):
    frames = []
    for i, profiles in enumerate(frames_profiles(n_frames)):
        frames.append(animate.rgb_from(animate.image_from(profiles, EXTENT)))
        print(f"pyautofit frame {i + 1}/{n_frames}")

    if write_pngs:
        animate.save_pngs(frames, "autofit")

    return animate.save_gif(frames, "pyautofit.gif")


if __name__ == "__main__":
    print(make(write_pngs=True))
