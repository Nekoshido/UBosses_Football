# -*- coding: utf-8 -*-

import platform

from selenium import webdriver


# under different operating systems
if platform.system() == 'Windows':
    EXECUTABLE = '/Users/Hecto/PycharmProjects/UBosses_Football/resources/firefox/firefox_driver/win/geckodriver.exe'
elif platform.system() == 'Darwin':
    EXECUTABLE = '/Users/hector.vivancos/PycharmProjects/UBosses_Football/resources/firefox/firefox_driver/mac/geckodriver'
else:
    EXECUTABLE = '../resources/firefox/firefox_driver/linux/geckodriver'

FFPROFILE = webdriver.FirefoxProfile()

# TODO(casals) migrate to BaseScraper load
print('Trying to open with extension')
if platform.system() != 'Windows':
    FFPROFILE.add_extension(extension='/Users/hector.vivancos/PycharmProjects/UBosses_Football/resources/firefox/plugins/addblock/addblock.xpi')
    print('Finished load extension')
