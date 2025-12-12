# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 12:01:12 2025

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
import numpy as np
from datetime import datetime

daily = '-4EWBOctxq3o30yFX09lj'

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

df = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\O-HSTeamMaster.xlsx")


for i in range(0,len(df)):
    nrank = srank = twitter = insta = web = logo = bio = mascott = address = zip_code = None
    slug = df.at[i, 'Team URL'].split('school/')[1][:-1]
    url = 'https://www.on3.com/_next/data/'+daily+'/high-school/'+slug+'.json?id='+slug
    headers = {'User-Agent': random.choice(header_list)}
    proxy = random.choice(proxies)
    r = requests.get(url, headers=headers,proxies = {'http':proxy, 'https':proxy})
    r = r.json()
    try:
        if r['pageProps']['__N_REDIRECT_STATUS'] == 308:
            continue
    except:
        pass
    try:
        r['pageProps']
    except:
        continue
    try:
        nrank = r['pageProps']['rankings']['nationalRank']
        srank = r['pageProps']['rankings']['stateRank']
    except:
        nrank = None
        srank = None
    try:
        twitter = 'https://x.com/' + r['pageProps']['orgInfo']['socials']['footballTwitter']
    except:
        twitter = None
    try:
        insta = 'https://instagram.com/' + r['pageProps']['orgInfo']['socials']['footballInstagram']
    except:
        insta = None
    web  = r['pageProps']['orgInfo']['website']
    try:
        logo ='https://on3static.com/cdn-cgi/image/height=120,width=120,quality=95,fit=contain'+ r['pageProps']['orgInfo']['defaultAsset']['source']
    except:
        logo = None
    bio = r['pageProps']['orgInfo']['bio']
    mascott = r['pageProps']['orgInfo']['mascot']
    zip_code = r['pageProps']['orgInfo']['zipCode']
    address = r['pageProps']['orgInfo']['address']
    
    df.at[i,'National Rank'] = nrank
    df.at[i,'State Rank'] = srank
    df.at[i,'Twitter'] = twitter
    df.at[i,'Instagram'] = insta
    df.at[i,'Website'] = web
    df.at[i,'Logo'] = logo
    df.at[i,'Bio'] = bio
    df.at[i,'Mascott'] = mascott
    df.at[i,'Address'] = address
    df.at[i,'Zip Code'] = zip_code
    
df.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\O-HSTeamMaster-ExtraInfo(10-7).xlsx")