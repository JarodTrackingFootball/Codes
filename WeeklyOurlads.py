# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:48:36 2023

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
import numpy as np
import random

session = requests.Session()
response = session.get('https://www.ourlads.com/ncaa-football-depth-charts/', timeout=30)
cks = session.cookies


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


#database = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_031325-113127am.xlsx")

today = date.today()
today = today.strftime("%b-%d-%Y")

conversions = pd.read_csv(r'C:\Users\jtsve\OneDrive\Desktop\Template Files\ScrapingConversion.csv')
school_dic = conversions.set_index('R')['T'].to_dict()
position_dic = conversions.set_index('P')['P.1'].to_dict()

pst = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\OurladsPostitionSlotTable(9-27).xlsx")

ourlads_map = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Ourlads Mapped Players 7.15.24.xlsx")

df1 = pd.DataFrame({'Team Name':[''],'Depth Chart Link':['']})

proxy = proxies[0]
headers = {'User-Agent': random.choice(header_list)}
page = requests.get('https://www.ourlads.com/ncaa-football-depth-charts/', cookies=cks,headers=headers,proxies = {'http':proxy, 'https':proxy})
soup = BeautifulSoup(page.text, 'html.parser')

team_links = soup.find_all('div', class_='ncaa-dc-mm-team-links')

for team in team_links:
    link = team.find('a').get('href')
    team_name = link.split("s=")[1].split("&")[0]
    team_id = link.split("id=")[1]
    full_link = f"https://www.ourlads.com/ncaa-football-depth-charts/depth-chart/{team_name}/{team_id}"
    team_name = team_name.title()
    try:
        team_name = team_name.replace('-',' ')
    except:
        pass
    new_row = {'Team Name':team_name,'Depth Chart Link':full_link}
    df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
    
df1.drop(index=df1.index[0], 
        axis=0, 
        inplace=True)  

df1 = df1.reset_index(drop=True)
df1.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\OurladsTeamDepthChartLinks.xlsx',index=False)


for i in range(1,len(df1)):
    headers = {'User-Agent': random.choice(header_list)}
    proxy = random.choice(proxies)
    df2 = pd.DataFrame({'Link':[''],'Player ID':[''], 'Player ID Number':['']})
    page = requests.get(df1.at[i, 'Depth Chart Link'], cookies=cks,headers=headers,proxies = {'http':proxy, 'https':proxy})
    soup = BeautifulSoup(page.text, 'html.parser')
    team_name = df1.at[i, 'Team Name']
    tables = soup.find_all('table', class_='table table-bordered')
    df = pd.DataFrame()
    for table in tables:
        df_one=pd.read_html(str(table))[0]
        frames = [df, df_one]
        df = pd.concat(frames)

    for table in tables:
        links = table.find_all('a')
        for link in links:
            player_link = link.get('href')
            player_id = link.text
            player_id_number = player_link.split('/')[-1]
            new_row = {'Link':player_link, 'Player ID':player_id, 'Player ID Number':player_id_number}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
            
    index_names = df2[df2['Player ID Number'] == '0'].index
    df2.drop(index_names, inplace=True)
    df2 = df2.reset_index(drop=True)    

    index_names = df2[df2['Player ID'] == ''].index 
    df2.drop(index_names, inplace=True)
    df2 = df2.reset_index(drop=True)     
    
    rows = [3, 6, 9, 12, 15]
    """
    index_names = df[df['No.'] != df['No.']].index
    df.drop(index_names, inplace=True)
    df = df.reset_index(drop=True) 
    """
    index_names = df[df['No.'] =='Offense'].index
    df.drop(index_names, inplace=True)
    df = df.reset_index(drop=True)  
    
    index_names = df[df['No.'] =='Defense'].index
    df.drop(index_names, inplace=True)
    df = df.reset_index(drop=True)  
    
    index_names = df[df['No.'] =='Special Teams'].index
    df.drop(index_names, inplace=True)
    df = df.reset_index(drop=True)  

    temp_df = df.copy()
    temp_df['Position Slot'] = None
    temp = 1
    side = 1
    temp_df['Match 1'] = temp_df['Player 1'] + " " + temp_df['Pos']
    temp_df['Match 2'] = temp_df['Player 2'] + " " + temp_df['Pos']
    try:
        temp_df['Match 3'] = temp_df['Player 3'] + " " + temp_df['Pos']
    except:
        pass
    try:
        temp_df['Match 4'] = temp_df['Player 4'] + " " + temp_df['Pos']
    except:
        pass
    try:
        temp_df['Match 5'] = temp_df['Player 5'] + " " + temp_df['Pos']
    except:
        pass
    for r in range(len(temp_df)):
        tempstr = str(temp)
        if temp_df.at[r, 'Pos'] == 'FB' and side == 2:
            temp_df.at[r, 'Position Slot'] = f"O12"
            continue
        elif temp_df.at[r, 'Pos'] == 'RB' and side == 2:
            temp_df.at[r, 'Position Slot'] = f"O12"
            continue
        elif temp_df.at[r, 'Pos'] == 'TB' and side == 2:
            temp_df.at[r, 'Position Slot'] = f"O12"
            continue
        elif temp_df.at[r, 'Pos'] == 'RB-B' and side == 2:
            temp_df.at[r, 'Position Slot'] = f"O12"
            continue
        elif temp_df.at[r, 'Pos'] == 'SB' and side == 2:
            temp_df.at[r, 'Position Slot'] = f"O12"
            continue
        elif temp_df.at[r, 'Pos'] == 'KR' and side == 2:
            temp_df.at[r, 'Position Slot'] = f"ST7"
            continue
        elif temp_df.at[r, 'Pos'] == 'FS' and side == 3:
            temp_df.at[r, 'Position Slot'] = f"D12"
            continue
        elif temp_df.at[r, 'Pos'] == 'NB' and side == 3:
            temp_df.at[r, 'Position Slot'] = f"D12"
            continue
        elif temp_df.at[r, 'Pos'] == 'RCB' and side == 3:
            temp_df.at[r, 'Position Slot'] = f"D12"
            continue
        elif temp_df.at[r, 'Pos'].lower() == 'star' and side == 3:
            temp_df.at[r, 'Position Slot'] = f"D12"
        elif temp_df.at[r, 'Pos'] == 'STUD' and side == 3:
            temp_df.at[r, 'Position Slot'] = f"D12"
        elif temp_df.at[r, 'Pos'] == 'LION' and side == 3:
            temp_df.at[r, 'Position Slot'] = f"D12"
            continue
        elif temp_df.at[r, 'Pos']  == 'INJ':
            continue
        elif temp_df.at[r, 'Pos'] == 'SUS':
            continue
        elif temp_df.at[r, 'Pos'] == 'RES':
            continue
        
        if side == 1:
            temp_df.at[r, 'Position Slot'] = f"O{tempstr}"
        elif side == 2:
            temp_df.at[r, 'Position Slot'] = f"D{tempstr}"
        else:
            temp_df.at[r, 'Position Slot'] = f"ST{tempstr}"
        temp = temp + 1
        if temp == 12:
            side = side + 1
            if side == 4:
                side = 1
            temp = 1
    # Add empty columns in the specified rows
    for row in rows:
        df.insert(row, f'Player URL {row}','')
    

    mapping_dict = df2.set_index('Player ID')['Link'].to_dict()
    df[f'Player URL 3'] = df[f'Player 1'].map(mapping_dict)
    
    mapping_dict = df2.set_index('Player ID')['Link'].to_dict()
    df[f'Player URL 6'] = df[f'Player 2'].map(mapping_dict)
    
    mapping_dict = df2.set_index('Player ID')['Link'].to_dict()
    df[f'Player URL 9'] = df[f'Player 3'].map(mapping_dict)
    
    mapping_dict = df2.set_index('Player ID')['Link'].to_dict()
    df[f'Player URL 12'] = df[f'Player 4'].map(mapping_dict)
    
    mapping_dict = df2.set_index('Player ID')['Link'].to_dict()
    df[f'Player URL 15'] = df[f'Player 5'].map(mapping_dict)

    #Cut the columns and add to the bottom
    cut_columns = df.iloc[:, 4:7]
    new_rows = pd.concat([df['Pos'].copy() + ' 2', cut_columns], axis=1)
    new_rows.columns = ['Pos', 'No.','Player 1', 'Player URL 3']
    df = pd.concat([df, new_rows], ignore_index=True)
    
    cut_columns = df.iloc[:, 7:10]
    new_rows = pd.concat([df['Pos'].copy() + ' 3', cut_columns], axis=1)
    new_rows.columns = ['Pos', 'No.','Player 1', 'Player URL 3']
    df = pd.concat([df, new_rows], ignore_index=True)
    
    cut_columns = df.iloc[:, 10:13]
    new_rows = pd.concat([df['Pos'].copy() + ' 4', cut_columns], axis=1)
    new_rows.columns = ['Pos', 'No.','Player 1', 'Player URL 3']
    df = pd.concat([df, new_rows], ignore_index=True)
    
    cut_columns = df.iloc[:, 13:16]
    new_rows = pd.concat([df['Pos'].copy() + ' 5', cut_columns], axis=1)
    new_rows.columns = ['Pos', 'No.','Player 1', 'Player URL 3']
    df = pd.concat([df, new_rows], ignore_index=True)

    #Remove other columns and remove blanks
    df = df.iloc[:, :4]
    index_names = df[df['Player 1'] != df['Player 1']].index
    df.drop(index_names, inplace=True)
    df = df.reset_index(drop=True) 
    
    def find_number(link):
       for col in temp_df.columns:  # Exclude the last column "Number"
           if link in temp_df[col].values:
               return temp_df.loc[temp_df[col] == link, 'Position Slot'].values[0]
       return None

   # Apply the function to create the "Number" column in df2
    df['Match ID'] = df['Player 1'] + " " + df['Pos']
    """
    for l in range(len(df)):
        if " 2" in df.at[l, 'Match ID']:
            df.at[l, 'Match ID'] = df.at[l, 'Match ID'].replace(" 2","")
        if " 3" in df.at[l, 'Match ID']:
            df.at[l, 'Match ID'] = df.at[l, 'Match ID'].replace(" 3","")
        if " 4" in df.at[l, 'Match ID']:
            df.at[l, 'Match ID'] = df.at[l, 'Match ID'].replace(" 4","")
        if " 5" in df.at[l, 'Match ID']:
            df.at[l, 'Match ID'] = df.at[l, 'Match ID'].replace(" 5","")
    """
    for l in range(len(df)):
        try:
            if " 2" in df.at[l, 'Match ID'][-2:]:
                df.at[l, 'Match ID'] = df.at[l, 'Match ID'][:-2]
            if " 3" in df.at[l, 'Match ID'][-2:]:
                df.at[l, 'Match ID'] = df.at[l, 'Match ID'][:-2]
            if " 4" in df.at[l, 'Match ID'][-2:]:
                df.at[l, 'Match ID'] = df.at[l, 'Match ID'][:-2]
            if " 5" in df.at[l, 'Match ID'][-2:]:
                df.at[l, 'Match ID'] = df.at[l, 'Match ID'][:-2]
        except:
            continue
    df['Position Slot'] = df['Match ID'].apply(find_number)

    df['Depth Position'] = None
    df['First Name'] = None
    df['Last Name'] = None
    df['Ourlads ID'] = None
    df['Basic Position'] = None
    
    for k in range(len(df)):
        df.at[k, 'Basic Position'] = df.at[k, 'Pos']
        try:
            df.at[k, 'Depth Position'] = df.at[k, 'Pos'].split(" ")[1]
            df.at[k, 'Depth Position'] = int(df.at[k, 'Depth Position'])
        except:
            df.at[k, 'Depth Position'] = 1
        if df.at[k, 'Depth Position'] > 1:
            df.at[k, 'Pos'] = df.at[k, 'Pos'].replace(" ",":")
        else:
            df.at[k, 'Pos'] = df.at[k, 'Pos'] + ":1"
        try:
            df.at[k, 'Last Name'] = df.at[k, 'Player 1'].split(",")[0]
            df.at[k, 'First Name'] = df.at[k, 'Player 1'].split(", ")[1].split(" ")[0]
        except:
            df.at[k, 'Last Name'] = df.at[k, 'Player 1']
            df.at[k, 'First Name'] = None
        try:
            df.at[k, 'Ourlads ID'] = df.at[k,'Player URL 3'].split('/')[-1]
        except:
            continue
    df = df.drop('Match ID', axis=1)
    column_to_move = df.pop('Position Slot')

    # Insert the column to the second position (index 1)
    df.insert(1, 'Position Slot', column_to_move)
    df.columns = ['Pos','Position Slot', 'Number', 'Player ID', 'Ourlads URL', 'Depth Position','First Name', 'Last Name',
                  'Ourlads Id', 'Basic Position']
    df['College Team'] = team_name
    
    
    if i == 1:
        player_data = df
    else:
        frames = [player_data, df]
        player_data = pd.concat(frames)
     
   
#df.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\OurladsDepthChartsScrape(FCS-SmallSchool).xlsx",index=False)   

column_to_move = player_data.pop('Position Slot')

# Insert the column to the second position (index 1)
player_data.insert(1, 'Position Slot', column_to_move)

"""
for i in range(len(player_data)):
    if "KR" in player_data.at[i, 'Pos'] and ("O" in player_data.at[i, 'Position Slot'] or "D" in player_data.at[i, 'Position Slot']):
        player_data.at[i, 'Position Slot'] = 'ST7'
    elif "PR" in player_data.at[i, 'Pos'] and ("O" in player_data.at[i, 'Position Slot'] or "D" in player_data.at[i, 'Position Slot']):
        player_data.at[i, 'Position Slot'] = 'ST6'
    if player_data.at[i, 'Pos'] == 'H' or player_data.at[i, 'Pos'] == 'H 2' or player_data.at[i, 'Pos'] == 'H 3':
        player_data.at[i, 'Position Slot'] = 'ST5'
"""

temp1 = player_data.copy()
temp1 = temp1.reset_index(drop=True)
temp1['All Positions'] = temp1.groupby('Ourlads Id')['Pos'].transform(lambda x: '/'.join(x))
temp1 = temp1.dropna(subset=['Ourlads Id'])
#temp1 = temp1[temp1['All Positions'].str.contains('/')]
#player_data = pd.merge(player_data, temp1[['Ourlads Id', 'All Positions']], on='Ourlads Id', how='left')
player_data = temp1.copy()
player_data = player_data.reset_index(drop=True)
for t in range(len(player_data)):
    if player_data.at[t, 'All Positions'] != player_data.at[t, 'All Positions']:
        player_data.at[t, 'All Positions'] = player_data.at[t, 'Pos']
        

column_to_move = player_data.pop('All Positions')

# Insert the column to the second position (index 1)
player_data.insert(1, 'All Positions', column_to_move)

player_data['College Team'] = player_data['College Team'].map(school_dic)

player_data = player_data.drop_duplicates()


player_data['Pos'] = player_data['Basic Position']
player_data = player_data.drop('Basic Position', axis=1)

new_order = ['Ourlads Id', 'All Positions', 'Position Slot', 'Pos', 'Depth Position', 'Number',
             'First Name', 'Last Name', 'College Team', 'Player ID', 'Ourlads URL']

player_data_final = player_data[new_order]

player_data_final.columns = ['Ourlads Id', 'Depth Chart', 'Position Slot', 'Position', 'String', 'College Jersey #',
             'First Name', 'Last Name', 'College Name', 'Player ID', 'Ourlads URL']

index_names = player_data_final[player_data_final['Ourlads URL'] != player_data_final['Ourlads URL']].index

player_data_final.drop(index_names, inplace=True)
player_data_final = player_data_final.reset_index(drop=True)

player_data_final['Position'] = player_data_final['Position'].str.strip()

for u in range(len(player_data_final)):
    try:
        player_data_final.at[u, 'Position'] = player_data_final.at[u, 'Position'].split(" ")[0]
    except:
        continue

player_data_final['Match'] = player_data_final['First Name'] + " " + player_data_final['Last Name'] + " " + player_data_final['College Name']

player_data_final.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\DepthCharts('+str(today)+').xlsx',index=False)     


player_data_final['Ourlads Id'] = player_data_final['Ourlads Id'].astype(int)

pd_temp = pd.merge(player_data_final, ourlads_map[['Slug', 'Ourlads Id']], on='Ourlads Id', how='left' )

template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")

for i in range(len(pd_temp)):
    template.at[i, 'Slug'] = pd_temp.at[i,'Slug']
    template.at[i, '247 Key'] = pd_temp.at[i,'Match']
    template.at[i, 'Ourlads Id'] = pd_temp.at[i, 'Ourlads Id']
    template.at[i, 'College Active'] = 'Y'
    template.at[i, 'Depth Chart'] = pd_temp.at[i, 'Depth Chart']
    template.at[i, 'Ourlads URL'] = pd_temp.at[i, 'Ourlads URL']
    template.at[i, 'Ourlads Team'] = pd_temp.at[i, 'College Name']

template.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\DepthChartsImport('+str(today)+').xlsx',index=False)

# Step 1: take the first letter of Position Slot
player_data_final['odk'] = player_data_final['Position Slot'].str[0]

# Step 2: convert single-letter S to ST
player_data_final['odk'] = player_data_final['odk'].replace({'S': 'ST'})

player_data_final['slot'] = player_data_final['Position Slot'].str.extract(r'(\d+)')

for i in range(len(player_data_final)):
    pst.at[i, 'slot'] = player_data_final.at[i, 'slot']
    pst.at[i, 'odk'] = player_data_final.at[i, 'odk']
    pst.at[i, 'pos'] = player_data_final.at[i, 'Position']
    pst.at[i, 'College Team'] = player_data_final.at[i, 'College Name']
    pst.at[i, 'odkslot'] = player_data_final.at[i, 'Position Slot']

pst = pst.drop_duplicates()

pst.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\PositionSlotTable('+str(today)+').xlsx',index=False)

#############################################################################################################

#############################################################################################################

#############################################################################################################
"""
df = player_data_final.copy()

database['Ourlads Id'] = database['Ourlads Id'].astype(float)
df['Ourlads Id'] = df['Ourlads Id'].astype(float)

df = pd.merge(df, database[['Slug', 'Ourlads Id', 'Depth Chart']], on='Ourlads Id', how='left')

condition = (df['Depth Chart_x'] != df['Depth Chart_y']) | (df['Slug'] != df['Slug'])

df_new = df[condition]
df.rename(columns={'Depth Chart_x':'Depth Chart'}, inplace=True)
df = df.drop('Depth Chart_y', axis=1)

df_new.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\DepthChartUPDATES("+str(today)+").xlsx",index=False)    
"""