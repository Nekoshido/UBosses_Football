from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from source_code.scraper.transfermarkt.models import constants
from source_code.scraper.common import transfermarkt_models
from source_code import settings

if __name__ == "__main__":
    try:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE, executable_path=settings.EXECUTABLE)
    except Exception:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE)

    season = constants.YEARS[constants.YEARS_INDEX]
    site = '{}/{}/startseite/wettbewerb/{}/plus/?saison_id={}'.format(constants.TRANSFERMARKT_URL,
                                                                      constants.LEAGUES_LINK[constants.LEAGUE_INDEX],
                                                                      constants.LEAGUES_SHORT[constants.LEAGUE_INDEX],
                                                                      constants.YEARS[constants.YEARS_INDEX])
    print(site)
    browser.get(site)
    page = browser.page_source
    soup = BeautifulSoup(page, "html.parser")

    table_teams = soup.find('div', {'id': 'yw1'})
    teams = table_teams.find_all('a', {'class': 'vereinprofil_tooltip tooltipstered'})
    list_array = []
    for team in teams:
        team_href = team.get('href')
        if team_href not in list_array:
            list_array.append(team_href)
    for link in list_array:
        team_link = '{}{}'.format(constants.TRANSFERMARKT_URL,link)
        browser.get(team_link)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        team_name = soup.find('h1', {'itemprop': 'name'}).find('b').text
        print(team_name)
        break
