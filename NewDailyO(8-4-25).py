# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 11:29:54 2025

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

today =date.today()
today = today.strftime("%b-%d-%Y")

daily = '48Oq8eRGaOPdgfLPyVtCH'

database = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_080125-111719am.xlsx")


database['PFF ID'] = database['PFF ID'].str.lower()

warnings.simplefilter(action='ignore', category=FutureWarning)

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

new_schools = pd.DataFrame({'Player URL':[''],'Key':[''],'Offer List':['']})

data.close()
#Run On3 API Pull
#Create the data frame
player_data = pd.DataFrame({'On3 Slug':[''], 'Recruitment Key':[''], 'URL':[''], 'First Name':[''], 'Last Name':[''],'City': [''], 'State':[''],
                         'High School':[''], 'Ht':[''], 'Wt':[''], 'Consensus Rating':[''], 'Consensus Stars':[''], 
                         'Consensus National Rank': [''], 'Consensus Position Rank':[''], 'Consensus State Rank':[''],
                         'Position':[''], 'Year':[''], 'Photo':[''], 'Status':[''],'Commit Date':[''], 'Offer Count':[''], 'Offers':[''],
                         'Committed School':['']})

#r_list = []
#Get the API URL
for y in range(2026,2030):
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
            committed_school = None
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
                if "committed" == status.lower():
                    commit_date =  r['list'][i]['status']['date']
                    try:
                        date_str = commit_date.split("T")[0]
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        commit_date = date_obj.strftime('%m/%d/%Y')
                    except:
                        pass
                    committed_school = col_dic[r['list'][i]['status']['committedOrganization']['key']]
            except:
                pass
        except:
            pass
        interests = r['list'][i]['recruitmentInterests']
        for interest in interests:
            if interest['offer'] == True:
                col_key = interest['organizationKey']
                college_name = col_dic[col_key]
                offer_list.append(college_name)
        try:
            converted_offers = pd.DataFrame(offer_list, columns=['School'])
            converted_offers['School'] = converted_offers.replace({'School':school_dic})
            offer_list = converted_offers['School'].values.tolist()
            offer_count = len(offer_list)
            #Put offers into a single string CS
            for t in range(len(offer_list)):
                if type(offer_list[t]) == float:
                    del offer_list[t]
                    break
            if offer_count > 0:
                offers = ",".join(offer_list)
            else:
                offers = None
        except:
            pass
        #Add player data into the data frame
        new_row = {'On3 Slug':on3_slug, 'Recruitment Key':recruitment_key, 'URL':player_url, 'First Name':first_name, 'Last Name':last_name,'City':city, 'State':state,
                         'High School':high_school, 'Ht':ht, 'Wt':wt, 'Consensus Rating':rating, 'Consensus Stars':stars, 
                         'Consensus National Rank':national, 'Consensus Position Rank':position_rank, 'Consensus State Rank':state_rank,
                         'Position':position, 'Year':year, 'Photo':photo,'Status':status,'Commit Date':commit_date,'Offer Count':offer_count, 'Offers':offers,
                         'Committed School':committed_school}
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
                committed_school = None
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
                    if "committed" == status.lower():
                        commit_date =  r['list'][i]['status']['date']
                        try:
                            date_str = commit_date.split("T")[0]
                            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                            commit_date = date_obj.strftime('%m/%d/%Y')
                        except:
                            pass
                        committed_school = col_dic[r['list'][i]['status']['committedOrganization']['key']]
                except:
                    pass
            except:
                pass
            interests = r['list'][i]['recruitmentInterests']
            for interest in interests:
                if interest['offer'] == True:
                    col_key = interest['organizationKey']
                    try:
                        college_name = col_dic[col_key]
                        offer_list.append(college_name)
                    except:
                        new_row1 = {'Player URL':player_url,'Key':col_key,'Offer List':offer_list}
                        new_schools = pd.concat([new_schools,pd.DataFrame([new_row1])],ignore_index=True)
            try:
                converted_offers = pd.DataFrame(offer_list, columns=['School'])
                converted_offers['School'] = converted_offers.replace({'School':school_dic})
                offer_list = converted_offers['School'].values.tolist()
                offer_count = len(offer_list)
                #Put offers into a single string CS
                for t in range(len(offer_list)):
                    if type(offer_list[t]) == float:
                        del offer_list[t]
                        break
                if offer_count > 0:
                    offers = ",".join(offer_list)
                else:
                    offers = None
            except:
                pass
            #Add player data into the data frame
            new_row = {'On3 Slug':on3_slug, 'Recruitment Key':recruitment_key, 'URL':player_url, 'First Name':first_name, 'Last Name':last_name,'City':city, 'State':state,
                             'High School':high_school, 'Ht':ht, 'Wt':wt, 'Consensus Rating':rating, 'Consensus Stars':stars, 
                             'Consensus National Rank':national, 'Consensus Position Rank':position_rank, 'Consensus State Rank':state_rank,
                             'Position':position, 'Year':year, 'Photo':photo,'Status':status,'Commit Date':commit_date,'Offer Count':offer_count, 'Offers':offers,
                             'Committed School':committed_school}
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


player_data.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\On3Raw"+str(today)+".csv",index=False)

player_data['Offer Count'] = player_data['Offer Count'].replace(0, '')

player_data['On3 Player Id'] = player_data['On3 Slug'].str.extract(r'-([^-\s]+)$')

#player_data = pd.merge(player_data, on3_links, on='URL', how='left')
player_data = pd.merge(player_data, on3_issues, on='URL', how='left')
for i in range(len(player_data)):
    if type(player_data.at[i, 'Issue']) == float:
        player_data.at[i, 'Issue'] = 'NEW'
####################################################################################

for i in range(len(player_data)):
    if player_data.at[i, "Issue"] == 'NEW':
        try:
            player_id = player_data.at[i, 'First Name'] + " " + player_data.at[i, 'Last Name'] + " " + player_data.at[i, 'State'] + " " + str(player_data.at[i, 'Year'])
            player_data.at[i, 'ID'] = player_id.lower()
        except:
            continue

#Transform into template
template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")
template1 = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")
j = 0
k = 0

for i in range(0, len(player_data)):
    #Sort the data into the import template format
    if player_data.at[i, 'Issue'] == 'NEW':
        template1.at[j, 'HS Class'] = player_data.at[i, 'Year']
        template1.at[j, 'Last Name'] = player_data.at[i, 'Last Name']
        template1.at[j, 'First Name'] = player_data.at[i, 'First Name']
        template1.at[j, 'HS State'] = player_data.at[i, 'State']
        template1.at[j, 'HS Name'] = player_data.at[i, 'High School']
        template1.at[j, 'HS City'] = player_data.at[i, 'City']
        template1.at[j, 'HS Primary Pos'] = player_data.at[i, 'Position']
        template1.at[j, 'HS Positions'] = player_data.at[i, 'Position']
        template1.at[j, 'HS Height'] = player_data.at[i, 'Ht']
        template1.at[j, 'HS Weight'] = player_data.at[i, 'Wt']
        template1.at[j, 'On3 URL'] = player_data.at[i, 'URL']
        template1.at[j, 'Offer Count'] = player_data.at[i, 'Offer Count']
        template1.at[j, 'Offer Schools'] = player_data.at[i, 'Offers']
        template1.at[j, 'Committed School'] = player_data.at[i, 'Committed School']
        template1.at[j, 'Committed To Date'] = player_data.at[i, 'Commit Date']
        template1.at[j, 'Player Photo'] = player_data.at[i, 'Photo']
        #template1.at[j, 'Twitter URL'] = player_data.at[i, 'Twitter Handle']
        #template1.at[j, 'Instagram URL'] = player_data.at[i, 'Instagram Handle']
        template1.at[j, 'Slug'] = player_data.at[i,'Issue']
        template1.at[j, 'PFF ID'] = player_data.at[i,'ID']
        template1.at[j, 'Industry Rating'] = 0
        template1.at[j, 'Industry Star'] = 0
        template1.at[j, '247 Star'] = 0
        template1.at[j, 'On3 Player Id'] = player_data.at[i, 'On3 Player Id']
        j = j + 1
    else:
        template.at[k, 'HS Class'] = player_data.at[i, 'Year']
        template.at[k, 'Last Name'] = player_data.at[i, 'Last Name']
        template.at[k, 'First Name'] = player_data.at[i, 'First Name']
        template.at[k, 'HS State'] = player_data.at[i, 'State']
        template.at[k, 'HS Name'] = player_data.at[i, 'High School']
        template.at[k, 'HS City'] = player_data.at[i, 'City']
        template.at[k, 'HS Primary Pos'] = player_data.at[i, 'Position']
        template.at[k, 'HS Height'] = player_data.at[i, 'Ht']
        template.at[k, 'HS Weight'] = player_data.at[i, 'Wt']
        template.at[k, 'On3 URL'] = player_data.at[i, 'URL']
        template.at[k, 'Offer Count'] = player_data.at[i, 'Offer Count']
        template.at[k, 'Offer Schools'] = player_data.at[i, 'Offers']
        template.at[k, 'Committed School'] = player_data.at[i, 'Committed School']
        template.at[k, 'Committed To Date'] = player_data.at[i, 'Commit Date']
        template.at[k, 'Player Photo'] = player_data.at[i, 'Photo']
        #template.at[k, 'Twitter URL'] = player_data.at[i, 'Twitter Handle']
        #template.at[k, 'Instagram URL'] = player_data.at[i, 'Instagram Handle']
        template.at[k, 'Slug'] = player_data.at[i,'Issue']
        template.at[k, 'PFF ID'] = player_data.at[i,'ID']
        template.at[k, 'On3 Player Id'] = player_data.at[i, 'On3 Player Id']
        k = k + 1

template = template.reset_index(drop=True)

for i in range(len(template)):
    if template.at[i, 'Slug'] == 'OK':
        template.at[i, 'Slug'] = None

template1 = pd.merge(template1, database[['PFF ID','Slug', 'HS Name', 'On3 URL']], on='PFF ID', how='left')  

for i in range(len(template1)):
    if type(template1.at[i, 'Slug_y']) != float:
        if template1.at[i,'HS Name_x'] != template1.at[i, 'HS Name_y']:
            template1.at[i,'247 Key'] = 'HS Match Error'
template1['Slug_x'] = template1['Slug_y']
template1['SSA ID'] = template1['On3 URL_y']

for i in range(len(template1)):
    if template1.at[i, '247 Key'] == 'HS Match Error':
        template1.at[i, 'Ryzer ID'] = template1.at[i, 'HS Name_y']
    if type(template1.at[i, 'SSA ID']) == str:
        if template1.at[i, 'SSA ID'] == template1.at[i, 'On3 URL_x']:
            template1.at[i, 'SSA ID'] = None

template1.drop('HS Name_y', axis=1, inplace=True)
template1.drop('Slug_y', axis=1, inplace=True)
template1.drop('On3 URL_y', axis=1, inplace=True)

template1.rename(columns={'HS Name_x':'HS Name'}, inplace=True)
template1.rename(columns={'Slug_x':'Slug'}, inplace=True)
template1.rename(columns={'On3 URL_x':'On3 URL'}, inplace=True)

template1['PFF ID'] = template1['First Name'] + " "  + template1['Last Name'] + " " + template1['HS Name']

template = pd.merge(template, database[['Offer Schools','Committed School', 'On3 URL','Player Photo']], on='On3 URL', how='left')

for i in range(len(template)):
    offer_check = 'good'
    committed_check = 'bad'
    photo_check = 'bad'
    offers1 = []
    offers2 = []
    try:
        offers1 = sorted(template.at[i, 'Offer Schools_x'].split(","))
    except:
        offers1 = [template.at[i, 'Offer Schools_x']]
    try:
        offers2 = sorted(template.at[i, 'Offer Schools_y'].split(", "))
    except:
        offers2 =  [template.at[i, 'Offer Schools_y']]
    for offer in offers1:
        if offer in offers2:
            continue
        else:
            offer_check = 'bad'
            break
    if offer_check == 'good':
        template.at[i, 'Offer Schools_x'] = None
    if template.at[i, 'Committed School_x'] == template.at[i, 'Committed School_y']:
        committed_check = 'good'
        template.at[i, 'Committed School_x'] = None
    if template.at[i, 'Player Photo_x'] == template.at[i, 'Player Photo_y']:
        photo_check = 'good'
        template.at[i, 'Player Photo_x'] = None
    else:
        try:
            if "247sports" in template.at[i, 'Player Photo_y']:
                photo_check = 'good'
                template.at[i, 'Player Photo_x'] = None
        except:
            pass


template.drop('Offer Schools_y', axis=1, inplace=True)
template.drop('Committed School_y', axis=1, inplace=True)
template.drop('Player Photo_y', axis=1, inplace=True)   

template.rename(columns={'Offer Schools_x':'Offer Schools'}, inplace=True)
template.rename(columns={'Committed School_x':'Committed School'}, inplace=True)
template.rename(columns={'Player Photo_x':'Player Photo'}, inplace=True) 

template = template.reset_index(drop=True)
bad_index = []

for t in range(len(template)):
    if template.at[t, 'Slug'] != None:
        bad_index.append(t)
        continue
    if template.at[t, 'Offer Schools'] == None and template.at[t, 'Committed School'] != template.at[t, 'Committed School']:
        bad_index.append(t)
        continue
template.drop(bad_index, inplace=True)
template = template.reset_index(drop=True) 

template = pd.merge(template, database[['Slug', 'On3 URL']], on='On3 URL', how='left')

template['Slug_x'] = template['Slug_y']
template.drop('Slug_y',axis=1,inplace=True)
template.rename(columns={'Slug_x':'Slug'}, inplace=True)

index_names = template[template['Slug'] != template['Slug']].index

template.drop(index_names, inplace=True)
template = template.reset_index(drop=True)

cols = ['Slug', 'Offer Schools', 'Committed School']
template.loc[:, ~template.columns.isin(cols)] = np.nan

template = template[~(template['Offer Schools'].isna() & template['Committed School'].isna())]


template.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\'' + str(today) + 'OPlayers.xlsx', index=False)
template1.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\'' + str(today) + 'NEWOPlayers.xlsx', index=False)
                         
