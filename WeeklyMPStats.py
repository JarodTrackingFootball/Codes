# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 12:48:48 2024

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
import numpy as np
from selenium.webdriver.chrome.options import Options
import json
import warnings
import zipfile
import io
import subprocess

def first_non_null(series):
    return series.dropna().iloc[0] if not series.dropna().empty else None

sas_url = "https://sttfb2produseast.blob.core.windows.net/production-data?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacuptfx&se=2051-08-13T04:32:29Z&st=2021-08-11T20:32:29Z&spr=https&sig=0oX%2Fgj7PXeJsHI37E6TS8pzRY1MY3DnEPbApnQ6kWVU%3D"

conversions = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Scraping Conversion.xlsx")
position_dic = conversions.set_index('Pos')['PosFix'].to_dict()

today =date.today()
today = today.strftime("%b-%d-%Y")

stats_template = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\HS Production Import (1).xlsx")

hm_master = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\2026Hudl-MPMaster.csv")

daily_num = '1764019328'

warnings.simplefilter(action='ignore', category=FutureWarning)

header_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']

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
        
db = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_102125-080844am.xlsx") 

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE','DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
cats_yds = ['rushing', 'passing', 'receiving','touchdowns',]
total_cats_def = [['tackles','tot-tcks'],['sacks','tot-sacks'],['interceptions','tot-ints']]
classes = [12,11,10,9]

df = pd.DataFrame({'First Name':[''],'Last Name':[''],'Maxpreps URL':[''],'Positions':[''],
                   'HS Name':[''],'HS State':[''],'HS City':[''],'HS Class':['']})
global first
first = True
for state in states:
    for class_ in classes:
        for cat in cats_yds:
            time.sleep(1)
            column_names = []
            headers = {'User-Agent': random.choice(header_list)}
            proxy = random.choice(proxies)
            url = 'https://www.maxpreps.com/_next/data/'+daily_num+'/'+state+'/football/stat-leaders/offense/'+cat+'/yds.json?classyear='+str(class_)
            try:
                response = requests.get(url, headers=headers,proxies = {'http':proxy, 'https':proxy})
                r = response.json()
            except:
                time.sleep(10)
                try:
                    response = requests.get(url, headers=headers,proxies = {'http':proxy, 'https':proxy})
                    r = response.json()
                except:
                    continue
            
            for temp in r['pageProps']['statLeadersListData']['columns']:
                column_names.append(temp['displayName'])
            column_names.append('Maxpreps URL')
            df1 = pd.DataFrame(columns=column_names)
            rows = r['pageProps']['statLeadersListData']['rows']
            for row in rows:
                hs_class = None
                stats = []
                first_name = row[0]
                last_name = row[1]
                mp_url = 'https://www.maxpreps.com'+row[2]
                mp_url = mp_url.replace('/football/stats','')
                positions = row[3]
                try:
                    positions = positions.replace(", ","/")
                except:
                    pass
                city = row[5]
                hs_name = row[6]
                player_state = row[10]
                stats = row[8]
                stats.append(mp_url)
                if class_ == 12:
                    hs_class = 2026
                elif class_ == 11:
                    hs_class = 2027
                elif class_ == 10:
                    hs_class = 2028
                else:
                    hs_class = 2029
                new_row = pd.Series(stats, index=column_names)
                df1.loc[len(df1)] = new_row
                if first == True:
                    stats_df = df1
                else:
                    frames= [stats_df,df1]
                    stats_df = pd.concat(frames)
                first = False
                new_row = {'First Name':first_name,'Last Name':last_name,'Maxpreps URL':mp_url,'Positions':positions,
                                   'HS Name':hs_name,'HS State':player_state,'HS City':city,"HS Class":hs_class}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        stats_df = stats_df.drop_duplicates(keep='first') 
        stats_df = stats_df.reset_index(drop=True)  
        for cat in total_cats_def:
            time.sleep(1)
            column_names = []
            headers = {'User-Agent': random.choice(header_list)}
            proxy = random.choice(proxies)
            url = 'https://www.maxpreps.com/_next/data/'+daily_num+'/'+state+'/football/stat-leaders/defense/'+cat[0]+'/'+cat[1]+'.json?classyear='+str(class_)
            try:
                response = requests.get(url, headers=headers,proxies = {'http':proxy, 'https':proxy})
                r = response.json()
            except:
                time.sleep(10)
                try:
                    response = requests.get(url, headers=headers,proxies = {'http':proxy, 'https':proxy})
                    r = response.json()
                except:
                    continue
            
            for temp in r['pageProps']['statLeadersListData']['columns']:
                column_names.append(temp['displayName'])
            column_names.append('Maxpreps URL')
            df1 = pd.DataFrame(columns=column_names)
            
            rows = r['pageProps']['statLeadersListData']['rows']
            for row in rows:
                hs_class = None
                first_name = row[0]
                last_name = row[1]
                mp_url = 'https://www.maxpreps.com'+row[2]
                mp_url = mp_url.replace('/football/stats','')
                positions = row[3]
                try:
                    positions = positions.replace(", ","/")
                except:
                    pass
                city = row[5]
                hs_name = row[6]
                player_state = row[10]
                stats = row[8]
                stats.append(mp_url)
                if class_ == 12:
                    hs_class = 2026
                elif class_ == 11:
                    hs_class = 2027
                elif class_ == 10:
                    hs_class = 2028
                else:
                    hs_class = 2029
                new_row = pd.Series(stats, index=column_names)
                df1.loc[len(df1)] = new_row
                if first == True:
                    stats_df = df1
                else:
                    frames= [stats_df,df1]
                    stats_df = pd.concat(frames)
                first = False
                new_row = {'First Name':first_name,'Last Name':last_name,'Maxpreps URL':mp_url,'Positions':positions,
                                   'HS Name':hs_name,'HS State':player_state,'HS City':city,"HS Class":hs_class}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
stats_df = stats_df.drop_duplicates(keep='first') 
stats_df = stats_df.reset_index(drop=True)

df = df.drop_duplicates(subset='Maxpreps URL',keep='first') 
df = df.reset_index(drop=True)                

df = pd.merge(df, stats_df, on='Maxpreps URL',how='left')
df.drop(index=df.index[0], 
        axis=0, 
        inplace=True)   
#Reset the index after dropping duplicated to parse easier
df = df.reset_index(drop=True)
df["HS Class"] = df["HS Class"].astype(str)
df['GUID'] = df['First Name'] + " " + df['Last Name'] + " " +df['HS State']+ " " + df['HS Class']
df['PFF ID'] = df['GUID'] + " " + df['HS Name']

df = pd.merge(df, db[['Slug','Maxpreps URL']], on='Maxpreps URL',how='left')
df = df.groupby('Maxpreps URL').agg(first_non_null).reset_index()
df = df.replace(0, np.nan)
df = df.replace("0", np.nan)
df.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\MPStatsUpdates('+str(today)+')-RAW.csv',index=False)    
df1 = df.copy()
index_names = df[df['Slug'] != df['Slug']].index

df.drop(index_names, inplace=True)
df = df.reset_index(drop=True)

#df = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\MPStatsUpdates(Sep-29-2025)-RAW.csv")

df['Positions'] = df['Positions'].map(position_dic)

df = df.groupby('Maxpreps URL').agg(first_non_null).reset_index()
df = df.replace("0", np.nan)
df = df.replace("0.0", np.nan)
"""
# 1️⃣ Create JSON metadata
metadata = {"source": "maxpreps", "year": 2025}

# 2️⃣ Create an in-memory ZIP
with zipfile.ZipFile("maxpreps_2025.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    # Add CSV version of your dataframe
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    zf.writestr("maxpreps_player-production-data.csv", csv_buffer.getvalue())

    # Add JSON file
    zf.writestr("settings.json", json.dumps(metadata, indent=4))

zip_path = "/tmp/maxpreps_2025.zip"    
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
for i in range(len(df)):
    stats_template.at[i,'slug'] = df.at[i, 'Slug']
    stats_template.at[i,'Source'] = 'Maxpreps'
    stats_template.at[i,'Year'] = 2025
    stats_template.at[i,'Rush Att'] = df.at[i, 'Carries']
    stats_template.at[i,'Rush Yard'] = df.at[i, 'Rushing Yards']
    stats_template.at[i,'Rush TD'] = df.at[i, 'Rushing TDs']
    stats_template.at[i,'Pass Att'] = df.at[i, 'Passing Att']
    stats_template.at[i,'Pass Comp'] = df.at[i, 'Completions']
    stats_template.at[i,'Pass Yard'] = df.at[i, 'Passing Yards']
    stats_template.at[i,'Pass TD'] = df.at[i, 'Passing TDs']
    stats_template.at[i,'Pass Int'] = df.at[i, 'Passing Int']
    stats_template.at[i,'Rec'] = df.at[i, 'Receptions']
    stats_template.at[i,'Rec Yards'] = df.at[i, 'Receiving Yards']
    stats_template.at[i,'Rec TD'] = df.at[i, 'Receiving TDs']
    #stats_template.at[i,'Kickoff Ret'] = df.at[i, 'Slug']
    stats_template.at[i,'Int Ret'] = df.at[i, 'Interceptions']
    stats_template.at[i,'Int Ret Yard'] = df.at[i, 'Interceptions Yards']
    stats_template.at[i,'Fumble'] = df.at[i, 'Offensive Fumbles']
    stats_template.at[i,'Tackle Solo'] = df.at[i, 'Solo Tackle']
    stats_template.at[i,'Tackle Assist'] = df.at[i, 'Assists']
    stats_template.at[i,'Tackle For Loss'] = df.at[i, 'Tackles For Loss']
    stats_template.at[i,'Sack'] = df.at[i, 'Sacks'] 
    #stats_template.at[i,'Sack Yard'] = df.at[i, 'Sack Yards Lost']
    stats_template.at[i,'QB Hurry'] = df.at[i, 'QB Hurries']
    stats_template.at[i,'Games'] = df.at[i, 'Games Played']
    #stats_template.at[i,'Class'] = df.at[i, 'HS Class']

stats_template.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\MPStatsUpdates('+str(today)+').xlsx',index=False)    
    

df1 = pd.merge(df1, hm_master[['Maxpreps URL', 'Hudl URL', 'Athletic URL', 'Milesplit URL']], on='Maxpreps URL', how='left')   

stat_cols = [
    "Rushing Yards", "Rushing TDs",
    "Passing Yards", "Passing TDs",
    "Receiving Yards", "Receiving TDs",
    "Total Tackles", "Sacks", "Interceptions"
]

frames = []
for col in stat_cols:
    if col in df.columns:
        # drop NA so nlargest doesn't choke on missing values
        df1[col] = pd.to_numeric(df1[col], errors="coerce")
        top50 = df1[df1[col].notna()].nlargest(1000, col).copy()
        frames.append(top50)
    else:
        print(f"Warning: '{col}' not found in df columns")

# combine all top-50 cuts
combined = pd.concat(frames, ignore_index=True)

# remove duplicates by Maxpreps URL (keeps first occurrence)
leaders_unique = combined.drop_duplicates(subset="Maxpreps URL", keep="first").reset_index(drop=True)
index_names = leaders_unique[leaders_unique['Slug'] == leaders_unique['Slug']].index

leaders_unique.drop(index_names, inplace=True)
leaders_unique = leaders_unique.reset_index(drop=True)


template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")

for i in range(len(leaders_unique)):
    template.at[i, 'HS Class'] = leaders_unique.at[i, 'HS Class']
    template.at[i, 'Last Name'] = leaders_unique.at[i, 'Last Name']
    template.at[i, 'First Name'] = leaders_unique.at[i, 'First Name']
    template.at[i, 'HS State'] = leaders_unique.at[i, 'HS State']
    template.at[i, 'HS Name'] = leaders_unique.at[i, 'HS Name']
    template.at[i, 'HS City'] = leaders_unique.at[i, 'HS City']
    template.at[i, 'Maxpreps URL'] = leaders_unique.at[i, 'Maxpreps URL']
    template.at[i, 'Hudl URL'] = leaders_unique.at[i, 'Hudl URL']
    template.at[i, 'Athletic URL'] = leaders_unique.at[i, 'Athletic URL']
    template.at[i, 'Milesplit URL'] = leaders_unique.at[i, 'Milesplit URL']
    template.at[i, 'PFF ID'] = leaders_unique.at[i, 'PFF ID']
    

leaders_unique.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\MPStatsUpdates('+str(today)+')-leaders.csv',index=False)

    