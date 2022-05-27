from collections import Callable

from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pathlib
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from source_code.scraper.whoscored_scraper.models import constants_whoscored, metrics_extractor
from source_code import settings
from source_code.scraper.whoscored_scraper.models.constants_whoscored import RETRIES
from source_code.scraper.whoscored_scraper.models.metrics_extractor import get_player_list
from source_code.scraper.whoscored_scraper.models.url_builder import url_builder


def search_player_in_list(name, player_list):
    for idx, element in enumerate(player_list):
        if element.name == name:
            return idx
    return None


def get_competition(browser, *args):
    try:
        soup = BeautifulSoup(browser.page_source, "html.parser")
        return soup.find('dl', {'id': 'tournamentOptions'}).find_all('dd')
    except:
        return None


def get_teams(browser, *args):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    table_teams = soup.find_all('table', {'class': 'grid with-centered-columns hover'})[0].find('tbody')
    teams = table_teams.find_all('tr')
    if constants_whoscored.LEAGUE_INDEX == 9 or \
            (constants_whoscored.LEAGUE_INDEX == 12 and constants_whoscored.SEASON_INDEX > 11):  # MLS has 2 conferences
        table_teams_v2 = soup.find_all('table', {'class': 'grid with-centered-columns hover'})[3].find('tbody')
        teams2 = table_teams_v2.find_all('tr')
        teams = teams + teams2
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    print("SEASON: " + str(constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]))
    print("Len Teams: " + str(len(teams[constants_whoscored.TEAM_INDEX:])))
    return teams if (len(teams[constants_whoscored.TEAM_INDEX:]) > 0) else None


def _get_error_display(browser, view_index, player_index):
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
        time.sleep(3)

        defensive_button = browser.find_elements_by_class_name('in-squad-detailed-view')[view_index]
        actions = ActionChains(browser)
        actions.move_to_element(defensive_button)
        actions.click(defensive_button)
        actions.perform()
        time.sleep(3)
        return metrics_extractor.get_player_list(browser, player_index)


def _get_detail_error_display(browser, detail):
    try:
        Select(browser.find_element_by_id('category')).select_by_visible_text(
            not_new_seasons[0])
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
        history_button = \
            browser.find_element_by_id('sub-navigation').find_elements_by_tag_name('li')[4]
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

        time.sleep(4)

        return get_player_list(browser, 4)


def _get_summary_error_display(browser):
    try:
        Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
        time.sleep(5)
        Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
        page = browser.page_source
        soup = BeautifulSoup(page, "html.parser")
        return soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')
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
        return soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')


def _select_metric_tab(browser, index):
    time.sleep(2)
    button = browser.find_elements_by_class_name('in-squad-detailed-view')[index]
    actions = ActionChains(browser)
    actions.move_to_element(button)
    actions.click(button)
    actions.perform()
    time.sleep(4)


def _cross_get_player_list(browser):
    for i in range(4):
        _select_metric_tab(browser, index=i)


def _get_player_list_safe(function: Callable, browser, *index):
    for i in range(RETRIES):
        exit_clause = function(browser, index[1])
        if exit_clause:
            return exit_clause
        time.sleep(2)
    _cross_get_player_list(browser)
    if index[0] == 0:
        _select_metric_tab(browser, index=index[1] - 1)
    else:
        print("NOT NORMAL: ", index)
        _select_metric_tab(browser, index=index[1] - 1)
        Select(browser.find_element_by_id('subcategory')).select_by_visible_text(index[2])
    print(" *** Retry FAKE LOOP ***")
    return _get_player_list_safe(function, browser, *index)


def get_passing(browser, args):
    player_team = args[0]
    try:
        time.sleep(1)
        _select_metric_tab(browser, index=2)

        time.sleep(1)
        start = time.time()
        # player_list_passing = retry_helper(get_player_list, browser, *[3])
        player_list_passing = _get_player_list_safe(get_player_list, browser, *[0, 3])
        if player_list_passing[0].get_attribute("innerText") == 'There are no results to display':
            Select(browser.find_element_by_id('stageId')).select_by_visible_text(not_new_seasons[0])
            time.sleep(5)
            Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
            player_list_passing = browser.find_elements_by_id("player-table-statistics-body")[
                3].find_elements_by_tag_name('tr')
        for player_row in player_list_passing:
            name = metrics_extractor.get_player_name(player_row)
            if name in player_team:
                player_team[name] = metrics_extractor.passing(player_team[name], player_row)

        done = time.time()
        elapsed = done - start
        print("Passing Time: " + str(elapsed))
        return player_team

    except Exception as e:
        print("Exception: ", e)
        return None


def _click_search_in_details(browser):
    comp_button = browser.find_element_by_class_name('search-button-container').find_element_by_class_name(
        'search-button')
    actions = ActionChains(browser)
    actions.move_to_element(comp_button)
    actions.click(comp_button)
    actions.perform()


def get_details(browser, args):
    player_team = args[0]

    _select_metric_tab(browser, index=3)
    time.sleep(2)

    global_start = time.time()

    Select(browser.find_element_by_id('statsAccumulationType')).select_by_value("2")
    time.sleep(2)
    _click_search_in_details(browser)
    time.sleep(2)
    detail_list = [x.text for x in
                   browser.find_element_by_id('category').find_elements_by_tag_name("option")]

    for detail in detail_list:

        Select(browser.find_element_by_id('statsAccumulationType')).select_by_value("2")
        time.sleep(1)

        Select(browser.find_element_by_id('category')).select_by_visible_text(detail)

        time.sleep(5)

        # player_list_detailed = retry_helper(get_player_list, browser, *[4])
        player_list_detailed = _get_player_list_safe(get_player_list, browser, *[0, 4])

        if player_list_detailed[0].get_attribute("innerText") == 'There are no results to display':
            print("No Display")
            player_list_detailed = _get_detail_error_display(browser, detail)

        if detail == "Tackles":
            startt = time.time()
            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.tackles(player_team[name], player_row)
            finish = time.time()
            timet = finish - startt
            print("Tackles " + str(timet))

        elif detail == "Interception":
            startt = time.time()

            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.interceptions(player_team[name], player_row)
            finish = time.time()
            timet = finish - startt
            print("Interception " + str(timet))

        elif detail == "Fouls":
            startt = time.time()

            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.fouls(player_team[name], player_row)
            finish = time.time()
            timet = finish - startt
            print("Fouls " + str(timet))

        elif detail == "Cards":
            startt = time.time()
            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.cards(player_team[name], player_row)
            finish = time.time()
            timet = finish - startt
            print("Cards " + str(timet))

        elif detail == "Offsides":
            startt = time.time()
            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.offside(player_team[name], player_row)
            finish = time.time()
            timet = finish - startt
            print("Offsides " + str(timet))

        elif detail == "Clearances":
            startt = time.time()
            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.clearances(player_team[name], player_row)
            finish = time.time()
            timet = finish - startt
            print("Clearances " + str(timet))

        elif detail == "Blocks":
            startt = time.time()

            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.blocks(player_team[name], player_row)
            finish = time.time()
            timet = finish - startt
            print("Blocks " + str(timet))

        elif detail == "Saves":
            startt = time.time()

            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.saves(player_team[name], player_row)

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
                time.sleep(5)
                # player_shot_detailed = retry_helper(get_player_list, browser, *[4])
                player_shot_detailed = _get_player_list_safe(get_player_list, browser, *[1, 4, shot_detail])
                for player_row in player_shot_detailed:
                    name = metrics_extractor.get_player_name(player_row)
                    if shot_detail == "Zones":
                        if name in player_team:
                            player_team[name] = metrics_extractor.shot_zones(player_team[name], player_row)
                    elif shot_detail == "Situations":
                        if name in player_team:
                            player_team[name] = metrics_extractor.shot_situations(player_team[name],
                                                                                  player_row)
                    elif shot_detail == "Accuracy":
                        if name in player_team:
                            player_team[name] = metrics_extractor.shot_accuracy(player_team[name],
                                                                                player_row)
                    elif shot_detail == "Body Parts":
                        if name in player_team:
                            player_team[name] = metrics_extractor.shot_body_parts(player_team[name],
                                                                                  player_row)
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
                time.sleep(4)
                player_goal_detailed = _get_player_list_safe(get_player_list, browser, *[1, 4, goal_detail])
                # Select(browser.find_element_by_id('subcategory')).select_by_visible_text(goal_detail)
                # player_goal_detailed = retry_helper(get_player_list, browser, *[4])
                for player_row in player_goal_detailed:
                    name = metrics_extractor.get_player_name(player_row)
                    if goal_detail == "Zones":
                        if name in player_team:
                            player_team[name] = metrics_extractor.goal_zones(player_team[name], player_row)
                    elif goal_detail == "Situations":
                        if name in player_team:
                            player_team[name] = metrics_extractor.goal_situations(player_team[name],
                                                                              player_row)
                    elif goal_detail == "Body Parts":
                        if name in player_team:
                            player_team[name] = metrics_extractor.goal_body_parts(player_team[name],
                                                                              player_row)

                finish = time.time()
                timet = finish - startt
                print("Goals: " + str(timet))

        elif detail == "Dribbles":
            startt = time.time()

            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.dribbles(player_team[name], player_row)

            finish = time.time()
            timet = finish - startt
            print("Dribbles " + str(timet))

        elif detail == "Possession loss":
            startt = time.time()

            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.possession_loss(player_team[name], player_row)

            finish = time.time()
            timet = finish - startt
            print("Possession loss " + str(timet))

        elif detail == "Aerial":
            startt = time.time()
            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.aerial(player_team[name], player_row)

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

                time.sleep(4)
                player_pass_detailed = _get_player_list_safe(get_player_list, browser, *[1, 4, pass_detail])
                # player_pass_detailed = retry_helper(get_player_list, browser, *[4])

                time.sleep(1)
                for player_row in player_pass_detailed:
                    name = metrics_extractor.get_player_name(player_row)
                    if pass_detail == "Length":
                        if name in player_team:
                            player_team[name] = metrics_extractor.pass_length(player_team[name], player_row)
                    elif pass_detail == "Type":
                        if name in player_team:
                            player_team[name] = metrics_extractor.pass_type(player_team[name], player_row)
                finish = time.time()
                timet = finish - startt
                print("Passes " + str(timet))

        elif detail == "Key passes":
            print("======")
            print("Key Passes")
            print("======")
            startt = time.time()
            key_pass_list = [x.text for x in
                             browser.find_element_by_id('subcategory').find_elements_by_tag_name(
                                 "option")]
            print("Len key_pass_list: " + str(len(key_pass_list)))
            for key_pass_detail in key_pass_list:
                Select(browser.find_element_by_id('subcategory')).select_by_visible_text(
                    key_pass_detail)
                time.sleep(4)
                # player_key_pass_detailed = retry_helper(get_player_list, browser, *[4])
                player_key_pass_detailed = _get_player_list_safe(get_player_list, browser, *[1, 4, key_pass_list])

                for player_row in player_key_pass_detailed:
                    name = metrics_extractor.get_player_name(player_row)
                    if key_pass_detail == "Length":
                        if name in player_team:
                            player_team[name] = metrics_extractor.key_passes_length(player_team[name],
                                                                                player_row)
                    elif key_pass_detail == "Type":
                        if name in player_team:
                            player_team[name] = metrics_extractor.key_passes_type(player_team[name],
                                                                              player_row)
                finish = time.time()
                timet = finish - startt
                print("Key Passes " + str(timet))

        elif detail == "Assists":
            startt = time.time()

            for player_row in player_list_detailed:
                name = metrics_extractor.get_player_name(player_row)
                if name in player_team:
                    player_team[name] = metrics_extractor.assist(player_team[name], player_row)
            finish = time.time()
            timet = finish - startt
            print("Assists " + str(timet))

    done = time.time()
    elapsed = done - global_start
    print("Detail: " + str(elapsed))
    return player_team


def get_ofensive(browser, args):
    player_team = args[0]
    try:
        start = time.time()
        _select_metric_tab(browser, index=1)

        time.sleep(3)
        # player_list_offensive = retry_helper(get_player_list, browser, *[2])
        player_list_offensive = _get_player_list_safe(get_player_list, browser, *[0, 2])
        if player_list_offensive[0].get_attribute("innerText") == 'There are no results to display':
            player_list_offensive = _get_error_display(browser, 1, 2)

        for player_row in player_list_offensive:
            name = metrics_extractor.get_player_name(player_row)
            if name in player_team:
                player_team[name] = metrics_extractor.offensive(player_team[name], player_row)

        done = time.time()
        elapsed = done - start
        print("Offensive Time: " + str(elapsed))

        return player_team

    except Exception as e:
        print("Exception: ", e)
        return None


def get_defensive(browser, args):
    player_team = args[0]
    try:
        start = time.time()

        _select_metric_tab(browser, index=0)
        # player_list_defensive = retry_helper(get_player_list, browser, *[1])
        player_list_defensive = _get_player_list_safe(get_player_list, browser, *[0, 1])
        if player_list_defensive[0].get_attribute("innerText") == 'There are no results to display':
            player_list_defensive = _get_error_display(browser, 0, 1)
        for player_row in player_list_defensive:
            name = metrics_extractor.get_player_name(player_row)
            if name in player_team:
                player_team[name] = metrics_extractor.defensive(player_team[name], player_row)
        done = time.time()
        elapsed = done - start
        print("Defensive Time: " + str(elapsed))
        return player_team
    except Exception as e:
        print("Exception: ", e)
        return None


def create_file(team_name, competition):
    directory = 'data/%s/%s/' % (
        constants_whoscored.LEAGUES_LINK[constants_whoscored.LEAGUE_INDEX],
        constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    players_file_name = directory + '%s- -%s - Players-%s.json' % (
        team_name, competition.replace("/", "-").split('-')[0],
        constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX])
    return open(players_file_name, 'w')


def get_archive_summary(browser, idx_c):
    try:
        actions = ActionChains(browser)
        actions.perform()
        time.sleep(3)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')
        if player_list[0].text == 'There are no results to display':
            player_list = _get_summary_error_display(browser)
        player_team = {}
        print("Len Seasons: " + str(len(player_list)))
        for player_row in player_list:
            new_player = metrics_extractor.create_player(soup=soup, player_row=player_row,
                                                         competition=competition)
            player_team[new_player.name] = new_player
        return player_team
    except Exception as e:
        print("Exception: ", e)
        return None


def get_summary(browser, idx_c):
    try:
        comp_button = browser.find_element_by_id('tournamentOptions').find_elements_by_tag_name('dd')[idx_c[0]]
        actions = ActionChains(browser)
        actions.move_to_element(comp_button)
        actions.click(comp_button)
        actions.perform()
        time.sleep(3)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        player_list = soup.find('tbody', {'id': 'player-table-statistics-body'}).find_all('tr')
        if player_list[0].text == 'There are no results to display':
            player_list = _get_summary_error_display(browser)
        player_team = {}
        print("Len Seasons: " + str(len(player_list)))
        for player_row in player_list:
            new_player = metrics_extractor.create_player(soup=soup, player_row=player_row,
                                                         competition=competition)
            player_team[new_player.name] = new_player
        return player_team
    except Exception as e:
        print("Exception: ", e)
        return None


def retry_helper(function: Callable, browser, *args):
    for i in range(RETRIES):
        exit_clause = function(browser, args)
        if exit_clause:
            return exit_clause
        time.sleep(2)
    browser.refresh()
    time.sleep(3)
    print(" *** Retry LOOP ***")
    return retry_helper(function, browser, *args)


if __name__ == "__main__":
    try:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE, executable_path=settings.EXECUTABLE)
    except Exception:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE)

    site = url_builder()

    print(site)
    browser.get(site)
    time.sleep(3)
    browser.execute_script("document.body.style.zoom = '30%';")

    browser.get(site)
    time.sleep(3)

    actions = ActionChains(browser)

    try:
        continue_button = browser.find_element_by_class_name('details_continue--2CnZz').find_element_by_tag_name('span')
        actions.move_to_element(continue_button)
        actions.click(continue_button).perform()
    except:
        print("not button")
    teams = retry_helper(get_teams, browser)
    for idx, team in enumerate(teams[constants_whoscored.TEAM_INDEX:]):
        print('Progress: ' + str(constants_whoscored.TEAM_INDEX + idx) + ' / ' + str(len(teams) - 1))
        print("League Number: " + str(constants_whoscored.LEAGUE_INDEX))
        url = team.find('a', {'class': 'team-link'}).get('href')
        team_name = team.find('a', {'class': 'team-link'}).text
        #  CURRENT SEASON

        if constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX] == constants_whoscored.SEASON_NUMBER[
            len(constants_whoscored.SEASON_NUMBER) - 1]:
            site = '{}{}'.format(constants_whoscored.WHOSCORED_URL, url)
            print(site)
            browser.get(site)
            time.sleep(2)
            option_list = retry_helper(get_competition, browser)
            season_list = [x.text for x in
                           option_list]
            for idx_c, competition in enumerate(season_list):
                if competition in constants_whoscored.EXCLUDED_COMPETITIONS:
                    continue
                else:

                    print("+++++++++")
                    print(competition)
                    print("+++++++++")
                    if idx_c != 0:
                        summary_button = \
                            browser.find_element_by_id('team-squad-stats-options').find_elements_by_tag_name('li')[0]
                        actions = ActionChains(browser)
                        actions.move_to_element(summary_button)
                        actions.click(summary_button)
                        actions.perform()
                        time.sleep(2)
                    print("Summary")
                    args = [idx_c]
                    player_team = retry_helper(get_summary, browser, *args)

                    # press defensive button
                    player_team = retry_helper(get_defensive, browser, player_team)

                    # press offensive button
                    player_team = retry_helper(get_ofensive, browser, player_team)

                    # press passing button
                    player_team = retry_helper(get_passing, browser, player_team)

                    # press details button
                    player_team = retry_helper(get_details, browser, player_team)

                    players_file = create_file(team_name, competition)
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
            for season in season_list:
                split_season = season.split('-')[1].split(' ')[1].split('/')[0]
                if split_season == constants_whoscored.SEASON_NUMBER[constants_whoscored.SEASON_INDEX]:
                    new_season_list.append(season)
                else:
                    not_new_seasons.append(season)
            for competition in new_season_list:
                print("+++++++++")
                print(competition)
                print("+++++++++")
                Select(browser.find_element_by_id('stageId')).select_by_visible_text(competition)
                page = browser.page_source

                time.sleep(5)
                args = [0]

                player_team = retry_helper(get_archive_summary, browser, *args)

                # press defensive button
                player_team = retry_helper(get_defensive, browser, player_team)

                # press offensive button
                player_team = retry_helper(get_ofensive, browser, player_team)

                # press passing button
                player_team = retry_helper(get_passing, browser, player_team)

                # press details button
                player_team = retry_helper(get_details, browser, player_team)

                players_file = create_file(team_name, competition)
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
