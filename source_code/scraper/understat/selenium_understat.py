import time


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
from source_code.scraper.common import understat_models
from source_code.scraper.understat.models import constants_understat

from source_code import settings

if __name__ == "__main__":
    try:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE, executable_path=settings.EXECUTABLE)
    except Exception:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE)
    site = constants_understat.UNDERSTAT_URL
    print(site)
    browser.get(site)
    #browser.execute_script("document.body.style.zoom='50%'")
    #browser.execute_script('document.body.style.MozTransform = "scale(0.50)";')
    #browser.execute_script('document.body.style.MozTransformOrigin = "0 0";')
    page = browser.page_source
    soup = BeautifulSoup(page, "html.parser")
    teams = soup.find('div', {'id': 'league-chemp'}).find('tbody').find_all('a')
    for team in teams:
        #team = teams[constants_understat.TEAM_INDEX]
        team_link = constants_understat.ORIGINAL_UNDERSTAT_URL + team.get('href')
        browser.get(team_link)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        situations = soup.find('div', {'id': 'team-statistics'}).find('tbody').find_all('tr')
        new_team = understat_models.Team()
        team_name = soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text
        new_team.name = team_name
        new_team.season = constants_understat.YEAR_TEXT
        competition_file_name = '%s -%s - %s.json' % (constants_understat.LEAGUE_TEXT, constants_understat.YEAR_TEXT, team_name)
        league_file = open(competition_file_name, 'w')
        #league_file.write(constants_understat.TEAMS_WRITE)
        players_file_name = 'data/%s- %s - Players-%s.json' % (
            team_name, constants_understat.LEAGUE_TEXT, constants_understat.YEAR_TEXT)
        players_file = open(players_file_name, 'w')
        #players_file.write(constants_understat.PLAYERS_WRITE)
        print(team_name)
        for situation in situations:
            situation_stats = situation.find_all('td')
            situation_performance = understat_models.TeamPerformance()
            situation_performance.shots = situation_stats[2].text
            situation_performance.goals = situation_stats[3].text
            situation_performance.shotsAgainst = situation_stats[4].text
            situation_performance.goalsAgainst = situation_stats[5].text
            situation_performance.xG = situation_stats[6].text.split('+')[0].split('-')[0]
            situation_performance.xGA = situation_stats[7].text.split('+')[0].split('-')[0]
            situation_performance.xGD = situation_stats[8].text
            situation_performance.xGSh = situation_stats[9].text
            situation_performance.xGASh = situation_stats[10].text
            new_team.performance_by_situation[situation_stats[1].text] = situation_performance.__dict__
        xpath = "// label[ @for = 'statistic-2']"
        menu_formation = browser.find_element_by_xpath(xpath)
        actions = ActionChains(browser)
        actions.move_to_element(menu_formation)
        actions.click(menu_formation)
        actions.perform()
        soup = BeautifulSoup(browser.page_source, "html.parser")
        formations = soup.find('div', {'id': 'team-statistics'}).find('tbody').find_all('tr')
        for formation in formations:
            formation_stats = formation.find_all('td')
            formation_performance = understat_models.TeamPerformance()
            formation_performance.min = formation_stats[2].text
            formation_performance.shots = formation_stats[3].text
            formation_performance.goals = formation_stats[4].text
            formation_performance.shotsAgainst = formation_stats[5].text
            formation_performance.goalsAgainst = formation_stats[6].text
            formation_performance.xG = formation_stats[7].text.split('+')[0].split('-')[0]
            formation_performance.xGA = formation_stats[8].text.split('+')[0].split('-')[0]
            formation_performance.xGD = formation_stats[9].text
            formation_performance.xG90 = formation_stats[10].text
            formation_performance.xGA90 = formation_stats[11].text
            new_team.performance_by_formation[formation_stats[1].text] = formation_performance.__dict__
        xpath = "// label[ @for = 'statistic-3']"
        menu_game_state = browser.find_element_by_xpath(xpath)
        actions = ActionChains(browser)
        actions.move_to_element(menu_game_state)
        actions.click(menu_game_state)
        actions.perform()
        soup = BeautifulSoup(browser.page_source, "html.parser")
        game_states = soup.find('div', {'id': 'team-statistics'}).find('tbody').find_all('tr')
        for game_state in game_states:
            game_state_stats = game_state.find_all('td')
            game_state_performance = understat_models.TeamPerformance()
            game_state_performance.min = game_state_stats[2].text
            game_state_performance.shots = game_state_stats[3].text
            game_state_performance.goals = game_state_stats[4].text
            game_state_performance.shotsAgainst = game_state_stats[5].text
            game_state_performance.goalsAgainst = game_state_stats[6].text
            game_state_performance.xG = game_state_stats[7].text.split('+')[0].split('-')[0]
            game_state_performance.xGA = game_state_stats[8].text.split('+')[0].split('-')[0]
            game_state_performance.xGD = game_state_stats[9].text
            game_state_performance.xG90 = game_state_stats[10].text
            game_state_performance.xGA90 = game_state_stats[11].text
            new_team.performance_by_game_state[game_state_stats[1].text] = game_state_performance.__dict__
        xpath = "// label[ @for = 'statistic-4']"
        menu_timing = browser.find_element_by_xpath(xpath)
        actions = ActionChains(browser)
        actions.move_to_element(menu_timing)
        actions.click(menu_timing)
        actions.perform()
        soup = BeautifulSoup(browser.page_source, "html.parser")
        timings = soup.find('div', {'id': 'team-statistics'}).find('tbody').find_all('tr')
        for timing in timings:
            timing_stats = timing.find_all('td')
            timing_performance = understat_models.TeamPerformance()
            timing_performance.shots = timing_stats[2].text
            timing_performance.goals = timing_stats[3].text
            timing_performance.shotsAgainst = timing_stats[4].text
            timing_performance.goalsAgainst = timing_stats[5].text
            timing_performance.xG = timing_stats[6].text.split('+')[0].split('-')[0]
            timing_performance.xGA = timing_stats[7].text.split('+')[0].split('-')[0]
            timing_performance.xGD = timing_stats[8].text
            timing_performance.xGSh = timing_stats[9].text
            timing_performance.xGASh = timing_stats[10].text
            new_team.performance_by_timing[timing_stats[1].text] = timing_performance.__dict__
        xpath = "// label[ @for = 'statistic-5']"
        menu_shot_zones = browser.find_element_by_xpath(xpath)
        actions = ActionChains(browser)
        actions.move_to_element(menu_shot_zones)
        actions.click(menu_shot_zones)
        actions.perform()
        soup = BeautifulSoup(browser.page_source, "html.parser")
        shot_zones = soup.find('div', {'id': 'team-statistics'}).find('tbody').find_all('tr')
        for shot_zone in shot_zones:
            shot_zone_stats = shot_zone.find_all('td')
            shot_zone_performance = understat_models.TeamPerformance()
            shot_zone_performance.shots = shot_zone_stats[2].text
            shot_zone_performance.goals = shot_zone_stats[3].text
            shot_zone_performance.shotsAgainst = shot_zone_stats[4].text
            shot_zone_performance.goalsAgainst = shot_zone_stats[5].text
            shot_zone_performance.xG = shot_zone_stats[6].text.split('+')[0].split('-')[0]
            shot_zone_performance.xGA = shot_zone_stats[7].text.split('+')[0].split('-')[0]
            shot_zone_performance.xGD = shot_zone_stats[8].text
            shot_zone_performance.xGSh = shot_zone_stats[9].text
            shot_zone_performance.xGASh = shot_zone_stats[10].text
            new_team.performance_by_shot_zones[shot_zone_stats[1].text] = shot_zone_performance.__dict__
        xpath = "// label[ @for = 'statistic-6']"
        menu_attack_speed = browser.find_element_by_xpath(xpath)
        actions = ActionChains(browser)
        actions.move_to_element(menu_attack_speed)
        actions.click(menu_attack_speed)
        actions.perform()
        soup = BeautifulSoup(browser.page_source, "html.parser")
        attacks_speed = soup.find('div', {'id': 'team-statistics'}).find('tbody').find_all('tr')
        for attack_speed in attacks_speed:
            attack_speed_stats = attack_speed.find_all('td')
            attack_speed_performance = understat_models.TeamPerformance()
            attack_speed_performance.shots = attack_speed_stats[2].text
            attack_speed_performance.goals = attack_speed_stats[3].text
            attack_speed_performance.shotsAgainst = attack_speed_stats[4].text
            attack_speed_performance.goalsAgainst = attack_speed_stats[5].text
            attack_speed_performance.xG = attack_speed_stats[6].text.split('+')[0].split('-')[0]
            attack_speed_performance.xGA = attack_speed_stats[7].text.split('+')[0].split('-')[0]
            attack_speed_performance.xGD = attack_speed_stats[8].text
            attack_speed_performance.xGSh = attack_speed_stats[9].text
            attack_speed_performance.xGASh = attack_speed_stats[10].text
            new_team.performance_by_attack_speed[attack_speed_stats[1].text] = attack_speed_performance.__dict__
        xpath = "// label[ @for = 'statistic-7']"
        menu_result = browser.find_element_by_xpath(xpath)
        actions = ActionChains(browser)
        actions.move_to_element(menu_result)
        actions.click(menu_result)
        actions.perform()
        soup = BeautifulSoup(browser.page_source, "html.parser")
        results = soup.find('div', {'id': 'team-statistics'}).find('tbody').find_all('tr')
        for result in results:
            result_stats = result.find_all('td')
            result_performance = understat_models.TeamPerformance()
            result_performance.shots = result_stats[2].text
            result_performance.goals = result_stats[3].text
            result_performance.shotsAgainst = result_stats[4].text
            result_performance.goalsAgainst = result_stats[5].text
            result_performance.xG = result_stats[6].text.split('+')[0].split('-')[0]
            result_performance.xGA = result_stats[7].text.split('+')[0].split('-')[0]
            result_performance.xGD = result_stats[8].text
            result_performance.xGSh = result_stats[9].text
            result_performance.xGASh = result_stats[10].text
            new_team.performance_by_result[result_stats[1].text] = result_performance.__dict__
        dict_to_write = {"team": str(new_team.name),
                         "season": str(new_team.season),
                         "situation": new_team.performance_by_situation,
                         "formation": new_team.performance_by_formation,
                         "game_state": new_team.performance_by_game_state,
                         "timing": new_team.performance_by_timing,
                         "shot_zones": new_team.performance_by_shot_zones,
                         "attack_speed": new_team.performance_by_attack_speed,
                         "result": new_team.performance_by_result,
                         }
        write = '{0}'.format(
            json.dumps(dict_to_write, indent=4, separators=(',', ': '))
        )
        league_file.write(write)
        players = soup.find('div', {'id': 'team-players'}).find('tbody').find_all('tr')
        for idx, player in enumerate(players):
            player_link = constants_understat.ORIGINAL_UNDERSTAT_URL + player.find_all('td')[1].find('a').get('href')
            browser.get(player_link)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            name = soup.find('div', {'class': 'header-wrapper'}).text.split("\n")[1].split('\t')[4]
            print(name)
            seasons = soup.find('div', {'id': 'player-groups'}).find('tbody').find_all('tr')
            enter = True
            for season in seasons:
                season_stats = season.find_all('td')
                if (season_stats[1].text == constants_understat.SEASON_TEXT) and enter:
                    new_player = understat_models.Player()
                    new_player.name = name
                    new_player.team = season_stats[2].text
                    new_player.season = constants_understat.YEAR_TEXT
                    season_performance = understat_models.Performance()
                    season_performance.apps = season_stats[3].text
                    season_performance.min = season_stats[4].text
                    season_performance.goals = season_stats[5].text
                    season_performance.assist = season_stats[6].text
                    season_performance.sh90 = season_stats[7].text
                    season_performance.kp90 = season_stats[8].text
                    season_performance.xG = season_stats[9].text.split('+')[0].split('-')[0]
                    season_performance.xA = season_stats[10].text.split('+')[0].split('-')[0]
                    season_performance.xG90 = season_stats[11].text
                    season_performance.xA90 = season_stats[12].text
                    new_player.general = season_performance.__dict__
                    xpath = "// label[ @for = 'groups-field-2']"
                    menu_position = browser.find_element_by_xpath(xpath)
                    actions = ActionChains(browser)
                    actions.move_to_element(menu_position)
                    actions.click(menu_position)
                    actions.perform()
                    select_drop_year = browser.find_elements_by_class_name('custom-select-styled')[1]
                    actions = ActionChains(browser)
                    actions.move_to_element(select_drop_year)
                    actions.click(select_drop_year)
                    actions.perform()
                    select_season = browser.find_elements_by_class_name("custom-select-options")[1].\
                        find_elements_by_css_selector("li")
                    new_season = select_season[0]
                    for seas in select_season:
                        if seas.get_attribute("innerHTML") == constants_understat.SEASON_TEXT:
                            new_season = seas
                    actions = ActionChains(browser)
                    actions.move_to_element(new_season)
                    actions.click(new_season)
                    actions.perform()
                    soup = BeautifulSoup(browser.page_source, "html.parser")
                    positions = soup.find('div', {'id': 'player-groups'}).find('tbody').find_all('tr')
                    for position in positions:
                        position_stats = position.find_all('td')
                        position_performance = understat_models.Performance()
                        position_performance.apps = position_stats[2].text
                        position_performance.min = position_stats[3].text
                        position_performance.goals = position_stats[4].text
                        position_performance.assist = position_stats[5].text
                        position_performance.sh90 = position_stats[6].text
                        position_performance.kp90 = position_stats[7].text
                        position_performance.xG = position_stats[8].text.split('+')[0].split('-')[0]
                        position_performance.xA = position_stats[9].text.split('+')[0].split('-')[0]
                        position_performance.xG90 = position_stats[10].text
                        position_performance.xA90 = position_stats[11].text
                        new_player.performance_by_position[position_stats[1].text] = position_performance.__dict__
                    xpath = "// label[ @for = 'groups-field-3']"
                    menu_situation = browser.find_element_by_xpath(xpath)
                    actions = ActionChains(browser)
                    actions.move_to_element(menu_situation)
                    actions.click(menu_situation)
                    actions.perform()
                    soup = BeautifulSoup(browser.page_source, "html.parser")
                    situations = soup.find('div', {'id': 'player-groups'}).find('tbody').find_all('tr')
                    for situation in situations:
                        situation_stats = situation.find_all('td')
                        situation_performance = understat_models.Performance()
                        situation_performance.shots = situation_stats[2].text
                        situation_performance.goals = situation_stats[3].text
                        situation_performance.KP = situation_stats[4].text
                        situation_performance.assist = situation_stats[5].text
                        situation_performance.xG = situation_stats[6].text.split('+')[0].split('-')[0]
                        situation_performance.xA = situation_stats[7].text.split('+')[0].split('-')[0]
                        situation_performance.xG90 = situation_stats[8].text
                        situation_performance.xA90 = situation_stats[9].text
                        situation_performance.xGSh = situation_stats[10].text
                        situation_performance.xAKP = situation_stats[11].text
                        new_player.performance_by_situation[situation_stats[1].text] = situation_performance.__dict__
                    xpath = "// label[ @for = 'groups-field-4']"
                    menu_shot_zones = browser.find_element_by_xpath(xpath)
                    actions = ActionChains(browser)
                    actions.move_to_element(menu_shot_zones)
                    actions.click(menu_shot_zones)
                    actions.perform()
                    soup = BeautifulSoup(browser.page_source, "html.parser")
                    shot_zones = soup.find('div', {'id': 'player-groups'}).find('tbody').find_all('tr')
                    for shot_zone in shot_zones:
                        shot_zone_stats = shot_zone.find_all('td')
                        shot_zone_performance = understat_models.Performance()
                        shot_zone_performance.shots = shot_zone_stats[2].text
                        shot_zone_performance.goals = shot_zone_stats[3].text
                        shot_zone_performance.KP = shot_zone_stats[4].text
                        shot_zone_performance.assist = shot_zone_stats[5].text
                        shot_zone_performance.xG = shot_zone_stats[6].text.split('+')[0].split('-')[0]
                        shot_zone_performance.xA = shot_zone_stats[7].text.split('+')[0].split('-')[0]
                        shot_zone_performance.xGSh = shot_zone_stats[8].text
                        shot_zone_performance.xAKP = shot_zone_stats[9].text
                        new_player.performance_by_shot_zones[shot_zone_stats[1].text] = shot_zone_performance.__dict__
                    xpath = "// label[ @for = 'groups-field-5']"
                    menu_shot_types = browser.find_element_by_xpath(xpath)
                    actions = ActionChains(browser)
                    actions.move_to_element(menu_shot_types)
                    actions.click(menu_shot_types)
                    actions.perform()
                    soup = BeautifulSoup(browser.page_source, "html.parser")
                    shot_types = soup.find('div', {'id': 'player-groups'}).find('tbody').find_all('tr')
                    for shot_type in shot_types:
                        shot_type_stats = shot_type.find_all('td')
                        shot_type_performance = understat_models.Performance()
                        shot_type_performance.shots = shot_type_stats[2].text
                        shot_type_performance.goals = shot_type_stats[3].text
                        shot_type_performance.KP = shot_type_stats[4].text
                        shot_type_performance.assist = shot_type_stats[5].text
                        shot_type_performance.xG = shot_type_stats[6].text.split('+')[0].split('-')[0]
                        shot_type_performance.xA = shot_type_stats[7].text.split('+')[0].split('-')[0]
                        shot_type_performance.xGSh = shot_type_stats[8].text
                        shot_type_performance.xAKP = shot_type_stats[9].text
                        new_player.performance_by_shot_types[shot_type_stats[1].text] = shot_type_performance.__dict__
                    enter = False

                    player_to_write = {"name": str(new_player.name),
                                     "season": str(new_player.season),
                                     "team": new_player.team,
                                     "general": new_player.general,
                                     "performance_by_position": new_player.performance_by_position,
                                     "performance_by_situation": new_player.performance_by_situation,
                                     "performance_by_shot_zones": new_player.performance_by_shot_zones,
                                     "performance_by_shot_types": new_player.performance_by_shot_types,
                                     }
                    write = '{0}'.format(
                        json.dumps(player_to_write, indent=4, separators=(',', ': ')))
                    if idx == 0:
                        write = "[" + write + ","
                    elif idx == (len(players)-1):
                        write = write + "]"
                    else:
                        write = write + ","
                    players_file.write(write)
        players_file.close()
        league_file.close()
