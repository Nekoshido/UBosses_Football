# -*- coding: utf-8 -*-

YEARS = ['2014', '2015', '2016', '2017']

SEASONS = ['2014/2015', '2015/2016', '2016/2017', '2017/2018']

LEAGUES = ['EPL', 'La_liga', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL']

# league_num is the league
TEAM_INDEX = 0
LEAGUE_NUM = 0
YEARS_INDEX = 0
LEAGUE_TEXT = LEAGUES[LEAGUE_NUM]
YEAR_TEXT = YEARS[YEARS_INDEX]
SEASON_TEXT = SEASONS[YEARS_INDEX]

ORIGINAL_UNDERSTAT_URL = 'https://understat.com/'
UNDERSTAT_URL = ORIGINAL_UNDERSTAT_URL + 'league/' + LEAGUE_TEXT + '/' + YEAR_TEXT

PLAYERS_WRITE = ('Name, Season, Team, General Performance, Performance by Position, Performance by Situation,'
                 ' Performance by Shot Zones, Performance by Shot Types\n')

TEAMS_WRITE = ('Name, Season, Team, Performance by Situation, Performance by Formation, Performance by Game State, '
               'Performance by Timing, Performance by Shot Zones, Performance by Attack Speed, '
               'Performance by Result\n')

