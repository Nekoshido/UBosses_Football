# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 11:29:09 2017

@author: Hector
"""

# import libraries
import urllib2, sys, time, platform, csv
from bs4 import BeautifulSoup

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select


from requests import get
#classes

class Player():
    def __init__(self):
        self.name = ''
        self.ID = 0
        self.position_sw = ''
        self.position_trnfmrkt = ''
        self.team = ''
        
        self.age = ''
        self.height = ''
        self.weight = ''
        self.year = ''
        
        self.swn_score = ''
        self.swn_score_list = []
        
        self.app_tot = ''
        self.app_full = ''
        self.app_sub_on = ''
        self.app_sub_off = ''
        
        self.goals = []
        self.goal_tot = 0
        self.goal_right = 0
        self.goal_left = 0
        self.goal_head= 0
        self.goal_other = 0
        
        self.shot_acc = 0
        self.shot_on = 0
        self.shot_off = 0
        self.shot_block = 0
        self.shot_conv = 0
        self.shot_fail = 0

        self.tt_chances_created = 0
        self.assist = 0
        self.key_passes = 0
        self.tt_chan_pitch = []
        
        self.avg_pass_acc = 0
        self.succ_pass = 0
        self.unsucc_pass = 0
        self.succ_long_balls = 0
        self.unsucc_long_balls = 0
        self.succ_head_pass = 0
        self.unsucc_head_pass = 0
        self.succ_through_ball = 0
        self.unsucc_through_ball = 0
        self.succ_cross_ball = 0
        self.unsucc_cross_ball = 0
        self.pass_forward = 0
        self.pass_backward = 0
        
        self.avg_pass_length = 0
        self.avg_long_ball_length = 0
        self.avg_back_pass_length = 0
        self.avg_forw_pass_length = 0
        
        self.avg_duels_won = 0
        self.succ_tackle = 0
        self.unsucc_tackle = 0
        self.suff_foul = 0
        self.comm_foul = 0
        self.succ_take_on = 0
        self.unsucc_take_on = 0
        self.succ_head_duel = 0
        self.unsucc_head_duel = 0      
        
        self.avg_def_act = 0
        self.def_clear = 0
        self.interception = 0
        self.block = 0
        
        self.total_def_err = 0
        self.led_attempt_goal = 0
        self.led_goal = 0        
        
        self.tot_yel_card = 0
        self.viol_yel_card = 0
        self.tack_yel_card = 0
        self.verb_yel_card = 0
        self.oth_yel_card = 0
        self.tot_red_card = 0
        self.viol_red_card = 0
        self.tack_red_card = 0
        self.verb_red_card = 0
        self.oth_red_card = 0   
        
    def __str__(self):
        string = 'Name: ' + self.name + '\n'
        string = string + 'Appearance: ' + str(self.app_tot) + '\n'
        string = string + 'Goals: ' + str(self.goal_tot )+ '\n'
        string = string + 'Shot Accuracy: ' + str(self.shot_acc) + '\n'
        string = string + 'Total Chances: ' + str(self.tt_chances_created) + '\n'
        string = string + 'Pass Accuracy: ' + str(self.avg_pass_acc )+ '\n'
        string = string + 'Pass length: ' + str(self.avg_pass_length) + '\n'
        string = string + 'Duels Won: ' + str(self.avg_duels_won) + '\n'
        string = string + 'Defensive Actions: ' + str(self.avg_def_act) + '\n'
        string = string + 'Defensive Errors: ' + str(self.total_def_err) + '\n'
        string = string + 'Yellow/Red Cards: ' + str(self.tot_yel_card) + '/'+  str(self.tot_red_card )+ '\n'
        return string
        
        
class Goalkeeper():
    
    def __init__(self):
        self.name = ''
        self.ID = 0
        self.position_sw = ''
        self.position_trnfmrkt = ''
        self.team = ''
        
        self.age = ''
        self.height = ''
        self.weight = ''
        self.year = ''
        
        self.swn_score = ''
        self.swn_score_list = []
        
        self.app_tot = ''
        self.app_full = ''
        self.app_sub_on = ''
        self.app_sub_off = ''
        
        self.clean_sheets = 0
        self.goal_conceed = []
        self.total_goal_conceed = 0
        
        self.avg_goals_conceed = 0
        self.goals_corner= 0
        self.goals_set_piece_crosses = 0
        self.goals_direct_free_kicks = 0
        self.goals_open_play = 0
        self.goals_open_play_outside_box = 0
        self.goals_others = 0
        self.total_goal_conceed2 = 0
        self.goals_zone = []
   
        self.avg_saves_per_game = 0
        self.saves_per_game_list = []
        self.num_saves = 0
        self.saves_position_list = []
        self.num_saves2 = 0
        self.penalties_conceded = 0
        self.penalties_saved = 0
        self.penalties_list = []
        
        self.avg_saves_per_goal = 0
        self.saves_per_goal_list = []
        self.total_saves_goal = 0
        
        self.avg_claims_success = 0
        self.claims_success_list = []
        self.tot_claims_success = 0
        self.claims_fail_list = []
        self.tot_claims_fail = 0       
        
        self.avg_punches = 0       
        self.punches_success_list = []
        self.tot_punches_success = 0
        self.punches_fail_list = []
        self.tot_punches_fail = 0  

        self.avg_dist_succ = 0 
        self.succ_goal_kicks = 0
        self.unsucc_goal_kicks = 0
        self.succ_kicks_from_hands = 0        
        self.unsucc_kicks_from_hands = 0  
        self.succ_threw_out = 0 
        self.unsucc_threw_out = 0         
        self.succ_other = 0
        self.unsucc_other = 0
        
        self.dis_length = 0
        self.goal_kicks_length = 0       
        self.kicks_from_hands = 0         
        self.threw_out_length = 0 
        self.other_length = 0        
        
        self.tot_yel_card = 0
        self.viol_yel_card = 0
        self.tack_yel_card = 0
        self.verb_yel_card = 0
        self.oth_yel_card = 0
        self.tot_red_card = 0
        self.viol_red_card = 0
        self.tack_red_card = 0
        self.verb_red_card = 0
        self.oth_red_card = 0        
        
    def __str__(self):
        string = 'Name: ' + self.name + '\n'
        string = string + 'Appearance: ' + str(self.app_tot) + '\n'
        string = string + 'Clean Sheets: ' + str(self.clean_sheets )+ '\n'
        string = string + 'Avg Goals Conceed: ' + str(self.avg_goals_conceed) + '\n'
        string = string + 'Avg Saves per Game: ' + str(self.avg_saves_per_game) + '\n'
        string = string + 'Avg Saves per Goal: ' + str(self.avg_saves_per_goal )+ '\n'
        string = string + 'Avg Claim Success: ' + str(self.avg_claims_success) + '\n'
        string = string + 'Avg Punches: ' + str(self.avg_punches) + '\n'
        string = string + 'Dist Success: ' + str(self.avg_dist_succ) + '\n'
        string = string + 'Dist Length: ' + str(self.dis_length) + '\n'
        string = string + 'Yellow/Red Cards: ' + str(self.tot_yel_card) + '/'+  str(self.tot_red_card )+ '\n'
        return string                
        
        
PLAYER_ID = 0     
#code
# under different operating systems
if platform.system() == 'Windows':
    PHANTOMJS_PATH = './phantomjs-2.1.1-windows/bin/phantomjs.exe'
else:
    PHANTOMJS_PATH = './phantomjs-2.1.1-windows/bin/phantomjs.exe'  
  
leagues = ['spanish-la-liga-season-', 'english-premier-league', 'italian-serie-a', 'german-bundesliga', 'french-ligue-1', 'dutch-eredivisie', 'russian-premier-league', 'us-major-league-soccer','brazilian-serie-a', 'mexican-liga-mx', 'mexican-primera-apertura', 'english-football-league-championship', 'australian-a-league', 'turkish-super-lig', 'portuguese-primeira-liga']
league_team_list = ['Spanish La Liga', 'English Barclays Premier League']

# league_num is the league
league_num = 0
league_text = league_team_list[league_num]
url = 'http://www.squawka.com/football-stats/'+leagues[league_num]+'-season-'


years = ['2012-2013', '2013-2014','2014-2015','2015-2016','2016-2017']
values_num = ['4', '69','136', '176', '712']
hdr = {'User-Agent': 'Mozilla/5.0'}

delay0 = 5
delay1 = 2
delay = 8 # seconds
delay2 = 10 # seconds
arial_label = 'A tabular representation of the data in the chart.'

can_Load = True
reload(sys)
sys.setdefaultencoding('utf8')

ffprofile = webdriver.FirefoxProfile()
print 'Trying to open with extension'
ffprofile.add_extension(extension='C:\Users\Hector\AppData\Roaming\Mozilla\Firefox\Profiles\9u09psq3.default\extensions\{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi')
browser = webdriver.Firefox(firefox_profile=ffprofile)
print 'Finished load extension'

for num_season in range(len(years)):
    season = years[num_season]
    site = url+season
    browser.get(site)
    req = urllib2.Request(url+season,headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
    teams = soup.find_all("a", class_="fsclt-club-link")

    
    for team in teams:
        
        team_name = team.find('span',{'class':'fsclt-club-name'}).text 
        print team_name

        players_file = open('%s-LaLiga-players-%s.csv'%(team_name, season),'w')
        goalkeepers_file = open('%s- LaLiga-goalkeepers-%s.csv'%(team_name, season),'w')    
            
        write = 'Name, Position_SW, Team, Age, Height, Weight, Year, Total Appearances, Full Appearances, Sub ON Appearances, Sub OFF Appearances, Total Goals, Goals Right Foot, Goals Left Foot, Goals Head, Other Goals,'
        write = write + 'Shot Accuracy(%), Shots ON Target, Shots OFF Target, Blocked Shots, Goals Concerted, Failed Goals, Total Chances Created, Player Assist, Player Key Passes, Total chances RB(%), Total chances RCAR(%),'
        write = write + 'Total chances WR(%), Total chances EXTR(%), Total chances GK(%), Total chances CB(%), Total chances MC(%), Total chances OMF(%), Total chances FW(%), Total chances LB(%), Total chances LCAR(%), Total chances WL(%), Total chances EXTL(%),'
        write = write + 'Average pass Accuracy(%), Successful Passes, Unsuccessful Passes, Successful Long Balls, Unsuccessful Long Balls, Successful Headed Passes, Unsuccessful Headed Passes, Successful Through Balls, Unsuccessful Through Balls,'    
        write = write + 'Successful Cross Ball, Unsuccessful Cross Ball, Passes Forward, Passes Backward, Average Pass Length, Average Long Ball Length, Average Back Pass Length, Average Forward Pass Length, Average Duels Won(%),'
        write = write + 'Successful Tackles, Total Tackles, Successful Fouls, Total Fouls, Successful Take On, Total Take on, Successful Headed Duel, Total Headed Duel, Successful Tackles, Total Tackles,'
        write = write + 'Average Defensive Actions, Defensive Clearances, Defensive Interceptions, Defensive Blocks, Total Defensive Errors, Led Attempt Goal, Led Goal,'
        write = write + 'Total Yellow Card, Violence Yellow Card, Tackle Yellow Card, Verbal Yellow Card, Other Yellow Card, Total Red Card, Violence Red Card, Tackle Red Card, Verbal Red Card, Other Red Card\n'
        players_file.write(write) 
       
        write = 'Name, Position_SW, Team, Age, Height, Weight, Year, Total Appearances, Full Appearances, Sub ON Appearances, Sub OFF Appearances, Clean Sheets, Total Goal Conceed,'
        write = write + 'Average Goals Conceed, Goals From Corner, Goals Set Piece Crosses, Goals Direct Free Kicks, Goals Open Play, Goals Open Play Outside Box, Other Goals, Goals Conceed 2, Average Saves Per Game,'
        write = write + 'Num Saves, Num Saves 2, Penalties Conceded, Penalties Saved, Average Saves Per Goal Total Saves Goal, Average Claims Success, Total Claims Success, Total Claims Fail, Average Punches,'
        write = write + 'Total Punches Success, Total Punches Fail, Average Distance Success, Successful Goal Kicks, Unsuccessful Goal Kicks, Successful Kicks From Hands, Unsuccessful Kicks From Hands, Successful Threw Out, Unsuccessful Threw Out,'
        write = write + 'Successful Others, Unsuccessful Others, Average Distance Length, Length Goal Kicks, Length Kicks From Hands, Length Threw Out, Length Other,'
        write = write + 'Total Yellow Card, Violence Yellow Card, Tackle Yellow Card, Verbal Yellow Card, Other Yellow Card, Total Red Card, Violence Red Card, Tackle Red Card, Verbal Red Card, Other Red Card\n'
    
        goalkeepers_file.write(write)    
        

        link = team.get('href')
        new_link = link + '#performance-score#spanish-la-liga#season-'+season.replace('-','/')+"#"+values_num[num_season]+ "#all-matches#1-38#by-match"
        
        browser.get(new_link)
        browser.implicitly_wait(delay)
        
        time.sleep(delay)        
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        players = soup.find('ul',{'id':'players-list'})
        players2 = players.find_all('a',{'class':'fixture-card-link-wrap'})
        
        for player in players2:
            name = player.find('span',{'class':'name'}).text
            position = player.find('span',{'class':'position'}).text 
            player_link = player.get('href') 
            #print 'Link: ', player_link
            #player_link = 'http://www.squawka.com/players/marc-andre-ter-stegen/stats'
            #player_link = 'http://www.squawka.com/players/lionel-messi/stats'
            pla_app_link = player_link +'#total-appearances#'+team_name+'#spanish-la-liga#23#season-'+season.replace('-','/')+"#"+values_num[num_season]+"#all-matches#1-38#by-match"
            #pla_app_link = 'http://www.squawka.com/players/alexis-sanchez/stats#total-appearances#Barcelona#spanish-la-liga#23#season-2012/2013#4#all-matches#1-38#by-match'
            #pla_app_link = 'http://www.squawka.com/players/marc-andre-ter-stegen/stats#total-appearances#barcelona-(current)#spanish-la-liga#23#season-2016/2017#712#all-matches#1-38#'
            #pla_app_link = 'http://www.squawka.com/players/victor-valdes/stats#total-appearances#barcelona#spanish-la-liga#23#season-2012/2013#4#all-matches#1-38#type'
            try:
                browser.get(pla_app_link) 
                can_Load = True
            
            except:
                print "Cannot access: " + pla_app_link
                can_Load = False
                
            browser.implicitly_wait(delay1)
            
            time.sleep(delay1)
            
            #action = webdriver.ActionChains(browser)
            appearances = int(browser.find_element_by_id('stat-1').find_element_by_class_name('stat').get_attribute("innerHTML"))
            #action.move_to_element(element).perform()
            
            soup_players = BeautifulSoup(browser.page_source, "html.parser")
            if(can_Load):
                #'Goalkeeper'                         
                if( position != 'Goalkeeper'):
                    player_sw = Player()
                    
                    tmp_name = soup_players.find('div',{'id':'playerssecontent'}).text.split('\n')[2].split(" ")
                    tmp_name = tmp_name[:len(tmp_name)-1]
                    player_sw.name = ' '.join(tmp_name)
                    print player_sw.name
                    player_sw.year = season.replace('-','/')
                    player_sw.team = team_name                    
                    
                    height_str = "Compare "+player_sw.name+"'s Height against other players"
                    height_t = soup_players.find('a',{'title':height_str}).text
                    player_sw.position_sw = position
                    #print browser.find_element_by_id('player-info').get_attribute("innerHTML")
                    player_sw.height = height_t.split('\n')[2]
                    weight_str = "Compare "+player_sw.name+"'s Weight against other players"
                    weight_t = soup_players.find('a',{'title':weight_str}).text
                    player_sw.weight = weight_t.split('\n')[2]
                    
                    #print browser.find_element_by_id('the-graph-1').get_attribute("innerHTML")

                    try:
                        select = Select(browser.find_element_by_id('club_id')).select_by_visible_text(team_name)
                        element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "statistics-options")))
                        select = Select(browser.find_element_by_id('competition')).select_by_visible_text(league_text)
                        season_name = 'Season ' + season.replace('-','/')
                        browser.implicitly_wait(delay0)
                        time.sleep(delay0)   
                        select = Select(browser.find_element_by_id('season')).select_by_visible_text(season_name)
                        
                        menu_goal = browser.find_element_by_id('stat-1') 
                        actions = ActionChains(browser) 
                        actions.move_to_element(menu_goal)
                        actions.click(menu_goal)
                        actions.perform()
                        browser.implicitly_wait(delay0)
                        time.sleep(delay0)                            
                        
                    except:
                        print 'Loyal'

                    not_click = True
                    while(not_click):
                        try:
                            menu_goal = browser.find_element_by_id('stat-1') 
                            actions = ActionChains(browser) 
                            actions.move_to_element(menu_goal)
                            actions.click(menu_goal)
                            actions.perform()
                            soup_appearance = BeautifulSoup(browser.page_source, "html.parser")                       
                            app_list = soup_appearance.find('div',{'id': 'stat-graph-1'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')
                            not_click = False
                        except:
                            browser.implicitly_wait(delay1)
                            time.sleep(delay1)        
                            
                
                    player_sw.app_tot = browser.find_element_by_id('stat-1').find_element_by_class_name('stat').get_attribute("innerHTML")
                    
                    
                    if(player_sw.app_tot>0):
                        print 'Appearances: ', player_sw.app_tot
                        soup_appearance = BeautifulSoup(browser.page_source, "html.parser")                       
                        app_list = soup_appearance.find('div',{'id': 'stat-graph-1'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')
                        #print soup_appearance.find('div',{'id': 'stat-graph-1'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td').text            
                        player_sw.app_full = int(app_list[1].text)
                        player_sw.app_sub_off = int(app_list[3].text)                    
                        player_sw.app_sub_on = int(app_list[5].text)  
                                    
                        player_sw.goal_tot = browser.find_element_by_id('stat-3').find_element_by_class_name('stat').get_attribute("innerHTML")
                        if (player_sw.goal_tot != 0):
                            
                            #browser.execute_script("window.scrollBy(0,840);")                       
                            
                            menu_goal = browser.find_element_by_id('stat-3') 
                            actions = ActionChains(browser) 
                            actions.move_to_element(menu_goal)
                            actions.click(menu_goal)
                            actions.perform()
                            #player_goal_part_link = player_link +'#total-goals-scored#'+team_name+'-(current)#spanish-la-liga#23#season-'+season.replace('-','/')+"#"+values_num[num_season]+"#all-matches#1-38#by-match#body-part"
                            #browser.get(player_goal_part_link)
                            #browser.refresh()
                            #browser.implicitly_wait(delay2)
                            #time.sleep(delay2)
                            
                            element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "stat-graph-3")))
                            not_click = True
                            while(not_click):
                                try:
                                    
                                    menu_goal = browser.find_element_by_id('stat-3') 
                                    actions = ActionChains(browser) 
                                    actions.move_to_element(menu_goal)
                                    actions.click(menu_goal)
                                    actions.perform()
                                    element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "stat-graph-3")))
                                    
                                    menu_goal2 = browser.find_element_by_id('stat-3_body_part')
                                    actions = ActionChains(browser)  
                                    actions.move_to_element(menu_goal2)
                                    actions.click(menu_goal2)
                                    actions.perform()
                                   
                                    #browser.implicitly_wait(delay2)
                        
                                    #time.sleep(delay2)  
                                    element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-3a")))
                                    
                                    soup_goal_part = BeautifulSoup(browser.page_source, "html.parser") 
                                                           
                                    goal_part = soup_goal_part.find('div',{'id': 'the-graph-3a'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')   
                                    player_sw.goal_tot = int(browser.find_element_by_id('stat-3').find_element_by_class_name('stat').get_attribute("innerHTML")) 
                                    player_sw.goal_left = int(goal_part[1].text)
                                    player_sw.goal_right = int(goal_part[2].text)
                                    player_sw.goal_head = int(goal_part[3].text)
                                    player_sw.goal_other = int(goal_part[4].text)
                                    not_click = False
                                except:
                                    browser.implicitly_wait(delay1)
                                    time.sleep(delay1) 
                                
      
                                
                            #player_shoot_acc_link = player_link +'#shot-accuracy#'+team_name+'-(current)#spanish-la-liga#23#season-'+season.replace('-','/')+"#"+values_num[num_season]+"#all-matches#1-38#by-match#body-part"
                            #browser.get(player_shoot_acc_link)
                            #browser.refresh()
                                
                        not_click = True
                        while(not_click):
                            try:                        
                                menu_goal = browser.find_element_by_id('stat-4') 
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_goal)
                                actions.click(menu_goal)
                                actions.perform()
                                
                                
                                element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "the-graph-4")))
                                #browser.implicitly_wait(delay2)
                                #time.sleep(delay2)
                                
                                soup_shot_part = BeautifulSoup(browser.page_source, "html.parser") 
                                player_sw.shot_acc = int(browser.find_element_by_id('stat-4').find_element_by_class_name('stat').get_attribute("innerHTML").split('%')[0])
                                shot_acc_list = soup_shot_part.find('p',{'id': 'dp-shotaccuracy-goalmouth-text'}).text.split(' ')
                                not_click = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1) 
                                
                        not_click = True
                        while(not_click):
                            try:                        
                                menu_shot = browser.find_element_by_id('stat-4_conversion')                        
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_shot)
                                actions.click(menu_shot)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "stat-graph-4")))
                                #browser.implicitly_wait(delay2)
                                #time.sleep(delay2)
                                
                                soup_shot_part_2 = BeautifulSoup(browser.page_source, "html.parser") 
                                shot_part = soup_shot_part_2.find('div',{'id': 'the-graph-4a'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')
                                
                                #player_sw.shot_acc = int(browser.find_element_by_id('stat-4').find_element_by_class_name('stat').get_attribute("innerHTML").split("%")[0]) 
                                player_sw.shot_on = int(shot_acc_list[0])
                                player_sw.shot_off = int(shot_acc_list[5])
                                player_sw.shot_block = int(shot_acc_list[10])
                                player_sw.shot_conv = int(shot_part[1].text)
                                player_sw.shot_fail = int(shot_part[3].text)
                                not_click = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1) 
                                
                        not_click = True
                        while(not_click):
                            try:                            
                                menu_chance = browser.find_element_by_id('stat-6') 
                                actions.reset_actions()
                                actions.move_to_element(menu_chance)
                                actions.click(menu_chance)
                                actions.perform()
                                
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "kaypass_bar")))
                                #browser.implicitly_wait(delay2)
                                #time.sleep(delay2)
                                soup_chance = BeautifulSoup(browser.page_source, "html.parser") 
                                chance_cre = soup_chance.find('div',{'id': 'the-graph-6a'})
                                chance_cre = chance_cre.find('div',{'aria-label': arial_label})
                                chance_cre = chance_cre.find('tbody')
                                chance_cre = chance_cre.findAll('td')
                                player_sw.tt_chances_created = int(browser.find_element_by_id('stat-6').find_element_by_class_name('stat').get_attribute("innerHTML")) 
                                
                                player_sw.assist = int(chance_cre[1].text) 
                                player_sw.key_passes = int(chance_cre[2].text) 
                                not_click = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1) 
                                
                                
                        not_click = True
                        while(not_click):
                            try:
                            
                                menu_chance = browser.find_element_by_id('stat-6_pitch_view')
                                
                                actions = ActionChains(browser)    
                                actions.move_to_element(menu_chance)
                                actions.click(menu_chance)
                                actions.perform()
                               
                                element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "dp-active-layer")))
                                #browser.implicitly_wait(delay2)
                    
                                #time.sleep(delay2)  
                                soup_menu_chance_map = BeautifulSoup(browser.page_source, "html.parser") 
                                chance_map = soup_menu_chance_map.find('div',{'id': 'dp-active-layer'}).findAll('tspan')
            
                                for chance_zone in xrange(len(chance_map)):
                                    player_sw.tt_chan_pitch.append(float(chance_map[chance_zone].text.split('%')[0]))
                                not_click = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)


                        not_click = True
                        while(not_click):
                            try:
    
                                menu_pass = browser.find_element_by_id('stat-7') 
                                
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_pass)
                                actions.click(menu_pass)
                                actions.perform()
            
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-7")))
            
                                soup_pass = BeautifulSoup(browser.page_source, "html.parser")      
                                player_sw.avg_pass_acc =  int(browser.find_element_by_id('stat-7').find_element_by_class_name('stat').get_attribute("innerHTML").split('%')[0])                      
                                
                                chance_cre = soup_pass.find('div',{'id': 'the-graph-7'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')
                                
                                player_sw.succ_pass = int(''.join(chance_cre[1].text.split(",")))
                                player_sw.unsucc_pass = int(''.join(chance_cre[7].text.split(",")))
                                player_sw.succ_long_balls = int(''.join(chance_cre[5].text.split(",")))
                                player_sw.unsucc_long_balls = int(''.join(chance_cre[11].text.split(",")))
                                player_sw.succ_head_pass = int(''.join(chance_cre[2].text.split(",")))
                                player_sw.unsucc_head_pass = int(''.join(chance_cre[8].text.split(",")))
                                player_sw.succ_through_ball = int(''.join(chance_cre[3].text.split(",")))
                                player_sw.unsucc_through_ball = int(''.join(chance_cre[9].text.split(",")))
                                player_sw.succ_cross_ball = int(''.join(chance_cre[4].text.split(",")))
                                player_sw.unsucc_cross_ball = int(''.join(chance_cre[10].text.split(",")))
                                not_click = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
                                
                                
                        not_click = True
                        while(not_click):
                            try:
                                menu_chance = browser.find_element_by_id('stat-7_type')
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_chance)
                                actions.click(menu_chance)
                                actions.perform() 
                                element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "the-graph-7a")))
                        
                                soup_menu_pass_avg = BeautifulSoup(browser.page_source, "html.parser") 
                                avg_pass_map = soup_menu_pass_avg.find('div',{'id': 'the-graph-7a'})
                               
                                avg_pass_map = avg_pass_map.find('div',{'aria-label': arial_label})
                                avg_pass_map = avg_pass_map.find('tbody')
                                avg_pass_map=avg_pass_map.findAll('td')
                                player_sw.pass_forward =  int(''.join(avg_pass_map[1].text.split(",")))
                                player_sw.pass_backward = int(''.join(avg_pass_map[3].text.split(","))) 
                                not_click = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
                                
                        not_fail = True
                        while(not_fail):
                            try:                         
                                menu_length = browser.find_element_by_id('stat-8')
                                
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_length)
                                actions.click(menu_length)
                                actions.perform()
            
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-8")))
                                
                                soup_length_pass = BeautifulSoup(browser.page_source, "html.parser")    
                                
                                player_sw.avg_pass_length =  int(browser.find_element_by_id('stat-8').find_element_by_class_name('stat').get_attribute("innerHTML").split('m')[0])
                                pss_leng_lt = soup_length_pass.find('div',{'id': 'the-graph-8'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')                        
                                player_sw.avg_long_ball_length = int(pss_leng_lt[1].text)
                                player_sw.avg_back_pass_length = int(pss_leng_lt[2].text)
                                player_sw.avg_forw_pass_length = int(pss_leng_lt[3].text)
                                not_fail = False
                            except:
                               browser.implicitly_wait(delay1)
                               time.sleep(delay1) 


                        not_fail = True
                        while(not_fail):
                            try:                           
                        
                                menu_duels = browser.find_element_by_id('stat-9') 
                                
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_duels)
                                actions.click(menu_duels)
                                actions.perform()
                                
                                element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "stat-graph-9")))
                                soup_duels_won = BeautifulSoup(browser.page_source, "html.parser" )                                                                                        
                                player_sw.avg_duels_won =  int(browser.find_element_by_id('stat-9').find_element_by_class_name('stat').get_attribute("innerHTML").split('%')[0])
                                
                                duels_lt = soup_length_pass.find('div',{'id': 'duel_won_suc'}).find('div',{'id': 'duels_won_tackle_title'}).text.split('-')[1].split(' ')[1].split('/')
                                player_sw.succ_tackle = int(duels_lt[0])
                                player_sw.unsucc_tackle = int(duels_lt[1])
                                duels_lt = soup_length_pass.find('div',{'id': 'duel_won_suc'}).find('div',{'id': 'duels_won_foul_title'}).text.split('-')[1].split(' ')[1].split('/')
                                player_sw.suff_foul = int(duels_lt[0])
                                player_sw.comm_foul = int(duels_lt[1])
                                duels_lt = soup_length_pass.find('div',{'id': 'duel_won_suc'}).find('div',{'id': 'duels_won_takeon_title'}).text.split('-')[1].split(' ')[1].split('/')
            
                                player_sw.succ_take_on = int(duels_lt[0])
                                player_sw.unsucc_take_on = int(duels_lt[1])
                                duels_lt = soup_length_pass.find('div',{'id': 'duel_won_suc'}).find('div',{'id': 'duels_won_headed_duel_title'}).text.split('-')[1].split(' ')[1].split('/')
            
                                player_sw.succ_head_duel = int(duels_lt[0])
                                player_sw.unsucc_head_duel = int(duels_lt[1])
                                not_fail = False
                            except:
                               browser.implicitly_wait(delay1)
                               time.sleep(delay1) 
                                    
                        not_fail = True
                        while(not_fail):
                            try:                        
                                menu_duels = browser.find_element_by_id('stat-10') 
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_duels)
                                actions.click(menu_duels)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-10")))
                                
                                soup_avg_def = BeautifulSoup(browser.page_source, "html.parser" )
                                player_sw.avg_def_act = int(browser.find_element_by_id('stat-10').find_element_by_class_name('stat').get_attribute("innerHTML"))                      
                                
                                avg_def_lt = soup_avg_def.find('div',{'id': 'the-graph-10'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')                                                         
                                player_sw.def_clear = int(avg_def_lt[1].text)
                                player_sw.interception = int(avg_def_lt[3].text)
                                player_sw.block = int(avg_def_lt[5].text)
                                not_fail = False
                            except:
                               browser.implicitly_wait(delay1)
                               time.sleep(delay1) 
                                    
                        
                        player_sw.total_def_err = int(browser.find_element_by_id('stat-11').find_element_by_class_name('stat').get_attribute("innerHTML"))
                        if(player_sw.total_def_err>0):
                            
                            not_fail = True
                            while(not_fail):
                                try:
                                    menu_def_error = browser.find_element_by_id('stat-11')  
                                    actions = ActionChains(browser) 
                                    actions.move_to_element(menu_def_error)
                                    actions.click(menu_def_error)
                                    actions.perform()       
                                    element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "stat-graph-11")))                                                
                                    soup_defensive_error = BeautifulSoup(browser.page_source, "html.parser" )                                                
                                    def_err_lt = soup_defensive_error.find('div',{'id': 'the-graph-11'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')   
                                    player_sw.led_attempt_goal = int(def_err_lt[1].text)
                                    player_sw.led_goal = int(def_err_lt[3].text) 
                                    not_fail = False
                                except:
                                   browser.implicitly_wait(delay1)
                                   time.sleep(delay1) 
                        
                        not_fail = True
                        while(not_fail):
                            try:
                                menu_cards = browser.find_element_by_id('stat-12') 
                                
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_cards)
                                actions.click(menu_cards)
                                actions.perform()       
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-12")))                                                               
                                soup_cards = BeautifulSoup(browser.page_source, "html.parser" )                               
                                cards_list = (browser.find_element_by_id('stat-12').find_element_by_class_name('stat').get_attribute("innerHTML")).split('/')
                                player_sw.tot_yel_card = int(cards_list[0])
                                yell_card_lt = soup_cards.find('div',{'id': 'the-graph-12'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')    
                                player_sw.viol_yel_card = int(yell_card_lt[1].text)
                                player_sw.tack_yel_card = int(yell_card_lt[2].text)
                                player_sw.verb_yel_card = int(yell_card_lt[3].text)
                                player_sw.oth_yel_card = int(yell_card_lt[4].text)
                                player_sw.tot_red_card =  int(cards_list[1])
                                not_fail = False
                            except:
                               browser.implicitly_wait(delay1)
                               time.sleep(delay1) 
                        
                        not_fail = True
                        while(not_fail):
                            try:
                                menu_chance = browser.find_element_by_id('stat-12_red_cards')
                                actions = ActionChains(browser)  
                                actions.move_to_element(menu_chance)
                                actions.click(menu_chance)
                                actions.perform()
                               
                                element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "the-graph-12a")))
                                
                                soup_red_cards = BeautifulSoup(browser.page_source, "html.parser" )
                                red_card_lt = soup_red_cards.find('div',{'id': 'the-graph-12a'})                          
                                red_card_lt = red_card_lt.find('div',{'aria-label': arial_label})
            
                                red_card_lt = red_card_lt.find('tbody')
            
                                red_card_lt = red_card_lt.findAll('td')
                             
                                player_sw.viol_red_card = int(red_card_lt[1].text)
                                player_sw.tack_red_card = int(red_card_lt[2].text)
                                player_sw.verb_red_card = int(red_card_lt[3].text)
                                player_sw.oth_red_card = int(red_card_lt[4].text)
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
    
                        write = player_sw.name.encode('utf-8') + ',' + str(player_sw.position_sw) + ','+ (player_sw.team).encode('utf-8')  + ','+ str(player_sw.age) + ','+ str(player_sw.height) + ','+ str(player_sw.weight)+ ','+ str(player_sw.year)+ ','
                        write = write + str(player_sw.app_tot) + ','+ str(player_sw.app_full) + ','+ str(player_sw.app_sub_on) + ','+ str(player_sw.app_sub_off) + ','
                        write = write + str(player_sw.goal_tot) + ','+ str(player_sw.goal_right) + ','+ str(player_sw.goal_left) + ','+ str(player_sw.goal_head) + ',' + str(player_sw.goal_other) + ','
                        write = write + str(player_sw.shot_acc) + ','+ str(player_sw.shot_on) + ','+ str(player_sw.shot_off) + ','+ str(player_sw.shot_block) + ',' + str(player_sw.shot_conv) + ',' + str(player_sw.shot_fail) + ','    
                        write = write + str(player_sw.tt_chances_created) + ','+ str(player_sw.assist) + ','+ str(player_sw.key_passes) + ','+ str(player_sw.tt_chan_pitch[0]) + ',' + str(player_sw.tt_chan_pitch[1]) + ','+ str(player_sw.tt_chan_pitch[2]) + ','+ str(player_sw.tt_chan_pitch[3]) + ','+ str(player_sw.tt_chan_pitch[4]) + ','+ str(player_sw.tt_chan_pitch[5]) + ','+ str(player_sw.tt_chan_pitch[6]) + ','+ str(player_sw.tt_chan_pitch[7]) + ','+ str(player_sw.tt_chan_pitch[8]) + ','+ str(player_sw.tt_chan_pitch[9]) + ','+ str(player_sw.tt_chan_pitch[10]) + ','+ str(player_sw.tt_chan_pitch[11]) + ','+ str(player_sw.tt_chan_pitch[12]) + ','
                        write = write + str(player_sw.avg_pass_acc) + ','+ str(player_sw.succ_pass) + ','+ str(player_sw.unsucc_pass) + ','+ str(player_sw.succ_long_balls) + ','+ str(player_sw.unsucc_long_balls) + ','+ str(player_sw.assist) + ','+ str(player_sw.tt_chances_created) + ','+ str(player_sw.succ_head_pass) 
                        write = write + str(player_sw.unsucc_head_pass) + ','+ str(player_sw.succ_through_ball) + ','+ str(player_sw.unsucc_through_ball) + ','+ str(player_sw.succ_cross_ball) + ','+ str(player_sw.unsucc_cross_ball) + ','
                        write = write + str(player_sw.pass_forward) + ','+ str(player_sw.pass_backward) + ',' + str(player_sw.avg_pass_length) + ','+ str(player_sw.avg_long_ball_length) + ','
                        write = write + str(player_sw.avg_back_pass_length) + ','+ str(player_sw.avg_forw_pass_length) + ',' + str(player_sw.avg_duels_won) + ','+ str(player_sw.succ_tackle) + ','        
                        write = write + str(player_sw.unsucc_tackle) + ','+ str(player_sw.suff_foul) + ',' + str(player_sw.comm_foul) + ','+ str(player_sw.succ_take_on) + ','  
                        write = write + str(player_sw.unsucc_take_on) + ','+ str(player_sw.succ_head_duel) + ',' + str(player_sw.unsucc_head_duel) + ','+ str(player_sw.avg_def_act) + ','    
                        write = write + str(player_sw.def_clear) + ','+ str(player_sw.interception) + ',' + str(player_sw.block) + ','+ str(player_sw.total_def_err) + ',' 
                        write = write + str(player_sw.led_attempt_goal) + ','+ str(player_sw.led_goal) + ',' + str(player_sw.tot_yel_card) + ','+ str(player_sw.viol_yel_card) + ',' 
                        write = write + str(player_sw.tack_yel_card) + ','+ str(player_sw.verb_yel_card) + ',' + str(player_sw.oth_yel_card) + ','+ str(player_sw.tot_red_card) + ','       
                        write = write + str(player_sw.viol_red_card) + ','+ str(player_sw.tack_red_card) + ',' + str(player_sw.verb_red_card) + ','+ str(player_sw.oth_red_card) + '\n'         
    
    
                        players_file.write(write)   
                else:
                    goalkeeper_sw = Goalkeeper()
                    
                    tmp_name = soup_players.find('div',{'id':'playerssecontent'}).text.split('\n')[2].split(" ")
                    tmp_name = tmp_name[:len(tmp_name)-1]
                    goalkeeper_sw.name = ' '.join(tmp_name)
                    goalkeeper_sw.year = season
                    goalkeeper_sw.team = team                    
                    
                    height_str = "Compare "+goalkeeper_sw.name+"'s Height against other players"
                    height_t = soup_players.find('a',{'title':height_str}).text
                    goalkeeper_sw.position_sw = position
                    #print browser.find_element_by_id('player-info').get_attribute("innerHTML")
                    goalkeeper_sw.height = height_t.split('\n')[2]
                    weight_str = "Compare "+goalkeeper_sw.name+"'s Weight against other players"
                    weight_t = soup_players.find('a',{'title':weight_str}).text
                    goalkeeper_sw.weight = weight_t.split('\n')[2]

                    try:
                        select = Select(browser.find_element_by_id('club_id')).select_by_visible_text(team_name)
                        element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "statistics-options")))
                        select = Select(browser.find_element_by_id('competition')).select_by_visible_text(league_text)
                        season_name = 'Season ' + season.replace('-','/')
                        browser.implicitly_wait(delay0)
                        time.sleep(delay0)   
                        select = Select(browser.find_element_by_id('season')).select_by_visible_text(season_name)
                        
                        browser.implicitly_wait(delay0)
                        time.sleep(delay0)   
                    except:
                        print 'Loyal'
                    
                    #print browser.find_element_by_id('the-graph-1').get_attribute("innerHTML")
                    goalkeeper_sw.app_tot = int(browser.find_element_by_id('stat-1').find_element_by_class_name('stat').get_attribute("innerHTML"))
                    if(goalkeeper_sw.app_tot>0):
                        print 'Appearances: ', goalkeeper_sw.app_tot
                        not_fail = True
                        while(not_fail):
                            try:
                                menu_app = browser.find_element_by_id('stat-1') 
                                
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_app)
                                actions.click(menu_app)
                                actions.perform()
            
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-1")))                   
                                
                                soup_appearance = BeautifulSoup(browser.page_source, "html.parser")   
                              
                                app_list = soup_appearance.find('div',{'id': 'the-graph-1'})
                                app_list = app_list.find('div',{'aria-label': arial_label})
                                app_list = app_list.find('tbody')
                                app_list = app_list.findAll('td')
                                #print soup_appearance.find('div',{'id': 'stat-graph-1'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td').text            
                                goalkeeper_sw.app_full = int(app_list[1].text)
                                goalkeeper_sw.app_sub_off = int(app_list[3].text)                    
                                goalkeeper_sw.app_sub_on = int(app_list[5].text)  
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
                                
                        not_fail = True
                        while(not_fail):
                            try:                                
                                menu_clean = browser.find_element_by_id('stat-3')                    
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_clean)
                                actions.click(menu_clean)
                                actions.perform()
              
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-3")))
                                
                                
                                soup_clean_sheet = BeautifulSoup(browser.page_source, "html.parser" )
                                goalkeeper_sw.clean_sheets = int(browser.find_element_by_id('stat-3').find_element_by_class_name('stat').get_attribute("innerHTML"))
                                '''                            
                                ptt_clean_sheet = soup_clean_sheet.find('div',{'id': 'the-graph-3'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('tr')
                                
                                total_goals = 0
                                for goals_conceed in xrange(len(ptt_clean_sheet)):
                                    date = ptt_clean_sheet[goals_conceed].findAll('td')[0].text
                                    goals = int(ptt_clean_sheet[goals_conceed].findAll('td')[1].text)
                                    total_goals = total_goals + goals
                                    goalkeeper_sw.goal_conceed.append([date, goals])
                                goalkeeper_sw.total_goal_conceed = total_goals
                                
                                goalkeeper_sw.avg_goals_conceed = float(browser.find_element_by_id('stat-4').find_element_by_class_name('stat').get_attribute("innerHTML"))
                                '''
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)                                

                        not_fail = True
                        while(not_fail):
                            try:                         
                                menu_app = browser.find_element_by_id('stat-4')                         
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_app)
                                actions.click(menu_app)
                                actions.perform()
            
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-4-type")))                   
                                
                                soup_goals_conceed = BeautifulSoup(browser.page_source, "html.parser")   
                              
                                goals_conced = soup_goals_conceed.find('div',{'id': 'the-graph-4-type'})
                                goals_conced = goals_conced.find('div',{'aria-label': arial_label})
                                goals_conced = goals_conced.find('tbody')
                                goals_conced = goals_conced.findAll('td')
                                
                                
                                goalkeeper_sw.goals_corner= int(goals_conced[1].text)
                                goalkeeper_sw.goals_set_piece_crosses = int(goals_conced[1].text)
                                goalkeeper_sw.goals_direct_free_kicks = int(goals_conced[1].text)
                                goalkeeper_sw.goals_open_play = int(goals_conced[1].text)
                                goalkeeper_sw.goals_open_play_outside_box = int(goals_conced[1].text)
                                goalkeeper_sw.goals_others = int(goals_conced[1].text)
                                goalkeeper_sw.avg_goals_conceed =  goalkeeper_sw.goals_corner+goalkeeper_sw.goals_set_piece_crosses+goalkeeper_sw.goals_direct_free_kicks + goalkeeper_sw.goals_open_play + goalkeeper_sw.goals_open_play_outside_box + goalkeeper_sw.goals_others
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
                                
                                
                        not_fail = True
                        while(not_fail):
                            try:                          
                                menu_clean = browser.find_element_by_id('stat-4_zone')                    
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_clean)
                                actions.click(menu_clean)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-4-zone")))     
                                soup_goals_conceed = BeautifulSoup(browser.page_source, "html.parser")   
                                
                                goals_conced = soup_goals_conceed.find('div',{'id': 'the-graph-4-zone'})
                                goals_conced = goals_conced.find('p',{'id': 'dp-goalmouth-text'})
                                goals_conced = goals_conced.find('span',{'class': 'gm_num'})
                                
                                goalkeeper_sw.total_goal_conceed2 = int(goals_conced.text)
                                goalkeeper_sw.goals_zone = []
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)    
                                
                        not_fail = True
                        while(not_fail):
                            try:                                  
                                menu_clean = browser.find_element_by_id('stat-6')                    
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_clean)
                                actions.click(menu_clean)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-6-type")))     
                                soup_goals_conceed = BeautifulSoup(browser.page_source, "html.parser")   
                                
                       
                                goalkeeper_sw.avg_saves_per_game = float(browser.find_element_by_id('stat-6').find_element_by_class_name('stat').get_attribute("innerHTML"))
            
                                saves_game = soup_goals_conceed.find('div',{'id': 'the-graph-6-type'})
                                saves_game = saves_game.find('div',{'aria-label': arial_label})
                                saves_game = saves_game.find('tbody')
                                saves_game = saves_game.findAll('tr')
                                
                                total_saves = 0
                                for saves_con in xrange(len(saves_game)):
                                    date = saves_game[saves_con].findAll('td')[0].text
                                    saves = int(saves_game[saves_con].findAll('td')[1].text)
                                    total_saves = total_saves + saves
                                    goalkeeper_sw.saves_per_game_list.append([date, saves])
                                
                                goalkeeper_sw.saves_per_game_list = []
                                goalkeeper_sw.num_saves = total_saves
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)                          

                        not_fail = True
                        while(not_fail):
                            try:                        
                                menu_penalty = browser.find_element_by_id('stat-6_penalty_success')                    
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_penalty)
                                actions.click(menu_penalty)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-penalty_success")))     
                                soup_penalties_map = BeautifulSoup(browser.page_source, "html.parser")  
                                
                                num_penalties = soup_goals_conceed.find('div',{'id': 'the-graph-penalty_success'})
                                num_penalties = num_penalties.find('p',{'id': 'dp-goalmouth-text2'})
                                num_penalties = num_penalties.findAll('span')
            
                                
                                goalkeeper_sw.saves_position_list = []
                                goalkeeper_sw.penalties_conceded = int(num_penalties[0].text)
                                goalkeeper_sw.penalties_saved = (num_penalties[1].text)
                                goalkeeper_sw.penalties_list = []
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)     
                        not_fail = True
                        while(not_fail):
                            try:        
                                menu_penalty = browser.find_element_by_id('stat-7')                    
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_penalty)
                                actions.click(menu_penalty)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "stat-graph-7")))     
                                soup_saves_goal = BeautifulSoup(browser.page_source, "html.parser")  
                                
                                goalkeeper_sw.avg_saves_per_goal = float(browser.find_element_by_id('stat-7').find_element_by_class_name('stat').get_attribute("innerHTML"))
             
                                
                                saves_goal = soup_saves_goal.find('div',{'id': 'the-graph-7'})
                                saves_goal = saves_goal.find('div',{'aria-label': arial_label})
                                saves_goal = saves_goal.find('tbody')
                                saves_goal = saves_goal.findAll('tr')
                                
                                total_saves = 0
                                for saves_con in xrange(len(saves_goal)):
                                    date = saves_goal[saves_con].findAll('td')[0].text
                                    saves = float(saves_goal[saves_con].findAll('td')[1].text)
                                    total_saves = total_saves + saves
                                    goalkeeper_sw.saves_per_goal_list.append([date, saves])
                                
                                goalkeeper_sw.total_saves_goal = total_saves  
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)    
                                

                        not_fail = True
                        while(not_fail):
                            try:   
                                menu_claim = browser.find_element_by_id('stat-8')                    
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_claim)
                                actions.click(menu_claim)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "stat-graph-8")))     
                                soup_claim_succ = BeautifulSoup(browser.page_source, "html.parser") 
                              
                                goalkeeper_sw.avg_claims_success = float(browser.find_element_by_id('stat-8').find_element_by_class_name('stat').get_attribute("innerHTML").split('%')[0])
            
                                claims_succ = soup_claim_succ.find('div',{'id': 'the-graph-8-type'})
                                claims_succ = claims_succ.find('div',{'aria-label': arial_label})
                                claims_succ = claims_succ.find('tbody')
                                claims_succ = claims_succ.findAll('tr')
                                
                                total_succ = 0
                                total_unsucc = 0
                                
                                for clais_ind in xrange(len(claims_succ)):
                                    date = claims_succ[clais_ind].findAll('td')[0].text
                                    claims_num = int(claims_succ[clais_ind].findAll('td')[1].text)
                                    total_succ = total_succ + claims_num
                                    claims_num_un = int(claims_succ[clais_ind].findAll('td')[2].text)
                                    total_unsucc = total_unsucc + claims_num_un
                                    goalkeeper_sw.claims_success_list.append([date, claims_num])
                                    goalkeeper_sw.claims_fail_list.append([date, claims_num_un])                 
            
                                goalkeeper_sw.tot_claims_success = total_succ
                                goalkeeper_sw.tot_claims_fail = total_unsucc       
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
                                
                        not_fail = True
                        while(not_fail):
                            try:                                   
                                menu_punch = browser.find_element_by_id('stat-9')                    
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_punch)
                                actions.click(menu_punch)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-9-type")))     
                                soup_punches = BeautifulSoup(browser.page_source, "html.parser") 
                                                  
                                
                                goalkeeper_sw.avg_punches = float(browser.find_element_by_id('stat-9').find_element_by_class_name('stat').get_attribute("innerHTML").split('%')[0])       
                               
                               
                                avg_punches_m = soup_punches.find('div',{'id': 'the-graph-9-type'})
                                avg_punches_m = avg_punches_m.find('div',{'aria-label': arial_label})
                                avg_punches_m = avg_punches_m.find('tbody')
                                avg_punches_m = avg_punches_m.findAll('tr')
                                
                                total_succ = 0
                                total_unsucc = 0
                                
                                for punch_index in xrange(len(avg_punches_m)):
                                    
                                    date = avg_punches_m[punch_index].findAll('td')[0].text
                                    punch_num = int(avg_punches_m[punch_index].findAll('td')[1].text)
                                    total_succ = total_succ + punch_num
                                    
                                    punch_num_un = int(avg_punches_m[punch_index].findAll('td')[2].text)
                                    total_unsucc = total_unsucc + punch_num_un
                                    
                                    goalkeeper_sw.punches_success_list.append([date, punch_num])
                                    goalkeeper_sw.punches_fail_list.append([date, total_unsucc])                         
                               
                                goalkeeper_sw.tot_punches_success = total_succ
                                goalkeeper_sw.tot_punches_fail = total_unsucc  
                        
                                goalkeeper_sw.avg_dist_succ = float(browser.find_element_by_id('stat-10').find_element_by_class_name('stat').get_attribute("innerHTML").split('%')[0])
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
                                
                        not_fail = True
                        while(not_fail):
                            try:                                  
                                menu_dist_success = browser.find_element_by_id('stat-10')                    
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_dist_success)
                                actions.click(menu_dist_success)
                                actions.perform()
                                
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-10-type")))     
                                soup_dist_succ = BeautifulSoup(browser.page_source, "html.parser")        
                                
                                dist_succ = soup_dist_succ.find('div',{'id': 'the-graph-10-type'})
                                dist_succ = dist_succ.find('div',{'aria-label': arial_label})
                                dist_succ = dist_succ.find('tbody')
                                dist_succ = dist_succ.findAll('td')                    
                                
                                goalkeeper_sw.succ_goal_kicks = int(dist_succ[1].text)
                                goalkeeper_sw.unsucc_goal_kicks = int(dist_succ[6].text)
                                goalkeeper_sw.succ_kicks_from_hands = int(dist_succ[2].text)       
                                goalkeeper_sw.unsucc_kicks_from_hands = int(dist_succ[7].text)
                                goalkeeper_sw.succ_threw_out = int(dist_succ[3].text)
                                goalkeeper_sw.unsucc_threw_out = int(dist_succ[8].text)       
                                goalkeeper_sw.succ_other = int(dist_succ[4].text)
                                goalkeeper_sw.unsucc_other = int(dist_succ[9].text)
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
                        
                         
                        menu_dist_length = browser.find_element_by_id('stat-11')                    
                        actions = ActionChains(browser) 
                        actions.move_to_element(menu_dist_length)
                        actions.click(menu_dist_length)
                        actions.perform()
                        
                        element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-11-type")))     
                        soup_dist_length = BeautifulSoup(browser.page_source, "html.parser")     
    
                        dist_length = soup_dist_length.find('div',{'id': 'the-graph-11-type'})
                        dist_length = dist_length.find('div',{'aria-label': arial_label})
                        dist_length = dist_length.find('tbody')
                        dist_length = dist_length.findAll('td') 

                        goalkeeper_sw.dis_length = float(dist_length[1].text)
                        goalkeeper_sw.goal_kicks_length = float(dist_length[2].text)       
                        goalkeeper_sw.kicks_from_hands = float(dist_length[3].text)         
                        goalkeeper_sw.threw_out_length = float(dist_length[4].text) 
                        goalkeeper_sw.other_length = float(dist_length[5].text)

                                          
                        not_fail = True
                        while(not_fail):
                            try:                         
                                menu_cards = browser.find_element_by_id('stat-12') 
                                
                                actions = ActionChains(browser) 
                                actions.move_to_element(menu_cards)
                                actions.click(menu_cards)
                                actions.perform()
            
                                element = WebDriverWait(browser, delay2).until(EC.element_to_be_clickable((By.ID, "the-graph-12")))                 
                                
                                soup_cards = BeautifulSoup(browser.page_source, "html.parser" )
                                
                                cards_list = (browser.find_element_by_id('stat-12').find_element_by_class_name('stat').get_attribute("innerHTML")).split('/')
                               
                                goalkeeper_sw.tot_yel_card = int(cards_list[0])
                                yell_card_lt = soup_cards.find('div',{'id': 'the-graph-12'}).find('div',{'aria-label': arial_label}).find('tbody').findAll('td')    
                                goalkeeper_sw.viol_yel_card = int(yell_card_lt[1].text)
                                goalkeeper_sw.tack_yel_card = int(yell_card_lt[2].text)
                                goalkeeper_sw.verb_yel_card = int(yell_card_lt[3].text)
                                goalkeeper_sw.oth_yel_card = int(yell_card_lt[4].text)
                                
                                goalkeeper_sw.tot_red_card =  int(cards_list[1])
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)

                        not_fail = True
                        while(not_fail):
                            try:                                           
                                menu_chance = browser.find_element_by_id('stat-12_red_cards')
                                actions = ActionChains(browser)  
                                actions.move_to_element(menu_chance)
                                actions.click(menu_chance)
                                actions.perform()
                               
                                element = WebDriverWait(browser, delay2).until(EC.presence_of_element_located((By.ID, "stat-graph-12-red")))
                                
                                soup_red_cards = BeautifulSoup(browser.page_source, "html.parser" )
                                red_card_lt = soup_red_cards.find('div',{'id': 'the-graph-12a'})                          
                                red_card_lt = red_card_lt.find('div',{'aria-label': arial_label})
            
                                red_card_lt = red_card_lt.find('tbody')
            
                                red_card_lt = red_card_lt.findAll('td')
                             
                                goalkeeper_sw.viol_red_card = int(red_card_lt[1].text)
                                goalkeeper_sw.tack_red_card = int(red_card_lt[2].text)
                                goalkeeper_sw.verb_red_card = int(red_card_lt[3].text)
                                goalkeeper_sw.oth_red_card = int(red_card_lt[4].text) 
                                not_fail = False
                            except:
                                browser.implicitly_wait(delay1)
                                time.sleep(delay1)
                        
                        write = str(goalkeeper_sw.name) + ',' + str(goalkeeper_sw.position_sw) + ','+ str(goalkeeper_sw.team) + ','+ str(goalkeeper_sw.age) + ','+ str(goalkeeper_sw.height) + ','+ str(goalkeeper_sw.weight)+ ','+ str(goalkeeper_sw.year)+ ','
                        write = write + str(goalkeeper_sw.app_tot) + ','+ str(goalkeeper_sw.app_full) + ','+ str(goalkeeper_sw.app_sub_on) + ','+ str(goalkeeper_sw.app_sub_off) + ','                  
                        
                        write = write + str(goalkeeper_sw.clean_sheets) + ','+ str(goalkeeper_sw.total_goal_conceed) + ','+ str(goalkeeper_sw.avg_goals_conceed) + ','+ str(goalkeeper_sw.goals_corner) + ',' 
                        write = write + str(goalkeeper_sw.goals_set_piece_crosses) + ','+ str(goalkeeper_sw.goals_direct_free_kicks) + ','+ str(goalkeeper_sw.goals_open_play) + ','+ str(goalkeeper_sw.goals_open_play_outside_box) + ',' 
                        write = write + str(goalkeeper_sw.goals_others) + ','+ str(goalkeeper_sw.total_goal_conceed2) + ','+ str(goalkeeper_sw.avg_saves_per_game) + ','+ str(goalkeeper_sw.num_saves) + ',' 
                        write = write + str(goalkeeper_sw.num_saves2) + ','+ str(goalkeeper_sw.penalties_conceded) + ','+ str(goalkeeper_sw.penalties_saved) + ',' 
                        
                        write = write + str(goalkeeper_sw.avg_saves_per_goal) + ','+ str(goalkeeper_sw.total_saves_goal) + ','+ str(goalkeeper_sw.avg_claims_success) + ','+ str(goalkeeper_sw.tot_claims_success) + ',' 
                        write = write + str(goalkeeper_sw.tot_claims_fail) + ','+ str(goalkeeper_sw.avg_punches) + ','+ str(goalkeeper_sw.tot_punches_success) + ','+ str(goalkeeper_sw.tot_punches_fail) + ',' 
                        write = write + str(goalkeeper_sw.avg_dist_succ) + ','+ str(goalkeeper_sw.succ_goal_kicks) + ','+ str(goalkeeper_sw.unsucc_goal_kicks) + ','+ str(goalkeeper_sw.succ_kicks_from_hands) + ',' 
    
                        write = write + str(goalkeeper_sw.unsucc_kicks_from_hands) + ','+ str(goalkeeper_sw.succ_threw_out) + ','+ str(goalkeeper_sw.unsucc_threw_out) + ','+ str(goalkeeper_sw.succ_other) + ',' 
                        write = write + str(goalkeeper_sw.unsucc_other) + ','+ str(goalkeeper_sw.dis_length) + ','+ str(goalkeeper_sw.goal_kicks_length) + ','+ str(goalkeeper_sw.kicks_from_hands) + ',' 
                        write = write + str(goalkeeper_sw.threw_out_length) + ','+ str(goalkeeper_sw.other_length) + ','+ str(goalkeeper_sw.tot_yel_card) + ','+ str(goalkeeper_sw.viol_yel_card) + ','
                        write = write + str(goalkeeper_sw.tack_yel_card) + ','+ str(goalkeeper_sw.verb_yel_card) + ','+ str(goalkeeper_sw.oth_yel_card) + ','+ str(goalkeeper_sw.tot_red_card) + ','
                        write = write + str(goalkeeper_sw.viol_red_card) + ','+ str(goalkeeper_sw.tack_red_card) + ','+ str(goalkeeper_sw.verb_red_card) + ','+ str(goalkeeper_sw.oth_red_card) + '\n'                    
                        goalkeepers_file.write(write)                    


        players_file.close()
        goalkeepers_file.close()                  
            #soup_players = BeautifulSoup(browser.page_source, "html.parser")
            
            #print soup_players.find('td',{'id':'stat-2'}).find('span',{'class':'stat'}).text 
            #print soup_players.find('td',{'id':'stat-1'}).find('span',{'class':'stat'}).text
            