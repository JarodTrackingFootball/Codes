# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 09:00:28 2024

@author: jtsve
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:34:52 2023

@author: jtsve
"""


from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import requests
import pandas as pd
import math
from datetime import date
import random
from selenium.webdriver.chrome.options import Options
import json


df = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\NewGuystoScrape-H(11-5).csv")

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920x1080")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

for i in range(47228,len(df)):
    if df.at[i, 'Maxpreps URL'] == df.at[i, 'Maxpreps URL']:
        player_url = df.at[i, 'Maxpreps URL']

        driver.get(player_url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            temp = soup.find('div',class_='sc-7cdd6a26-0 dBejBl')
            temp = temp.find_all('div',class_='secondary')[-1].text
        except:
            temp=''
        try:
            temp2 = soup.find('div', class_='secondary').text
            year = temp2.split('• ')[1]
        except:
            pass
        if 'lbs' not in temp:
            pass
        else:
            try:
                ft = int(temp.split("\'")[0])*12
                inches = int(temp.split("\"")[0].split("\'")[1])
                height = ft + inches
                weight = int(temp.split(" lbs")[0].split(" ")[-1])
                if df.at[i, 'HS Height'] != df.at[i, 'HS Height']:
                    df.at[i, 'HS Height'] = height
                if df.at[i, 'HS Weight'] != df.at[i, 'HS Weight']:
                    df.at[i, 'HS Weight'] = weight
            except:
                pass
        try:
            position_temp = soup.find_all('a',class_='sc-51f90f89-0 dhSYvb secondary')
            for temporary in position_temp:
                sport = temporary.find('span', class_='primary').text
                if "Football" not in sport:
                    continue
                try:
                    positions = temporary.text.split("• ")[1]
                    if ", " in positions:
                        positions= positions.replace(", ","/")
                except:
                    continue
                if df.at[i, 'HS Positions'] != df.at[i, 'HS Positions'] :
                    df.at[i, 'HS Positions']  = positions
                    break
        except:
            pass
        if df.at[i, 'HS Class'] != df.at[i, 'HS Class']:
            df.at[i, 'HS Class'] = year

        try:
            bio = soup.find('div',class_='sc-6efe20cf-0 kNRsRb').text
        except:
            continue
        if "Basketball" in bio:
            basketball = 1
        else:
            basketball = 0
        if "Baseball" in bio:
            baseball = 1
        else:
            baseball = 0    
        if "Golf" in bio:
            golf = 1
        else:
            golf = 0  
        if "Hockey" in bio:
            hockey = 1
        else:
            hockey = 0  
        if "Lacrosse" in bio:
            lacrosse = 1
        else:
            lacrosse = 0  
        if "Rugby" in bio:
            rugby = 1
        else:
            rugby = 0  
        if "Soccer" in bio:
            soccer = 1
        else:
            soccer = 0 
        if "Swimming" in bio:
            swimming = 1
        else:
            swimming = 0  
        if "Tennis" in bio:
            tennis = 1
        else:
            tennis = 0 
        if "Volleyball" in bio:
            volleyball = 1
        else:
            volleyball = 0  
        if "Wrestling" in bio:
            wrestling = 1
        else:
            wrestling = 0 
        if "Track" in bio:
            track = 1
        else:
            track = 0  

        if df.at[i, 'Baseball'] != 1:
             df.at[i, 'Baseball'] = baseball
        if df.at[i, 'Basketball'] != 1:
            df.at[i, 'Basketball'] = basketball
        if df.at[i, 'Golf'] != 1:
            df.at[i, 'Golf'] = golf
        if df.at[i, 'Hockey'] != 1:
            df.at[i, 'Hockey'] = hockey
        if df.at[i, 'Lacrosse'] != 1:
            df.at[i, 'Lacrosse'] = lacrosse
        if df.at[i, 'Rugby'] != 1:
            df.at[i, 'Rugby'] = rugby
        if df.at[i, 'Soccer'] != 1:
            df.at[i, 'Soccer'] = soccer
        if df.at[i, 'Swimming'] != 1:
            df.at[i, 'Swimming'] = swimming
        if df.at[i, 'Tennis'] != 1:
            df.at[i, 'Tennis'] = tennis
        if df.at[i, 'Volleyball'] != 1:
            df.at[i, 'Volleyball'] = volleyball
        if df.at[i, 'Wrestling'] != 1:
            df.at[i, 'Wrestling'] = wrestling
        if df.at[i, 'Track'] != 1:
            df.at[i, 'Track'] = track

driver.quit()
df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\NewPlayerstoImport(11-7).csv",index=False)
