# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 09:11:51 2025

@author: jtsve
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 11:38:46 2025

@author: jtsve
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 11:28:42 2022

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
df = pd.read_excel(r"C:\Users\jtsve\Downloads\TF Master CFB Staff Directory 8.12.25 (1).xlsx")
df['Twitter Bio'] = None

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
#driver.set_page_load_timeout(10)

def search_bing(search):
    driver.get("https://duckduckgo.com/?t=h_&q="+search+"&ia=web")
    time.sleep(2)
    #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'b_content')))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    cards = soup.find_all('h2', class_='LnpumSThxEWMIsDdAT17 CXMyPcQ6nDv47DKFeywM')
    return cards

for i in range(7217,len(df)):
    if df.at[i, 'Twitter'] == df.at[i, 'Twitter']:
        continue
    
    search = df.at[i, 'Unique ID'] + ' Twitter'
    cards = search_bing(search)
    cards = cards[0:2]
    for card in cards:
        card = card.find('a').get('href')
        if "x.com" not in card and "twitter.com" not in card:
            continue
        
        driver.get(card)
        try:
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[1]/div[3]/div/div/span')))
        except:
            continue
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            bio = soup.find('div', {'data-testid':'UserDescription'}).text
        except:
            bio = ""
        df.at[i, 'Twitter'] = card
        df.at[i, 'Twitter Bio'] = bio
        continue
    
df.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\StaffTwitters.xlsx", index=False)   
