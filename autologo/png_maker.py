import autolens as al
import autolens.plot as aplt

from autologo.strokes import PYAUTO_STROKES, light_profiles_from

# grid = al.Grid2DIterate.uniform(
#     shape_native=(150, 150),
#     pixel_scales=0.05,
#     fractional_accuracy=0.9999,
#     sub_steps=[2, 4, 8, 16, 24],
# )

grid = al.Grid2D.uniform(
    shape_native=(150, 150),
    pixel_scales=0.05,
)

source_galaxy = al.Galaxy(
    redshift=1.0,
    # "PyAuto" (light_0 ... light_19) is shared with the PyAutoGalaxy / PyAutoFit logos.
    **light_profiles_from(PYAUTO_STROKES, al.lp),
    light_20=al.lp.Sersic(
        centre=(-1.3, -2.2),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=100.0),
        intensity=0.6,
        effective_radius=1.0,
        sersic_index=2.5,
    ),
    light_21=al.lp.Sersic(
        centre=(-1.6, -2.1),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=100.0),
        intensity=0.6,
        effective_radius=1.0,
        sersic_index=2.5,
    ),
    light_22=al.lp.Sersic(
        centre=(-2, -1.6),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=5.0),
        intensity=0.5,
        effective_radius=0.8,
        sersic_index=2.5,
    ),
    light_23=al.lp.Sersic(
        centre=(-2, -1.9),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=5.0),
        intensity=0.5,
        effective_radius=0.8,
        sersic_index=2.5,
    ),
    light_24=al.lp.Sersic(
        centre=(-1.5, -0.7),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=0.0),
        intensity=0.6,
        effective_radius=1.0,
        sersic_index=2.5,
    ),
    light_25=al.lp.Sersic(
        centre=(-1.25, -0.55),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=-35.0),
        intensity=0.6,
        effective_radius=0.9,
        sersic_index=2.5,
    ),
    light_26=al.lp.Sersic(
        centre=(-1.25, -0.95),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=35.0),
        intensity=0.6,
        effective_radius=0.8,
        sersic_index=2.5,
    ),
    light_27=al.lp.Sersic(
        centre=(-1.65, -1.2),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=-65.0),
        intensity=0.5,
        effective_radius=0.9,
        sersic_index=2.5,
    ),
    light_28=al.lp.Sersic(
        centre=(-2.0, -0.85),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=-35.0),
        intensity=0.35,
        effective_radius=0.8,
        sersic_index=2.5,
    ),
    light_29=al.lp.Sersic(
        centre=(-2.0, -0.4),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=15.0),
        intensity=0.5,
        effective_radius=1.1,
        sersic_index=2.5,
    ),
    light_30=al.lp.Sersic(
        centre=(-1.9, 0.3),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=90.0),
        intensity=0.5,
        effective_radius=0.5,
        sersic_index=2.5,
    ),
    light_31=al.lp.Sersic(
        centre=(-1.3, 0.3),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=90.0),
        intensity=0.5,
        effective_radius=0.5,
        sersic_index=2.5,
    ),
    light_32=al.lp.Sersic(
        centre=(-1.4, 0.6),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.15, angle=13.0),
        intensity=0.6,
        effective_radius=0.8,
        sersic_index=2.5,
    ),
    light_33=al.lp.Sersic(
        centre=(-1.8, 0.95),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.2, angle=95.0),
        intensity=0.6,
        effective_radius=0.9,
        sersic_index=2.5,
    ),
    light_34=al.lp.Sersic(
        centre=(-1.1, 1.9),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.2, angle=155.0),
        intensity=0.5,
        effective_radius=0.8,
        sersic_index=2.5,
    ),
    light_35=al.lp.Sersic(
        centre=(-1.2, 1.5),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.2, angle=65.0),
        intensity=0.5,
        effective_radius=0.5,
        sersic_index=2.5,
    ),
    light_36=al.lp.Sersic(
        centre=(-1.5, 1.7),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.2, angle=165.0),
        intensity=0.7,
        effective_radius=0.5,
        sersic_index=2.5,
    ),
    light_37=al.lp.Sersic(
        centre=(-1.8, 2.0),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.2, angle=110.0),
        intensity=0.7,
        effective_radius=0.45,
        sersic_index=2.5,
    ),
    light_38=al.lp.Sersic(
        centre=(-2.1, 1.9),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.2, angle=30.0),
        intensity=0.7,
        effective_radius=0.5,
        sersic_index=2.5,
    ),
    light_39=al.lp.Sersic(
        centre=(-2.1, 1.45),
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.2, angle=150.0),
        intensity=0.7,
        effective_radius=0.6,
        sersic_index=2.5,
    ),
)



include_2d = aplt.Include2D(light_profile_centres=False)


galaxy_plotter = aplt.GalaxyPlotter(
    galaxy=source_galaxy, grid=grid, include_2d=include_2d
)
galaxy_plotter.figures_2d(image=True)


from matplotlib import rc, rcParams
import matplotlib.lines as mlines

rcParams["axes.spines.left"] = False
rcParams["axes.spines.right"] = False
rcParams["axes.spines.top"] = False
rcParams["axes.spines.bottom"] = False


rcParams["xtick.top"] = False  # draw ticks on the top side
rcParams["xtick.bottom"] = False  # draw ticks on the bottom side
rcParams["xtick.labeltop"] = False  # draw label on the top
rcParams["xtick.labelbottom"] = False

rcParams["ytick.left"] = False  # draw ticks on the left side
rcParams["ytick.right"] = False  # draw ticks on the right side
rcParams["ytick.labelleft"] = False  # draw tick labels on the left side#%%
rcParams["ytick.labelright"] = False

rcParams["image.aspect"] = "auto"


import numpy as np
import os

# pl2 = al.mp.PowerLaw(einstein_radius=7,
#                         ell_comps=al.convert.ell_comps_from(axis_ratio=0.5, angle=-35),
#                          centre=(2, -2),
#                       slope=2.1)


r_eins = np.arange(0, 10.75, 0.15)

r_eins_decrease = list(r_eins[::-1])
factor_list = list(np.linspace(0, 1, len(r_eins_decrease)))

fig_path = os.getcwd()

start_value = 12.5

extent_start = [-start_value, start_value, -start_value, start_value]
extent_final = [-4.0, 4.0, -4.0, 4.0]

image_plane_grid = al.Grid2D.uniform(shape_native=(1000, 1000), pixel_scales=0.025)

# image_plane_grid = al.Grid2D.uniform(shape_native=(375, 375), pixel_scales=0.075)

for i in range(len(r_eins_decrease)):

    factor = factor_list[i]

    extent_0 = (1.0 - factor) * extent_start[0] + (factor) * extent_final[0]
    extent_1 = (1.0 - factor) * extent_start[1] + (factor) * extent_final[1]
    extent_2 = (1.0 - factor) * extent_start[2] + (factor) * extent_final[2]
    extent_3 = (1.0 - factor) * extent_start[3] + (factor) * extent_final[3]

    extent = [extent_0, extent_1, extent_2, extent_3]

    pl = al.mp.PowerLaw(
        einstein_radius=r_eins_decrease[i],
        ell_comps=al.convert.ell_comps_from(axis_ratio=0.6, angle=-15),
        centre=(0, 0),
        slope=2.3,
    )
    lens_galaxy = al.Galaxy(redshift=0.2, mass_1=pl)
    tracer = al.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

    include_2d = aplt.Include2D(
        radial_critical_curves=False,
        radial_caustics=False,
        tangential_critical_curves=False,
        tangential_caustics=False,
        light_profile_centres=False,
        mass_profile_centres=False,
    )
    matplot_2d = aplt.MatPlot2D(
        output=aplt.Output(
            path=f"{fig_path}/pngs/", filename=f"{i}_autolens", format="png", bbox_inches="tight",
        ),
        axis = aplt.Axis(extent=extent),
        figure=aplt.Figure(figsize=(24, 12), aspect="auto"),
        title=aplt.Title(label=""),
        #    xlabel=aplt.XLabel(label=""),
        #    ylabel=aplt.YLabel(label=""),
        colorbar=False,
            )

    tracer_plotter = aplt.TracerPlotter(
        tracer=tracer,
        grid=image_plane_grid,
        include_2d=include_2d,
        mat_plot_2d=matplot_2d,
    )

    tracer_plotter.figures_2d(image=True)

    print(f"pngs {i}")


