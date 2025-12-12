# -*- coding: utf-8 -*-
"""
Created on Fri May 12 09:54:17 2023

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
import re

df = pd.read_excel(r"C:\Users\jtsve\OneDrive\Documents\FindTwitters-3-5-17.xlsx")

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
for i in range(2068,len(df)):
    bio = None
    search = df.at[i, 'Unique ID']
    driver.get("https://x.com/explore")
    time.sleep(5)
    search_box = driver.find_element("xpath",'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input')
    search_box.send_keys(search)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    try:
        driver.find_element("xpath", '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span').click()
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[1]/div/div/button/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span[1]').click()
        time.sleep(2)
    except:
        continue
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        bio = soup.find('div', {'data-testid':'UserDescription'}).text
    except:
        bio = ""
    df.at[i, 'Twitter'] = driver.current_url
    df.at[i, 'Bio'] = bio
    
driver.quit()

df.to_excel(r"C:\Users\jtsve\OneDrive\Documents\FindTwitters(5-17)-RESULTS3.xlsx",index=False)


