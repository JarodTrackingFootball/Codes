# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 09:52:37 2023

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
from selenium.webdriver.chrome.options import Options
import random

header_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']


proxy_username = 'jtnoah'
proxy_password = '6FD76B600F96231CD1E5A90035200C04'
proxy_ips = ['23.94.248.15:34555', '107.172.45.115:42720',
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

teams = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Master School List(HM Updated).xlsx")
database = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_080125-111719am.xlsx")

teams = teams[teams['MP Link'].isna() == False]

df = pd.DataFrame({'First Name':[''], 'Last Name':[''], 'HS Name':[''], 'Maxpreps URL':[''], 'Position':[''],
                   'Year':[''], 'Height':[''], 'Weight':['']})

#df = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\2024MaxprepsMaster.csv")

for i in range(15964,len(teams)):
    if i == 5000:
        player_data.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\2025MaxprepsMaster-1.csv", index=False)            
    if i == 10000:
        player_data.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\2025MaxprepsMaster-2.csv", index=False)            
                            
    url = teams.at[i, 'MP Link'] + 'football/roster'
    headers = {'User-Agent': random.choice(header_list)}
    proxy = random.choice(proxies)
    position = None
    height = None
    weight = None
    year = None
    first_name = None
    name = None
    last_name = None
    player_url = None
    school = teams.at[i, 'MP School']
    state = teams.at[i, 'State']
    city = teams.at[i, 'City']
    
    try:
        page = requests.get(url,headers=headers,proxies = {'http':proxy, 'https':proxy})
    except:
        time.sleep(150)
        page = requests.get(url,headers=headers,proxies = {'http':proxy, 'https':proxy})
    soup = BeautifulSoup(page.text, 'lxml')
    try:
        cards = soup.find('tbody').find_all('tr')
    except:
        continue
    
    table = soup.find('table')
    df1=pd.read_html(str(table))[0]
    
    df1['First Name'] = None
    df1['Last Name'] = None
    df1['Maxpreps URL'] = None
    df1['HS Name'] = school
    df1['HS City'] = city
    df1['HS State'] = state
    df1 = df1.replace('-','')
    for r in range(len(df1)):
        position = None
        height = None
        weight = None
        year = None
        first_name = None
        name = None
        last_name = None
        player_url = None
        hs_class = None
        try:
            name = df1.at[r,'Player']
        except:
            continue
        try:
            df1.at[r, 'First Name'] = name.split(" ")[0]
            words = name.split()
            df1.at[r, 'Last Name'] = " ".join(words[1:])
        except:
            pass
        weight = df1.at[r,'Weight']
        try:
            weight = weight.replace(" lbs","")
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
        year = df1.at[r, 'Grade']
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
        df1.at[r, 'Grade'] = hs_class
    
    for r in range(len(cards)):
        player_url = cards[r].find('a').get('href')
        df1.at[r, 'Maxpreps URL'] = 'https://www.maxpreps.com/' + player_url
    if i == 1:
        player_data = df1.copy()
    else:
        frames= [player_data,df1]
        player_data = pd.concat(frames)
    
#temp = player_data.copy()

player_data = player_data.drop_duplicates()


df = pd.merge(player_data, database[['Slug','Maxpreps URL']], on='Maxpreps URL', how='left')

df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\2025MaxprepsMaster.csv", index=False)            
            