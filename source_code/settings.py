# -*- coding: utf-8 -*-

import platform

from selenium import webdriver


# under different operating systems
if platform.system() == 'Windows':
    EXECUTABLE = '../resources/firefox/firefox_driver/win/geckodriver.exe'
elif platform.system() == 'Darwin':
    EXECUTABLE = '../resources/firefox/firefox_driver/mac/geckodriver'
else:
    EXECUTABLE = '../resources/firefox/firefox_driver/linux/geckodriver'

FFPROFILE = webdriver.FirefoxProfile()

# TODO (casals) migrate to BaseScraper load
print('Trying to open with extension')
FFPROFILE.add_extension(extension='../resources/firefox/plugins/addblock/addblock.xpi')
print('Finished load extension')
