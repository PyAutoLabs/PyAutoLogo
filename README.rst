PyAutoLogo
==========

Code to produce the **PyAutoLens**, **PyAutoGalaxy** and **PyAutoFit** animated logos and host them.

All three logos are 1860 x 924 pixel looping GIFs (72 frames at 100 ms, final frame held for 2.1 s)
coloured with matplotlib's ``jet`` colormap. Every letter is drawn by elongated Sersic light profiles,
and the "PyAuto" row is shared by all three (``autologo/strokes.py``).

================================  =====================================  ===========================================
GIF                               Generator                              Animation
================================  =====================================  ===========================================
``gifs/pyautolens.gif``           ``autologo/png_maker.py`` +            A lens galaxy's Einstein radius shrinks to
                                  ``autologo/make_gifs.py``              zero, unlensing the arcs into "PyAuto Lens".
``gifs/pyautogalaxy.gif``         ``autologo/make_pyautogalaxy.py``      A rotating spiral galaxy unwinds its arms
                                                                         into "PyAuto Galaxy".
``gifs/pyautofit.gif``            ``autologo/make_pyautofit.py``         A model fit converges from a random prior
                                                                         draw onto "PyAuto Fit".
================================  =====================================  ===========================================

Regenerating the logos
----------------------

Run from the repository root, with ``autogalaxy`` and ``autofit`` installed:

.. code-block:: bash

    python -m autologo.make_pyautogalaxy
    python -m autologo.make_pyautofit

Each script writes its GIF to ``gifs/`` and the individual frames to the git-ignored ``pngs/`` folder,
taking under a minute on a laptop. Shared rendering (grid, colour scale, GIF timing) is in
``autologo/animate.py``.

The PyAutoLens logo was made with an older ``autolens`` plotting API: ``python -m autologo.png_maker``
renders its frames into ``pngs/`` and ``autologo/make_gifs.py`` assembles them, after which the GIF was
optimised with ezgif.
