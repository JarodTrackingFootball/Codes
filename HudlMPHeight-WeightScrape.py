# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 09:39:59 2023

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

df = pd.read_excel(r"C:\Users\jtsve\Downloads\HMPTrackGuys(2-2).xlsx")


options = Options()
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)


for i in range(0,len(df)):
    twitter = None
    last_highlight = None
    if df.at[i, 'Hudl URL'] != df.at[i, 'Hudl URL']:
        continue
    """
    try:
        driver.get(df.at[i, 'Hudl URL'])
    except:
        driver.quit()
        driver = webdriver.Chrome(options=options)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    if soup.find_all('div', class_='feeditem shared-highlight'):
        highlight = 1
        highlights = soup.find_all('div', class_='feeditem shared-highlight')
    else:
        highlight = 0
        last_highlight = None

    
    if highlight == 1:
        if highlights[0].get('data-feed-content-id') == 'pinned-feed-item':
            try:
                last_highlight = highlights[1].find('p', class_='uni-text--micro uni-text--nonessential uni-margin--eighth--top').text
            except:
                 last_highlight = highlights[0].find('p', class_='uni-text--micro uni-text--nonessential uni-margin--eighth--top').text
        else:
            last_highlight = highlights[0].find('p', class_='uni-text--micro uni-text--nonessential uni-margin--eighth--top').text
    """
    url_go = df.at[i, 'Hudl URL']+'/about'
    try:
        driver.get(url_go)
    except:
        driver.quit()
        driver = webdriver.Chrome(options=options)
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/div[1]/div/section/div[2]/div[1]/div[1]/h2')))
    except:
        continue
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        school_raw = soup.find('p', class_='uni-text--large u-text-overflow').text
        school = school_raw.split(" -")[0]
    except:
        pass
    try:
        school = school.split(" High School")[0]
    except:
        pass
    
    height = None
    weight = None
    pos = None
    year = None
    hs_class = None
    city = None
    
    try:
        city = soup.find_all('p', class_='uni-text--large u-text-overflow')[1].text
        city = city.split(",")[0]
    except:
        pass
    
    cards = soup.find_all('li', class_='styles__essential-item___1VOaL')
    for card in cards:
        try:
            if "height" in card.text.lower():
                raw_height = card.text.split(": ")[1]
                height = (int(raw_height.split("'")[0]) * 12) + int(raw_height.split("'")[1].split("\"")[0])
            elif "weight" in card.text.lower():
                weight = card.text.split(": ")[1]
                weight = weight[:-3]
                weight = int(weight)
            elif "position" in card.text.lower():
                pos = card.text.split(": ")[1]
                pos = pos.replace(", ","/")
                if "SF" in pos or "PF" in pos or "SG" in pos or "PG" in pos:
                    pos = None
            if "class of" in card.text.lower():
                try:
                    hs_class = int(card.text.split(": ")[1])
                except:
                    pass
        except:
            continue

    df.at[i, "HS Height"] = height
    #if df.at[i, 'HS Name'] != df.at[i, 'HS Name']:
        #df.at[i, 'HS Name'] = school
    df.at[i, 'HS Weight'] = weight
    if df.at[i, 'HS Positions'] != df.at[i, 'HS Positions']:
        df.at[i, 'HS Positions'] = pos

    #df.at[i, 'HS Class'] = hs_class

    if df.at[i, 'HS City'] != df.at[i, 'HS City']:
        df.at[i, 'HS City'] = city

    try:
        picture = soup.find('img', class_='uni-avatar__img').get('src')
        if picture == 'https://sc.hudl.com/images/thumb-user.svg':
            picture = None
    except:
        picture = None
        
    df.at[i, 'Player Photo'] = picture

    
    info = soup.find_all('li', class_='styles__essential-item___1VOaL')
    for inf in info:
        if inf.find('h5', class_='uni-item-title uni-item-title--caps styles__essential-item__label___259Vl').text == 'Twitter: ':
            twitter = inf.find('a', class_='uni-link--article styles__essential-item__value___2T_jc').text
            twitter = 'https://x.com/' + twitter[1:]
            has_twitter = True
        else:
            twitter = None
            has_twitter = False
    #Other sports
    try:
        bio = soup.find('div', class_='styles__team-history-card__list___3r6Jq').text
    except:
        bio = ''
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
    
    df.at[i, 'X URL'] = twitter
    df.at[i, 'Basketball'] = basketball
    df.at[i, 'Baseball'] = baseball
    df.at[i, 'Golf'] = golf
    df.at[i, 'Hockey'] = hockey
    df.at[i, 'Lacrosse'] = lacrosse
    df.at[i, 'Rugby'] = rugby
    df.at[i, 'Soccer'] = soccer
    df.at[i, 'Swimming'] = swimming
    df.at[i, 'Volleyball'] = volleyball
    df.at[i, 'Tennis'] = tennis
    df.at[i, 'Wrestling'] = wrestling
    df.at[i, 'Track'] = track
    #df.at[i, 'GPA'] = last_highlight
    
driver.quit()
df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\NewGuysTrack(2-2).csv", index=False)
