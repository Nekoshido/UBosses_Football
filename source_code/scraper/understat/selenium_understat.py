import time


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from source_code.scraper.squawka_scraper.models import constants
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
    page = browser.page_source
    soup = BeautifulSoup(page, "html.parser")
    teams = soup.find('div', {'id': 'league-chemp'}).find('tbody').find_all('a')
    team = teams[constants_understat.TEAM_INDEX]
    team_link = constants_understat.ORIGINAL_UNDERSTAT_URL + team.get('href')
    browser.get(team_link)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    players = soup.find('div', {'id': 'team-players'}).find('tbody').find_all('tr')
    for player in players:
        player_link = constants_understat.ORIGINAL_UNDERSTAT_URL + player.find_all('td')[1].find('a').get('href')
        browser.get(player_link)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        name = soup.find('div', {'class': 'header-wrapper'}).text.split("\n")[1].split('\t')[4]
        print(name)
        seasons = soup.find('div', {'id': 'player-groups'}).find('tbody').find_all('tr')
        for season in seasons:
            season_stats = season.find_all('td')
            if season_stats[1].text == constants_understat.SEASON_TEXT:
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
                new_player.general = season_performance
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
                    new_player.performance_by_position[position_stats[1].text] = position_performance
                print(new_player.performance_by_position)
                xpath = "// label[ @for = 'groups-field-3']"
                menu_position = browser.find_element_by_xpath(xpath)
                actions = ActionChains(browser)
                actions.move_to_element(menu_position)
                actions.click(menu_position)
                actions.perform()





