# Gradify

A python 3 library to generate CSS gradient from an image.

Forked from https://github.com/fraser-hemp/gradify

# Installation

`pip install git+ssh://git@github.com/QueraTeam/gradify.git`

# Usage

gradify.gradify(fp, single_color=False, use_color_spread=False)

- `fp`: a filename (string), pathlib.Path object or a file object.
The file object must implement read(), seek(), and tell() methods,
and be opened in binary mode.
- `single_color`: only produce a single, uniform background color -
this is much quicker and has all browser support
- `use_color_spread`: this flag will give the color which has the least
spread over the image the highest priority when assigning directions
(opposed to most dominant color). This feature improves overall accuracy,
however adds complexity and in unique cases it produces counter-intuitive results

```py
import gradify
css = gradify.gradify('sample.png')
```

# Notes

There are constants you can tweak which will later be flags (Black/White sensitivity, image resolution, uniformness of colors) although generally the default vals are generally best.

The only suggestion is increasing the uniformness (by lowering it's val) can improve the general case, improve speed, but decrease the upper limits of accuracy. Increasing sensitivity to black will do the same.

# License MIT

Copyright (c) 2017 Mohammad Javad Naderi

Copyright (c) 2015 Fraser Hemphill

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
