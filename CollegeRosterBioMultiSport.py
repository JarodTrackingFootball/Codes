# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:30:42 2023

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
import warnings
import random

header_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']


proxy_username = 'jtnoah'
proxy_password = '6FD76B600F96231CD1E5A90035200C04'
proxy_ips = ['23.94.248.15:34555', '23.95.111.212:24557', '107.172.45.115:42720',
             '198.23.224.24:24557','198.23.234.157:34555']
proxy_list = []
proxies = []
for proxy_temp in proxy_ips:
    temp = "http://{0}:{1}@{2}".format(proxy_username, proxy_password, proxy_temp)    
    proxy_list.append(temp)

for proxy in proxy_list:
    try:
        r = requests.get('http://ipinfo.io/json',proxies = {'http':proxy, 'https':proxy})
    except:
        continue
    if r.status_code == 200:
        proxies.append(proxy)

df = pd.read_excel(r"C:\Users\jtsve\OneDrive\Documents\CollegeSpecialiststoRUN.xlsx")


for i in range(0,len(df)):
    if i == 5000:
        df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\CollegeSpecialist-BioRun(9-3).csv", index=False) 
    if i == 10000:
        df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\CollegeSpecialist-BioRun(9-3).csv", index=False)        
    basketball= 0
    baseball= 0
    golf= 0
    hockey= 0
    lacrosse= 0
    powerlifting= 0
    rugby= 0
    soccer= 0
    tennis= 0
    volleyball= 0
    wrestling= 0
    swimming = 0
    track = 0
    bio = None
    url = df.at[i, 'College URL']
    headers = {'User-Agent': random.choice(header_list)}
    proxy = random.choice(proxies)
    try:
        r = requests.get(url, headers=headers, proxies = {'http':proxy, 'https':proxy})
    except:
        pass
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        bio = soup.find('section',{'id':'sidearm-roster-player-bio'}).text
    except:
        pass
    if bio == None:
        try:
            bio = soup.find('section',{'id':'sidearm-roster-player-summary'}).text
        except:
            pass
    if bio == None:
        try:
            bio = soup.find('section',{'id':'sidearm-roster-player-bio sidearm-roster-player-section'}).text
        except:
            pass
    if bio == None:
        try:
            bio = soup.find('div', class_='tab-pane-contents p-3 synopsis').text
        except:
            pass
    if bio == None:
        try:
            bio = soup.find('div', class_='synopsis clearfix').text
        except:
            pass
    if bio == None:
        df.at[i, 'PAI'] = 'BIO ERROR'
        continue
    try:
        bio = bio.lower().split("personal")[0]
    except:
        pass
    if "basketball" in bio or 'point guard' in bio or 'shooting guard' in bio or 'small forward' in bio or 'power forward' in bio:
        basketball = 1
    if "baseball" in bio or 'pitcher' in bio or 'shortstop' in bio or 'short stop' in bio or 'catcher' in bio or 'outfielder' in bio:
        baseball = 1
    if "golf" in bio:
        golf = 1
    if "hockey" in bio:
        hockey = 1
    if "lacrosse" in bio or 'lax' in bio:
        lacrosse = 1
    if "powerlifting" in bio or "power lifting" in bio:
        powerlifting = 1
    if "rugby" in bio:
        rugby = 1
    if "soccer" in bio:
        soccer = 1
    if "tennis" in bio:
        tennis = 1
    if "wrestling" in bio or 'wrestle' in bio or 'wrestler' in bio:
        wrestling = 1
    if "volleyball" in bio:
        volleyball = 1
    if "swimming" in bio:
        swimming = 1
    if "track" in bio or 't&f' in bio or 'shot put' in bio or 'discus' in bio or 'high jump' in bio or 'long jump' in bio or 'sprinter' in bio or "triple jump" in bio:
        track = 1
    if 'state champ' in bio or 'state champion' in bio:
        notes = "State Champ"
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


df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\CollegeSpecialist-BioRun(9-3).csv", index=False)        
        
        
        
        
        