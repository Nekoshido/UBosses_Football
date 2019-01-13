
import time
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
    site = '{}/x/profil/spieler/{}'.format(constants.TRANSFERMARKT_URL,constants.PLAYER_INDEX
                                                                     )
    players_file_name = 'players_transfermarkt.csv'
    players_file = open(players_file_name, 'w')
    #players_file.write(constants.PLAYERS_WRITE)

    browser.get(site)
    page = browser.page_source
    soup = BeautifulSoup(page, "html.parser")
    for player_id in range(constants.PLAYER_INDEX+1, 999999):
        player_page = '{}/x/profil/spieler/{}'.format(constants.TRANSFERMARKT_URL,player_id)
        browser.get(player_page)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        player = transfermarkt_models.Player()
        try:
            player.number = soup.find('span', {'class': 'dataRN'})
        except:
            print('No Number')
        try:
            player.name = soup.find('h1', {'itemprop': 'name'}).text
        except:
            print('No Name')

        table_data = soup.find('table', {'class': 'auflistung'})
        table_list = table_data.find_all('tr')
        for tr in table_list:
            row = tr.find('th').text.split('\n')[0]
            if row == "Fecha de nacimiento:":
                print("Fecha de nacimiento: ", tr.find('td').text.split('\n')[0])
                player.birthday = tr.find('td').text.split('\n')[0]
            elif row == "Altura:":
                print("Altura: ", tr.find('td').text.split('\n')[0])
                player.height = tr.find('td').text.split('\n')[0]
            elif row == "Nacionalidad:":
                nationality_list = []
                for nation in tr.find_all('img'):
                    nationality_list.append(nation.get('title'))
                player.nationalities = nationality_list
                print("nacionalidad: ",  player.nationalities)
            elif row == "Pie:":
                print("pie: ", tr.find('td').text.split('\n')[0])
                player.height = tr.find('td').text.split('\n')[0]
            elif row == "Contrato hasta::":
                print("until: ", tr.find('td').text.split('\n')[0])
                player.height = tr.find('td').text.split('\n')[0]
            elif row == "Agente:":
                print("agente: ", tr.find('a').text)
                player.agent = tr.find('a').text
            elif row == "Talla:":
                print("talla: ", tr.find('td').text.split('\n')[0])
                player.size = tr.find('td').text.split('\n')[0]
            elif row == "Lugar de nacimiento:":
                print("lugar: ", tr.find('span').text.split('\n')[0])
                player.place_of_birth = tr.find('span').text.split('\n')[0]
            elif row == "Nombre en país de origen:":
                print("full name: ", tr.find('td').text.split('\n')[0])
                player.full_name = tr.find('td').text.split('\n')[0]
        main_position = soup.find('div', {'class': 'hauptposition-left'}).text.split('Posición principal')[1].split(':')[1].split('\t')[0]
        print(main_position)
        player.main_position = soup.find('div', {'class': 'hauptposition-left'}).text.split('Posición principal')[1].split(':')[1].split('\t')[0]
        other_positions = soup.find('div', {'class': 'nebenpositionen'}).text.split('Posición secundaria:')[1].split('\n')[1].split('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')
        position_list= []
        for position in other_positions:
            if position != '':
                if len(position.split('\t\t')) == 1:
                    position_list.append(position.split('\t\t')[0])
                else:
                    position_list.append(position.split('\t\t')[1])
        market_link = '{}/x/marktwertverlauf/spieler/{}'.format(constants.TRANSFERMARKT_URL, player_id)
        browser.get(market_link)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        market_price = soup.find('g', {'class': 'highcharts-markers highcharts-tracker'}).find_all('image')
        print(market_price)
        browser.implicitly_wait(5)
        time.sleep(5)
        market_img = browser.find_element_by_xpath("//g[@class='highcharts-markers highcharts-tracker']")
        print("=======================")
        print(market_img)
        actions = ActionChains(browser)
        actions.move_to_element(market_img)
        actions.click(market_img)
        actions.perform()


        break
        #print(name)
        #print(birthday)
        #table = soup.find('table', {'class': 'auflistung'}).text
        #print(table)
