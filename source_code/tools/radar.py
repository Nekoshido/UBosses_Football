import numpy as np
import matplotlib.pyplot as plt

import source_code.tools.constants as constants


def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    return limits[1] - (x - limits[0])


def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    """
    # for d, (y1, y2) in zip(data[1:], ranges[1:]):
    # for d, (y1, y2) in zip(data, ranges):
    #     assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    sdata = []
    for d, (y1, y2) in zip(data, ranges):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        if d > y2: d = y2
        if d < y1: d = y1
        sdata.append((d - y1) / (y2 - y1) * (x2 - x1) + x1)
    return sdata


class ComplexRadar():
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles = np.arange(0, 360, 360. / len(variables))

        axes = [fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True,
                             label="axes{}".format(i))
                for i in range(len(variables))]

        l, text = axes[0].set_thetagrids(angles, labels=variables)
        axes[0].tick_params(pad=20)
        [txt.set_rotation(angle - 90) for txt, angle in zip(text, angles)]
        # axes[0].set_title("Ronaldo")
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):

            # l, text = axes[i].set_thetagrids( np.array([angles[i]]), labels= np.array([variables[i]]))
            # axes[i].tick_params(width=2, pad=15)
            # text[0].set_rotation(angles[i]-90)

            grid = np.linspace(*ranges[i], num=n_ordinate_levels)
            gridlabel = ["{}".format(round(x, 2))
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1]  # hack to invert grid
                # gridlabels aren't reversed
            gridlabel[0] = ""  # clean up origin

            # radii = ax.convert_xunits(grid)
            # radii = np.asarray(radii)

            # ax.set_yticks(radii)
            #
            # ax.set_yticklabels(gridlabel)
            #
            # ax.set_rlabel_position(angles[i])

            ax.set_rgrids(grid, labels=gridlabel,
                          angle=angles[i])
            # ax.spines["polar"].set_visible(False)
            if ranges[i][0] > ranges[i][1]:
                tmp_range = (ranges[i][1], ranges[i][0])
            else:
                tmp_range = ranges[i]
            ax.set_ylim(tmp_range)
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]

    def plot(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        l = self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
        return l

    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)


fig1 = plt.figure(figsize=(8, 8))

variables_midfield = ("Scoring contribution", "Through ball", "Chances created",
                      "% Passing", "Long Balls", "Interceptions",
                      "Tackles", "Tackles accuracy", "Fouls",
                      "Dispossessed", "Successful Dribbles")

variables_forward = ("% Passing", "% Shooting", "Shots",
                     "Non-Penalty Goals", "% Goal Conversion", "Successful Dribbles",
                     "Dispossessed", "Int+Tackles", "Throughballs",
                     "Key Passes", "Assists")

variables_fullback = ("Passing %", "Interceptions", "Tackles %",
                      "Tackles", "Fouls", "Dribbled Past", "Aerial Wins",
                      "Dispossessed", "Successful Dribbles",
                      "Crossing %", "Comp. Crosses", "Key Passes")

variables_centerback = ("Interceptions", "Tackles", "Tackles %",
                        "Dribbled Past", "Passing %", "Long Balls",
                        "Long Balls %", "Aerial Wins", "Aerial Wins %",
                        "Fouls", "Clearances", "Total Block")

ranges_forward = [(60.249548, 84.768278), (0.458333, 0.757576), (1.079975, 3.823562),
                  (0.093976, 0.458415), (0.065471, 0.150828), (0.227998, 2.968950),
                  (3.013611, 0.813238), (0.494256, 3.413170), (0.000000, 0.182096),
                  (0.564970, 2.543016), (0.000000, 0.350861)]

ranges_midfield = [(0.0, 0.664351), (0.0, 0.195313), (0.193237, 2.578699),
                   (68.782996, 89.389483), (0.507248, 5.478869), (0.276554, 2.386976),
                   (0.696775, 3.401383), (43.750000, 81.915052), (2.614228, 0.555767),
                   (2.633632, 0.231204), (0.116280, 2.694309)]

ranges_fullback = [(65.312280, 87.936531), (0.785714, 3.327623), (56.944444, 87.500000),
                   (1.029225, 3.569316), (2.142857, 0.490597), (1.592686, 0.256847),
                   (0.383564, 3.195443), (1.638058, 0.103093), (0.073171, 1.708861),
                   (0.000000, 37.500000), (0.000000, 1.555058), (0.123144, 1.696841)]

ranges_centerback = [(0.614300, 3.528430), (1.056413, 3.152353), (50.394737, 98.846154),
                     (1.769866, 0.023038), (56.367473, 84.551554), (0.819657, 4.292086),
                     (23.160839, 56.932084), (0.572950, 3.434169), (32.321429, 66.666667),
                     (2.021546, 0.503185), (1.130538, 5.267605), (0.749127, 2.525655)]
#
ranges = ranges_forward
variables = variables_forward

# ranges = ranges_midfield
# variables = variables_midfield

# ranges = ranges_fullback
# variables = variables_fullback

# ranges = ranges_centerback
# variables = variables_centerback

radar = ComplexRadar(fig1, variables, ranges)
lax = []

index = ["Scott McTominay"]

colors = [
    (
        constants.BARCELONA_PLOT,
        constants.BARCELONA_FILL
    )
]

datas = [
    (
        76.64670658682635, 0.47619047619047616, 2.0, 0.32204628916382455, 0.16102314458191228, 0.7619047619047619,
        1.1428571428571428, 1.0476190476190477, 0.0, 0.5714285714285714, 0.09523809523809523

    )]

for i, name in enumerate( index):
    # data = df_midfield.iloc[i].values
    data = datas[i]
    color_plot = colors[i][0]
    color_fill = colors[i][1]
    l, = radar.plot(data, label=name, color=color_plot)
    lax.append(l)
    radar.fill(data, alpha=0.2, color=color_fill)
#
# legendax = fig1.add_axes([0.8, 0.8, 0.1, .1])
# legendax.legend(handles=lax, labels=index, loc=3, bbox_to_anchor=(0, 0, 1, 1), bbox_transform=fig1.transFigure)
# legendax.axis('off')

plt.show()
