# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 07:53:02 2022

@author: jtsve
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 09:22:49 2022

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
import random
import datetime

database = pd.read_excel(r"C:\Users\jtsve\Downloads\tf hs export 11.5.xlsx")

template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")

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

#Import Dictionaries for Conversions
#Import conversion templates
data = pd.ExcelFile(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\R and O id table.xlsx")
rivals_issues = data.parse('Rivals')
on3_issues = data.parse('On3')
conversions = pd.read_csv(r'C:\Users\jtsve\OneDrive\Desktop\Template Files\ScrapingConversion.csv')
school_dic = conversions.set_index('R')['T'].to_dict()
school_dic['Virginia Military'] = 'Virginia Military Institute'
state_dic = conversions.set_index('State')['State.1'].to_dict()
country_dic = conversions.set_index('Unnamed: 12')['Unnamed: 13'].to_dict()
position_dic = conversions.set_index('P')['P.1'].to_dict()

colleges_dic_file = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\OCollegeKeys.csv")
col_dic = colleges_dic_file.set_index('Key')['School'].to_dict()

new_schools = pd.DataFrame({'Player URL':[''],'Key':[''],'Offer List':['']})
data.close()

daily = 'rAJq5rAtz5_GRCEEJe113'
#Create the data frame
player_data = pd.DataFrame({'On3 Slug':[''], 'Recruitment Key':[''], 'URL':[''], 'First Name':[''], 'Last Name':[''],'City': [''], 'State':[''],
                         'High School':[''], 'Ht':[''], 'Wt':[''], 'Consensus Rating':[''], 'Consensus Stars':[''], 
                         'Consensus National Rank': [''], 'Consensus Position Rank':[''], 'Consensus State Rank':[''],
                         'Position':[''], 'Year':[''], 'Photo':[''], 'Status':[''],'Commit Date':[''], 'Offer Count':[''], 'Offers':[''],
                         'Committed School':['']})

#r_list = []
#Get the API URL
for y in range(2026,2027):
    url = 'https://www.on3.com/_next/data/'+daily+'/rivals/search.json?sportKey=1&minClassYear='+str(y)+'&maxClassYear='+str(y)
    year = y
    #sport = '&sportkey=1'
    headers = {'User-Agent': random.choice(header_list)}
    proxy = random.choice(proxies)
    #Get the json fromn the api 
    response = requests.get(url, headers=headers,proxies = {'http':proxy, 'https':proxy})
    r = response.json()
    r = r['pageProps']
    #Get basic search info
    pages = r['searchData']['pagination']['pageCount']
    per_page = r['searchData']['pagination']['itemsPerPage']
    total_players = r['searchData']['pagination']['count']
    
    college_list = r['siteData']['siteUrls']
    
    r = r['searchData']
    #Get page 1 of data
    for i in range(0, len(r['list'])):
        try:
            ht = None
            wt = None
            year1 = None
            high_school = None
            city = None
            state = None
            commit_date = None
            photo = None
            position = None
            offer_list = []
            offers = None
            offer_count = 0
            signed_school = None
            #Get all of the data from the Json file
            player_url = 'https://www.on3.com/rivals/' + r['list'][i]['slug'] + "/"
            on3_slug = r['list'][i]['slug']
            recruitment_key = r['list'][i]['recruitmentKey']
            first_name = r['list'][i]['firstName']
            last_name = r['list'][i]['lastName']
            city = r['list'][i]['hometown']['name']
            state = r['list'][i]['hometown']['state']['abbreviation']
            high_school = r['list'][i]['highSchoolName']
            ht = r['list'][i]['height']
            wt = r['list'][i]['weight']
            try:
                rating = r['list'][i]['rating']['consensusRating']
            except:
                rating = None
            try:
                stars = r['list'][i]['rating']['consensusStars']
            except:
                stars = None
            try:
                national = r['list'][i]['rating']['consensusNationalRank']  
            except:
                national = None
            try:
                position_rank = r['list'][i]['rating']['consensusPositionRank']  
            except:
                position_rank = None
            try:
                state_rank = r['list'][i]['rating']['consensusStateRank']
            except:
                state_rank = None
            try:
                position =  r['list'][i]['position']['abbreviation']
            except:
                position = None
            try:
                photo = r['list'][i]['defaultAssetUrl'] 
            except:
                photo = None
            try:
                status = r['list'][i]['status']['type']
            except:
                status = None
            try:
                if "signed" == status.lower():
                    signed_school = col_dic[r['list'][i]['status']['committedOrganization']['key']]
            except:
                pass
        except:
            pass
       
        #Add player data into the data frame
        new_row = {'On3 Slug':on3_slug, 'Recruitment Key':recruitment_key, 'URL':player_url, 'First Name':first_name, 'Last Name':last_name,'City':city, 'State':state,
                         'High School':high_school, 'Ht':ht, 'Wt':wt, 'Consensus Rating':rating, 'Consensus Stars':stars, 
                         'Consensus National Rank':national, 'Consensus Position Rank':position_rank, 'Consensus State Rank':state_rank,
                         'Position':position, 'Year':year, 'Photo':photo,'Status':status,
                         'Signed School':signed_school}
        player_data = pd.concat([player_data, pd.DataFrame([new_row])], ignore_index=True)
    #Get the rest of the pages of data  
    for j in range(2, pages + 1):
        headers = {'User-Agent': random.choice(header_list)}
        proxy = random.choice(proxies)
        url = 'https://www.on3.com/_next/data/'+daily+'/rivals/search.json?sportKey=1&minClassYear='+str(y)+'&maxClassYear='+str(y)+'&page='+str(j)
        
        response = requests.get(url,headers=headers,proxies = {'http':proxy, 'https':proxy})
        #r_list.append(r)
        r = response.json()
        
        try:
            r = r['pageProps']['searchData']
        except:
            pass
    
        
    
        for i in range(0, len(r['list'])):
            try:
                ht = None
                wt = None
                year1 = None
                high_school = None
                city = None
                state = None
                commit_date = None
                photo = None
                position = None
                offer_list = []
                offers = None
                signed_school = None
                offer_count = 0
                player_url = 'https://www.on3.com/rivals/' + r['list'][i]['slug'] + "/"
                on3_slug = r['list'][i]['slug']
                recruitment_key = r['list'][i]['recruitmentKey']
                first_name = r['list'][i]['firstName']
                last_name = r['list'][i]['lastName']
                try:
                    city = r['list'][i]['hometown']['name']
                except:
                    city = None
                try:
                    state = r['list'][i]['hometown']['state']['abbreviation']
                except:
                    state = None
                try:
                    high_school = r['list'][i]['highSchoolName']
                except:
                    high_school = None
                try:
                    ht = r['list'][i]['height']
                except:
                    ht = None
                try:
                    wt = r['list'][i]['weight']
                except:
                    wt = None
                try:
                    rating = r['list'][i]['rating']['consensusRating']
                except:
                    rating = None
                try:
                    stars = r['list'][i]['rating']['consensusStars']
                except:
                    stars = None
                try:
                    national = r['list'][i]['rating']['consensusNationalRank']  
                except:
                    national = None
                try:
                    position_rank = r['list'][i]['rating']['consensusPositionRank']  
                except:
                    position_rank = None
                try:
                    state_rank = r['list'][i]['rating']['consensusStateRank']
                except:
                    state_rank = None
                try:
                    position =  r['list'][i]['position']['abbreviation']
                except:
                    position = None
                try:
                    photo = r['list'][i]['defaultAssetUrl'] 
                except:
                    photo = None
                try:
                    status = r['list'][i]['status']['type']
                except:
                    status = None
                try:
                    if "signed" == status.lower():
                        signed_school = col_dic[r['list'][i]['status']['committedOrganization']['key']]
                except:
                    pass
            except:
                pass
           
            #Add player data into the data frame
            new_row = {'On3 Slug':on3_slug, 'Recruitment Key':recruitment_key, 'URL':player_url, 'First Name':first_name, 'Last Name':last_name,'City':city, 'State':state,
                             'High School':high_school, 'Ht':ht, 'Wt':wt, 'Consensus Rating':rating, 'Consensus Stars':stars, 
                             'Consensus National Rank':national, 'Consensus Position Rank':position_rank, 'Consensus State Rank':state_rank,
                             'Position':position, 'Year':year, 'Photo':photo,'Status':status,
                             'Signed School':signed_school}
            player_data = pd.concat([player_data, pd.DataFrame([new_row])], ignore_index=True)
new_schools.to_csv(r"C:\Users\jtsve\OneDrive\Documents\NewSchoolstoAdd.csv",index=False)

player_data = player_data.drop_duplicates() 
player_data.drop(index=player_data.index[0], 
        axis=0, 
        inplace=True)   
  
player_data = player_data.reset_index(drop=True)     
#Convert states 
player_data['State'] = player_data['State'].map(state_dic)

player_data['Position'] = player_data['Position'].map(position_dic)
player_data['Position'] = player_data['Position'].replace('ATH','')


player_data.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\On3Raw12-6.csv",index=False)


player_data['On3 Player Id'] = player_data['On3 Slug'].str.extract(r'-([^-\s]+)$')

player_data = player_data[player_data['Signed School'].notna()]



####################################################################################
#player_data['Slug'] = None
index_names = database[database['On3 URL'] != database['On3 URL']].index
database.drop(index_names, inplace = True)
database = database.reset_index(drop=True)

#player_data['Slug'] = player_data['URL'].map(database.set_index('On3 URL')['Slug'])
player_data.rename(columns={'URL': 'On3 URL'}, inplace=True)
player_data = pd.merge(player_data, database[['Slug','On3 URL']], on='On3 URL', how='left')




player_data = player_data.drop_duplicates()
player_data = player_data.reset_index(drop=True)

for i in range(0, len(player_data)):
    #Sort the data into the import template format
    template.at[i, 'Slug'] = player_data.at[i,'Slug']
    template.at[i, 'On3 URL'] = player_data.at[i,'On3 URL']
    template.at[i, 'College Name'] = player_data.at[i,'Signed School']
    template.at[i, 'Committed School'] = player_data.at[i,'Signed School']
    template.at[i, 'Recruiting Class'] = 2026
    try:
        position = player_data.at[i, 'Position'].split('/')[0]
    except:
        position = player_data.at[i, 'Position']
    template.at[i, 'College Primary Pos'] = position
    template.at[i, 'College Positions'] = player_data.at[i,'Position']
    template.at[i, 'College Height'] = player_data.at[i,'Ht']
    template.at[i, 'College Weight'] = player_data.at[i,'Wt']
    template.at[i, 'College Active'] = 'Y'
    template.at[i, 'HS Name'] = player_data.at[i,'High School']
    template.at[i, 'HS City'] = player_data.at[i,'City']
    template.at[i, 'HS State'] = player_data.at[i,'State']
    template.at[i, 'First Name'] = player_data.at[i,'First Name']
    template.at[i, 'Last Name'] = player_data.at[i,'Last Name']

template.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\On3SigningDay2026-4.xlsx', index=False)



