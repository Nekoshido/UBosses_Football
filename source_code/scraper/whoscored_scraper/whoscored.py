from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import chain, zip_longest
import json
import pathlib
import time

from selenium.webdriver.common.action_chains import ActionChains
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

if __name__ == "__main__":
    try:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE, executable_path=settings.EXECUTABLE)
    except Exception:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE)


    site = '{}/Regions/{}/Tournaments/{}/Seasons/{}/{}'.format(constants_whoscored.WHOSCORED_URL,
                                                              constants_whoscored.LEAGUES_ID[constants_whoscored.LEAGUE_INDEX],
                                                            constants_whoscored.LEAGUES_NUM[constants_whoscored.LEAGUE_INDEX],
                                                               constants_whoscored.SEASON_ID[constants_whoscored.LEAGUE_INDEX][constants_whoscored.SEASON_INDEX],
                                                               constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX])
    browser.get(site)
    page = browser.page_source
    time.sleep(5)
    #continue_button = soup.find('a', {'class': 'details_continue--2CnZz'})
    continue_button = browser.find_element_by_class_name('details_continue--2CnZz')
    actions = ActionChains(browser)
    actions.move_to_element(continue_button)
    actions.click(continue_button)
    actions.perform()
    soup = BeautifulSoup(page, "html.parser")
    table_teams = soup.find_all('table', {'class': 'grid with-centered-columns hover'})[0].find('tbody')
    teams = table_teams.find_all('tr')
    for idx, team in enumerate(teams[constants_whoscored.TEAM_INDEX:len(teams)-1]):
        print('Progress:' + str(idx) + ' / ' + str(len(teams)-1))
        url = team.find('a', {'class': 'team-link'}).get('href')
        team_name = team.find('a', {'class': 'team-link '}).text
        if constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX] == constants_whoscored.SEASON_NUMBER[len(constants_whoscored.SEASON_NUMBER)-1]:
            site = '{}{}'.format(constants_whoscored.WHOSCORED_URL, url)
        else:
            url = url.replace('Show', 'Archive')
            site = '{}{}'.format(constants_whoscored.WHOSCORED_URL, url)
        print(site)
        browser.get(site)
        page = browser.page_source
        soup = BeautifulSoup(page, "html.parser")
        options = soup.find('div', {'id': 'past-seasons'})
        option_list = options.find_all('option')

        season_list = [x.text for x in
                     browser.find_element_by_id('past-seasons').find_elements_by_tag_name("option")]
        new_season_list = []
        not_new_seasons = []
        for season in season_list:
            split_season = season.split('-')[1].split(' ')[1].split('/')[0]
            if split_season == constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]:
                new_season_list.append(season)
            else:
                not_new_seasons.append(season)
        for competition in new_season_list:
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

            # play_list_sel = browser.find_elements_by_id('player-table-statistics-body').find_elements_by_tag_name('tr')
            # player_selenium_list = []
            # for player_sel in play_list_sel:
            #     player_selenium_list.append(player_sel.get_attribute("innerText"))
            #
            # print(player_selenium_list)

            soup = BeautifulSoup(page, "html.parser")
            player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')


            if player_list[0].text == 'There are no results to display':
                Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                time.sleep(5)
                Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
            else:
                player_team = []
                for player_row in player_list:
                    new_player = whoscored_models.Player()
                    new_player.name = player_row.find('a', {'class': 'player-link'}).text
                    new_player.name = new_player.name[:len(new_player.name)-1]
                    new_player.season = constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]
                    new_player.birth = int(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]) - int(player_row.find('td', {'class': 'pn'}).find_all('span', {'class': 'player-meta-data'})[0].text)
                    new_player.team = player_row.find('td', {'class': 'pn'}).find('a', {'class': 'player-meta-data'}).text.split(',')[0]
                    new_player.position = player_row.find('td', {'class': 'pn'}).find_all('span', {'class': 'player-meta-data'})[1].text.split(' ')[2]
                    new_player.height = player_row.find_all("td")[3].text
                    new_player.weight = player_row.find_all("td")[4].text
                    new_player.appearances = player_row.find_all("td")[5].text
                    new_player.minutes_played = player_row.find_all("td")[6].text.strip('\t')
                    new_player.goals = player_row.find_all("td")[7].text.strip('\t')
                    new_player.assists = player_row.find_all("td")[8].text.strip('\t')
                    new_player.yellow_cards = player_row.find_all("td")[9].text.strip('\t')
                    new_player.red_cards = player_row.find_all("td")[10].text.strip('\t')
                    new_player.shots_per_game = player_row.find_all("td")[11].text.strip('\t')
                    new_player.pass_success_percentage = player_row.find_all("td")[12].text.strip('\t')
                    new_player.aerials_duels_won_per_game = player_row.find_all("td")[13].text.strip('\t')
                    new_player.man_of_the_match = player_row.find_all("td")[14].text.strip('\t')
                    new_player.rating = player_row.find_all("td")[15].text.strip('\t')
                    new_player.competition = competition
                    player_team.append(new_player)

                #press defensive button

                defensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[0]
                actions = ActionChains(browser)
                actions.move_to_element(defensive_button)
                actions.click(defensive_button)
                actions.perform()

                time.sleep(4)
                player_list_defensive = browser.find_elements_by_id("player-table-statistics-body")[1].find_elements_by_tag_name('tr')

                if player_list_defensive[0].get_attribute("innerText") == 'There are no results to display':
                    Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
                    time.sleep(5)
                    Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)

                    defensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[0]
                    actions = ActionChains(browser)
                    actions.move_to_element(defensive_button)
                    actions.click(defensive_button)
                    actions.perform()
                else:
                    for player_row in player_list_defensive:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].tackles_per_game = player_row.find_elements_by_tag_name("td")[7].get_attribute("innerHTML").strip('\t')
                        player_team[index].interceptions_per_game = player_row.find_elements_by_tag_name("td")[8].get_attribute("innerHTML").strip('\t')
                        player_team[index].fouls_per_game = player_row.find_elements_by_tag_name("td")[9].get_attribute("innerHTML").strip('\t')
                        player_team[index].offside_won_per_game = player_row.find_elements_by_tag_name("td")[10].get_attribute("innerHTML").strip('\t')
                        player_team[index].clarances_per_game = player_row.find_elements_by_tag_name("td")[11].get_attribute("innerHTML").strip('\t')
                        player_team[index].dribbled_past_per_game = player_row.find_elements_by_tag_name("td")[12].get_attribute("innerHTML").strip('\t')
                        player_team[index].outfielder = player_row.find_elements_by_tag_name("td")[13].get_attribute("innerHTML").strip('\t')
                        player_team[index].own_goals = player_row.find_elements_by_tag_name("td")[14].get_attribute("innerHTML").strip('\t')

        offensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[1]
        actions = ActionChains(browser)
        actions.move_to_element(offensive_button)
        actions.click(offensive_button)
        actions.perform()

        time.sleep(2)
        player_list_offensive = browser.find_elements_by_id("player-table-statistics-body")[2]\
            .find_elements_by_tag_name('tr')

        if player_list_offensive[0].get_attribute("innerText") == 'There are no results to display':
            Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
            time.sleep(5)
            Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
        else:
            for player_row in player_list_offensive:
                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                index = search_player_in_list(name, player_team)
                player_team[index].key_passes_per_game = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].dribbles_per_game = player_row.find_elements_by_tag_name("td")[11].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].fouled_per_game = player_row.find_elements_by_tag_name("td")[12].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].offsides_per_game = player_row.find_elements_by_tag_name("td")[13].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].dispossessed_per_game = player_row.find_elements_by_tag_name("td")[14].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].bad_control_per_game = player_row.find_elements_by_tag_name("td")[
                    15].get_attribute("innerHTML").strip('\t')

        passing_button = browser.find_elements_by_class_name('in-squad-detailed-view')[2]
        actions = ActionChains(browser)
        actions.move_to_element(passing_button)
        actions.click(passing_button)
        actions.perform()

        time.sleep(2)

        player_list_passing = browser.find_elements_by_id("player-table-statistics-body")[3] \
            .find_elements_by_tag_name('tr')

        if player_list_passing[0].get_attribute("innerText") == 'There are no results to display':
            Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
            time.sleep(5)
            Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
        else:
            for player_row in player_list_passing:
                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                index = search_player_in_list(name, player_team)
                player_team[index].average_passes_per_game = player_row.find_elements_by_tag_name("td")[9].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].pass_success_percentage = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].crosses_per_game = player_row.find_elements_by_tag_name("td")[11].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].long_balls_per_game = player_row.find_elements_by_tag_name("td")[12].get_attribute(
                    "innerHTML").strip('\t')
                player_team[index].through_balls_per_game = player_row.find_elements_by_tag_name("td")[13].get_attribute(
                    "innerHTML").strip('\t')

        detailed_button = browser.find_elements_by_class_name('in-squad-detailed-view')[3]
        actions = ActionChains(browser)
        actions.move_to_element(detailed_button)
        actions.click(detailed_button)
        actions.perform()

        time.sleep(2)

        Select(browser.find_element_by_id('statsAccumulationType')).select_by_value("1")

        time.sleep(2)

        detail_list = [x.text for x in
                     browser.find_element_by_id('category').find_elements_by_tag_name("option")]

        for detail in detail_list:
            Select(browser.find_element_by_id('category')).select_by_visible_text(detail)

            time.sleep(3)

            player_list_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                .find_elements_by_tag_name('tr')

            if player_list_detailed[0].get_attribute("innerText") == 'There are no results to display':
                Select(browser.find_element_by_id('category')).select_by_visible_text(not_new_seasons[0])
                time.sleep(5)
                Select(browser.find_element_by_id('category')).select_by_visible_text(detail)
            else:
                if detail == "Tackles":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)

                        player_team[index].total_tackles_won = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute("innerText").strip('\t')
                        player_team[index].player_gets_dribbled = player_row.find_elements_by_tag_name("td")[
                            8].get_attribute(
                            "innerText").strip('\t')
                        player_team[index].total_tackle_attempts = player_row.find_elements_by_tag_name("td")[9].get_attribute(
                            "innerText").strip('\t')

                elif detail == "Interception":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].interceptions = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerText").strip('\t')

                elif detail == "Fouls":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].fouled = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].fouls = player_row.find_elements_by_tag_name("td")[
                            8].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Cards":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].yellow_cards_per_90 = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].red_cards_per_90 = player_row.find_elements_by_tag_name("td")[
                            8].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Offsides":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].caught_offside = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Clearances":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].total_clearances = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Blocks":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].blocked_shots = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].blocked_crosses = player_row.find_elements_by_tag_name("td")[
                            8].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].blocked_passes = player_row.find_elements_by_tag_name("td")[9].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Saves":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].gk_totalsaves = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].gk_saves_insix_yard_box = player_row.find_elements_by_tag_name("td")[
                            8].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].gk_saves_in_penalty_area = player_row.find_elements_by_tag_name("td")[9].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].gk_saves_from_outside_of_the_box = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Shots":


                        shot_list = [x.text for x in
                                       browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]

                        for shot_detail in shot_list:
                            Select(browser.find_element_by_id('subcategory')).select_by_visible_text(shot_detail)

                            time.sleep(3)

                            player_shot_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                                .find_elements_by_tag_name('tr')

                            for player_row in player_shot_detailed:
                                name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                                index = search_player_in_list(name, player_team)

                                if shot_detail == "Zones":
                                    player_team[index].total_shots_per_90 = \
                                    player_row.find_elements_by_tag_name("td")[
                                        7].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shots_from_outside_the_penalty_area = player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shots_from_inside_thesix_yard_box = player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shots_from_inside_the_penalty_area = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t')

                                elif shot_detail == "Situations":
                                    player_team[index].shot_open_play = player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_counter = player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_setpiece = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_penalty_taken = player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                        "innerHTML").strip('\t')
                                elif shot_detail == "Accuracy":
                                    player_team[index].shot_offtarget = player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_onpost = player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_ontarget = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_blocked = player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                        "innerHTML").strip('\t')
                                elif shot_detail == "Body Parts":
                                    player_team[index].shot_right_foot = player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_left_foot = player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_head = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                        "innerHTML").strip('\t')
                                    player_team[index].shot_other = player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                        "innerHTML").strip('\t')

                elif detail == "Goals":
                    # subcategories

                    goal_list = [x.text for x in
                                 browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]

                    for goal_detail in goal_list:

                        Select(browser.find_element_by_id('subcategory')).select_by_visible_text(goal_detail)

                        time.sleep(3)

                        player_goal_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                            .find_elements_by_tag_name('tr')

                        for player_row in player_goal_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                            index = search_player_in_list(name, player_team)

                            if goal_detail == "Zones":
                                player_team[index].total_goal_per_90 = player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goals_from_inside_thesix_yard_box = player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goals_from_inside_the_penalty_area = player_row.find_elements_by_tag_name("td")[
                                    9].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goals_from_outside_the_penalty_area = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                    "innerHTML").strip('\t')
                            elif goal_detail == "Situations":
                                player_team[index].goal_open_play = player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goal_counter = player_row.find_elements_by_tag_name("td")[
                                    9].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goal_setpiece = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goal_penaltyscored = player_row.find_elements_by_tag_name("td")[
                                    11].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goal_own = player_row.find_elements_by_tag_name("td")[
                                    12].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goal_normal = player_row.find_elements_by_tag_name("td")[13].get_attribute(
                                    "innerHTML").strip('\t')
                            elif goal_detail == "Body Parts":
                                player_team[index].goal_right_foot = player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goal_left_foot = player_row.find_elements_by_tag_name("td")[
                                    9].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goal_head = player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].goal_other = player_row.find_elements_by_tag_name("td")[
                                    11].get_attribute(
                                    "innerHTML").strip('\t')

                elif detail == "Dribbles":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].unsuccessful_dribbles = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].successful_dribbles = player_row.find_elements_by_tag_name("td")[
                            8].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].total_dribbles = player_row.find_elements_by_tag_name("td")[
                            9].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Possession loss":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].unsuccessful_touches = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].dispossessed_per_90 = player_row.find_elements_by_tag_name("td")[
                            8].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Aerial":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)

                        player_team[index].total_aerial_duels = player_row.find_elements_by_tag_name("td")[
                            7].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].aerials_duels_won_per_90 = player_row.find_elements_by_tag_name("td")[
                            8].get_attribute(
                            "innerHTML").strip('\t')
                        player_team[index].aerial_duels_lost = player_row.find_elements_by_tag_name("td")[
                            9].get_attribute(
                            "innerHTML").strip('\t')

                elif detail == "Passes":
                    # subcategories

                    pass_list = [x.text for x in
                                 browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                    for pass_detail in pass_list:

                        Select(browser.find_element_by_id('subcategory')).select_by_visible_text(pass_detail)

                        time.sleep(3)

                        player_pass_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                            .find_elements_by_tag_name('tr')

                        for player_row in player_pass_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                            index = search_player_in_list(name, player_team)

                            if pass_detail == "Length":

                                player_team[index].total_passes = \
                                player_row.find_elements_by_tag_name("td")[
                                    7].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].accurate_long_balls = \
                                player_row.find_elements_by_tag_name("td")[
                                    8].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].inaccurate_long_balls = \
                                player_row.find_elements_by_tag_name("td")[
                                    9].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].accurate_short_passes = \
                                player_row.find_elements_by_tag_name("td")[10].get_attribute(
                                    "innerHTML").strip('\t')
                                player_team[index].inaccurate_short_passes = \
                                    player_row.find_elements_by_tag_name("td")[11].get_attribute(
                                        "innerHTML").strip('\t')
                            elif pass_detail == "Type":
                                player_team[index].accurate_cross_passes = \
                                    player_row.find_elements_by_tag_name("td")[
                                        7].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].inaccurate_cross_passes = \
                                    player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].accurate_corner_passes = \
                                    player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].inaccurate_corner_passes = \
                                    player_row.find_elements_by_tag_name("td")[
                                        10].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].accurate_freekicks = \
                                    player_row.find_elements_by_tag_name("td")[
                                        11].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].inaccurate_freekicks = \
                                    player_row.find_elements_by_tag_name("td")[
                                        12].get_attribute(
                                        "innerHTML").strip('\t')
                elif detail == "Key passes":

                    key_pass_list = [x.text for x in
                                 browser.find_element_by_id('subcategory').find_elements_by_tag_name("option")]
                    for key_pass_detail in key_pass_list:
                        Select(browser.find_element_by_id('subcategory')).select_by_visible_text(key_pass_detail)

                        time.sleep(3)

                        player_key_pass_detailed = browser.find_elements_by_id("player-table-statistics-body")[4] \
                            .find_elements_by_tag_name('tr')

                        for player_row in player_key_pass_detailed:
                            name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                            index = search_player_in_list(name, player_team)

                            if key_pass_detail == "Length":
                                player_team[index].total_key_pass = \
                                    player_row.find_elements_by_tag_name("td")[
                                        7].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].long_key_pass = \
                                    player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].short_key_pass = \
                                    player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t')

                            elif key_pass_detail == "Type":
                                player_team[index].key_pass_cross = \
                                    player_row.find_elements_by_tag_name("td")[
                                        7].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].key_pass_corner = \
                                    player_row.find_elements_by_tag_name("td")[
                                        8].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].key_pass_throughball = \
                                    player_row.find_elements_by_tag_name("td")[
                                        9].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].key_pass_freekick = \
                                    player_row.find_elements_by_tag_name("td")[
                                        10].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].key_pass_throwin = \
                                    player_row.find_elements_by_tag_name("td")[
                                        11].get_attribute(
                                        "innerHTML").strip('\t')
                                player_team[index].key_passes_others = \
                                    player_row.find_elements_by_tag_name("td")[
                                        12].get_attribute(
                                        "innerHTML").strip('\t')
                elif detail == "Assists":
                    for player_row in player_list_detailed:
                        name = player_row.find_element_by_class_name('player-link').get_attribute("innerText")
                        index = search_player_in_list(name, player_team)
                        player_team[index].cross_assist = \
                            player_row.find_elements_by_tag_name("td")[
                                7].get_attribute(
                                "innerHTML").strip('\t')
                        player_team[index].corner_assist = \
                            player_row.find_elements_by_tag_name("td")[
                                8].get_attribute(
                                "innerHTML").strip('\t')
                        player_team[index].throughball_assist = \
                            player_row.find_elements_by_tag_name("td")[
                                9].get_attribute(
                                "innerHTML").strip('\t')
                        player_team[index].freeckick_assist = \
                            player_row.find_elements_by_tag_name("td")[
                                10].get_attribute(
                                "innerHTML").strip('\t')
                        player_team[index].throw_in_assist = \
                            player_row.find_elements_by_tag_name("td")[
                                11].get_attribute(
                                "innerHTML").strip('\t')
                        player_team[index].other_assist = \
                            player_row.find_elements_by_tag_name("td")[
                                12].get_attribute(
                                "innerHTML").strip('\t')
                        player_team[index].total_assist_per_game = \
                            player_row.find_elements_by_tag_name("td")[
                                13].get_attribute(
                                "innerHTML").strip('\t')

        for idx, player in enumerate(player_team):
            write = '{0}'.format(
                json.dumps(player.__dict__, indent=4, separators=(',', ': ')))

            if idx == 0:
                write = "[" + write + ","
            elif idx == (len(player_team) - 1):
                write = write + "]"
            else:
                write = write + ","

            players_file.write(write)

        players_file.close()
        time.sleep(15)

