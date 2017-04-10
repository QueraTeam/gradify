from PIL import Image, ImageFilter
from operator import itemgetter
import sys


""" Image Gradients
Python 3 module for analysing an image for its 4 most prominent colors, and creating a CSS gradient.
Original source code: https://github.com/fraser-hemp/gradify
Forked and modified by Mohammad Javad Naderi
"""


class Gradify:
    """ Image Analyser
    Main class to do the analysis
    """

    # Cross browser prefixes.
    BROWSER_PREFIXES = ["", "-webkit-", "-moz-", "-o-", "-ms-"]

    def __init__(self, fp, single_color=False, use_color_spread=False, black_sensitivity=4.3, white_sensitivity=3,
                 num_colors=4, resize=55, uniformness=7, webkit_only=False):

        self.MAX_COLORS = num_colors
        self.RESIZE_VAL = resize
        self.UNIFORMNESS = uniformness
        self.spread_quadrants = True

        if webkit_only:
            self.BROWSER_PREFIXES = ["-webkit-"]

        self.IGNORED_COLORS = {
            "BLACK": {
                "col": (0, 0, 0),
                "radius": black_sensitivity
            },
            "WHITE": {
                "col": (255, 255, 255),
                "radius": white_sensitivity
            }
        }

        # 1 color background (no gradient)
        self.single_color = single_color

        # Uses color's spread in each quadrant rather than it's strength: flattens bell curve of accuracy
        self.use_color_spread = use_color_spread
        
        self.image = Image.open(fp).resize((100, 100), Image.ANTIALIAS)

    def get_directions(self):

        col = self.get_colors()

        if self.single_color:
            return col
            # self.pairs.append((self.num_done, col))
            # return
        quad_cols = [0] * 4
        taken = [0] * 4
        cols_quads = [0] * 4

        for i in range(len(col)):
            count = 0
            # 0 - left, 1 - bottom, 2 - right, 3 - top
            a = [0] * 4
            for pix in self.image.getdata():
                if self.get_rgb_diff(pix, col[i]) < 4.2:
                    if int((count % 100) / 50) == 1:
                        a[2] += 1
                    else:
                        a[0] += 1
                    if int((count / 100.0) / 50) == 0:
                        a[3] += 1
                    else:
                        a[1] += 1
                count += 1
            cols_quads[i] = a
            while 0 in taken and not self.use_color_spread:
                best_quad = a.index(max(a))
                if max(a) == 0:
                    best_quad = taken.index(0)
                if taken[best_quad] == 0:
                    taken[best_quad] = 1
                    col[i] = list(col[i])
                    col[i].append(best_quad * 90)
                    quad_cols[i] = col[i]
                    break
                else:
                    a[best_quad] = 0

        if self.use_color_spread:
            quad_cols = self.calculate_spread(cols_quads, col)

        return quad_cols
        # self.pairs.append((self.num_done, quad_cols))

    @staticmethod
    def calculate_spread(spread_quads, col):
        strength_spread = []
        quad_cols = [0] * 4
        taken_col = [0] * 4
        taken_quads = [0] * 4
        for quad in spread_quads:
            top = quad[3] * 1.0 / (quad[1] + 0.01)
            left = quad[2] * 1.0 / (quad[0] + 0.01)
            if left < 1:
                left = 1 / (left + 0.01)
            if top < 1:
                top = 1 / (top + 0.01)
            strength_spread.append(top)
            strength_spread.append(left)
        # TODO: Make more readable
        while 0 in taken_col:
            best_col = int(strength_spread.index(max(strength_spread)) / 2)
            if max(strength_spread) is 0:
                best_col = taken_col.index(0)
            if taken_col[best_col] is 0:
                best_quad = spread_quads[best_col].index(max(spread_quads[best_col]))
                if max(spread_quads[best_col]) is 0:
                    sys.stderr.write(str(spread_quads))
                    best_quad = taken_quads.index(0)
                if taken_quads[best_quad] is 0:
                    taken_quads[best_quad] = 1
                    taken_col[best_col] = 1
                    col[best_col] = list(col[best_col])
                    col[best_col].append(best_quad * 90)
                    quad_cols[best_col] = col[best_col]
                spread_quads[best_col][best_quad] = 0
            strength_spread[strength_spread.index(max(strength_spread))] = 0

        return quad_cols

    def generate_css(self):
        c = self.get_directions()
        i = 0
        s = "background:"
        if self.single_color:
            s += "rgb(" + str(c[0]) + "," + str(c[1]) + "," + str(c[2]) + ");"
        else:
            s += "rgb(" + str(c[0][0]) + "," + str(c[0][1]) + "," + str(c[0][2]) + ");"
            s += "background:"
            for prefix in self.BROWSER_PREFIXES:
                for color in c:
                    s += prefix + "linear-gradient(" + str(color[3]) + "deg, rgba(" + str(color[0]) + "," + str(
                        color[1]) + "," + str(color[2]) + "," + str(1) + ") 0%, rgba(" + str(color[0]) + "," + str(
                        color[1]) + "," + str(color[2]) + ",0) 100%)"
                    i += 1
                    if i == self.MAX_COLORS:
                        s += ";"
                        break
                    s += ","
        return s

    def get_colors(self):
        image = self.image.resize((55, 55), Image.ANTIALIAS)

        h = image.filter(ImageFilter.BLUR)
        h = h.histogram()
        colors = []
        # split into red, green, blue
        r = h[0:256]
        g = h[256:256 * 2]
        b = h[256 * 2: 256 * 3]
        # Rank the histogram in order of appearance
        self.ranked_colors = sorted(image.getcolors(image.size[0] * image.size[1]), key=itemgetter(0))
        for i in range(len(self.ranked_colors)):
            colors.append(self.ranked_colors[len(self.ranked_colors) - 1 - i])
        if self.MAX_COLORS is 1:
            return colors[0]
        else:
            return self.find_best_colors(colors)

    @staticmethod
    def get_rgb_diff(old, new):
        # Currently an approximation of LAB colorspace
        return abs(1.4 * abs(old[0] - new[0]) ** (1 / 2.0) + .8 * abs(old[1] - new[1]) ** (1 / 2.0) + .8 * abs(
            old[2] - new[2]) ** (1 / 2.0)) ** (1 / 2.0)

    def find_single_color(self, colors):
        for i in range(len(colors)):
            diffB = self.get_rgb_diff(self.IGNORED_COLORS["BLACK"]["col"], colors[i][1])
            diffW = self.get_rgb_diff(self.IGNORED_COLORS["WHITE"]["col"], colors[i][1])
            if diffB > 4 and diffW > 3.5:
                # IF too close to Black or White, ignore this color
                sys.stderr.write(str(diffB) + "\n")
                sys.stderr.write(str(colors[i][1]) + "\n")
                return colors[i][1]
        # Worst-case return first color
        return colors[0][1]

    def find_best_colors(self, colors):
        selected_colors = []
        sensitivity = self.UNIFORMNESS
        ignored_radius = 0
        if self.single_color:
            return self.find_single_color(colors)
        while len(selected_colors) < self.MAX_COLORS:
            selected_colors = []
            for i in range(len(colors)):
                bad_color = False
                for col, col_dict in self.IGNORED_COLORS.items():
                    diff = self.get_rgb_diff(col_dict["col"], colors[i][1])
                    if diff < col_dict["radius"] - ignored_radius:
                        # IF too close to Black or White, ignore this color
                        bad_color = True
                        break
                for j in range(len(selected_colors)):
                    diff = self.get_rgb_diff(colors[i][1], selected_colors[j])
                    if diff < sensitivity:
                        # IF too close to any other selected color, ignore.
                        bad_color = True
                        break
                if bad_color:
                    continue
                selected_colors.append(colors[i][1])
            if ignored_radius < 2:
                ignored_radius += 1
            else:
                sensitivity -= 1
                ignored_radius = 0

        return selected_colors[0:4]


def gradify(fp, single_color=False, use_color_spread=False):
    g = Gradify(fp, single_color=single_color, use_color_spread=use_color_spread)
    return g.generate_css()
