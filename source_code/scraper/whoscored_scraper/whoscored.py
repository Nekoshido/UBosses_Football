from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import chain, zip_longest
import json
import pathlib
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from source_code.scraper.whoscored_scraper.models import constants_whoscored
from source_code.scraper.common import whoscored_models
from source_code import settings

def search_player_in_list(name, player_list):
    for idx, element in enumerate(player_list):
        if element.name == name:
            return idx
    return None

def clean_float(number):
    # print("&" + str(number) + "&")
    if number == "-" or number == 'N/A ' or number == 'N/A':
        return 0
    else:
        return float(number)

if __name__ == "__main__":
    try:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE, executable_path=settings.EXECUTABLE)
    except Exception:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE)

    # try:
    #     path_to_extension = '/Users/Hecto/PycharmProjects/UBosses_Football/resources/chrome/plugins/ublock.crx'
    #
    #     chrome_options = Options()
    #     chrome_options.add_argument('load-extension=' + path_to_extension)
    #     browser = webdriver.Chrome(executable_path='/Users/Hecto/PycharmProjects/UBosses_Football/resources/chrome/chrome_driver/win/chromedriver.exe',
    #                                chrome_options=chrome_options)
    # except Exception:
    #     browser = webdriver.Chrome()


    if constants_whoscored.LEAGUE_INDEX in [9]:
        site = '{}/Regions/{}/Tournaments/{}/Seasons/{}/Stages/{}/Show/{}-{}'.format(constants_whoscored.WHOSCORED_URL,
                                                                  constants_whoscored.LEAGUES_ID[constants_whoscored.LEAGUE_INDEX],
                                                                constants_whoscored.LEAGUES_NUM[constants_whoscored.LEAGUE_INDEX],
                                                                   constants_whoscored.SEASON_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
                                                                     constants_whoscored.PLAYOFF_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
                                                                   constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX],
                                                                                     constants_whoscored.SEASON_NUMBER[
                                                                                         constants_whoscored.SEASON_INDEX])
    else:
        site = '{}/Regions/{}/Tournaments/{}/Seasons/{}/{}'.format(constants_whoscored.WHOSCORED_URL,
                                                                  constants_whoscored.LEAGUES_ID[constants_whoscored.LEAGUE_INDEX],
                                                                constants_whoscored.LEAGUES_NUM[constants_whoscored.LEAGUE_INDEX],
                                                                   constants_whoscored.SEASON_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
                                                                   constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX])


    print(site)
    browser.get(site)
    time.sleep(3)
    browser.execute_script("document.body.style.zoom = '30%';")

    continue_button = browser.find_element_by_class_name('details_continue--2CnZz').find_element_by_tag_name('span')
    actions = ActionChains(browser)
    actions.move_to_element(continue_button)
    actions.click(continue_button).perform()
    soup = BeautifulSoup(browser.page_source, "html.parser")
    table_teams = soup.find_all('table', {'class': 'grid with-centered-columns hover'})[0].find('tbody')
    teams = table_teams.find_all('tr')
    print("SEASON: " + str(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]))
    print("Len Teams: " + str(len(teams[constants_whoscored.TEAM_INDEX:])))
    print(teams)
    for idx, team in enumerate(teams[constants_whoscored.TEAM_INDEX:]):
        print('Progress: ' + str(constants_whoscored.TEAM_INDEX + idx) + ' / ' + str(len(teams)-1))
        url = team.find('a', {'class': 'team-link'}).get('href')
        team_name = team.find('a', {'class': 'team-link'}).text
        if constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX] == constants_whoscored.SEASON_NUMBER[len(constants_whoscored.SEASON_NUMBER)-1]:
            site = '{}{}'.format(constants_whoscored.WHOSCORED_URL, url)

            print(site)
            browser.get(site)
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            options = soup.find('dl', {'id': 'tournamentOptions'})
            option_list = options.find_all('dd')

            season_list = [x.text for x in
                           option_list]
            print("Len Seasons: " + str(len(season_list)))
            for idx_c, competition in enumerate(season_list):
                if competition == "Copa Libertadores" or competition == 'AFC Champions League':
                    continue
                else:

                    print("+++++++++")
                    print(competition)
                    print("+++++++++")
                    if idx_c != 0:
                        summary_button = browser.find_element_by_id('team-squad-stats-options').find_elements_by_tag_name('li')[0]
                        actions = ActionChains(browser)
                        actions.move_to_element(summary_button)
                        actions.click(summary_button)
                        actions.perform()
                        time.sleep(2)

                    comp_button = browser.find_element_by_id('tournamentOptions').find_elements_by_tag_name('dd')[idx_c]
                    actions = ActionChains(browser)
                    actions.move_to_element(comp_button)
                    actions.click(comp_button)
                    actions.perform()

                    time.sleep(3)

                    directory = 'data/%s/%s/' % (
                        constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX],
                        constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
                    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
                    players_file_name = directory + '%s- -%s - Players-%s.json' % (
                        team_name, competition.split('-')[0],
                        constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
                    players_file = open(players_file_name, 'w')

                    soup = BeautifulSoup(browser.page_source, "html.parser")

                    player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')

                    if player_list[0].text == 'There are no results to display':
                        try:
                            Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                            time.sleep(5)
                            Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                            page = browser.page_source
                            soup = BeautifulSoup(page, "html.parser")
                            player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')
                        except:
                            print("CrashSummary")
                            restart_team = browser.find_element_by_class_name(
                                'team-profile-side-box').find_element_by_class_name('team-link')
                            actions = ActionChains(browser)
                            actions.move_to_element(restart_team)
                            actions.click(restart_team)
                            actions.perform()
                            time.sleep(3)
                            soup = BeautifulSoup(browser.page_source, "html.parser")
                            player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')

                    player_team = {}
                    start = time.time()
                    print("Len Seasons: " + str(len(player_list)))
                    for player_row in player_list:
                        new_player = whoscored_models.Player()
                        new_player.name = player_row.find('a', {'class': 'player-link'}).text
                        new_player.name = new_player.name[:len(new_player.name) - 1]
                        new_player.url = player_row.find('a', {'class': 'player-link'})['href']
                        new_player.id = new_player.url.split('/')[2]
                        new_player.nationality = player_row.find_all('td')[1].find('span')['class'][2].split('-')[1]
                        new_player.season = int(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
                        new_player.birth = int(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]) - int(
                            player_row.find('td', {'class': 'pn'}).find_all('span', {'class': 'player-meta-data'})[0].text)
                        new_player.team = \
                        soup.find('span', {'class': 'team-header-name'}).text
                        new_player.position = \
                        player_row.find('td', {'class': 'pn'}).find_all('span', {'class': 'player-meta-data'})[
                            1].text.split(' ')[2]
                        new_player.height = clean_float(player_row.find_all("td")[3].text)
                        new_player.weight = clean_float(player_row.find_all("td")[4].text)
                        new_player.appearances = player_row.find_all("td")[5].text
                        new_player.minutes_played = clean_float(player_row.find_all("td")[6].text.strip('\t'))
                        new_player.goals = clean_float(player_row.find_all("td")[7].text.strip('\t'))
                        new_player.assists = clean_float(player_row.find_all("td")[8].text.strip('\t'))
                        new_player.yellow_cards = clean_float(player_row.find_all("td")[9].text.strip('\t'))
                        new_player.red_cards = clean_float(player_row.find_all("td")[10].text.strip('\t'))
                        new_player.shots_per_game = clean_float(player_row.find_all("td")[11].text.strip('\t'))
                        new_player.pass_success_percentage = clean_float(player_row.find_all("td")[12].text.strip('\t'))
                        new_player.aerials_duels_won_per_game = clean_float(player_row.find_all("td")[13].text.strip('\t'))
                        new_player.man_of_the_match = clean_float(player_row.find_all("td")[14].text.strip('\t'))
                        new_player.rating = clean_float(player_row.find_all("td")[15].text.strip('\t'))
                        new_player.competition = competition.split('-')[0]
                        player_team[new_player.name] = new_player

                    # press defensive button

                    defensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[0]
                    actions = ActionChains(browser)
                    actions.move_to_element(defensive_button)
                    actions.click(defensive_button)
                    actions.perform()

                    time.sleep(5)

                    player_list_defensive = browser.find_elements_by_id("player-table-statistics-body")[
                        1].find_elements_by_tag_name('tr')
                    done = time.time()
                    elapsed = done - start
                    start = time.time()
                    print("Summary: " + str(elapsed))
                    if player_list_defensive[0].get_attribute("innerText") == 'There are no results to display':
                        print("Error Display")
                        try:
                            Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                            time.sleep(5)
                            Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                        except:
                            print("CrashDefensive")
                            restart_team = browser.find_element_by_class_name(
                                'team-profile-side-box').find_element_by_class_name('team-link')
                            actions = ActionChains(browser)
                            actions.move_to_element(restart_team)
                            actions.click(restart_team)
                            actions.perform()
                            time.sleep(3)

                            defensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[0]
                            actions = ActionChains(browser)
                            actions.move_to_element(defensive_button)
                            actions.click(defensive_button)
                            actions.perform()
                            time.sleep(3)
                            player_list_defensive = browser.find_elements_by_id("player-table-statistics-body")[
                                1].find_elements_by_tag_name('tr')

                    print(player_team)
                    for player_row in player_list_defensive:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText").strip('\t')
                        # index = search_player_in_list(name, player_team)
                        player_team[name].tackles_per_game = clean_float(player_row.find_elements_by_tag_name("td")[7].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].interceptions_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            8].get_attribute("innerHTML").strip('\t'))
                        player_team[name].fouls_per_game = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].offside_won_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            10].get_attribute("innerHTML").strip('\t'))
                        player_team[name].clarances_per_game = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].dribbled_past_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            12].get_attribute("innerHTML").strip('\t'))
                        player_team[name].outfielder = clean_float(player_row.find_elements_by_tag_name("td")[13].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].own_goals = clean_float(player_row.find_elements_by_tag_name("td")[14].get_attribute(
                            "innerHTML").strip('\t'))

                    offensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[1]
                    actions = ActionChains(browser)
                    actions.move_to_element(offensive_button)
                    actions.click(offensive_button)
                    actions.perform()
                    done = time.time()
                    elapsed = done - start
                    start = time.time()
                    print("Defensive: " + str(elapsed))

                    time.sleep(2)
                    player_list_offensive = browser.find_elements_by_id("player-table-statistics-body")[2] \
                        .find_elements_by_tag_name('tr')

                    if player_list_offensive[0].get_attribute("innerText") == 'There are no results to display':
                        try:
                            Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                            time.sleep(5)
                            Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                        except:
                            print("CrashOffensive")
                            restart_team = browser.find_element_by_class_name(
                                'team-profile-side-box').find_element_by_class_name('team-link')
                            actions = ActionChains(browser)
                            actions.move_to_element(restart_team)
                            actions.click(restart_team)
                            actions.perform()
                            time.sleep(2)
                            actions.perform()
                            offensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[1]
                            actions = ActionChains(browser)
                            actions.move_to_element(offensive_button)
                            actions.click(offensive_button)
                            actions.perform()
                            time.sleep(2)
                            player_list_offensive = browser.find_elements_by_id("player-table-statistics-body")[2] \
                                .find_elements_by_tag_name('tr')

                    for player_row in player_list_offensive:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText").strip('\t')
                        # index = search_player_in_list(name, player_team)
                        player_team[name].key_passes_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            10].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].dribbles_per_game = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].fouled_per_game = clean_float(player_row.find_elements_by_tag_name("td")[12].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].offsides_per_game = clean_float(player_row.find_elements_by_tag_name("td")[13].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].dispossessed_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            14].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].bad_control_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            15].get_attribute("innerHTML").strip('\t'))

                    passing_button = browser.find_elements_by_class_name('in-squad-detailed-view')[2]
                    actions = ActionChains(browser)
                    actions.move_to_element(passing_button)
                    actions.click(passing_button)
                    actions.perform()

                    time.sleep(2)

                    done = time.time()
                    elapsed = done - start
                    start = time.time()
                    print("Ofensive: " + str(elapsed))

                    player_list_passing = browser.find_elements_by_id("player-table-statistics-body")[3] \
                        .find_elements_by_tag_name('tr')

                    if player_list_passing[0].get_attribute("innerText") == 'There are no results to display':
                        Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                        time.sleep(5)
                        Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                        player_list_passing = browser.find_elements_by_id("player-table-statistics-body")[3] \
                            .find_elements_by_tag_name('tr')

                    for player_row in player_list_passing:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        # index = search_player_in_list(name, player_team)
                        player_team[name].average_passes_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            9].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].pass_success_percentage = clean_float(player_row.find_elements_by_tag_name("td")[
                            10].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].crosses_per_game = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].long_balls_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            12].get_attribute(
                            "innerHTML").strip('\t'))
                        player_team[name].through_balls_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                            13].get_attribute(
                            "innerHTML").strip('\t'))

                    detailed_button = browser.find_elements_by_class_name('in-squad-detailed-view')[3]
                    actions = ActionChains(browser)
                    actions.move_to_element(detailed_button)
                    actions.click(detailed_button)
                    actions.perform()

                    time.sleep(2)

                    done = time.time()
                    elapsed = done - start
                    start = time.time()
                    print("Passing: " + str(elapsed))

                    Select(browser.find_element_by_id('statsAccumulationType')).select_by_value("2")

                    time.sleep(2)

                    detail_list = [x.text for x in
                                   browser.find_element_by_id('category').find_elements_by_tag_name("option")]

                    for detail in detail_list:
                        Select(browser.find_element_by_id('category')).select_by_visible_text(detail)

                        time.sleep(3)

                        player_list_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                            .find_elements_by_tag_name('tr')

                        if player_list_detailed[0].get_attribute("innerText") == 'There are no results to display':
                            print("No Display")
                            try:
                                Select(browser.find_element_by_id('category')).select_by_visible_text(not_new_seasons[0])
                                time.sleep(5)
                                Select(browser.find_element_by_id('category')).select_by_visible_text(detail)
                            except:
                                print("CRASH")
                                restart_team = browser.find_element_by_class_name(
                                    'team-profile-side-box').find_element_by_class_name('team-link')
                                actions = ActionChains(browser)
                                actions.move_to_element(restart_team)
                                actions.click(restart_team)
                                actions.perform()
                                time.sleep(3)
                                history_button = browser.find_element_by_id('sub-navigation').find_elements_by_tag_name('li')[4]
                                actions = ActionChains(browser)
                                actions.move_to_element(history_button)
                                actions.click(history_button)
                                actions.perform()
                                time.sleep(1)

                                detailed_button = browser.find_elements_by_class_name('in-squad-detailed-view')[3]
                                actions = ActionChains(browser)
                                actions.move_to_element(detailed_button)
                                actions.click(detailed_button)
                                actions.perform()

                                time.sleep(1)

                                Select(browser.find_element_by_id('category')).select_by_visible_text(detail)

                                time.sleep(3)

                                player_list_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                    .find_elements_by_tag_name('tr')

                        if detail == "Tackles":
                            startt = time.time()


                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].total_tackles_won = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute("innerText").strip('\t'))
                                player_team[name].player_gets_dribbled = clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerText").strip('\t'))
                                player_team[name].total_tackle_attempts = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute(
                                    "innerText").strip('\t'))
                                player_team[name].total_tackles_won_per90 = player_team[name].total_tackles_won / (player_team[name].minutes_played / 90.0)
                                player_team[name].player_gets_dribbled_per90 = player_team[name].player_gets_dribbled / (player_team[name].minutes_played / 90.0)
                                player_team[name].total_tackle_attempts_per90 = player_team[name].total_tackle_attempts / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Tackles " + str(timet))

                        elif detail == "Interception":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].interceptions = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerText").strip('\t'))
                                player_team[name].interceptions_per90 = player_team[name].interceptions /player_team[name].minutes_played
                            finish = time.time()
                            timet = finish - startt
                            print("Interception " + str(timet))

                        elif detail == "Fouls":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].fouled = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].fouls = clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].fouled_per90 = player_team[name].fouled /player_team[name].minutes_played
                                player_team[name].fouls_per90 = player_team[name].fouls /player_team[name].minutes_played

                            finish = time.time()
                            timet = finish - startt
                            print("Fouls " + str(timet))

                        elif detail == "Cards":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].total_yellow_cards = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].total_red_cards = clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t'))

                                player_team[name].total_yellow_cards_per90 = player_team[name].total_yellow_cards / (player_team[name].minutes_played / 90.0)
                                player_team[name].total_red_cards_per90 = player_team[name].total_red_cards / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Cards " + str(timet))

                        elif detail == "Offsides":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].caught_offside = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))

                                player_team[name].caught_offside_per90 = player_team[name].caught_offside / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Offsides " + str(timet))

                        elif detail == "Clearances":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].total_clearances = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].total_clearances_per90 = player_team[name].total_clearances / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Clearances " + str(timet))

                        elif detail == "Blocks":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].blocked_shots = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].blocked_crosses = clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].blocked_passes = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute(
                                    "innerHTML").strip('\t'))

                                player_team[name].blocked_shots_per90 = player_team[name].blocked_shots / (player_team[name].minutes_played / 90.0)
                                player_team[name].blocked_crosses_per90 = player_team[name].blocked_crosses / (player_team[name].minutes_played / 90.0)
                                player_team[name].blocked_passes_per90 = player_team[name].blocked_passes / (player_team[name].minutes_played / 90.0)
                            finish = time.time()
                            timet = finish - startt
                            print("Blocks " + str(timet))

                        elif detail == "Saves":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].gk_totalsaves = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].gk_saves_insix_yard_box = clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].gk_saves_in_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].gk_saves_from_outside_of_the_box = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                    "innerHTML").strip('\t'))

                                player_team[name].gk_totalsaves_per90 = player_team[name].gk_totalsaves / (player_team[name].minutes_played / 90.0)
                                player_team[name].gk_saves_insix_yard_box_per90 = player_team[name].gk_saves_insix_yard_box / (player_team[name].minutes_played / 90.0)
                                player_team[name].gk_saves_in_penalty_area_per90 = player_team[name].gk_saves_in_penalty_area / (player_team[name].minutes_played / 90.0)
                                player_team[name].gk_saves_from_outside_of_the_box_per90 = player_team[name].gk_saves_from_outside_of_the_box / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Saves " + str(timet))

                        elif detail == "Shots":
                            print("======")
                            print("Shots")
                            print("======")
                            startt = time.time()
                            shot_list = [x.text for x in
                                           browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                            print("Len Shot List: " + str(len(shot_list)))
                            for shot_detail in shot_list:
                                Select(browser.find_element_by_id('subcategory')).select_by_visible_text(shot_detail)

                                time.sleep(3)

                                player_shot_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                    .find_elements_by_tag_name('tr')

                                print("Len player_shot_detailed: " + str(len(player_shot_detailed)))
                                for player_row in player_shot_detailed:
                                    name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                    # index = search_player_in_list(name, player_team)
                                    if shot_detail == "Zones":
                                        player_team[name].total_shots = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            7].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shots_from_outside_the_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shots_from_inside_thesix_yard_box = clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shots_from_inside_the_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                            "innerHTML").strip('\t'))

                                        player_team[name].total_shots_per90 = player_team[name].total_shots / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shots_from_outside_the_penalty_area_per90 = player_team[name].shots_from_outside_the_penalty_area / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shots_from_inside_thesix_yard_box_per90 = player_team[name].shots_from_inside_thesix_yard_box / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shots_from_inside_the_penalty_area_per90 = player_team[name].shots_from_inside_the_penalty_area / (player_team[name].minutes_played / 90.0)


                                    elif shot_detail == "Situations":
                                        player_team[name].shot_open_play = clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_counter = clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_setpiece = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_penalty_taken = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                            "innerHTML").strip('\t'))

                                        player_team[name].shot_open_play_per90 = player_team[name].shot_open_play / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_counter_per90 = player_team[name].shot_counter / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_setpiece_per90 = player_team[name].shot_setpiece / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_penalty_taken_per90 = player_team[name].shot_penalty_taken / (player_team[name].minutes_played / 90.0)


                                    elif shot_detail == "Accuracy":
                                        player_team[name].shot_offtarget = clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_onpost = clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_ontarget = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_blocked = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                            "innerHTML").strip('\t'))

                                        player_team[name].shot_offtarget_per90 = player_team[name].shot_offtarget / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_onpost_per90 = player_team[name].shot_onpost / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_ontarget_per90 = player_team[name].shot_ontarget / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_blocked_per90 = player_team[name].shot_blocked / (player_team[name].minutes_played / 90.0)

                                    elif shot_detail == "Body Parts":
                                        player_team[name].shot_right_foot = clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_left_foot = clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_head = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].shot_other = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                            "innerHTML").strip('\t'))

                                        player_team[name].shot_right_foot_per90 = player_team[name].shot_right_foot / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_left_foot_per90 = player_team[name].shot_left_foot / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_head_per90 = player_team[name].shot_head / (player_team[name].minutes_played / 90.0)
                                        player_team[name].shot_other_per90 = player_team[name].shot_other / (player_team[name].minutes_played / 90.0)


                                finish = time.time()
                                timet = finish - startt
                                print("Shots " + str(timet))

                        elif detail == "Goals":
                            # subcategories
                            print("======")
                            print("Goals")
                            print("======")
                            startt = time.time()
                            goal_list = [x.text for x in
                                         browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                            print("Len goal_list: " + str(len(goal_list)))
                            for goal_detail in goal_list:

                                Select(browser.find_element_by_id('subcategory')).select_by_visible_text(goal_detail)

                                time.sleep(3)

                                player_goal_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                    .find_elements_by_tag_name('tr')

                                print("Len player_goal_detailed: " + str(len(player_goal_detailed)))
                                for player_row in player_goal_detailed:
                                    name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                    # index = search_player_in_list(name, player_team)
                                    if goal_detail == "Zones":
                                        player_team[name].total_goal = clean_float(player_row.find_elements_by_tag_name("td")[
                                            7].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goals_from_inside_thesix_yard_box = clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goals_from_inside_the_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goals_from_outside_the_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                            "innerHTML").strip('\t'))

                                        player_team[name].total_goal_per90 = player_team[name].total_goal / (player_team[name].minutes_played / 90.0)
                                        player_team[name].goals_from_inside_thesix_yard_box_per90 = player_team[name].goals_from_inside_thesix_yard_box / (player_team[name].minutes_played / 90.0)
                                        player_team[name].goals_from_inside_the_penalty_area_per90 = player_team[name].goals_from_inside_the_penalty_area / (player_team[name].minutes_played / 90.0)
                                        player_team[name].goals_from_outside_the_penalty_area_per90 = player_team[name].goals_from_outside_the_penalty_area / (player_team[name].minutes_played / 90.0)

                                    elif goal_detail == "Situations":
                                        player_team[name].goal_open_play = clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goal_counter = clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goal_setpiece = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goal_penaltyscored = clean_float(player_row.find_elements_by_tag_name("td")[
                                            11].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goal_own = clean_float(player_row.find_elements_by_tag_name("td")[
                                            12].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goal_normal = clean_float(player_row.find_elements_by_tag_name("td")[13].get_attribute(
                                            "innerHTML").strip('\t'))

                                        player_team[name].goal_open_play_per90 = player_team[name].goal_open_play/ (player_team[name].minutes_played / 90.0)
                                        player_team[name].goal_counter_per90 = player_team[name].goal_counter/ (player_team[name].minutes_played / 90.0)
                                        player_team[name].goal_setpiece_per90 = player_team[name].goal_setpiece/ (player_team[name].minutes_played / 90.0)
                                        player_team[name].goal_penaltyscored_per90 = player_team[name].goal_penaltyscored/ (player_team[name].minutes_played / 90.0)
                                        player_team[name].goal_own_per90 = player_team[name].goal_own/ (player_team[name].minutes_played / 90.0)
                                        player_team[name].goal_normal_per90 = player_team[name].goal_normal/ (player_team[name].minutes_played / 90.0)

                                    elif goal_detail == "Body Parts":
                                        player_team[name].goal_right_foot = clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goal_left_foot = clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goal_head = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].goal_other = clean_float(player_row.find_elements_by_tag_name("td")[
                                            11].get_attribute(
                                            "innerHTML").strip('\t'))

                                        player_team[name].goal_right_foot_per90 = player_team[name].goal_right_foot / (player_team[name].minutes_played / 90.0)
                                        player_team[name].goal_left_foot_per90 = player_team[name].goal_left_foot / (player_team[name].minutes_played / 90.0)
                                        player_team[name].goal_head_per90 = player_team[name].goal_head / (player_team[name].minutes_played / 90.0)
                                        player_team[name].goal_other_per90 = player_team[name].goal_other / (player_team[name].minutes_played / 90.0)

                                finish = time.time()
                                timet = finish - startt
                                print("Goals: " + str(timet))

                        elif detail == "Dribbles":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].unsuccessful_dribbles = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].successful_dribbles = clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].total_dribbles = clean_float(player_row.find_elements_by_tag_name("td")[
                                    9].get_attribute(
                                    "innerHTML").strip('\t'))

                                player_team[name].unsuccessful_dribbles_per90 = player_team[name].unsuccessful_dribbles / (player_team[name].minutes_played / 90.0)
                                player_team[name].successful_dribbles_per90 = player_team[name].successful_dribbles / (player_team[name].minutes_played / 90.0)
                                player_team[name].total_dribbles_per90 = player_team[name].total_dribbles / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Dribbles " + str(timet))

                        elif detail == "Possession loss":
                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].unsuccessful_touches = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].total_dispossessed = clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t'))

                                player_team[name].unsuccessful_touches_per90 = player_team[name].unsuccessful_touches / (player_team[name].minutes_played / 90.0)
                                player_team[name].total_dispossessed_per_90 = player_team[name].total_dispossessed / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Possession loss " + str(timet))

                        elif detail == "Aerial":

                            startt = time.time()

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].total_aerial_duels = clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].total_aerials_duels_won = clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t'))
                                player_team[name].aerial_duels_lost = clean_float(player_row.find_elements_by_tag_name("td")[
                                    9].get_attribute(
                                    "innerHTML").strip('\t'))

                                player_team[name].total_aerial_duels_per_90 = player_team[name].total_aerial_duels / (player_team[name].minutes_played / 90.0)
                                player_team[name].total_aerials_duels_won_per_90 = player_team[name].total_aerials_duels_won / (player_team[name].minutes_played / 90.0)
                                player_team[name].aerial_duels_lost_per_90 = player_team[name].aerial_duels_lost / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Aerial " + str(timet))

                        elif detail == "Passes":
                            # subcategories
                            print("======")
                            print("Passes")
                            print("======")
                            startt = time.time()
                            pass_list = [x.text for x in
                                         browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                            print("Len pass_list: " + str(len(pass_list)))
                            for pass_detail in pass_list:

                                Select(browser.find_element_by_id('subcategory')).select_by_visible_text(pass_detail)

                                time.sleep(3)

                                player_pass_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                    .find_elements_by_tag_name('tr')

                                time.sleep(1)
                                print("Len player_pass_detailed: " + str(len(player_pass_detailed)))
                                for player_row in player_pass_detailed:
                                    name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                    # index = search_player_in_list(name, player_team)
                                    if pass_detail == "Length":

                                        player_team[name].total_passes = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            7].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].accurate_long_balls = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].inaccurate_long_balls = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].accurate_short_passes = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                            "innerHTML").strip('\t'))
                                        player_team[name].inaccurate_short_passes = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                                "innerHTML").strip('\t'))

                                        player_team[name].total_passes_per_90 = player_team[name].total_passes / (player_team[name].minutes_played / 90.0)
                                        player_team[name].accurate_long_balls_per_90 = player_team[name].accurate_long_balls / (player_team[name].minutes_played / 90.0)
                                        player_team[name].inaccurate_long_balls_per_90 = player_team[name].inaccurate_long_balls / (player_team[name].minutes_played / 90.0)
                                        player_team[name].accurate_short_passes_per_90 = player_team[name].accurate_short_passes / (player_team[name].minutes_played / 90.0)
                                        player_team[name].inaccurate_short_passes_per_90 = player_team[name].inaccurate_short_passes / (player_team[name].minutes_played / 90.0)

                                    elif pass_detail == "Type":

                                        player_team[name].accurate_cross_passes = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                7].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].inaccurate_cross_passes = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                8].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].accurate_corner_passes = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                9].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].inaccurate_corner_passes = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                10].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].accurate_freekicks = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                11].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].inaccurate_freekicks = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                12].get_attribute(
                                                "innerHTML").strip('\t'))

                                        player_team[name].accurate_cross_passes_per_90 = player_team[name].accurate_cross_passes / (player_team[name].minutes_played / 90.0)
                                        player_team[name].inaccurate_cross_passes_per_90 = player_team[name].inaccurate_cross_passes / (player_team[name].minutes_played / 90.0)
                                        player_team[name].accurate_corner_passes_per_90 = player_team[name].accurate_corner_passes / (player_team[name].minutes_played / 90.0)
                                        player_team[name].inaccurate_corner_passes_per_90 = player_team[name].inaccurate_corner_passes / (player_team[name].minutes_played / 90.0)
                                        player_team[name].accurate_freekicks_per_90 = player_team[name].accurate_freekicks / (player_team[name].minutes_played / 90.0)
                                        player_team[name].inaccurate_freekicks_per_90 = player_team[name].inaccurate_freekicks / (player_team[name].minutes_played / 90.0)

                                finish = time.time()
                                timet = finish - startt
                                print("Passes " + str(timet))

                        elif detail == "Key passes":
                            print("======")
                            print("Key Passes")
                            print("======")
                            startt = time.time()
                            key_pass_list = [x.text for x in
                                         browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                            print("Len key_pass_list: " + str(len(key_pass_list)))
                            for key_pass_detail in key_pass_list:
                                Select(browser.find_element_by_id('subcategory')).select_by_visible_text(key_pass_detail)

                                time.sleep(3)

                                player_key_pass_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                    .find_elements_by_tag_name('tr')

                                for player_row in player_key_pass_detailed:
                                    name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                    # index = search_player_in_list(name, player_team)
                                    if key_pass_detail == "Length":

                                        player_team[name].total_key_pass = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                7].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].long_key_pass = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                8].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].short_key_pass = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                9].get_attribute(
                                                "innerHTML").strip('\t'))

                                        player_team[name].total_key_pass_per_90 = player_team[name].total_key_pass / (player_team[name].minutes_played / 90.0)
                                        player_team[name].long_key_pass_per_90 = player_team[name].long_key_pass / (player_team[name].minutes_played / 90.0)
                                        player_team[name].short_key_pass_per_90 = player_team[name].short_key_pass / (player_team[name].minutes_played / 90.0)

                                    elif key_pass_detail == "Type":

                                        player_team[name].key_pass_cross = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                7].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].key_pass_corner = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                8].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].key_pass_throughball = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                9].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].key_pass_freekick = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                10].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].key_pass_throwin = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                11].get_attribute(
                                                "innerHTML").strip('\t'))
                                        player_team[name].key_passes_others = \
                                            clean_float(player_row.find_elements_by_tag_name("td")[
                                                12].get_attribute(
                                                "innerHTML").strip('\t'))

                                        player_team[name].key_pass_cross_per_90 = player_team[name].key_pass_cross / (player_team[name].minutes_played / 90.0)
                                        player_team[name].key_pass_corner_per_90 = player_team[name].key_pass_corner / (player_team[name].minutes_played / 90.0)
                                        player_team[name].key_pass_throughball_per_90 = player_team[name].key_pass_throughball / (player_team[name].minutes_played / 90.0)
                                        player_team[name].key_pass_freekick_per_90 = player_team[name].key_pass_freekick / (player_team[name].minutes_played / 90.0)
                                        player_team[name].key_pass_throwin_per_90 = player_team[name].key_pass_throwin / (player_team[name].minutes_played / 90.0)
                                        player_team[name].key_passes_others_per_90 = player_team[name].key_passes_others / (player_team[name].minutes_played / 90.0)

                                finish = time.time()
                                timet = finish - startt
                                print("Key Passes " + str(timet))

                        elif detail == "Assists":

                            startt = time.time()
                            player_key_pass_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                .find_elements_by_tag_name('tr')

                            for player_row in player_list_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                player_team[name].cross_assist = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        7].get_attribute(
                                        "innerHTML").strip('\t'))
                                player_team[name].corner_assist = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                player_team[name].throughball_assist = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                player_team[name].freeckick_assist = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        10].get_attribute(
                                        "innerHTML").strip('\t'))
                                player_team[name].throw_in_assist = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        11].get_attribute(
                                        "innerHTML").strip('\t'))
                                player_team[name].other_assist = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        12].get_attribute(
                                        "innerHTML").strip('\t'))
                                player_team[name].total_assist_per_game = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        13].get_attribute(
                                        "innerHTML").strip('\t'))

                                player_team[name].cross_assist_per_90 = player_team[name].cross_assist / (player_team[name].minutes_played / 90.0)
                                player_team[name].corner_assist_per_90 = player_team[name].corner_assist / (player_team[name].minutes_played / 90.0)
                                player_team[name].throughball_assist_per_90 = player_team[name].throughball_assist / (player_team[name].minutes_played / 90.0)
                                player_team[name].freeckick_assist_per_90 = player_team[name].freeckick_assist / (player_team[name].minutes_played / 90.0)
                                player_team[name].throw_in_assist_per_90 = player_team[name].throw_in_assist / (player_team[name].minutes_played / 90.0)
                                player_team[name].other_assist_per_90 = player_team[name].other_assist / (player_team[name].minutes_played / 90.0)
                                player_team[name].total_assist_per_game_per_90 = player_team[name].total_assist_per_game / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Assists " + str(timet))

                    done = time.time()
                    elapsed = done - start
                    print("Detail: " + str(elapsed))

                    for idx, player in enumerate(list(player_team)):
                        write = '{0}'.format(
                            json.dumps(player_team[player].__dict__, indent=4, separators=(',', ': ')))

                        if idx == 0:
                            write = "[" + write + ","
                        elif idx == (len(list(player_team)) - 1):
                            write = write + "]"
                        else:
                            write = write + ","

                        players_file.write(write)

                    players_file.close()

        else:
            url = url.replace('Show', 'Archive')
            site = '{}{}'.format(constants_whoscored.WHOSCORED_URL, url)
            print(site)
            browser.get(site)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            options = soup.find('div', {'id': 'past-seasons'})
            option_list = options.find_all('option')

            season_list = [x.text for x in
                         browser.find_element_by_id('past-seasons').find_elements_by_tag_name("option")]
            new_season_list = []
            not_new_seasons = []
            print("Len Seasons: " + str(len(season_list)))
            for season in season_list:
                split_season = season.split('-')[1].split(' ')[1].split('/')[0]
                if split_season == constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]:
                    new_season_list.append(season)
                else:
                    not_new_seasons.append(season)
            print("Len New Seasons: " + str(len(new_season_list)))
            for competition in new_season_list:
                print("+++++++++")
                print(competition)
                print("+++++++++")
                #while (Select(browser.find_element_by_id('club_id')).first_selected_option.text != team_name) and (Select(browser.find_element_by_id('club_id')).first_selected_option.text != team_name + " (Current)"):
                Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                page = browser.page_source

                time.sleep(5)

                directory = 'data/%s/%s/' % (
                    constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX], constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
                pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
                players_file_name = directory + '%s- -%s - Players-%s.json' % (
                    team_name, competition.split('-')[0],
                    constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
                players_file = open(players_file_name, 'w')

                soup = BeautifulSoup(browser.page_source, "html.parser")

                player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')

                if player_list[0].text == 'There are no results to display':
                    try:
                        Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                        time.sleep(5)
                        Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                        page = browser.page_source
                        soup = BeautifulSoup(page, "html.parser")
                        player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')
                    except:
                        restart_team = browser.find_element_by_class_name('team-profile-side-box').find_element_by_class_name('team-link')
                        actions = ActionChains(browser)
                        actions.move_to_element(restart_team)
                        actions.click(restart_team)
                        actions.perform()
                        time.sleep(3)
                        history_button = browser.find_element_by_id('sub-navigation').find_elements_by_tag_name('li')[4]
                        actions = ActionChains(browser)
                        actions.move_to_element(history_button)
                        actions.click(history_button)
                        actions.perform()
                        time.sleep(5)
                        soup = BeautifulSoup(browser.page_source, "html.parser")
                        player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')

                player_team = {}
                start = time.time()
                print("Len Player List: " + str(len(player_list)))
                for player_row in player_list:
                    new_player = whoscored_models.Player()
                    new_player.name = player_row.find('a', {'class': 'player-link'}).text
                    new_player.name = new_player.name[:len(new_player.name)-1]
                    new_player.url = player_row.find('a', {'class': 'player-link'})['href']
                    new_player.id = new_player.url.split('/')[2]
                    new_player.nationality = player_row.find_all('td')[1].find('span')['class'][2].split('-')[1]
                    new_player.season = int(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
                    new_player.birth = int(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]) - int(player_row.find('td', {'class': 'pn'}).find_all('span', {'class': 'player-meta-data'})[0].text)
                    new_player.team = player_row.find('td', {'class': 'pn'}).find('a', {'class': 'player-meta-data'}).text.split(',')[0]
                    new_player.position = player_row.find('td', {'class': 'pn'}).find_all('span', {'class': 'player-meta-data'})[1].text.split(' ')[2]
                    new_player.height = clean_float(player_row.find_all("td")[3].text)
                    new_player.weight = clean_float(player_row.find_all("td")[4].text)
                    new_player.appearances = player_row.find_all("td")[5].text
                    new_player.minutes_played = clean_float(player_row.find_all("td")[6].text.strip('\t'))
                    new_player.goals = clean_float(player_row.find_all("td")[7].text.strip('\t'))
                    new_player.assists = clean_float(player_row.find_all("td")[8].text.strip('\t'))
                    new_player.yellow_cards = clean_float(player_row.find_all("td")[9].text.strip('\t'))
                    new_player.red_cards = clean_float(player_row.find_all("td")[10].text.strip('\t'))
                    new_player.shots_per_game = clean_float(player_row.find_all("td")[11].text.strip('\t'))
                    new_player.pass_success_percentage = clean_float(player_row.find_all("td")[12].text.strip('\t'))
                    new_player.aerials_duels_won_per_game = clean_float(player_row.find_all("td")[13].text.strip('\t'))
                    new_player.man_of_the_match = clean_float(player_row.find_all("td")[14].text.strip('\t'))
                    new_player.rating = clean_float(player_row.find_all("td")[15].text.strip('\t'))
                    new_player.competition = competition.split('-')[0]
                    player_team[new_player.name] = new_player

                #press defensive button

                defensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[0]
                actions = ActionChains(browser)
                actions.move_to_element(defensive_button)
                actions.click(defensive_button)
                actions.perform()

                time.sleep(7)

                player_list_defensive = browser.find_elements_by_id("player-table-statistics-body")[1].find_elements_by_tag_name('tr')
                done = time.time()
                elapsed = done - start
                start = time.time()
                print("Summary: " + str(elapsed))
                if player_list_defensive[0].get_attribute("innerText") == 'There are no results to display':
                    try:
                        print("First crash")
                        Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                        time.sleep(5)
                        Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                    except:
                        print("CRASH")
                        restart_team = browser.find_element_by_class_name(
                            'team-profile-side-box').find_element_by_class_name('team-link')
                        actions = ActionChains(browser)
                        actions.move_to_element(restart_team)
                        actions.click(restart_team)
                        actions.perform()
                        time.sleep(3)
                        history_button = browser.find_element_by_id('sub-navigation').find_elements_by_tag_name('li')[4]
                        actions = ActionChains(browser)
                        actions.move_to_element(history_button)
                        actions.click(history_button)
                        actions.perform()
                        time.sleep(1)

                        defensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[0]
                        actions = ActionChains(browser)
                        actions.move_to_element(defensive_button)
                        actions.click(defensive_button)
                        actions.perform()
                        time.sleep(5)
                        player_list_defensive = browser.find_elements_by_id("player-table-statistics-body")[
                            1].find_elements_by_tag_name('tr')

                for player_row in player_list_defensive:
                    name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                    # index = search_player_in_list(name, player_team)
                    player_team[name].tackles_per_game = clean_float(player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t'))
                    player_team[name].interceptions_per_game = clean_float(player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t'))
                    player_team[name].fouls_per_game = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t'))
                    player_team[name].offside_won_per_game = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t'))
                    player_team[name].clarances_per_game = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t'))
                    player_team[name].dribbled_past_per_game = clean_float(player_row.find_elements_by_tag_name("td")[12].get_attribute("innerHTML").strip('\t'))
                    player_team[name].outfielder = clean_float(player_row.find_elements_by_tag_name("td")[13].get_attribute("innerHTML").strip('\t'))
                    player_team[name].own_goals = clean_float(player_row.find_elements_by_tag_name("td")[14].get_attribute("innerHTML").strip('\t'))

                offensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[1]
                actions = ActionChains(browser)
                actions.move_to_element(offensive_button)
                actions.click(offensive_button)
                actions.perform()
                done = time.time()
                elapsed = done - start
                start = time.time()
                print("Defensive: " + str(elapsed))

                time.sleep(2)
                player_list_offensive = browser.find_elements_by_id("player-table-statistics-body")[2]\
                    .find_elements_by_tag_name('tr')

                if player_list_offensive[0].get_attribute("innerText") == 'There are no results to display':
                    try:
                        Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                        time.sleep(5)
                        Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                    except:
                        restart_team = browser.find_element_by_class_name(
                            'team-profile-side-box').find_element_by_class_name('team-link')
                        actions = ActionChains(browser)
                        actions.move_to_element(restart_team)
                        actions.click(restart_team)
                        actions.perform()
                        time.sleep(2)
                        history_button = browser.find_element_by_id('sub-navigation').find_elements_by_tag_name('li')[4]
                        actions = ActionChains(browser)
                        actions.move_to_element(history_button)
                        actions.click(history_button)
                        time.sleep(2)
                        actions.perform()
                        offensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[1]
                        actions = ActionChains(browser)
                        actions.move_to_element(offensive_button)
                        actions.click(offensive_button)
                        actions.perform()
                        time.sleep(2)
                        player_list_offensive = browser.find_elements_by_id("player-table-statistics-body")[2] \
                            .find_elements_by_tag_name('tr')

                for player_row in player_list_offensive:
                    name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                    # index = search_player_in_list(name, player_team)
                    player_team[name].key_passes_per_game = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].dribbles_per_game = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].fouled_per_game = clean_float(player_row.find_elements_by_tag_name("td")[12].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].offsides_per_game = clean_float(player_row.find_elements_by_tag_name("td")[13].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].dispossessed_per_game = clean_float(player_row.find_elements_by_tag_name("td")[14].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].bad_control_per_game = clean_float(player_row.find_elements_by_tag_name("td")[
                        15].get_attribute("innerHTML").strip('\t'))

                passing_button = browser.find_elements_by_class_name('in-squad-detailed-view')[2]
                actions = ActionChains(browser)
                actions.move_to_element(passing_button)
                actions.click(passing_button)
                actions.perform()

                time.sleep(2)

                done = time.time()
                elapsed = done - start
                start = time.time()
                print("Ofensive: " + str(elapsed))

                player_list_passing = browser.find_elements_by_id("player-table-statistics-body")[3] \
                    .find_elements_by_tag_name('tr')

                if player_list_passing[0].get_attribute("innerText") == 'There are no results to display':
                    Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                    time.sleep(5)
                    Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                    player_list_passing = browser.find_elements_by_id("player-table-statistics-body")[3] \
                        .find_elements_by_tag_name('tr')

                for player_row in player_list_passing:
                    name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                    # index = search_player_in_list(name, player_team)
                    player_team[name].average_passes_per_game = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].pass_success_percentage = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].crosses_per_game = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].long_balls_per_game = clean_float(player_row.find_elements_by_tag_name("td")[12].get_attribute(
                        "innerHTML").strip('\t'))
                    player_team[name].through_balls_per_game = clean_float(player_row.find_elements_by_tag_name("td")[13].get_attribute(
                        "innerHTML").strip('\t'))

                detailed_button = browser.find_elements_by_class_name('in-squad-detailed-view')[3]
                actions = ActionChains(browser)
                actions.move_to_element(detailed_button)
                actions.click(detailed_button)
                actions.perform()

                time.sleep(2)

                done = time.time()
                elapsed = done - start
                start = time.time()
                print("Passing: " + str(elapsed))

                Select(browser.find_element_by_id('statsAccumulationType')).select_by_value("2")

                time.sleep(2)

                detail_list = [x.text for x in
                             browser.find_element_by_id('category').find_elements_by_tag_name("option")]

                for detail in detail_list:
                    Select(browser.find_element_by_id('category')).select_by_visible_text(detail)

                    time.sleep(3)

                    player_list_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                        .find_elements_by_tag_name('tr')

                    if player_list_detailed[0].get_attribute("innerText") == 'There are no results to display':
                        print("No Display")
                        try:
                            Select(browser.find_element_by_id('category')).select_by_visible_text(not_new_seasons[0])
                            time.sleep(5)
                            Select(browser.find_element_by_id('category')).select_by_visible_text(detail)
                        except:
                            print("CRASH")
                            restart_team = browser.find_element_by_class_name(
                                'team-profile-side-box').find_element_by_class_name('team-link')
                            actions = ActionChains(browser)
                            actions.move_to_element(restart_team)
                            actions.click(restart_team)
                            actions.perform()
                            time.sleep(3)
                            history_button = browser.find_element_by_id('sub-navigation').find_elements_by_tag_name('li')[4]
                            actions = ActionChains(browser)
                            actions.move_to_element(history_button)
                            actions.click(history_button)
                            actions.perform()
                            time.sleep(1)

                            detailed_button = browser.find_elements_by_class_name('in-squad-detailed-view')[3]
                            actions = ActionChains(browser)
                            actions.move_to_element(detailed_button)
                            actions.click(detailed_button)
                            actions.perform()

                            time.sleep(1)

                            Select(browser.find_element_by_id('category')).select_by_visible_text(detail)

                            time.sleep(5)

                            player_list_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                .find_elements_by_tag_name('tr')

                    if detail == "Tackles":
                        startt = time.time()


                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].total_tackles_won = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute("innerText").strip('\t'))
                            player_team[name].player_gets_dribbled = clean_float(player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerText").strip('\t'))
                            player_team[name].total_tackle_attempts = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute(
                                "innerText").strip('\t'))
                            player_team[name].total_tackles_won_per90 = player_team[name].total_tackles_won / (player_team[name].minutes_played / 90.0)
                            player_team[name].player_gets_dribbled_per90 = player_team[name].player_gets_dribbled / (player_team[name].minutes_played / 90.0)
                            player_team[name].total_tackle_attempts_per90 = player_team[name].total_tackle_attempts / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Tackles " + str(timet))

                    elif detail == "Interception":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].interceptions = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerText").strip('\t'))
                            player_team[name].interceptions_per90 = player_team[name].interceptions /player_team[name].minutes_played
                        finish = time.time()
                        timet = finish - startt
                        print("Interception " + str(timet))

                    elif detail == "Fouls":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].fouled = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].fouls = clean_float(player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].fouled_per90 = player_team[name].fouled /player_team[name].minutes_played
                            player_team[name].fouls_per90 = player_team[name].fouls /player_team[name].minutes_played

                        finish = time.time()
                        timet = finish - startt
                        print("Fouls " + str(timet))

                    elif detail == "Cards":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].total_yellow_cards = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].total_red_cards = clean_float(player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerHTML").strip('\t'))

                            player_team[name].total_yellow_cards_per90 = player_team[name].total_yellow_cards / (player_team[name].minutes_played / 90.0)
                            player_team[name].total_red_cards_per90 = player_team[name].total_red_cards / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Cards " + str(timet))

                    elif detail == "Offsides":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].caught_offside = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))

                            player_team[name].caught_offside_per90 = player_team[name].caught_offside / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Offsides " + str(timet))

                    elif detail == "Clearances":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].total_clearances = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].total_clearances_per90 = player_team[name].total_clearances / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Clearances " + str(timet))

                    elif detail == "Blocks":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].blocked_shots = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].blocked_crosses = clean_float(player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].blocked_passes = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute(
                                "innerHTML").strip('\t'))

                            player_team[name].blocked_shots_per90 = player_team[name].blocked_shots / (player_team[name].minutes_played / 90.0)
                            player_team[name].blocked_crosses_per90 = player_team[name].blocked_crosses / (player_team[name].minutes_played / 90.0)
                            player_team[name].blocked_passes_per90 = player_team[name].blocked_passes / (player_team[name].minutes_played / 90.0)
                        finish = time.time()
                        timet = finish - startt
                        print("Blocks " + str(timet))

                    elif detail == "Saves":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].gk_totalsaves = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].gk_saves_insix_yard_box = clean_float(player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].gk_saves_in_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[9].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].gk_saves_from_outside_of_the_box = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                "innerHTML").strip('\t'))

                            player_team[name].gk_totalsaves_per90 = player_team[name].gk_totalsaves / (player_team[name].minutes_played / 90.0)
                            player_team[name].gk_saves_insix_yard_box_per90 = player_team[name].gk_saves_insix_yard_box / (player_team[name].minutes_played / 90.0)
                            player_team[name].gk_saves_in_penalty_area_per90 = player_team[name].gk_saves_in_penalty_area / (player_team[name].minutes_played / 90.0)
                            player_team[name].gk_saves_from_outside_of_the_box_per90 = player_team[name].gk_saves_from_outside_of_the_box / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Saves " + str(timet))

                    elif detail == "Shots":
                        print("======")
                        print("Shots")
                        print("======")
                        startt = time.time()
                        shot_list = [x.text for x in
                                       browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                        print("Len Shot List: " + str(len(shot_list)))
                        for shot_detail in shot_list:
                            Select(browser.find_element_by_id('subcategory')).select_by_visible_text(shot_detail)

                            time.sleep(3)

                            player_shot_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                .find_elements_by_tag_name('tr')

                            print("Len player_shot_detailed: " + str(len(player_shot_detailed)))
                            for player_row in player_shot_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                if shot_detail == "Zones":
                                    player_team[name].total_shots = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        7].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shots_from_outside_the_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shots_from_inside_thesix_yard_box = clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shots_from_inside_the_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t'))

                                    player_team[name].total_shots_per90 = player_team[name].total_shots / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shots_from_outside_the_penalty_area_per90 = player_team[name].shots_from_outside_the_penalty_area / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shots_from_inside_thesix_yard_box_per90 = player_team[name].shots_from_inside_thesix_yard_box / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shots_from_inside_the_penalty_area_per90 = player_team[name].shots_from_inside_the_penalty_area / (player_team[name].minutes_played / 90.0)


                                elif shot_detail == "Situations":
                                    player_team[name].shot_open_play = clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_counter = clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_setpiece = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_penalty_taken = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                        "innerHTML").strip('\t'))

                                    player_team[name].shot_open_play_per90 = player_team[name].shot_open_play / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_counter_per90 = player_team[name].shot_counter / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_setpiece_per90 = player_team[name].shot_setpiece / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_penalty_taken_per90 = player_team[name].shot_penalty_taken / (player_team[name].minutes_played / 90.0)


                                elif shot_detail == "Accuracy":
                                    player_team[name].shot_offtarget = clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_onpost = clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_ontarget = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_blocked = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                        "innerHTML").strip('\t'))

                                    player_team[name].shot_offtarget_per90 = player_team[name].shot_offtarget / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_onpost_per90 = player_team[name].shot_onpost / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_ontarget_per90 = player_team[name].shot_ontarget / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_blocked_per90 = player_team[name].shot_blocked / (player_team[name].minutes_played / 90.0)

                                elif shot_detail == "Body Parts":
                                    player_team[name].shot_right_foot = clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_left_foot = clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_head = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].shot_other = clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                        "innerHTML").strip('\t'))

                                    player_team[name].shot_right_foot_per90 = player_team[name].shot_right_foot / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_left_foot_per90 = player_team[name].shot_left_foot / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_head_per90 = player_team[name].shot_head / (player_team[name].minutes_played / 90.0)
                                    player_team[name].shot_other_per90 = player_team[name].shot_other / (player_team[name].minutes_played / 90.0)


                            finish = time.time()
                            timet = finish - startt
                            print("Shots " + str(timet))

                    elif detail == "Goals":
                        # subcategories
                        print("======")
                        print("Goals")
                        print("======")
                        startt = time.time()
                        goal_list = [x.text for x in
                                     browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                        print("Len goal_list: " + str(len(goal_list)))
                        for goal_detail in goal_list:

                            Select(browser.find_element_by_id('subcategory')).select_by_visible_text(goal_detail)

                            time.sleep(3)

                            player_goal_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                .find_elements_by_tag_name('tr')

                            print("Len player_goal_detailed: " + str(len(player_goal_detailed)))
                            for player_row in player_goal_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                if goal_detail == "Zones":
                                    player_team[name].total_goal = clean_float(player_row.find_elements_by_tag_name("td")[
                                        7].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goals_from_inside_thesix_yard_box = clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goals_from_inside_the_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goals_from_outside_the_penalty_area = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t'))

                                    player_team[name].total_goal_per90 = player_team[name].total_goal / (player_team[name].minutes_played / 90.0)
                                    player_team[name].goals_from_inside_thesix_yard_box_per90 = player_team[name].goals_from_inside_thesix_yard_box / (player_team[name].minutes_played / 90.0)
                                    player_team[name].goals_from_inside_the_penalty_area_per90 = player_team[name].goals_from_inside_the_penalty_area / (player_team[name].minutes_played / 90.0)
                                    player_team[name].goals_from_outside_the_penalty_area_per90 = player_team[name].goals_from_outside_the_penalty_area / (player_team[name].minutes_played / 90.0)

                                elif goal_detail == "Situations":
                                    player_team[name].goal_open_play = clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goal_counter = clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goal_setpiece = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goal_penaltyscored = clean_float(player_row.find_elements_by_tag_name("td")[
                                        11].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goal_own = clean_float(player_row.find_elements_by_tag_name("td")[
                                        12].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goal_normal = clean_float(player_row.find_elements_by_tag_name("td")[13].get_attribute(
                                        "innerHTML").strip('\t'))

                                    player_team[name].goal_open_play_per90 = player_team[name].goal_open_play/ (player_team[name].minutes_played / 90.0)
                                    player_team[name].goal_counter_per90 = player_team[name].goal_counter/ (player_team[name].minutes_played / 90.0)
                                    player_team[name].goal_setpiece_per90 = player_team[name].goal_setpiece/ (player_team[name].minutes_played / 90.0)
                                    player_team[name].goal_penaltyscored_per90 = player_team[name].goal_penaltyscored/ (player_team[name].minutes_played / 90.0)
                                    player_team[name].goal_own_per90 = player_team[name].goal_own/ (player_team[name].minutes_played / 90.0)
                                    player_team[name].goal_normal_per90 = player_team[name].goal_normal/ (player_team[name].minutes_played / 90.0)

                                elif goal_detail == "Body Parts":
                                    player_team[name].goal_right_foot = clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goal_left_foot = clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goal_head = clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].goal_other = clean_float(player_row.find_elements_by_tag_name("td")[
                                        11].get_attribute(
                                        "innerHTML").strip('\t'))

                                    player_team[name].goal_right_foot_per90 = player_team[name].goal_right_foot / (player_team[name].minutes_played / 90.0)
                                    player_team[name].goal_left_foot_per90 = player_team[name].goal_left_foot / (player_team[name].minutes_played / 90.0)
                                    player_team[name].goal_head_per90 = player_team[name].goal_head / (player_team[name].minutes_played / 90.0)
                                    player_team[name].goal_other_per90 = player_team[name].goal_other / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Goals: " + str(timet))

                    elif detail == "Dribbles":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].unsuccessful_dribbles = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].successful_dribbles = clean_float(player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].total_dribbles = clean_float(player_row.find_elements_by_tag_name("td")[
                                9].get_attribute(
                                "innerHTML").strip('\t'))

                            player_team[name].unsuccessful_dribbles_per90 = player_team[name].unsuccessful_dribbles / (player_team[name].minutes_played / 90.0)
                            player_team[name].successful_dribbles_per90 = player_team[name].successful_dribbles / (player_team[name].minutes_played / 90.0)
                            player_team[name].total_dribbles_per90 = player_team[name].total_dribbles / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Dribbles " + str(timet))

                    elif detail == "Possession loss":
                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].unsuccessful_touches = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].total_dispossessed = clean_float(player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerHTML").strip('\t'))

                            player_team[name].unsuccessful_touches_per90 = player_team[name].unsuccessful_touches / (player_team[name].minutes_played / 90.0)
                            player_team[name].total_dispossessed_per_90 = player_team[name].total_dispossessed / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Possession loss " + str(timet))

                    elif detail == "Aerial":

                        startt = time.time()

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].total_aerial_duels = clean_float(player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].total_aerials_duels_won = clean_float(player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerHTML").strip('\t'))
                            player_team[name].aerial_duels_lost = clean_float(player_row.find_elements_by_tag_name("td")[
                                9].get_attribute(
                                "innerHTML").strip('\t'))

                            player_team[name].total_aerial_duels_per_90 = player_team[name].total_aerial_duels / (player_team[name].minutes_played / 90.0)
                            player_team[name].total_aerials_duels_won_per_90 = player_team[name].total_aerials_duels_won / (player_team[name].minutes_played / 90.0)
                            player_team[name].aerial_duels_lost_per_90 = player_team[name].aerial_duels_lost / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Aerial " + str(timet))

                    elif detail == "Passes":
                        # subcategories
                        print("======")
                        print("Passes")
                        print("======")
                        startt = time.time()
                        pass_list = [x.text for x in
                                     browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                        print("Len pass_list: " + str(len(pass_list)))
                        for pass_detail in pass_list:

                            Select(browser.find_element_by_id('subcategory')).select_by_visible_text(pass_detail)

                            time.sleep(3)

                            player_pass_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                .find_elements_by_tag_name('tr')

                            time.sleep(1)
                            print("Len player_pass_detailed: " + str(len(player_pass_detailed)))
                            for player_row in player_pass_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                if pass_detail == "Length":

                                    player_team[name].total_passes = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        7].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].accurate_long_balls = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].inaccurate_long_balls = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].accurate_short_passes = \
                                    clean_float(player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t'))
                                    player_team[name].inaccurate_short_passes = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                            "innerHTML").strip('\t'))

                                    player_team[name].total_passes_per_90 = player_team[name].total_passes / (player_team[name].minutes_played / 90.0)
                                    player_team[name].accurate_long_balls_per_90 = player_team[name].accurate_long_balls / (player_team[name].minutes_played / 90.0)
                                    player_team[name].inaccurate_long_balls_per_90 = player_team[name].inaccurate_long_balls / (player_team[name].minutes_played / 90.0)
                                    player_team[name].accurate_short_passes_per_90 = player_team[name].accurate_short_passes / (player_team[name].minutes_played / 90.0)
                                    player_team[name].inaccurate_short_passes_per_90 = player_team[name].inaccurate_short_passes / (player_team[name].minutes_played / 90.0)

                                elif pass_detail == "Type":

                                    player_team[name].accurate_cross_passes = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            7].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].inaccurate_cross_passes = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].accurate_corner_passes = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].inaccurate_corner_passes = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            10].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].accurate_freekicks = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            11].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].inaccurate_freekicks = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            12].get_attribute(
                                            "innerHTML").strip('\t'))

                                    player_team[name].accurate_cross_passes_per_90 = player_team[name].accurate_cross_passes / (player_team[name].minutes_played / 90.0)
                                    player_team[name].inaccurate_cross_passes_per_90 = player_team[name].inaccurate_cross_passes / (player_team[name].minutes_played / 90.0)
                                    player_team[name].accurate_corner_passes_per_90 = player_team[name].accurate_corner_passes / (player_team[name].minutes_played / 90.0)
                                    player_team[name].inaccurate_corner_passes_per_90 = player_team[name].inaccurate_corner_passes / (player_team[name].minutes_played / 90.0)
                                    player_team[name].accurate_freekicks_per_90 = player_team[name].accurate_freekicks / (player_team[name].minutes_played / 90.0)
                                    player_team[name].inaccurate_freekicks_per_90 = player_team[name].inaccurate_freekicks / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Passes " + str(timet))

                    elif detail == "Key passes":
                        print("======")
                        print("Key Passes")
                        print("======")
                        startt = time.time()
                        key_pass_list = [x.text for x in
                                     browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                        print("Len key_pass_list: " + str(len(key_pass_list)))
                        for key_pass_detail in key_pass_list:
                            Select(browser.find_element_by_id('subcategory')).select_by_visible_text(key_pass_detail)

                            time.sleep(3)

                            player_key_pass_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                .find_elements_by_tag_name('tr')

                            for player_row in player_key_pass_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                                # index = search_player_in_list(name, player_team)
                                if key_pass_detail == "Length":

                                    player_team[name].total_key_pass = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            7].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].long_key_pass = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].short_key_pass = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))

                                    player_team[name].total_key_pass_per_90 = player_team[name].total_key_pass / (player_team[name].minutes_played / 90.0)
                                    player_team[name].long_key_pass_per_90 = player_team[name].long_key_pass / (player_team[name].minutes_played / 90.0)
                                    player_team[name].short_key_pass_per_90 = player_team[name].short_key_pass / (player_team[name].minutes_played / 90.0)

                                elif key_pass_detail == "Type":

                                    player_team[name].key_pass_cross = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            7].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].key_pass_corner = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            8].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].key_pass_throughball = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            9].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].key_pass_freekick = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            10].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].key_pass_throwin = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            11].get_attribute(
                                            "innerHTML").strip('\t'))
                                    player_team[name].key_passes_others = \
                                        clean_float(player_row.find_elements_by_tag_name("td")[
                                            12].get_attribute(
                                            "innerHTML").strip('\t'))

                                    player_team[name].key_pass_cross_per_90 = player_team[name].key_pass_cross / (player_team[name].minutes_played / 90.0)
                                    player_team[name].key_pass_corner_per_90 = player_team[name].key_pass_corner / (player_team[name].minutes_played / 90.0)
                                    player_team[name].key_pass_throughball_per_90 = player_team[name].key_pass_throughball / (player_team[name].minutes_played / 90.0)
                                    player_team[name].key_pass_freekick_per_90 = player_team[name].key_pass_freekick / (player_team[name].minutes_played / 90.0)
                                    player_team[name].key_pass_throwin_per_90 = player_team[name].key_pass_throwin / (player_team[name].minutes_played / 90.0)
                                    player_team[name].key_passes_others_per_90 = player_team[name].key_passes_others / (player_team[name].minutes_played / 90.0)

                            finish = time.time()
                            timet = finish - startt
                            print("Key Passes " + str(timet))

                    elif detail == "Assists":

                        startt = time.time()
                        player_key_pass_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                            .find_elements_by_tag_name('tr')

                        for player_row in player_list_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")

                            # index = search_player_in_list(name, player_team)
                            player_team[name].cross_assist = \
                                clean_float(player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t'))
                            player_team[name].corner_assist = \
                                clean_float(player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t'))
                            player_team[name].throughball_assist = \
                                clean_float(player_row.find_elements_by_tag_name("td")[
                                    9].get_attribute(
                                    "innerHTML").strip('\t'))
                            player_team[name].freeckick_assist = \
                                clean_float(player_row.find_elements_by_tag_name("td")[
                                    10].get_attribute(
                                    "innerHTML").strip('\t'))
                            player_team[name].throw_in_assist = \
                                clean_float(player_row.find_elements_by_tag_name("td")[
                                    11].get_attribute(
                                    "innerHTML").strip('\t'))
                            player_team[name].other_assist = \
                                clean_float(player_row.find_elements_by_tag_name("td")[
                                    12].get_attribute(
                                    "innerHTML").strip('\t'))
                            player_team[name].total_assist_per_game = \
                                clean_float(player_row.find_elements_by_tag_name("td")[
                                    13].get_attribute(
                                    "innerHTML").strip('\t'))

                            player_team[name].cross_assist_per_90 = player_team[name].cross_assist / (player_team[name].minutes_played / 90.0)
                            player_team[name].corner_assist_per_90 = player_team[name].corner_assist / (player_team[name].minutes_played / 90.0)
                            player_team[name].throughball_assist_per_90 = player_team[name].throughball_assist / (player_team[name].minutes_played / 90.0)
                            player_team[name].freeckick_assist_per_90 = player_team[name].freeckick_assist / (player_team[name].minutes_played / 90.0)
                            player_team[name].throw_in_assist_per_90 = player_team[name].throw_in_assist / (player_team[name].minutes_played / 90.0)
                            player_team[name].other_assist_per_90 = player_team[name].other_assist / (player_team[name].minutes_played / 90.0)
                            player_team[name].total_assist_per_game_per_90 = player_team[name].total_assist_per_game / (player_team[name].minutes_played / 90.0)

                        finish = time.time()
                        timet = finish - startt
                        print("Assists " + str(timet))

                done = time.time()
                elapsed = done - start
                print("Detail: " + str(elapsed))

                for idx, player in enumerate(list(player_team)):
                    write = '{0}'.format(
                        json.dumps(player_team[player].__dict__, indent=4, separators=(',', ': ')))

                    if idx == 0:
                        write = "[" + write + ","
                    elif idx == (len(list(player_team)) - 1):
                        write = write + "]"
                    else:
                        write = write + ","

                    players_file.write(write)

                players_file.close()

