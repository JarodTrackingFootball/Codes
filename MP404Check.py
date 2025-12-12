# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 10:24:30 2025

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
import random
from selenium.webdriver.chrome.options import Options
import json


df = pd.read_excel(r"C:\Users\jtsve\Downloads\tf hs export 11.5.xlsx")

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920x1080")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

df['MP 404'] = None

for i in range(0,len(df)):
    if df.at[i, 'Maxpreps URL'] == df.at[i, 'Maxpreps URL']:
        player_url = df.at[i, 'Maxpreps URL']

        driver.get(player_url)
        time.sleep(1.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        try:
            temp = soup.find('a',class_='sc-63c3c392-2 ctOOgc athlete-name')
        except:
            df.at[i, 'MP 404'] = 1
            
driver.quit()
df.to_csv(r"C:\Users\jtsve\Downloads\MP404s.csv",index=False)
