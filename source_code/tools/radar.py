import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import constants


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


# df = pd.DataFrame({
#     "Spe": pd.Series([89, 83]),
#     "Str": pd.Series([69, 53]),
#     "Det": pd.Series([82, 44]),
#     "Extr": pd.Series([59, 74]),
#     "Int": pd.Series([63, 11]),
#     "Est": pd.Series([12, 69]),
#     "Ape": pd.Series([29, 13]),
# })

# df_midfield = pd.DataFrame({
#     "Long Balls": pd.Series([3.341067285]), #6
#     "% Passing": pd.Series([94.45114596]), #1
#     "Chances created": pd.Series([0.835266821]) ,#2
#     "Through ball": pd.Series([0.104408353]), #11
#     "Scoring contribution": pd.Series([0.104408353]),#7
#     "Successful Dribbles": pd.Series([0.522041763]), #8
#     "Dispossessed": pd.Series([0.939675174]), #3
#     "Fouls": pd.Series([0.835266821]), #4
#     "Tackles accuracy": pd.Series([63.63636364]), #10
#     "Tackles": pd.Series([0.730858469]), #9
#     "Interceptions": pd.Series([0.522041763]) #5
# })
#
# variables = [k[0] for k in df_midfield.iteritems()]
# ranges_midfield = [
#                 (66.486266, 88.591800),  # 1
#                 (0.248980, 2.471769),  # 2
#                 (2.742811, 0.257904),  # 3
#                 (2.547170, 0.522244),  # 4
#                 (0.219794, 2.307600),  # 5
#                 (0.333333, 5.039712),  # 6
#                 (0.0, 0.670211),  # 7
#                 (0.137625, 2.745110),  # 8
#                 (0.629371, 3.308796),  # 9
#                 (42.857143, 83.333333),  # 10
#                 (0.0, 0.180171),  # 11
#                 ]
#
#
# ranges = ranges_midfield
fig1 = plt.figure(figsize=(8, 8))

variables_midfield = ("Scoring contribution", "Through ball", "Chances created",
             "% Passing", "Long Balls", "Interceptions",
             "Tackles", "Tackles accuracy", "Fouls",
             "Dispossessed", "Successful Dribbles")

variables_forward = ("% Passing", "% Shooting", "Shots",
                 "Non-Penalty Goals", "% Goal Conversion", "Successful Dribbles",
                 "Dispossessed", "Int+Tackles", "Throughballs",
                 "Key Passes", "Assists")

ranges_forward = [(60.249548, 84.768278), (0.458333, 0.757576), (1.079975, 3.823562),
 (0.093976, 0.458415), (0.065471, 0.150828), (0.227998, 2.968950),
 (3.013611, 0.813238), (0.494256, 3.413170), (0.000000, 0.182096),
 (0.564970, 2.543016), (0.000000, 0.350861)]

ranges_midfield = [(0.0, 0.664351), (0.0, 0.195313), (0.193237, 2.578699),
          (68.782996, 89.389483), (0.507248, 5.478869), (0.276554, 2.386976),
          (0.696775, 3.401383), (43.750000, 81.915052), (2.614228, 0.555767),
          (2.633632, 0.231204), (0.116280, 2.694309)]

ranges = ranges_forward
variables = variables_forward

# ranges = ranges_midfield
# variables = variables_midfield

radar = ComplexRadar(fig1, variables, ranges)
lax = []

index = ["Xavi 2011"]

datas = [(
    75.63025210084034, 0.6875, 1.49843912591051, 0.12017044826007156, 0.08019708387356163, 2.9500520291363164,
    2.8563995837669096, 2.575442247658689, 0.18730489073881373, 1.7793964620187306, 0.09365244536940688
          )]

for i, name in enumerate(index):
    # data = df_midfield.iloc[i].values
    data = datas[i]
    color_plot = constants.MADRID_PLOT
    color_fill = constants.MADRID_FILL
    l, = radar.plot(data, label=name, color=color_plot)
    lax.append(l)
    radar.fill(data, alpha=0.2, color=color_fill)
#
# legendax = fig1.add_axes([0.8, 0.8, 0.1, .1])
# legendax.legend(handles=lax, labels=index, loc=3, bbox_to_anchor=(0, 0, 1, 1), bbox_transform=fig1.transFigure)
# legendax.axis('off')

plt.show()
