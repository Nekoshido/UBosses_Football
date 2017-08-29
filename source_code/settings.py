# -*- coding: utf-8 -*-

import platform
from selenium import webdriver

# under different operating systems
if platform.system() == 'Windows':
    executable = '../resources/geckodriver.exe'
else:
    executable = '../resources/geckodriver'

ffprofile = webdriver.FirefoxProfile()
print('Trying to open with extension')

ffprofile.add_extension(extension='../resources/addblock.xpi')

print('Finished load extension')
