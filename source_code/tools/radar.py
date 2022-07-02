import source_code.tools.models.constants as constants

#
from source_code.tools.models.complex_radar import run_radar
from source_code.tools.models.radar_constants import ranges_forward, variables_forward, ranges_midfield, \
    variables_midfield, ranges_centerback, variables_centerback

if __name__ == "__main__":
    colors = [
        (
            constants.BARCELONA_PLOT,
            constants.BARCELONA_FILL
        )
    ]

    datas = [
        (
            78.88631090487239,0.8333333333333334,2.8327868852459015,0.18427114677854514,0.06504942102714846,1.4163934426229507,1.1213114754098361,2.183606557377049,0.17704918032786884,2.537704918032787,0.17704918032786884

        )]

    ranges = ranges_forward
    variables = variables_forward
    #
    # ranges = ranges_midfield
    # variables = variables_midfield

    # ranges = ranges_fullback
    # variables = variables_fullback

    # ranges = ranges_centerback
    # variables = variables_centerback

    run_radar(datas=datas, ranges=ranges, variables=variables, colors=colors)
