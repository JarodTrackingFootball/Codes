# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 10:06:51 2026

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
from selenium.webdriver.chrome.options import Options
import random
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

database = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_121825-081353am.xlsx")

database = database[database['DirectAthletics URL'] == database['DirectAthletics URL']]

database = database.reset_index()

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
 
event_dic = {'55m':'55M', '60m':'60M','55m H':'55HH','60m H':'60HH','200m':'200M', '300m':'300M', '400m':'400M',
             '100m':'100M','Discus Throw':'Discus',
             '4 x 400m Relay':'1600R','4 x 100m Relay':'400R','4 x 200m Relay':'800R', '4 x 800m Relay':'3200R',
             '110m H':'110HH','300m H':'300IH', '400m H':'400H'}
       
df = pd.DataFrame() 

for i in range(len(database)):
    url = database.at[i, 'DirectAthletics URL']
    slug = database.at[i, 'Slug']
    if 'directathletics' in url:
        headers = {'User-Agent': random.choice(header_list)}
        proxy = random.choice(proxies)
        r = requests.get(url,headers=headers,proxies = {'http':proxy, 'https':proxy}) 
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            table = soup.find('table', class_='tablesorter')
            df1=pd.read_html(str(table))[0]
        except:
            continue
        df1['Slug'] = slug
        frames= [df,df1]
        df = pd.concat(frames)
        
        
df['Event'] = df['Event'].map(event_dic).fillna(df['Event'])
df = df[df['Event'] == df['Event']]
df = df.reset_index()
for i in range(0,len(df)):
    event = df.at[i, 'Event']
    result = df.at[i, 'Time/Mark']
    if event == "Discus" or event == "Shot Put" or event == "Long Jump" or event == 'Triple Jump' or event == "High Jump" or event == 'Pole Vault' or event == 'Javelin':
        if "m" in result:
            result = result.replace('m','')
            text = float(str(result).split('m')[0])
            inches = text*39.3700787
            ft = int(inches/12)
            inches = inches - (ft*12)
            if inches < 10:
                inches = f"0{inches}"
            else:
                inches = str(inches)
            result = f"{ft}{inches}"
            result = float(result)
            result = int(result)
            result = str(result)
        else:
            try:
                inches = int(float(result.split('\' ')[1].replace('"','')))
            except:
                continue
            if inches < 10:
                inches = f"0{inches}"
            else:
                inches = str(inches)
            result = result.split('\' ')[0] + inches
            result = float(result)
    else:
        if event != '800':
            try:
                result = float(result)
            except:
                pass
    df.at[i, 'Time/Mark'] = result
df = df[~df['Time/Mark'].astype(str).str.contains(r'[A-Za-z]', na=False)]

template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")
for i in range(0,len(df)):
    try:
        event = df.at[i, 'Event']
        template.at[i, event] = df.at[i, 'Time/Mark']
    except:
        continue
    template.at[i, 'TF Date'] = df.at[i, 'Date']
    #template.at[i, 'Athletic URL'] = df.at[i, 'URL']
    #template.at[i,'TF Year'] = df.at[i, 'Year']
    try:
        template.at[i,'TF Meet'] = (df.at[i, 'Meet'] + " TF Meet").strip()
    except:
        pass
    template.at[i, 'Slug'] = df.at[i, 'Slug']
    template.at[i, 'Track'] = 1
template.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\TrackRun(1-7).csv",index=False)
        
events_tf = ['55M', '60M','55HH', '60HH', '100M', '110HH', '200M', '300M', '300IH','400M','400H',
             '800','400R','800R','1600R','3200R','Shot Put','Discus', 'Javelin','High Jump',
             'Long Jump', 'Triple Jump', 'Pole Vault']

for event in events_tf:
    temp_df = template.dropna(subset=[event])
    #temp_df = temp_df.dropna(subset=['Slug'])
    temp_df.to_excel(r"C:\Users\jtsve\OneDrive\Documents\/"+event+"Updates-Other"+".xlsx",index=False)
        
        
        
        
        
    