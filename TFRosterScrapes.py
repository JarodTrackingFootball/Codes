# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:18:38 2025

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
import random


header_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36']


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


warnings.simplefilter(action='ignore', category=FutureWarning)

teams = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Master School List(HM Updated).xlsx")
    
df = pd.DataFrame({'Name':[''],'Milesplit URL':[''], 'HS Name':[''], 'HS State':[''],'Class':[''], 'Indoor':[''],'Outdoor':['']})

for i in range(17257,len(teams)):
    if teams.at[i, 'Milesplit URL'] != teams.at[i, 'Milesplit URL']:
        continue
    school = teams.at[i, 'Hudl Name']
    state = teams.at[i, 'State']
    team_url_org= teams.at[i, 'Milesplit URL']
    team_url = teams.at[i, 'Milesplit URL']
    try:
        team_url = team_url.split('school/')[0]
        if team_url != team_url_org:
            team_url = team_url + 'school'
    except:
        pass
    try:
        team_url = team_url + '/roster'
    except:
        continue
    headers = {'User-Agent': random.choice(header_list)}
    proxy = random.choice(proxies)
    try:
        r = requests.get(team_url, headers=headers, proxies = {'http':proxy, 'https':proxy})
        soup = BeautifulSoup(r.content, 'html.parser')
    except:
        continue
    cards = soup.find_all('li',class_='athlete-row data-row') 
    for card in cards:
        gender = None
        name = None
        class_= None
        ms_url = None
        indoor = None
        outdoor = None
        gender = card.find('div', class_='data-point w-20 w-md-10 text-lighter text-center text-uppercase column-gender').text
        if gender == 'f':
            continue
        name = card.find('div', class_='data-point w-30 w-md-50 d-flex align-items-center').find('a').text
        try:
            name = name.split(", ")[1] + " " + name.split(", ")[0]
        except:
            continue
        ms_url = card.find('div', class_='data-point w-30 w-md-50 d-flex align-items-center').find('a').get('href')
        class_ = card.find('div', class_='data-point w-20 text-lighter text-center column-grad-year').text
        indoor = card.find('div', class_='data-point w-20 w-md-10 text-lighter text-center').get('data-season-id')
        if indoor == '0':
            indoor = None
        else:
            indoor = True
        outdoor = card.find('div', class_='data-point w-10 text-lighter text-center').get('data-season-id')
        if outdoor == '0':
            outdoor = None
        else:
            outdoor = True
        if indoor == None and outdoor == None:
            continue
        new_row = {'Name':name,'Milesplit URL':ms_url, 'HS Name':school, 'HS State':state,
                   'Class':class_, 'Indoor':indoor,'Outdoor':outdoor}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\TFTeamsPlayerMaster(10-7)-RAW.csv",index=False)
