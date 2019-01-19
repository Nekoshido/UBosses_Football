from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import chain, zip_longest
import json
import pathlib

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from source_code.scraper.transfermarkt.models import constants_transfermarkt
from source_code.scraper.common import transfermarkt_models
from source_code import settings

def string_money_to_int(number):
    if number == "\xa0" or number == "-\xa0":
        return 0
    else:
        units_dic = ['Mill.', 'Th.']
        money_list = number.split(" ")
        units = float(money_list[0].replace(",", "."))
        if money_list[1] == units_dic[0]:
            return units * 1000000
        elif money_list[1] == units_dic[1]:
            return units * 1000
        else:
            return money_list[1]

def string_date_to_date(date):
    calendar = {'Jan': '01',
                'Feb': '02',
                'Mar': '03',
                'Apr': '04',
                'May': '05',
                'Jun': '06',
                'Jul': '07',
                'Aug': '08',
                'Sep': '09',
                'Oct': '10',
                'Nov': '11',
                'Dec': '12'}
    final_date = date.split("(")[0].split(" ")
    if int(final_date[1].split(',')[0]) < 10:
        day = '0' + final_date[1].split(',')[0]
    else:
        day = final_date[1].split(',')[0]
    final_date = day + "-" + calendar[final_date[0]] + "-" + final_date[2]
    return final_date

if __name__ == "__main__":
    try:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE, executable_path=settings.EXECUTABLE)
    except Exception:
        browser = webdriver.Firefox(firefox_profile=settings.FFPROFILE)
    for year in constants_transfermarkt.YEARS:

        season = constants_transfermarkt.YEARS[constants_transfermarkt.YEARS_INDEX]
        site = '{}/{}/startseite/wettbewerb/{}/plus/?saison_id={}'.format(constants_transfermarkt.TRANSFERMARKT_URL,
                                                                          constants_transfermarkt.LEAGUES_LINK[constants_transfermarkt.LEAGUE_INDEX],
                                                                          constants_transfermarkt.LEAGUES_SHORT[constants_transfermarkt.LEAGUE_INDEX],
                                                                          year)
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
            team_link = '{}{}'.format(constants_transfermarkt.TRANSFERMARKT_URL, link)
            browser.get(team_link)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            team = soup.find('div', {'class': 'dataHeader dataExtended'}).find('h1', {'itemprop': 'name'}).find('span').text

            directory = 'data/%s/%s/' % (
                constants_transfermarkt.LEAGUES_LINK[constants_transfermarkt.LEAGUE_INDEX], year)
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
            players_file_name = directory + '%s- %s - Players-%s.json' % (
                team, constants_transfermarkt.LEAGUES_LINK[constants_transfermarkt.LEAGUE_INDEX], year)
            players_file = open(players_file_name, 'w')

            players_team_odd = soup.find('div', {'id': 'yw1'}).find('tbody').find_all('tr', {'class': 'odd'})
            players_team_even = soup.find('div', {'id': 'yw1'}).find('tbody').find_all('tr', {'class': 'even'})
            player_team = list(filter(None.__ne__, chain.from_iterable(zip_longest(players_team_odd, players_team_even))))
            new_player_preview = transfermarkt_models.PlayerPreview()
            for idx, players in enumerate(player_team):
                new_player_preview.name = players.find('a', {'class': 'spielprofil_tooltip tooltipstered'}).text
                new_player_preview.value = string_money_to_int(players.find('td', {'class': 'rechts hauptlink'}).text)
                new_player_preview.position = players.find('table', {'class': 'inline-table'}).find_all('tr')[1].find('td').text
                new_player_preview.birth = string_date_to_date(players.find_all('td', {'class': 'zentriert'})[1].text)
                new_player_preview.number = players.find('div', {'class': 'rn_nummer'}).text
                new_player_preview.url = players.find('a', {'class': 'spielprofil_tooltip tooltipstered'})['href']
                new_player_preview.player_id = players.find('a', {'class': 'spielprofil_tooltip tooltipstered'})['id']
                new_player_preview.team = team
                new_player_preview.season = year

                write = '{0}'.format(
                    json.dumps(new_player_preview.__dict__, indent=4, separators=(',', ': ')))
                if idx == 0:
                    write = "[" + write + ","
                elif idx == (len(players) - 1):
                    write = write + "]"
                else:
                    write = write + ","
                players_file.write(write)

            players_file.close()
