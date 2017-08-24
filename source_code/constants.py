# -*- coding: utf-8 -*-

leagues = ['spanish-la-liga', 'english-premier-league', 'italian-serie-a', 'german-bundesliga',
           'french-ligue-1', 'dutch-eredivisie', 'russian-premier-league', 'us-major-league-soccer',
           'brazilian-serie-a', 'mexican-liga-mx', 'mexican-primera-apertura', 'english-football-league-championship',
           'australian-a-league', 'turkish-super-lig', 'portuguese-primeira-liga']
league_team_list = ['Spanish La Liga', 'English Barclays Premier League']

# league_num is the league
league_num = 0
league_text = league_team_list[league_num]
url = 'http://www.squawka.com/football-stats/' + leagues[league_num] + '-season-'

years = ['2012-2013', '2013-2014', '2014-2015', '2015-2016', '2016-2017']
values_num = ['4', '69', '136', '176', '712']
hdr = {'User-Agent': 'Mozilla/5.0'}

PLAYER_ID = 0

delay0 = 5
delay1 = 2
delay = 8  # seconds
delay2 = 10  # seconds
arial_label = 'A tabular representation of the data in the chart.'

can_Load = True

players_write = ('Name, Position_SW, Team, Age, Height, Weight, Year, Total Appearances, Full Appearances, '
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

goalkeepers_write = (
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
