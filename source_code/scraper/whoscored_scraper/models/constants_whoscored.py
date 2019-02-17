WHOSCORED_URL = 'https://www.whoscored.com/'

LEAGUES_LINK = ['Spain-La-Liga', 'England-Premier-League', 'Italy-Serie-A',
                'Germany-Bundesliga', 'France-Ligue-1', 'Portugal-Liga-NOS',
                'Netherlands-Eredivisie', 'Russia-Premier-League', 'Brazil-Brasileirão',
                'USA-Major-League-Soccer', 'Turkey-Super-Lig', 'England-Championship',
                'Argentina-Primera-División', 'China-Super-league', 'Germany-Bundesliga-II',
                'Sweden-Allsvenskan', ''] # plus Norway and Sweeden

LEAGUES_ID = ['206', '252', '108', '81', '74', '177', '155', '182', '95', '233', '225', '252', '11', '45', '81', '212']
LEAGUES_NUM = ['4', '2', '5', '3', '22', '21', '13', '77', '31', '85', '17', '7', '68', '162', '6', '40']

SEASON_ID = [['1929', '2596', '3004', '3470', '3922', '5435', '5933', '6436', '6960', '7466'],
             ['1849', '2458', '2935', '3389', '3853', '4311', '5826', '6335', '6829', '7361'],
             ['1957', '2626', '3054', '3512', '3978', '5441', '5970', '6461', '6974', '7468'],
             ['1903', '2520', '2949', '3424', '3863', '4336', '5870', '6392', '6902', '7405'],
             ['1839', '2417', '2920', '3356', '3836', '4279', '5830', '6318', '6833', '7344'],
             ['0', '0', '0', '0', '0', '0', '0', '6438', '6933', '7429'],
             ['0', '0', '0', '0', '3851', '4289', '5810', '6331', '6826', '7354'], # has to be recheck in the url Eredivise
             ['3861', '4303', '5859', '6357', '6819', '7389'],
             ['4185', '5713', '6242', '6700', '7243'], # only years in Brasileirao, will crash
             []]
SEASON_NUMBER = '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'


# 9 6 7
# 9 5 2
SEASON_INDEX = 9 # 0-9

LEAGUE_INDEX = 5

TEAM_INDEX = 2