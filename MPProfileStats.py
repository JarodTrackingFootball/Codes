# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 09:20:40 2024

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

daily = '1767997238'
df = pd.read_excel(r"C:\Users\jtsve\Downloads\tf hs export 11.5.xlsx")
stats_template = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\MPProfileStatTemplate.xlsx")

header_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36']


proxy_username = 'jtnoah'
proxy_password = '6FD76B600F96231CD1E5A90035200C04'
proxy_ips = ['23.94.248.15:34555', '107.172.45.115:42720',
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

 
stats_df = pd.DataFrame()
new_df = pd.DataFrame()

for i in range(0,len(df)):
    if df.at[i, 'Maxpreps URL'] != df.at[i, 'Maxpreps URL']:
        continue
    url = df.at[i, 'Maxpreps URL']    
    slug = df.at[i, 'Slug']
    #class_ = df.at[i, 'HS Class']
    if "stats" not in url:
        url = url.replace("/?",'/football/stats.json?')
        url = url.replace(".com/",f".com/_next/data/{daily}/")
    else:
        url = url.replace(".com/",f".com/_next/data/{daily}/").replace("stats/","stats.json")
    headers = {'User-Agent': random.choice(header_list)}
    proxy = random.choice(proxies)
    r = requests.get(url, headers=headers, proxies = {'http':proxy, 'https':proxy})
    try:
        r1 = r.json()
    except:
        continue
    try:
        runsj = len(r1['pageProps']['statsCardProps']['careerRollup']['groups'])
    except:
        continue
    for j in range(0,runsj):
        runsk = len(r1['pageProps']['statsCardProps']['careerRollup']['groups'][j]['subgroups'])
        for k in range(0,runsk):
            runsm = len(r1['pageProps']['statsCardProps']['careerRollup']['groups'][j]['subgroups'][k]['stats'])
            for m in range(0,runsm):
                year = '20' + r1['pageProps']['statsCardProps']['careerRollup']['groups'][j]['subgroups'][k]['stats'][m]['year'][0:2]
                df1 = r1['pageProps']['statsCardProps']['careerRollup']['groups'][j]['subgroups'][k]['stats'][m]['stats']
                temp_df = pd.DataFrame(df1)
                temp_df['Year'] = year
                frames = [stats_df,temp_df]
                stats_df = pd.concat(frames)
    stats_df.drop_duplicates(inplace=True)
    try:
        stats_df = stats_df.pivot_table(index="Year", columns="displayName", values="value", aggfunc="first")
    except:
        continue
    stats_df = stats_df.reset_index()
    stats_df['Slug'] = slug
    #stats_df['Class'] = class_

    frames = [new_df, stats_df]
    new_df = pd.concat(frames)

new_df.reset_index(inplace=True)
new_df = new_df.replace(0, np.nan)

new_df = new_df.reindex(columns=stats_template.columns)


dfs_by_year = {
    year: new_df[new_df['Year'] == year].copy()
    for year in new_df['Year'].unique()
}


for year, df_year in dfs_by_year.items():
    """
    # 1️⃣ Create JSON metadata
    metadata = {"source": "maxprepsprofile", "year": year}
    
    # 2️⃣ Create an in-memory ZIP
    with zipfile.ZipFile("maxpreps_"+str(year)+".zip", "w", zipfile.ZIP_DEFLATED) as zf:
        # Add CSV version of your dataframe
        csv_buffer = io.StringIO()
        df_year.to_csv(csv_buffer, index=False)
        zf.writestr("maxpreps_player-production-data.csv", csv_buffer.getvalue())
    
        # Add JSON file
        zf.writestr("settings.json", json.dumps(metadata, indent=4))
    
    zip_path = "/tmp/maxpreps_"+str(year)+".zip"    
    cmd = [
        "azcopy",
        "copy",
        zip_path,
        sas_url,
        "--overwrite=true"
    ]
    
    # Run the command and capture output
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        print("✅ Upload complete.")
    """

new_df.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\MPProfileStats(11-6)-RAW.csv',index=False)
for i in range(len(new_df)):
    #stats_template.at[i,'Class'] = new_df.at[i, 'Class']
    stats_template.at[i,'slug'] = new_df.at[i, 'Slug']
    stats_template.at[i,'Source'] = 'Maxpreps'
    stats_template.at[i,'Year'] = new_df.at[i, 'Year']
    stats_template.at[i,'Rush Att'] = new_df.at[i, 'Carries']
    stats_template.at[i,'Rush Yard'] = new_df.at[i, 'Rushing Yards']
    stats_template.at[i,'Rush TD'] = new_df.at[i, 'Rushing TDs']
    stats_template.at[i,'Pass Att'] = new_df.at[i, 'Passing Att']
    stats_template.at[i,'Pass Comp'] = new_df.at[i, 'Completions']
    stats_template.at[i,'Pass Yard'] = new_df.at[i, 'Passing Yards']
    stats_template.at[i,'Pass TD'] = new_df.at[i, 'Passing TDs']
    stats_template.at[i,'Pass Int'] = new_df.at[i, 'Passing Int']
    try:
        stats_template.at[i,'Field Goal Att'] = new_df.at[i, 'FG Attempted'] 
        stats_template.at[i,'Field Goal Made'] = new_df.at[i, 'FG Made']
        stats_template.at[i,'Field Goal Long'] = new_df.at[i, 'FG Long']   
    except:
        pass
    stats_template.at[i,'Rec'] = new_df.at[i, 'Receptions']
    stats_template.at[i,'Rec Yards'] = new_df.at[i, 'Receiving Yards']
    stats_template.at[i,'Rec TD'] = new_df.at[i, 'Receiving TDs']
    stats_template.at[i,'Int Ret'] = new_df.at[i, 'Interceptions']
    stats_template.at[i,'Int Ret Yard'] = new_df.at[i, 'Interceptions Yards']
    try:
        stats_template.at[i,'Fumble'] = new_df.at[i, 'Offensive Fumbles']
    except:
        pass
    stats_template.at[i,'Tackle Solo'] = new_df.at[i, 'Solo Tackle']
    stats_template.at[i,'Tackle Assist'] = new_df.at[i, 'Assists']
    stats_template.at[i,'Tackle For Loss'] = new_df.at[i, 'Tackles For Loss']
    stats_template.at[i,'Sack'] = new_df.at[i, 'Sacks'] 
    stats_template.at[i,'Sack Yard'] = new_df.at[i, 'Sacks Yards Lost']
    stats_template.at[i,'QB Hurry'] = new_df.at[i, 'QB Hurries']
    stats_template.at[i,'Games'] = new_df.at[i, 'Games Played']
    stats_template.at[i,'Kickoff Ret TD'] = new_df.at[i, 'Kickoffs Returned for Touchdown']
    stats_template.at[i,'Punt Ret TD'] = new_df.at[i, 'Punts Returned for Touchdown']
    #stats_template.at[i,'MP Last Updated Date'] = new_df.at[i, 'Updated Date']

stats_template.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\MPProfileStatsUpdates(11-6).csv',index=False)    
    
