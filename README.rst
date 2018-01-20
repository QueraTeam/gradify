=======
Gradify
=======

A python library to generate CSS gradient from an image. This is a fork of
https://github.com/fraser-hemp/gradify. The original gradify project had only a CLI
interface. With this fork, you can use gradify as a library in your Python code.

.. image:: https://user-images.githubusercontent.com/2115303/35187613-c6fe6fe8-fe3b-11e7-9b9d-3e088e460a1d.jpg

Installation
============

Install the latest release from PyPI:

.. code-block:: sh

    pip install gradify


Usage
=====

.. code-block:: python

    gradify.generate_css(fp, single_color=False, use_color_spread=False)

- ``fp``: a filename (string), pathlib.Path object or a file object.
  The file object must implement read(), seek(), and tell() methods,
  and be opened in binary mode.

- ``single_color``: only produce a single, uniform background color -
  this is much quicker and has all browser support

- ``use_color_spread``: this flag will give the color which has the least
  spread over the image the highest priority when assigning directions
  (opposed to most dominant color). This feature improves overall accuracy,
  however adds complexity and in unique cases it produces counter-intuitive results

Example:

.. code-block:: python

    import gradify
    css = gradify.generate_css('sample.png')

Advanced Usage
==============

You can use ``Gradify`` class for advanced usage.

.. code-block:: python

    from gradify import Gradify

    # simple usage
    g = Gradify('sample.png', single_color=False, use_color_spread=False)
    css = g.generate_css()

    # advanced usage
    g = Gradify('sample.png', single_color=False, use_color_spread=False, black_sensitivity=4.3,
                white_sensitivity=3, num_colors=4, resize=55, uniformness=7, use_prefixes=False)
    css = g.generate_css()


Default parameters produce good result.

From original repo:

    The only suggestion is increasing the uniformness (by lowering it's value). It can improve
    the general case, improve speed, but decrease the upper limits of accuracy.
    Increasing sensitivity to black will do the same.

Credits
=======

Many thanks to `Fraser Hemphill`_ for writing the original gradify project.

License
=======

MIT


.. _`Fraser Hemphill`: https://github.com/fraser-hemp
