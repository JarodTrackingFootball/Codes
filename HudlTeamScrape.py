
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 14:51:18 2022

@author: jarodsvensson
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
from selenium.webdriver.chrome.options import Options

def get_left_of_5th_slash(input_string):
    parts = input_string.split('/')
    if len(parts) > 5:
        return '/'.join(parts[:5])
    else:
        return input_string 

options = Options()
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

teams = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Master School List(HM Updated).xlsx")
database = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_080125-111719am.xlsx")


#player_data = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\2025HudlMaster2.csv")

for i in range(12823, len(teams)):
    if i == 5000:
        player_data.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\2026HudlMaster-pt1.csv", index=False)
    if i == 10000:
        player_data.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\2026HudlMaster-pt2.csv", index=False)
    try:
        url = teams.at[i, 'New Hudl URL']
        url = url + '/roster?ss=2025'
    except:
        continue
    
    driver.get(url)
    time.sleep(1)
    school = teams.at[i, 'Hudl Name']
    state = teams.at[i, 'State']
    city = teams.at[i, 'City']
    try:
        if school.isna():
            school = teams.at[i, 'Official ETS Name']
    except:
        pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        table = soup.find('table')
        df1=pd.read_html(str(table))[0]
    except:
        time.sleep(100)
        i = i-1
        continue
    temp = soup.find('tbody')
    try:
        cards = temp.find_all('tr')
    except:
        pass
    
    df1['First Name'] = None
    df1['Last Name'] = None
    df1['Hudl URL'] = None
    df1['HS Name'] = school
    df1['HS City'] = city
    df1['HS State'] = state
    
    df1 = df1.replace('-','')
    df1['Name'] = df1['Name'].str.replace('Default User Avatar Icon','')
    
    for r in range(len(df1)):
        position = None
        height = None
        weight = None
        year = None
        first_name = None
        name = None
        last_name = None
        player_url = None
        photo = None
        hs_class = None
        number = None
        name = df1.at[r,'Name']
        try:
            df1.at[r, 'First Name'] = name.split(" ")[0]
            words = name.split()
            df1.at[r, 'Last Name'] = " ".join(words[1:])
        except:
            pass
        weight = df1.at[r,'Weight']
        try:
            weight = weight.replace("lbs","")
        except:
            pass
        height = df1.at[r, 'Height']
        if weight == '0':
            weight = None
        try:
            weight = float(weight)
        except:
            pass
        try:
            ht = height
            ft = int(ht.split('\'')[0])
            inch = int(ht.split('\'')[1][:-1])
            height = (ft*12) + inch
        except:
            height = None
        df1.at[r,'Height'] = height
        df1.at[r, 'Weight'] = weight
        try:
            df1.at[r, 'Position'] = df1.at[r, 'Position'].replace(", ","/")
        except:
            pass
        year = df1.at[r, 'Class of']
        if year == 'Sr.':
            hs_class = 2026
        elif year == 'Jr.':
            hs_class = 2027
        elif year == 'So.':
            hs_class = 2028
        elif year == 'Fr.':
            hs_class = 2029
        else:
            hs_class = year
        df1.at[r, 'Class of'] = hs_class
    for r in range(len(cards)):
        player_url = cards[r].find('a', class_='u-link u-link--default styles_fullName__ZQeFR').get('href')
        player_url = get_left_of_5th_slash(player_url)
        df1.at[r, 'Hudl URL'] = player_url
    
    teams.at[i, 'Hudl Count'] = len(df1)
    
    if i == 0:
        player_data = df1.copy()
    else:
        frames= [player_data,df1]
        player_data = pd.concat(frames)
driver.quit()

player_data.drop(index=player_data.index[0], 
        axis=0, 
        inplace=True)   

player_data = player_data.drop_duplicates()


player_data = pd.merge(player_data, database[['Slug','Hudl URL']], on='Hudl URL', how='left')

player_data.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\2026HudlMaster.csv", index=False)

