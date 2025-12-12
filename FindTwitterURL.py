# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 08:19:12 2023

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

#Load in File
df = pd.read_excel(r"C:\Users\jtsve\Downloads\TF Master CFB Staff Directory 8.12.25.xlsx")


#df1 = pd.DataFrame({'Email':[''],'ID':[''],'Twitter URL':[''], 'Twitter Bio':['']})
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
    driver.get("https://www.bing.com/search?q="+search)
    time.sleep(1)
    #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'b_content')))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    cards = soup.find_all('li', class_='b_algo')
    return cards

for i in range(2068,len(df)):
    if df.at[i, 'Twitter'] == df.at[i, 'Twitter']:
        continue
    """
    if type(df.at[i, 'Twitter URL']) == str:
        continue
    """
    #email = df.at[i, 'E-mail']
    search = df.at[i, 'Unique ID'] + " x"
    cards = search_bing(search)
    cards = cards[0:2]
    for card in cards:
        if "twitter" in card.text.lower():
            page = card.find('a').get('href')
            if "twitter" in page:
                try:
                    driver.get(page)
                    time.sleep(2)
                except:
                    pass
            else:
                continue
            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                bio = soup.find('div', {'data-testid':'UserDescription'}).text
                df.at[i, 'Twitter'] = driver.current_url
                df.at[i, 'Bio'] = bio
                #df1 = df1.append({'Email':email,'ID':df.at[i, 'ID'],'Twitter URL':driver.current_url,'Twitter Bio':bio},ignore_index=True)
            except:
                continue

            break
        
driver.quit()

df.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\CFBStaff-Twitters(9-4).xlsx')