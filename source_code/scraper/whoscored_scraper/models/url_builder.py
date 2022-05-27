from source_code.scraper.whoscored_scraper.models import constants_whoscored


def create_mls_url():
    return '{}/Regions/{}/Tournaments/{}/Seasons/{}/Stages/{}/Show/{}-{}'.format(constants_whoscored.WHOSCORED_URL,
                                                                                 constants_whoscored.LEAGUES_ID[
                                                                                     constants_whoscored.LEAGUE_INDEX],
                                                                                 constants_whoscored.LEAGUES_NUM[
                                                                                     constants_whoscored.LEAGUE_INDEX],
                                                                                 constants_whoscored.SEASON_ID[
                                                                                     constants_whoscored.LEAGUE_INDEX][
                                                                                     constants_whoscored.SEASON_INDEX],
                                                                                 constants_whoscored.PLAYOFF_ID[
                                                                                     constants_whoscored.LEAGUE_INDEX][
                                                                                     constants_whoscored.SEASON_INDEX],
                                                                                 constants_whoscored.LEAGUES_LINK[
                                                                                     constants_whoscored.LEAGUE_INDEX],
                                                                                 constants_whoscored.SEASON_NUMBER[
                                                                                     constants_whoscored.SEASON_INDEX])


def create_eredivise_championship():
    return '{}/Regions/{}/Tournaments/{}/Seasons/{}/Stages/{}/Show/{}-{}-{}'.format(
        constants_whoscored.WHOSCORED_URL,
        constants_whoscored.LEAGUES_ID[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.LEAGUES_NUM[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.SEASON_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
        constants_whoscored.PLAYOFF_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
        constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.SEASON_NUMBER[
            constants_whoscored.SEASON_INDEX],
        constants_whoscored.SEASON_NUMBER[
            constants_whoscored.SEASON_INDEX + 1])


def create_current_eredivise_championship():
    return '{}/Regions/{}/Tournaments/{}/Seasons/{}/Stages/{}/Show/{}-{}-{}'.format(
        constants_whoscored.WHOSCORED_URL,
        constants_whoscored.LEAGUES_ID[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.LEAGUES_NUM[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.SEASON_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
        constants_whoscored.PLAYOFF_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
        constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.SEASON_NUMBER[
            constants_whoscored.SEASON_INDEX],
        str(int(constants_whoscored.SEASON_NUMBER[
            constants_whoscored.SEASON_INDEX])+1))


def create_china_superleage_url():
    return '{}/Regions/{}/Tournaments/{}/Seasons/{}/Stages/{}/Show/{}-{}-{}'.format(
        constants_whoscored.WHOSCORED_URL,
        constants_whoscored.LEAGUES_ID[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.LEAGUES_NUM[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.SEASON_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
        constants_whoscored.PLAYOFF_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
        constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.SEASON_NUMBER[
            constants_whoscored.SEASON_INDEX],
        constants_whoscored.SEASON_NUMBER[
            constants_whoscored.SEASON_INDEX])


def url_builder():
    if constants_whoscored.LEAGUE_INDEX in [9]:
        return create_mls_url()
    elif constants_whoscored.LEAGUE_INDEX in [5, 6, 11, 17, 18, 19, 20] and constants_whoscored.SEASON_INDEX < (
            len(constants_whoscored.SEASON_NUMBER) - 1):
        return create_eredivise_championship()
    elif constants_whoscored.LEAGUE_INDEX in [6, 11, 17, 18, 19, 20] and constants_whoscored.SEASON_INDEX == (
            len(constants_whoscored.SEASON_NUMBER)-1):
        return create_current_eredivise_championship()
    elif constants_whoscored.LEAGUE_INDEX in [13] and constants_whoscored.SEASON_INDEX < (
            len(constants_whoscored.SEASON_NUMBER)):
        return create_china_superleage_url()
    else:
        return '{}/Regions/{}/Tournaments/{}/Seasons/{}/{}'.format(constants_whoscored.WHOSCORED_URL,
                                                                   constants_whoscored.LEAGUES_ID[
                                                                       constants_whoscored.LEAGUE_INDEX],
                                                                   constants_whoscored.LEAGUES_NUM[
                                                                       constants_whoscored.LEAGUE_INDEX],
                                                                   constants_whoscored.SEASON_ID[
                                                                       constants_whoscored.LEAGUE_INDEX][
                                                                       constants_whoscored.SEASON_INDEX],
                                                                   constants_whoscored.LEAGUES_LINK[
                                                                       constants_whoscored.LEAGUE_INDEX])