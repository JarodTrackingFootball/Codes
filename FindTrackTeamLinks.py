# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 09:41:26 2024

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

def extract_left_of_6th_slash(text):
    # Split the text by "/"
    parts = text.split("/")
    
    # Check if there are enough parts to extract up to the 6th "/"
    if len(parts) >= 6:
        # Join everything before the 6th "/"
        return "/".join(parts[:6])
    else:
        # If there are not enough parts, return the original text
        return text
    
#Load in File
df = pd.read_excel(r"C:\Users\jtsve\Downloads\Master School List.xlsx")


options = Options()
options.add_argument("enable-automation")
options.add_argument("--mute-audio")
#options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

def search_bing(search):
    driver.get("https://duckduckgo.com/?t=h_&q="+search+"&ia=web")
    time.sleep(3)
    #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'b_content')))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    cards = soup.find_all('h2', class_='LnpumSThxEWMIsDdAT17 CXMyPcQ6nDv47DKFeywM')
    return cards



for i in range(44, len(df)):
    time.sleep(2)
    hs_name_ms = None
    hs_name_ath = None
    if df.at[i, 'MATCH SLUG HUDL'] != df.at[i, 'MATCH SLUG HUDL']:
        continue
    if df.at[i, 'Milesplit URL'] == 'AA PRIORITY FIND':
        search = df.at[i, 'MATCH SLUG HUDL'] + " Milesplit"
        cards = search_bing(search)
    
        try:
            card = cards[0]
        except:
            continue
        card = card.find('a').get('href')
        try:
            card.lower()
        except:
            continue
        if "milesplit" in card.lower():
            page = card
            #If the page is a hudl page, check that they play football
            try:
                driver.get(page)
                time.sleep(2)
            except:
                continue
            page = driver.current_url
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                hs_name_ms = soup.find('section', class_='jumbotron-content').text.strip()
                try:
                    hs_name_ms = hs_name_ms.split('\n')[0]
                except:
                    pass
                df.at[i, 'Milesplit Name'] = hs_name_ms
                df.at[i, 'Milesplit URL'] = page
            except:
                pass

        if df.at[i, 'Athletic URL'] == 'AA PRIORITY FIND':
            search = df.at[i, 'MATCH SLUG HUDL'] + " Athletic.net"
            cards = search_bing(search)
            try:
                card = cards[0]
            except:
                continue
            card = card.find('a').get('href')
            try:
                card.lower()
            except:
                continue
            if "athletic" in card.lower():
                page = card
                #If the page is a hudl page, check that they play football
                try:
                    driver.get(page)
                    time.sleep(2)
                except:
                    continue
                page = driver.current_url
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                try:
                    hs_name_ms = soup.find('h2', class_='mb-0').text.strip()
                    df.at[i, 'Athletic Name'] = hs_name_ms
                    df.at[i, 'Athletic URL'] = page
                except:
                    pass
        
driver.quit()  

df.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\MasterSchoolList-AddedTrack.xlsx",index=False)      
        