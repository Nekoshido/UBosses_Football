# -*- coding: utf-8 -*-

LEAGUES = ['spanish-la-liga', 'english-premier-league', 'italian-serie-a', 'german-bundesliga',
           'french-ligue-1', 'dutch-eredivisie', 'russian-premier-league', 'us-major-league-soccer',
           'brazilian-serie-a', 'mexican-liga-mx', 'mexican-primera-apertura', 'english-football-league-championship',
           'australian-a-league', 'turkish-super-lig', 'portuguese-primeira-liga']

LEAGUE_TEAM_LIST = ['Spanish La Liga', 'English Barclays Premier League', 'Italian Serie A', 'German Bundesliga',
                    'French Ligue 1', 'Dutch Eredivisie', 'Russian Premier League', 'US Major League Soccer',
                    'Brazilian Serie A', 'Mexican Liga MX - Clausura', 'Mexican Liga MX - Apertura',
                    'English Football League - Championship',
                    'Australian A-League', 'Turkish Super Lig', 'Portuguese Primeira Liga']

LEAGUES_LINK = ['spanish-la-liga', 'english-barclays-premier-league', 'italian-serie-a', 'german-bundesliga',
                'french-ligue-1', 'dutch-eredivisie', 'russian-premier-league', 'us-major-league-soccer',
                'brazilian-serie-a', 'mexican-liga-mx---clausura', 'mexican-liga-mx---apertura',
                'english-football-league---championship',
                'australian-a-league', 'turkish-super-lig', 'portuguese-primeira-liga']

# Index for the league in the url
LEAGUE_INDEX = ['23', '8', '21', '22',
                '24', '9', '129', '98',
                '363', '385', '199', '10',
                '214', '115', '99']

# Index of the season by league in the url
SEASON_INDEX_BY_LEAGUE = [['4', '69', '136', '176', '712','862'],  # Spanish La Liga
                          ['2', '64', '126', '165', '641', '819'],  # Premier League
                          ['6', '76', '137', '177', '717','869'],  # Serie A
                          ['5', '66', '129', '169', '682','846'],  # Bundesliga
                          ['3', '58', '118', '167', '629','822'],  # Ligue 1
                          ['', '77', '123', '164', '642','816'],  # Eredivisie
                          ['', '75', '133', '168', '',''],  # Russian Premier League
                          ['', '49', '95', '149', '498',''],  # US Major League Soccer
                          ['', '73', '103', '154', '545',''],  # Brazilian Serie A
                          ['', '99', '150', '', '',''],  # Mexican Liga MX - Clausura
                          ['', '74', '134', '162', '',''],  # Mexican Liga MX - Apertura
                          ['', '93', '127', '166', '657','829'],  # English Football League - Championship
                          ['', '94', '125', '173', '635',''],  # Australian A-League
                          ['', '', '145', '175', '715',''],  # Turkish Super Lig
                          ['', '', '', '', '714','852']  # Portuguese Primeira Liga
                          ]

LEAGUE_SPECIAL_PREMIER_LEAGUE = 'english-premier-league'

# league_num is the league
LEAGUE_NUM = 4
YEARS_INDEX = 4
TEAM_INDEX = 12
LEAGUE_TEXT = LEAGUE_TEAM_LIST[LEAGUE_NUM]
LEAGUE_URL = LEAGUES_LINK[LEAGUE_NUM]
LEAGUE_INDEX_NUM = LEAGUE_INDEX[LEAGUE_NUM]
SEASON_INDEX_LIST = SEASON_INDEX_BY_LEAGUE[LEAGUE_NUM]
SQUAWKA_URL = 'http://www.squawka.com/football-stats/' + LEAGUE_URL + '-season-'

YEARS = ['2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017','2017-2018' ]
VALUES_NUM = ['4', '69', '136', '176', '712']
HDR = {'User-Agent': 'Mozilla/5.0'}


PLAYER_ID = 0

DELAY = 8  # seconds
DELAY0 = 5
DELAY1 = 2
DELAY2 = 10

ARIAL_LABEL = 'A tabular representation of the data in the chart.'


CAN_LOAD = True

PLAYERS_WRITE = ('Name, Position_SW, Team, Age, Height, Weight, Year, Total Appearances, Full Appearances, '
                 'Sub ON Appearances, Sub OFF Appearances, Total Goals, Goals Right Foot, Goals Left Foot, Goals Head, '
                 'Other Goals, Shot Accuracy(%), Shots ON Target, Shots OFF Target, Blocked Shots, Goals Concerted, '
                 'Failed Goals, Total Chances Created, Player Assist, Player Key Passes, Total chances RB(%), '
                 'Total chances RCAR(%), Total chances WR(%), Total chances EXTR(%), Total chances GK(%), '
                 'Total chances CB(%), Total chances MC(%), Total chances OMF(%), Total chances FW(%), '
                 'Total chances LB(%), Total chances LCAR(%), Total chances WL(%), Total chances EXTL(%),'
                 'Average pass Accuracy(%), Successful Passes, Unsuccessful Passes, Successful Long Balls, '
                 'Unsuccessful Long Balls, Successful Headed Passes, Unsuccessful Headed Passes, '
                 'Successful Through Balls, Unsuccessful Through Balls, Successful Cross Ball, Unsuccessful Cross Ball,'
                 ' Passes Forward, Passes Backward, Average Pass Length, Average Long Ball Length, '
                 'Average Back Pass Length, Average Forward Pass Length, Average Duels Won(%), '
                 'Successful Tackles, Total Tackles, Successful Fouls, Total Fouls, Successful Take On, Total Take on, '
                 'Successful Headed Duel, Total Headed Duel, Successful Tackles, Total Tackles, '
                 'Average Defensive Actions, Defensive Clearances, Defensive Interceptions, Defensive Blocks, '
                 'Total Defensive Errors, Led Attempt Goal, Led Goal, Total Yellow Card, Violence Yellow Card, '
                 'Tackle Yellow Card, Verbal Yellow Card, Other Yellow Card, Total Red Card, Violence Red Card, '
                 'Tackle Red Card, Verbal Red Card, Other Red Card\n')

GOALKEEPERS_WRITE = (
    'Name, Position_SW, Team, Age, Height, Weight, Year, Total Appearances, Full Appearances, Sub ON Appearances, '
    'Sub OFF Appearances, Clean Sheets, Total Goal Conceed,''Average Goals Conceed, Goals From Corner, '
    'Goals Set Piece Crosses, Goals Direct Free Kicks, Goals Open Play, Goals Open Play Outside Box, Other Goals, '
    'Goals Conceed 2, Average Saves Per Game, Num Saves, Num Saves 2, Penalties Conceded, Penalties Saved, '
    'Average Saves Per Goal Total Saves Goal, Average Claims Success, Total Claims Success, Total Claims Fail, '
    'Average Punches, Total Punches Success, Total Punches Fail, Average Distance Success, Successful Goal Kicks, '
    'Unsuccessful Goal Kicks, Successful Kicks From Hands, Unsuccessful Kicks From Hands, Successful Threw Out, '
    'Unsuccessful Threw Out, Successful Others, Unsuccessful Others, Average Distance Length, Length Goal Kicks, '
    'Length Kicks From Hands, Length Threw Out, Length Other, Total Yellow Card, Violence Yellow Card, '
    'Tackle Yellow Card, Verbal Yellow Card, Other Yellow Card, Total Red Card, Violence Red Card, Tackle Red Card, '
    'Verbal Red Card, Other Red Card\n')

TEAMS_WRITE = ('Name, Season, Matches Played, League, Stadium, Location, Goals Scored, Goals Scored High Left, '
               'Goals Scored High Left Percent, Goals Scored High Center, Goals Scored High Center Percent,'
               'Goals Scored High Right, Goals Scored High Right Percent, Goals Scored Low Left,'
               'Goals Scored Low Left Percent, Goals Scored Low Centre Right, Goals Scored Low Centre Right Percent,'
               'Goals Scored Low Right, Goals Scored Low Right Percent, Goals Scored Right Foot,'
               'Goals Scored Left Foot, Goals Scored Head, Other Scored Goals, '
               'Goals Conceded, Goals Conceded High Left, Goals Conceded High Left Percent, Goals Conceded High Center,'
               'Goals Conceded High Center Percent, Goals Conceded High Right, Goals Conceded High Right Percent, '
               'Goals Conceded Low Left, Goals Conceded Low Left Percent, Goals Conceded Low Centre,'
               'Goals Conceded Low Centre Percent, Goals Conceded Low Right, Goals Conceded Low Right Percent,'
               'Goals Conceded Right Foot, Goals Conceded Right Foot Percent, Goals Conceded Left Foot, '
               'Goals Conceded Left Foot Percent, Goals Conceded Head, Other Conceded Goals, Set Piece Goals,'
               'Crossed Free Kicks, Direct Free Kicks, Corners, Penalties, Shot Accuracy(%), Shot Accuracy Positions'
               'Shots ON Target, Shots OFF Target, Blocked Shots, Goals Concerted, Total Chances Created, '
               'Player Assist, Player Key Passes, Total chances RB(%),'
               'Total chances RCAR(%), Total chances WR(%), Total chances EXTR(%), Total chances GK(%), '
               'Total chances CB(%), Total chances MC(%), Total chances OMF(%), Total chances FW(%), '
               'Total chances LB(%), Total chances LCAR(%), Total chances WL(%), Total chances EXTL(%), Possession'
               'Average pass Accuracy(%), Successful Passes, Unsuccessful Passes, Successful Long Balls, '
               'Unsuccessful Long Balls, Successful Headed Passes, Unsuccessful Headed Passes, '
               'Successful Through Balls, Unsuccessful Through Balls, Successful Cross Ball, Unsuccessful Cross Ball,'
               ' Passes Forward, Passes Backward, Average Pass Length, Average Long Ball Length,'
               'Average Back Pass Length, Average Forward Pass Length, Average Duels Won(%),'
               'Successful Tackles, Total Tackles, Successful Fouls, Total Fouls, Successful Take On, Total Take on, '
               'Successful Headed Duel, Total Headed Duel, Successful Tackles, Total Tackles, '
               'Average Defensive Actions, Defensive Clearances, Defensive Interceptions, Defensive Blocks, '
               'Total Yellow Card, Violence Yellow Card, '
               'Tackle Yellow Card, Verbal Yellow Card, Other Yellow Card, Total Red Card, Violence Red Card, '
               'Tackle Red Card, Verbal Red Card, Other Red Card\n')