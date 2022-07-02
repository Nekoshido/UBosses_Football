import numpy as np
import matplotlib.pyplot as plt


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

    @staticmethod
    def _invert(x, limits):
        """inverts a value x on a scale from
        limits[0] to limits[1]"""
        return limits[1] - (x - limits[0])

    def _scale_data(self, data, ranges):
        """scales data[1:] to ranges[0],
        """
        # for d, (y1, y2) in zip(data[1:], ranges[1:]):
        # for d, (y1, y2) in zip(data, ranges):
        #     assert (y1 <= d <= y2) or (y2 <= d <= y1)
        x1, x2 = ranges[0]
        sdata = []
        for d, (y1, y2) in zip(data, ranges):
            if y1 > y2:
                d = self._invert(d, (y1, y2))
                y1, y2 = y2, y1
            if d > y2: d = y2
            if d < y1: d = y1
            sdata.append((d - y1) / (y2 - y1) * (x2 - x1) + x1)
        return sdata

    def plot(self, data, *args, **kw):
        sdata = self._scale_data(data, self.ranges)
        l = self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
        return l

    def fill(self, data, *args, **kw):
        sdata = self._scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)


def run_radar(ranges, variables, datas, colors, index_name=""):
    fig1 = plt.figure(figsize=(8, 8))
    radar = ComplexRadar(fig1, variables, ranges)
    lax = []

    index = [index_name]

    for i, name in enumerate(index):
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
