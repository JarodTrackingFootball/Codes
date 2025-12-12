# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:03:24 2025

@author: jtsve
"""

import requests
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import math
from datetime import date
import warnings
from selenium.webdriver.chrome.options import Options

warnings.simplefilter(action='ignore', category=FutureWarning)

teams = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Master School List(HM Updated).xlsx")
    


options = Options()
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

df = pd.DataFrame({'Name':[''],'Athletic URL':[''], 'HS Name':[''], 'HS State':[''],'Roster Year':['']})

for i in range(10320,len(teams)):
    if teams.at[i, 'Athletic URL'] != teams.at[i, 'Athletic URL']:
        continue
    school = teams.at[i, 'Hudl Name']
    state = teams.at[i, 'State']
    team_url = teams.at[i, 'Athletic URL']
    try:
        team_url = team_url[:-4]
    except:
        continue
    for y in range(2025,2027):
        t_url = team_url + str(y)
        try:
            driver.get(t_url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'lxml')
        except:
            continue
        names_temp = soup.find('div', class_='col-6 ng-star-inserted')
        try:
            names = names_temp.find_all('div', class_='ng-star-inserted')
        except:
            continue
        for name in names:
            try:
                player_name = name.find('span', class_='text-truncate').text
                player_url = 'https://www.athletic.net' + name.find('a').get('href')
            except:
                continue
            
            new_row  = {'Name':player_name,'Athletic URL':player_url,'HS Name':school,'HS State':state,
                            'Roster Year':y}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

driver.quit()
#df_unique = df.drop_duplicates(subset=['Athletic URL'], keep=False)
df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\AthleticTeamsPlayerMaster(1-24)-RAW.csv",index=False)
