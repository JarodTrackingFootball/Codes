# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 09:09:26 2025

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

col_dic = {}

conversions = pd.read_csv(r'C:\Users\jtsve\OneDrive\Desktop\Template Files\ScrapingConversion.csv')
school_dic = conversions.set_index('R')['T'].to_dict()
school_dic['Virginia Military'] = 'Virginia Military Institute'
    
for y in range(1,19):

    url = 'https://api.on3.com/rdb/v1/team-rankings/rankings?orgType=College&sportKey=1&year=2025&page='+str(y)
    r1 = requests.get(url)
    r1 = r1.json()
    
    teams1 = r1['list']
    

    for team in teams1:
        key = team['currentOrganization']['key']
        name = team['currentOrganization']['name']
        col_dic.update({key:name})

col_dic = {k: school_dic.get(v, v) for k, v in col_dic.items()}

df = pd.DataFrame(list(col_dic.items()), columns=['Key', 'School'])

df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\OCollegeKeys.csv",index=False)
