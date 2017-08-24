# -*- coding: utf-8 -*-

leagues = ['spanish-la-liga-season-', 'english-premier-league', 'italian-serie-a', 'german-bundesliga',
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

delay0 = 5
delay1 = 2
delay = 8  # seconds
delay2 = 10  # seconds
arial_label = 'A tabular representation of the data in the chart.'

can_Load = True
