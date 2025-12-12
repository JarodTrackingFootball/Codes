# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 09:17:52 2024

@author: jtsve
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:36:27 2023

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


issues_247 = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\247Issues.xlsx")
conversions = pd.read_csv(r'C:\Users\jtsve\OneDrive\Desktop\Template Files\ScrapingConversion.csv')
school_dic = conversions.set_index('R')['T'].to_dict()
school_dic['Virginia Military'] = 'Virginia Military Institute'
state_dic = conversions.set_index('State')['State.1'].to_dict()
country_dic = conversions.set_index('Unnamed: 12')['Unnamed: 13'].to_dict()
position_dic = conversions.set_index('P')['P.1'].to_dict()

database = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_070725-103428am.xlsx")
database['PFF ID'] = database['PFF ID'].str.lower()
scrape_date = 100

def state_to_abbreviation(state_name):
    states_abbreviations = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
        'District Of Columbia':'DC'
    }

    return states_abbreviations.get(state_name, "Invalid State Name")


#Create the data frame
player_data = pd.DataFrame({'URL':[''],'Recruit URL':[''], 'Full Name':[''], 'First Name':[''], 'Last Name':[''], 'City': [''], 'State':[''],
                     'High School':[''], 'Ht':[''], 'Wt':[''], '247 Key':[''],'Last Updated':[''],'Updated Number':[''], 'Player Photo':[''],
                     'Position':[''], 'National Rank':[''],'State Rank':[''], 'Position Rank':[''],'Year':[''], '247 Rating':[''], 'Signed School':[''],'Status':[''],
                     '247 Star Rating':[''], 'Offers':[''], 'Offer Count':[''], 'Committed School':[''], 'Phone Number':[''], 'Commit Date':[''],
                     'Baseball':[''],'Basketball':[''],'Golf':[''],"Hockey":[''],'Lacrosse':[''], 'Powerlifting':[''],
                     'Rugby':[''], 'Soccer':[''],'Swimming':[''],  'Tennis':[''],'Volleyball':[''], 
                     'Wrestling':[''],'Track':['']})
update_num = None

options = Options()
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

for y in range(2026, 2030):
    page = 0
    #Get the json fromn the api 
    while True:
        page = page + 1
        try:
            url = 'https://247sports.com/season/'+str(y)+'-football/recruits.json?&Items=500&Page='+str(page)
            driver.get(url)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            r = json.loads(soup.text)
        except:
            #page = page -1 
            continue
        if len(r)==0:
            break
        
        for i in range(len(r)):
            basketball= None
            baseball= None
            golf= None
            hockey= None
            lacrosse= None
            powerlifting= None
            rugby= None
            soccer= None
            tennis= None
            volleyball= None
            wrestling= None
            swimming = None
            track = None
            commit_date = None
            try:
                photo = r[i]['Player']['DefaultAssetUrl']
            except:
                continue
            if photo == '/.':
                photo = None
            full_name = r[i]['Player']['DefaultName']
            first_name = r[i]['Player']['FirstName']
            last_name = r[i]['Player']['LastName']
            height = r[i]['Player']['Height']
            bio = r[i]['Player']['Bio']
            try:
                if "basketball" in bio or 'point guard' in bio or 'shooting guard' in bio or 'small forward' in bio or 'power forward' in bio:
                    basketball = 1
                if "baseball" in bio or 'pitcher' in bio or 'shortstop' in bio or 'short stop' in bio or 'catcher' in bio or 'outfielder' in bio:
                    baseball = 1
                if "golf" in bio:
                    golf = 1
                if "hockey" in bio:
                    hockey = 1
                if "lacrosse" in bio or 'lax' in bio:
                    lacrosse = 1
                if "powerlifting" in bio or "power lifting" in bio:
                    powerlifting = 1
                if "rugby" in bio:
                    rugby = 1
                if "soccer" in bio:
                    soccer = 1
                if "tennis" in bio:
                    tennis = 1
                if "wrestling" in bio or 'wrestle' in bio or 'wrestler' in bio:
                    wrestling = 1
                if "volleyball" in bio:
                    volleyball = 1
                if "swimming" in bio:
                    swimming = 1
                if "track" in bio or 't&f' in bio or 'shot put' in bio or 'discus' in bio or 'high jump' in bio or 'long jump' in bio or 'sprinter' in bio or "triple jump" in bio:
                    track = 1
            except:
                pass
            try:
                height = (float(height.split("-")[0])*12) + float(height.split("-")[1])
            except:
                height = None
            state = r[i]['Player']['Hometown']['State']
            try:
                state = state_to_abbreviation(state)
            except:
                pass
            city = r[i]['Player']['Hometown']['City']
            phone = r[i]['Player']['MobilePhoneContact']
            last_modified = r[i]['Player']['ModifiedDate']
            national_rank = r[i]['Player']['NationalRank']
            position_rank = r[i]['Player']['PositionRank']
            high_school = r[i]['Player']['PlayerHighSchool']['Name']
            position = r[i]['Player']['PrimaryPlayerPosition']['Abbreviation']
            rating = r[i]['Player']['Rating']
            star_rating = r[i]['Player']['StarRating']
            state_rank = r[i]['Player']['StateRank']
            player_url = r[i]['Player']['Url']
            weight = r[i]['Player']['Weight']
            
            try:
                year = int(last_modified.split("/")[-1].split(" ")[0])
                #if year < 2024:
                    #continue
                
                update_num = int(last_modified.split("/")[0] + last_modified.split("/")[1])
            except:
                pass
            #try:
                #if update_num < scrape_date:
                    #continue
            #except:
                #pass
            
            try:
                year = int(r[i]['Year'])
            except:
                pass
            recruit_url = r[i]['RecruitInterestsUrl']
            status = r[i]['HighestRecruitInterestEventType']
            if "commit" in status.lower():
                try:
                    commit_date = r[i]['AnnouncementDate'].split(" ")[0]
                except:
                    commit_date = None
            try:
                if status == '0':
                    status = None
            except:
                pass
            key = r[i]['Key']
            new_row = {'URL':player_url,'Recruit URL':recruit_url, 'Full Name':full_name, 'First Name':first_name, 'Last Name':last_name, 'City': city, 'State':state,
                                 'High School':high_school, 'Ht':height, 'Wt':weight, '247 Key':key,'Last Updated':last_modified, 'Updated Number':update_num,'Player Photo':photo,
                                 'Position':position, 'National Rank':national_rank,'State Rank':state_rank,'Position Rank':position_rank, 'Year':year, '247 Rating':rating,'Status':status,
                                 '247 Star Rating':star_rating,'Phone Number':phone, 'Commit Date':commit_date,
                                 'Basketball':basketball, 'Baseball':baseball,
                                 'Track':track,'Wrestling':wrestling,"Hockey":hockey, 'Soccer':soccer,'Swimming':swimming,
                                 'Volleyball':volleyball, 'Powerlifting':powerlifting, 'Rugby':rugby,
                                 'Golf':golf,
                                 'Lacrosse':lacrosse, 'Tennis':tennis,}
            player_data = pd.concat([player_data, pd.DataFrame([new_row])], ignore_index=True)

player_data = player_data.drop_duplicates() 
player_data.drop(index=player_data.index[0], 
        axis=0, 
        inplace=True)   
  
player_data = player_data.reset_index(drop=True)     
#Convert states 
player_data['State'] = player_data['State'].map(state_dic)


#Convert positions
player_data['Position'] = player_data['Position'].map(position_dic)
  

player_data['Industry Rating'] = None
player_data['Industry Stars'] = None
player_data['College Name'] = None
      

#Go to profiles to get offer/star data
for i in range(0,len(player_data)):
    college_name = None
    player_url = player_data.at[i, 'Recruit URL']
    try:
        driver.get(player_url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
    except:
        i = i-1
        continue
    
    
    #Get the Comp Rating and Stars
    try:
        comp_rating = soup.find('span', class_='number').text 
        stars = soup.find('div', class_='mini-header-comp__score')
        comp_stars = len(stars.find_all('span', class_='icon-starsolid yellow'))  
        try:
            player_data.at[i, 'Industry Rating'] = float(comp_rating) *100
        except:
            pass
        player_data.at[i, 'Industry Stars'] = comp_stars
    except:
        pass
    
    #Get Offers
    try:
        temp = soup.find('ul', class_='recruit-interest-index_lst')
        offers_soup = temp.find_all('div', class_='left') 
        offer_list = []
        offers = None
        committed_school = None
        offer_list1 = []
        offer_count = 0
    except:
        continue

    for offer_soup in offers_soup:
        
        status = offer_soup.find('span', class_='status').text
        if "committed" in status.lower():
            committed_school = offer_soup.find('a').text.replace('\n','').strip()
            try:
                committed_school = committed_school.replace(committed_school, school_dic[committed_school])
            except:
                pass
            offer_list.append(committed_school)
        elif 'Enrolled' in status:
            college_name = offer_soup.find('a').text.replace('\n','').strip()
            try:
                college_name = college_name.replace(college_name, school_dic[college_name])
            except:
                pass
            player_data.at[i, 'College Name'] = college_name
        else:
            if "Yes" in offer_soup.find('span', class_='offer').text:
                offer_list.append(offer_soup.find('a').text.replace('\n','').strip())
            else:
                continue

    #Convert offer schools for import to website
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
        continue
        
    player_data.at[i, 'Committed School'] = committed_school
    player_data.at[i, 'Offer Count'] = offer_count
    player_data.at[i, 'Offers'] = offers

driver.quit()
player_data.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\NumbersRun(7-28).csv',index=False)
player_data['URL'] = player_data['URL'].str.lower()
issues_247['URL'] = issues_247['URL'].str.lower()

player_data['Offer Count'] = player_data['Offer Count'].replace(0, '')
player_data['Position'] = player_data['Position'].replace("ATH", '')

player_data = pd.merge(player_data, issues_247, on='URL', how='left')
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
        template1.at[j, '247 URL'] = player_data.at[i, 'URL']
        template1.at[j, 'Offer Count'] = player_data.at[i, 'Offer Count']
        template1.at[j, 'Offer Schools'] = player_data.at[i, 'Offers']
        template1.at[j, 'Committed School'] = player_data.at[i, 'Committed School']
        template1.at[j, 'Committed To Date'] = player_data.at[i, 'Commit Date']
        template1.at[j, 'Player Photo'] = player_data.at[i, 'Player Photo']
        template1.at[j, 'Slug'] = player_data.at[i,'Issue']
        template1.at[j, 'PFF ID'] = player_data.at[i,'ID']
        template1.at[j, '247 Key'] = player_data.at[i,'247 Key']
        try:
            template1.at[j, 'Industry Rating'] = player_data.at[i,'Industry Rating']
        except:
            pass
        template1.at[j, 'Industry Star'] = player_data.at[i,'Industry Stars']
        template1.at[j, '247 Star'] = player_data.at[i,'247 Star Rating']
        #template1.at[j, 'Last Edited'] = player_data.at[i,'Last Updated']
        template1.at[j, 'College Name'] = player_data.at[i, 'College Name']
        template1.at[j, 'Basketball'] = player_data.at[i, 'Basketball']
        template1.at[j, 'Baseball'] = player_data.at[i, 'Baseball']
        template1.at[j, 'Golf'] = player_data.at[i, 'Golf']
        template1.at[j, 'Hockey'] = player_data.at[i, 'Hockey']
        template1.at[j, 'Lacrosse'] = player_data.at[i, 'Lacrosse']
        template1.at[j, 'Powerlifting'] = player_data.at[i, 'Powerlifting']
        template1.at[j, 'Rugby'] = player_data.at[i, 'Rugby']
        template1.at[j, 'Soccer'] = player_data.at[i, 'Soccer']
        template1.at[j, 'Tennis'] = player_data.at[i, 'Tennis']
        template1.at[j, 'Volleyball'] = player_data.at[i, 'Volleyball']
        template1.at[j, 'Wrestling'] = player_data.at[i, 'Wrestling']
        template1.at[j, 'Swimming'] = player_data.at[i, 'Swimming']
        template1.at[j, 'Track'] = player_data.at[i, 'Track']
        j = j + 1
    else:
        template.at[k, 'HS Class'] = player_data.at[i, 'Year']
        template.at[k, 'Last Name'] = player_data.at[i, 'Last Name']
        template.at[k, 'First Name'] = player_data.at[i, 'First Name']
        template.at[k, 'HS State'] = player_data.at[i, 'State']
        template.at[k, 'HS Name'] = player_data.at[i, 'High School']
        template.at[k, 'HS City'] = player_data.at[i, 'City']
        template.at[k, 'HS Primary Pos'] = player_data.at[i, 'Position']
        template.at[k, 'HS Positions'] = player_data.at[i, 'Position']
        template.at[k, 'HS Height'] = player_data.at[i, 'Ht']
        template.at[k, 'HS Weight'] = player_data.at[i, 'Wt']
        template.at[k, '247 URL'] = player_data.at[i, 'URL']
        template.at[k, 'Offer Count'] = player_data.at[i, 'Offer Count']
        template.at[k, 'Offer Schools'] = player_data.at[i, 'Offers']
        template.at[k, 'Committed School'] = player_data.at[i, 'Committed School']
        template.at[k, 'Committed To Date'] = player_data.at[k, 'Commit Date']
        template.at[k, 'Player Photo'] = player_data.at[i, 'Player Photo']
        template.at[k, 'Slug'] = player_data.at[i,'Issue']
        template.at[k, 'PFF ID'] = player_data.at[i,'ID']
        template.at[k, '247 Key'] = player_data.at[i,'247 Key']
        try:
            template.at[k, 'Industry Rating'] = player_data.at[i,'Industry Rating']
        except:
            pass
        template.at[k, 'Industry Star'] = player_data.at[i,'Industry Stars']
        template.at[k, '247 Star'] = player_data.at[i,'247 Star Rating']
        #template.at[k, 'Last Edited'] = player_data.at[i,'Last Updated']
        template.at[k, 'College Name'] = player_data.at[i, 'College Name']
        template.at[k, 'Basketball'] = player_data.at[i, 'Basketball']
        template.at[k, 'Baseball'] = player_data.at[i, 'Baseball']
        template.at[k, 'Golf'] = player_data.at[i, 'Golf']
        template.at[k, 'Hockey'] = player_data.at[i, 'Hockey']
        template.at[k, 'Lacrosse'] = player_data.at[i, 'Lacrosse']
        template.at[k, 'Powerlifting'] = player_data.at[i, 'Powerlifting']
        template.at[k, 'Rugby'] = player_data.at[i, 'Rugby']
        template.at[k, 'Soccer'] = player_data.at[i, 'Soccer']
        template.at[k, 'Tennis'] = player_data.at[i, 'Tennis']
        template.at[k, 'Volleyball'] = player_data.at[i, 'Volleyball']
        template.at[k, 'Wrestling'] = player_data.at[i, 'Wrestling']
        template.at[k, 'Swimming'] = player_data.at[i, 'Swimming']
        template.at[k, 'Track'] = player_data.at[i, 'Track']
        k = k + 1

template = template.reset_index(drop=True)
template1 = template1[template1['Slug']== 'NEW']

for i in range(len(template)):
    if template.at[i, 'Slug'] == 'OK':
        template.at[i, 'Slug'] = None

template1 = pd.merge(template1, database[['PFF ID','Slug', 'HS Name', '247 URL']], on='PFF ID', how='left')  

for i in range(len(template1)):
    if type(template1.at[i, 'Slug_y']) != float:
        if template1.at[i,'HS Name_x'] != template1.at[i, 'HS Name_y']:
            template1.at[i,'Ourlads Id'] = 'HS Match Error'
template1['Slug_x'] = template1['Slug_y']
template1['SSA ID'] = template1['247 URL_y']

for i in range(len(template1)):
    if template1.at[i, 'Ourlads Id'] == 'HS Match Error':
        template1.at[i, 'Ryzer ID'] = template1.at[i, 'HS Name_y']
    if type(template1.at[i, 'SSA ID']) == str:
        if template1.at[i, 'SSA ID'] == template1.at[i, '247 URL_x']:
            template1.at[i, 'SSA ID'] = None

template1.drop('HS Name_y', axis=1, inplace=True)
template1.drop('Slug_y', axis=1, inplace=True)
template1.drop('247 URL_y', axis=1, inplace=True)

template1.rename(columns={'HS Name_x':'HS Name'}, inplace=True)
template1.rename(columns={'Slug_x':'Slug'}, inplace=True)
template1.rename(columns={'247 URL_x':'247 URL'}, inplace=True)

template1['PFF ID'] = template1['First Name'] + " "  + template1['Last Name'] + " " + template1['HS Name']

template = pd.merge(template, database[['Offer Schools','Committed School', '247 URL','Player Photo',
                                        ]], on='247 URL', how='left')

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
            if "247sports" in template.at[i, 'Player Photo_y'].lower():
                photo_check = 'good'
                template.at[i, 'Player Photo_x'] = None
        except:
            pass

    if offer_check == committed_check == photo_check == 'good':
        template.drop(i, inplace=True)
        continue

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

template = pd.merge(template, database[['Slug', '247 URL']], on='247 URL', how='left')

template['Slug_x'] = template['Slug_y']
template.drop('Slug_y',axis=1,inplace=True)
template.rename(columns={'Slug_x':'Slug'}, inplace=True)

index_names = template[template['Slug'] != template['Slug']].index

template.drop(index_names, inplace=True)
template = template.reset_index(drop=True)

cols = ['Slug', 'Offer Schools', 'Committed School']
template.loc[:, ~template.columns.isin(cols)] = np.nan

template = template[~(template['Offer Schools'].isna() & template['Committed School'].isna())]

#Export to a csv with the current date and time
today =date.today()
today = today.strftime("%b-%d-%Y")


template.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\'' + str(today) + 'NumbersOffers.xlsx', index=False)
template1.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\'' + str(today) + 'NEWNumbersPlayers.xlsx', index=False)

