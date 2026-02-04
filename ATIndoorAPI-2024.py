# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 10:43:35 2024

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

warnings.simplefilter(action='ignore', category=FutureWarning)


database = pd.read_excel(r"C:\Users\jtsve\Downloads\TF HS Player Export 1-27-2026.xlsx")


last_day_val = 100

bad_links = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\TrackFlagList.xlsx")
bad_urls = bad_links['URL']


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

cks = '_ga=GA1.1.215681024.1745846030; __stripe_mid=567ab0fe-b527-4689-8b25-a98a92971fc33f44f0; CSUser=username=2560693&emailAddress=jtn47316@gmail.com&CommonName=JT Noah&EnableDisplayName=true; __qca=P1-17d32828-f180-4418-bc85-d9df98bac37f; _ncid=38ed48ee4447c258cec7bb393403067e; _au_1d=AU1D-0100-001751996125-ZWPWPDC8-493C; __gads=ID=e8bfe3ebebd2ccce:T=1745846034:RT=1757088866:S=ALNI_MZG-TpiT7CLcF154LX4aQ5tZ-GMbQ; __gpi=UID=000010a328f33fbf:T=1745846034:RT=1757088866:S=ALNI_Maf0ZxSQ4pMIbXOeWNcyL9u9NzRWA; _cc_id=3cc0c66df4619fc133c8404938d436b0; _ga_BY35Y57BMZ=GS2.1.s1767103790$o4$g0$t1767103791$j60$l0$h0; _ga_FVWZ0RM4DH=GS2.1.s1767103791$o4$g0$t1767103791$j60$l0$h0; _ga_ZXKS3ZXZ0V=GS2.1.s1768172880$o6$g0$t1768172880$j60$l0$h0; _ga_CV6QCFM8SJ=GS2.1.s1768172864$o21$g1$t1768172896$j28$l0$h0; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%2294aed4c6-f736-4ca8-8421-f26601a3d8b6%5C%22%2C%5B1763408245%2C772000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol8at52WDJw1fv3Vjo40M403IBSE_Q9iT1Tah12eCAwFlSQYYo69OO82234H0eIYtddWSun7wP7-FvXsNHzPcNynC_ufNGzMnJA46CpIWKdxkeBGrItC-OXwfVYwb7d_2hf3dAEPFpJTnn61d19HGsXVnmA8kQ%3D%3D%22%5D%5D; .AspNet.SharedCookie=CfDJ8C-EPVdx7spCk3oxADTNfA-11SObWbAIu8jJwWQpZDwLGTMOUNApOnqIlGMSvThJqzhog8R4ydunnggFoIRuVCBVRP0QoAYFB7Tbh_J_0f4B7YKh8K4_NglpkiAZqgWRLnfNLrfzpS4HDgEPPq-TdzG0EcwiQzWhv3q-DQOg1IncNOISKmpMd-HdESvMBYlBdQ9w8feRZU2FXfgva5rkryYNRt1pbz-8Zh_jOkvPfuK1nsRVKehHn_xqh3nU9gi52uXCyUTzni-2GkAVR-NWB0Cg5tlO8jS6nsZZwj4vTIstHjCZls11Udo5NfnnJMs_eB-RMS68o6UkVYXaURJSK1G-Tq0SBkhygOodtnUdTOKQFwgiXLFjF72ndzNuQQSrWcrMzToRKpVlyQNdaHC4LspR8CWWS4mJfxpEEGONZqgVfBxRlkyE1NL7_eYiNYOZTeHZt_sQ462r-WIbTSgc4SwxVwi6aZRBlm7kgagHoGsRpfsOE3J9K5vO6tgOyQw7fHh-8q-XLEE-7CxswlW6SunFMwVKovjNP3NkicTbhqukOhBEscu3Z5dsyjMiM9yeDFN85svYwZQ-YFEZQIAJ50mdKQIvreyuz7W2bF_hpWV5VkSePlQHoeRbSvQotGwpo5bbtWE1NL3XZi8-38IAUey4nov9rxUjw0E6dI-tNCV4n4uDaMTFZEAZrEZ87Z08YM5_8HdW-98owQa1OkU5WCc; ANETSettings=guid=d8574322-d8f8-4d0c-91de-6a2b1cfa6814&Sport=TF&User=2560693&Team=3050; __stripe_sid=e84d4269-39c1-485b-b307-f2c0fc231833f22fd7'


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
        


events_raw = ['55m', '60m','55mh','60mh', '200m', '400m','300m',
              'shot','hj', 'pv', 'lj', 'tj']


event_codes = {'55m':'55M', '60m':'60M','55mh':'55HH','60mh':'60HH', '200m':'200M', '400m':'400M','300m':'300M', 
              'shot':'Shot Put','hj':'High Jump', 'pv':'Pole Vault', 'lj':'Long Jump', 'tj':'Triple Jump'}

cutoffs_track = { '200m':29, '400m':70}

cutoffs_field = {'shot':2500,'hj':500, 'pv':800, 'lj':1500}

df = pd.DataFrame({'URL':[''],'Name':[''],'School':[''],'Class':[''], 'Event':[''],'State':[''],'Date':[''], 'Result':[''], 'State':[''],
                   'Meet':[''],'Wind Error':['']})


def scrape_rank(event_code):
    page = 1
    df1 = pd.DataFrame({'Athletic URL':[''],'Name':[''],'School':[''], 'Class':[''],'State':[''],'Event':[''],'Date':[''], 'Result':[''], 'State':[''],
                       'Meet':[''],'Wind Error':['']})
    event = event_codes[event_code]
    run = 0
    while True:
        headers = {'User-Agent': random.choice(header_list), 'cookie':cks}
        proxy = random.choice(proxies)
        payload = {'divListId':173005, 'eventShort':event_code,'gender':'m','mode':'list', 'reportType':'div','qParams':{'page':page}}
        url = 'https://www.athletic.net/api/v1/tfRankings/GetRankings'
        response1 = requests.post(url, headers=headers,proxies = {'http':proxy, 'https':proxy}, json=payload)
        r1 = response1.json()
        page = page+1
        try:
            athletes = r1['groupedRankings'][0]
            run = 0
        except:
            if run < 5:
                run = run + 1
            else:
                return(df1)
        if run == 0:
            for ath in athletes:
                url = None
                name = None
                result = None
                meet = None
                wind = None
                state = None
                pc = None
                wind_error = False
                player_class = None
                if event in ['55M','60M', '200M', '55HH', '400M', '60HH','300M','60HH']:
                    if ath['FAT'] != 1:
                        continue
                    
                url = 'https://www.athletic.net/athlete/'+str(ath['AthleteID'])+'/track-and-field/high-school'
                name = ath['AthleteName']
                result = str(ath['SortIntCalc'])
                if event in ['55M','60M', '200M', '55HH', '400M', '60HH','300M','60HH']:
                    if len(result) == 4:
                        result = str(result[0] + "." + result[1:3])
                    elif len(result) == 5:
                        result = str(result[0:2] + "." + result[2:4])
                    elif len(result) == 6:
                        result = str(result[0:3] + "." + result[3:5])
                else:
                    result = float(result)
                    result = (20000000-result)/1000
                    ft = int(result/12)
                    inches = int(result - (ft*12))
                    if inches < 10:
                        inches = f"0{inches}"
                    else:
                        inches = str(inches)
                    result = f"{ft}{inches}"
                try:
                    state = ath['State']
                except:
                    state = None
                try:
                    meet = ath['MeetName']
                except:
                    meet = None
                try:
                    meet = meet + " TF Meet"
                except:
                    pass
                try:
                    school = ath['TeamName']
                except:
                    school = None
                try:
                    pc = ath['GradeID']
                except:
                    pc = None
                if pc == 12:
                    player_class = 2026
                elif pc == 11:
                    player_class = 2028
                elif pc == 10:
                    player_class = 2028
                elif pc == 9:
                    player_class = 2029
                if wind!=None:
                    meet = f"{meet} ({wind}w)"
                try:
                    date = ath['ResultDate'].split("T")[0]
                    month = date.split("-")[1]
                    year = date.split("-")[0]
                    day = date.split("-")[2]
                    date = f"{month}/{day}/{year}"
                except:
                    pass
                date_val = int(f"{month}{day}")
                if date_val <= last_day_val:
                    continue
                else:
                    new_row = {'Athletic URL':url,'Name':name,'School':school,'Class':player_class,'State':state, 'Event':event,'Date':date, 'Result':result, 'State':state,
                                      'Meet':meet,'Wind Error':wind_error}
                    df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
                
                
#with requests.session() as s:
#    s.post(login, data=payload)
for event1 in events_raw:
    df1 = scrape_rank(event1)
    frames= [df,df1]
    df = pd.concat(frames)
        
df = df.reset_index(drop=True)

index_names = df[df['URL'] == ''].index

df.drop(index_names, inplace=True)
df = df.reset_index(drop=True)


#df['ID'] = None
#df['Unique ID'] = None

index_names = database[database['Athletic URL'] != database['Athletic URL']].index
database.drop(index_names, inplace = True)
database = database.reset_index(drop=True)
df = df.reset_index(drop=True)

#df['Slug'] = df['URL'].map(database.set_index('Athletic URL')['Slug'])

df = pd.merge(df, database[['Athletic URL', 'Slug']], on='Athletic URL',how='left')

today =date.today()
today = today.strftime("%b-%d-%Y")
    
df.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\'' + str(today) + 'AIndoorRankingsRAW.csv', index=False)

template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")

for i in range(0,len(df)):
    last_name = None
    template.at[i, 'Athletic URL'] = df.at[i, 'Athletic URL']
    try:
        template.at[i, 'First Name'] = df.at[i, 'Name'].split(" ")[0]
        words = df.at[i, 'Name'].split()
        last_name = " ".join(words[1:])
        template.at[i, 'Last Name'] = last_name
    except:
        template.at[i, 'Last Name'] = df.at[i, 'Name']
    #template.at[i,'TF Year'] = 2024
    template.at[i,'TF Meet'] = df.at[i, 'Meet']
    if df.at[i, 'Wind Error'] == True:
        template.at[i, '247 Key'] = "Wind Error"
    event = df.at[i, 'Event']
    template.at[i, event] = df.at[i, 'Result']
    template.at[i, 'Slug'] = df.at[i, 'Slug']
    template.at[i, 'HS Name'] = df.at[i, 'School']
    template.at[i, 'HS State'] = df.at[i, 'State']
    template.at[i, 'HS Class'] = df.at[i, 'Class']
    template.at[i, 'Track'] = 1
    template.at[i, 'TF Date'] = df.at[i, 'Date']

events_tf = list(event_codes.values())
for event in events_tf:
    temp_df = template.dropna(subset=[event])
    temp_df = temp_df.dropna(subset=['Slug'])
    temp_df['HS Class'] = None
    temp_df['HS State'] = None
    temp_df['HS Name'] = None
    temp_df['Last Name'] = None
    temp_df['First Name'] = None
    temp_df['Athletic URL'] = None
    temp_df.to_excel(r"C:\Users\jtsve\OneDrive\Documents\a"+event+"Updates"+".xlsx",index=False)


#driver.quit()

template.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\'' + str(today) + 'AIndoorRankings.csv', index=False)

