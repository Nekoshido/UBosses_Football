# -*- coding: utf-8 -*-

import platform
from selenium import webdriver

# under different operating systems
if platform.system() == 'Windows':
    EXECUTABLE = '../resources/geckodriver.exe'
else:
    EXECUTABLE = '../resources/geckodriver'

FFPROFILE = webdriver.FirefoxProfile()

# TODO migrate to BaseScraper load
print('Trying to open with extension')
FFPROFILE.add_extension(extension='../resources/addblock.xpi')
print('Finished load extension')
