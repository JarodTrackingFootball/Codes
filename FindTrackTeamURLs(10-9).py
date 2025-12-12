# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 13:35:59 2025

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
df = pd.read_excel(r"C:\Users\jtsve\Downloads\New CFB link finder.xlsx")


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
    time.sleep(3)
    #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'b_content')))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    cards = soup.find_all('h2', class_='LnpumSThxEWMIsDdAT17 CXMyPcQ6nDv47DKFeywM')
    return cards


for i in range(0, len(df)):
    time.sleep(2)
    if df.at[i, 'HS Name'] != df.at[i, 'HS Name']:
        continue
    try:
        name = df.at[i, 'First Name'] + " " + df.at[i, 'Last Name']
        school = df.at[i, 'HS Name']
    except:
        continue
    college = df.at[i, '247 Key']
    if type(school) == float:
        school = "Valkommen"

    #First look for Hudl URL
    if type(df.at[i, 'Hudl URL']) != str:
        search = df.at[i, 'Ryzer ID'] + " football hudl"
        cards = search_bing(search)
        cards = cards[0:1]
        for card in cards:
            card = card.find('a').get('href')
            if "hudl" not in card or "profile" not in card:
                continue
            try:
                card.lower()
            except:
                continue
            try:
                driver.get(card)
                time.sleep(3)
            except:
                continue
            card = driver.current_url
            if "hudl.com/profile" in card.lower():
                page = card
                if "hudl" in page.lower() == False:
                    continue

                try:
                    hudl_name = driver.find_element(By.CLASS_NAME, 'uni-headline--1').text
                except:
                    continue
                page = extract_left_of_6th_slash(page)
                try:
                    text = driver.find_element(By.CLASS_NAME, 'uni-link--implied').text
                    text = text.lower()
                except:
                    text = ""
                if "football" in text:
                    if len(school.split(" ")) > 1:
                        if school.split(" ")[0].lower() in text.lower() or school.split(" ")[1].lower() in text.lower(): 
                            if df.at[i, 'Last Name'].lower() in hudl_name.lower() and df.at[i, 'First Name'].lower() in hudl_name.lower():
                                df.at[i, 'Hudl URL'] = page
                                break
                            else:
                                if hudl_name.split(' ')[0].lower() in df.at[i,'First Name'].lower():
                                    df.at[i, 'Hudl URL'] = page
                                    #df.at[i, 'Updated'] = 'Hudl'
                                    break
                    else:
                        if school.lower() in text.lower() or college.lower() in text.lower():
                            if df.at[i, 'Last Name'].lower() in hudl_name.lower() and df.at[i, 'First Name'].lower() in hudl_name.lower():
                                df.at[i, 'Hudl URL'] = page
                                #df.at[i, 'Updated'] = 'Hudl'
                                break
                            else:
                                if hudl_name.split(' ')[0].lower() in df.at[i,'First Name'].lower():
                                    df.at[i, 'Hudl URL'] = page
                                    #df.at[i, 'Updated'] = 'Hudl'
                                    break                 

    #Check MaxPreps
    if type(df.at[i, 'Maxpreps URL']) != str:
        search = df.at[i, 'Ryzer ID'] + " football maxpreps"
        time.sleep(2)
        cards = search_bing(search)
        cards = cards[0:2]
        for card in cards:
            card = card.find('a').get('href')
            if "maxpreps" not in card.lower():
                continue
            try:
                card.lower()
            except:
                continue
            try:
                driver.get(card)
                time.sleep(3)
            except:
                continue
            card = driver.current_url
            if "maxpreps.com" in card.lower() and "athlete" in card.lower():
                page = card
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                if "maxpreps" in page.lower() == False:
                    break
                if "athlete" in page.lower() == False:
                    break
                if "roster" in page.lower():
                    break
                if "schedule" in page.lower():
                    break    
                try:
                    text = "football"
                except:
                    break   
                if 'football' in text.lower():
                    if df.at[i, 'Last Name'].lower() in page.lower() and df.at[i, 'First Name'][0:2].lower() in page.lower():
                        try:
                            text = soup.find('a', class_='sc-51f90f89-0 dhSYvb school-name').text
                        except:
                            text = 'Ooga Booga'
                        if len(school.split(" ")) > 1:
                            if school.split(" ")[0].lower() in text.lower() or school.split(" ")[1].lower() in text.lower():
                                df.at[i, 'Maxpreps URL'] = page
                                #df.at[i, 'Updated'] = 'MP'
                                break
                        else:
                            if school.lower() in text.lower():
                                df.at[i, 'Maxpreps URL'] = page
                                #df.at[i, 'Updated'] = 'MP'
                                break
"""
    #Check Athletic
    if type(df.at[i, 'Athletic URL']) != str:
        search = df.at[i, 'Ryzer ID'] + " athletic.net"
        cards = search_bing(search)
        cards = cards[0:2]
        for card in cards:
            card = card.find('a').get('href')
            try:
                if "athletic.net" in card.lower() and "athlete" in card.lower():
                    page = card
                    try:
                        driver.get(page)
                    except:
                        continue
                    page = driver.current_url
                    if "athletic" in page.lower() == False:
                        break
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    try:
                        ath_name = soup.find('a', class_='me-2 text-sport').text
                        ath_school = soup.find('h2', class_='mb-0').text
                    except:
                        break
                    if df.at[i, 'First Name'][0:2].lower() in ath_name.lower() and df.at[i, 'Last Name'].lower() in ath_name.lower():
                        if len(school.split(" ")) > 1:
                            if school.split(" ")[0].lower() in ath_school.lower() or school.split(" ")[1].lower() in ath_school.lower():
                                df.at[i, 'Athletic URL'] = page
                                break
                        else:
                            if school.lower() in ath_school.lower():
                                df.at[i, 'Athletic URL'] = page
                                break
            except:
                pass

    #Check Milesplit
    if type(df.at[i, 'Milesplit URL']) != str:
        search = df.at[i, 'Ryzer ID'] + " milesplit"
        cards = search_bing(search)
        cards = cards[0:2]
        for card in cards:
            if "milesplit.com/athletes/" in card.text.lower():
                page = card.find('a').get('href')
                
                try:
                    driver.get(page)
                    time.sleep(1.5)
                except:
                    break
                page = driver.current_url
                if "milesplit" in page.lower() == False:
                    break
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                try:
                    ms_name = soup.find('h1',class_='athlete-name').text.lower()
                    ms_school = soup.find('span',class_='current-school').text.lower()
                except:
                    break
                
                if df.at[i, 'Last Name'].lower() in ms_name and df.at[i, 'First Name'][0:2].lower() in ms_name:
                    if len(school.split(" ")) > 1:
                        if school.split(" ")[0].lower() in ms_school.lower() or school.split(" ")[1].lower() in ms_school.lower():
                            df.at[i, 'Milesplit URL'] = page
                            break
                    else:
                        if school.lower() in ms_school.lower():
                            df.at[i, 'Milesplit URL'] = page
                            break
                else:
                    break
"""

driver.quit()  
                  
df.to_excel(r"C:\Users\jtsve\OneDrive\Documents\CFBNewGuys-Links-3.xlsx", index=False)                  
                    
