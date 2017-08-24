# -*- coding: utf-8 -*-

import platform
from selenium import webdriver

# under different operating systems
if platform.system() == 'Windows':
    PHANTOMJS_PATH = './phantomjs-2.1.1-windows/bin/phantomjs.exe'
else:
    PHANTOMJS_PATH = './phantomjs-2.1.1-windows/bin/phantomjs.exe'

ffprofile = webdriver.FirefoxProfile()
print('Trying to open with extension')
ffprofile.add_extension(
    extension='C:\Users\Hector\AppData\Roaming\Mozilla\Firefox\Profiles\9u09psq3.default\extensions\{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi')

print('Finished load extension')
