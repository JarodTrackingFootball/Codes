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
import json
from selenium.webdriver.chrome.options import Options


conversions = pd.read_csv(r'C:\Users\jtsve\OneDrive\Desktop\Template Files\ScrapingConversion.csv')
school_dic = conversions.set_index('R')['T'].to_dict()
school_dic['Virginia Military'] = 'Virginia Military Institute'
state_dic = conversions.set_index('State')['State.1'].to_dict()
country_dic = conversions.set_index('Unnamed: 12')['Unnamed: 13'].to_dict()
position_dic = conversions.set_index('P')['P.1'].to_dict()

database = pd.read_excel(r"C:\Users\jtsve\Downloads\tf hs export 11.5.xlsx")

header_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A']



session = requests.Session()
response = session.get('https://247sports.com/Recruitment/jeremiah-smith-145416/RecruitInterests/', timeout=30)
cks = session.cookies

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
                     'High School':[''], 'Ht':[''], 'Wt':[''], '247 Key':[''],'Signed School':[''], 'Player Photo':[''],
                     'Position':[''], 'National Rank':[''],'State Rank':[''], '247 Rating':[''],'Status':[''],
                     '247 Star Rating':[''], 'Offers':[''], 'Offer Count':[''], 'Committed School':[''], 'Phone Number':['']})


options = Options()
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

for y in range(2026, 2027):
    headers = {
    'authority': '247sports.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/html; charset=utf-8',
    'referer': 'https://247sports.com/Season/2024-Football/Recruits/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
    'x-requested-with': 'XMLHttpRequest',
    }

    page = 0
    #Get the json fromn the api 
    while True:
        page = page + 1
        url = 'https://247sports.com/Season/2026-Football/Recruits.json?&Items=100&Page='+str(page)+'&RecruitInterestEvents.Type=6'
        driver.get(url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        r = json.loads(soup.text)
        if len(r)==0:
            break
        
        for i in range(len(r)):
            photo = r[i]['Player']['DefaultAssetUrl']
            if photo == '/.':
                photo = None
            full_name = r[i]['Player']['DefaultName']
            first_name = r[i]['Player']['FirstName']
            last_name = r[i]['Player']['LastName']
            height = r[i]['Player']['Height']
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
            high_school = r[i]['Player']['PlayerHighSchool']['Name']
            position = r[i]['Player']['PrimaryPlayerPosition']['Abbreviation']
            rating = r[i]['Player']['Rating']
            star_rating = r[i]['Player']['StarRating']
            state_rank = r[i]['Player']['StateRank']
            player_url = r[i]['Player']['Url']
            weight = r[i]['Player']['Weight']
            recruit_url = r[i]['RecruitInterestsUrl']
            status = r[i]['HighestRecruitInterestEventType']
            try:
                if status == '0':
                    status = None
            except:
                pass
            key = r[i]['Key']
            signed = r[i]['SignedInstitution']
            new_row = {'URL':player_url,'Recruit URL':recruit_url, 'Full Name':full_name, 'First Name':first_name, 'Last Name':last_name, 'City': city, 'State':state,
                                 'High School':high_school, 'Ht':height, 'Wt':weight, '247 Key':key,'Signed School':signed,'Player Photo':photo,
                                 'Position':position, 'National Rank':national_rank,'State Rank':state_rank, '247 Rating':rating,'Status':status,
                                 '247 Star Rating':star_rating,'Phone Number':phone}
            player_data = pd.concat([player_data, pd.DataFrame([new_row])], ignore_index=True)            

player_data = player_data.drop_duplicates() 
player_data.drop(index=player_data.index[0], 
        axis=0, 
        inplace=True)   
  
player_data = player_data.reset_index(drop=True)     
#Convert states 
player_data['State'] = player_data['State'].map(state_dic)

player_data['Signed School'] = player_data['Signed School'].map(school_dic)


#Convert positions
player_data['Position'] = player_data['Position'].map(position_dic)
  

player_data['Comp Rating'] = None
player_data['Comp Stars'] = None
      


for i in range(0,len(player_data)):
    headers = {'User-Agent': random.choice(header_list)}
    player_url = player_data.at[i, 'Recruit URL']
    if player_data.at[i, 'Status'] == 'Enrolled':
        continue

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
        player_data.at[i, 'Comp Rating'] = comp_rating
        player_data.at[i, 'Comp Stars'] = comp_stars
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

    signed_school = offers_soup[0].find('a').text.replace('\n','').strip()
    try:
        signed_school = signed_school.replace(signed_school, school_dic[signed_school])
    except:
        pass
        
    player_data.at[i, 'Signed School'] = signed_school


#Transform into template
template1 = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")

for i in range(0, len(player_data)):
    #Sort the data into the import template format
    template1.at[i, 'Last Name'] = player_data.at[i, 'Last Name']
    template1.at[i, 'First Name'] = player_data.at[i, 'First Name']
    template1.at[i, 'HS State'] = player_data.at[i, 'State']
    template1.at[i, 'HS Name'] = player_data.at[i, 'High School']
    template1.at[i, 'HS City'] = player_data.at[i, 'City']
    template1.at[i, 'College Primary Pos'] = player_data.at[i,'Position']
    template1.at[i, 'College Positions']= player_data.at[i, 'Position']
    template1.at[i, 'College Height'] = player_data.at[i, 'Ht']
    template1.at[i, 'College Weight'] = player_data.at[i, 'Wt']
    template1.at[i, 'College Active'] = 'Y'
    template1.at[i, '247 URL'] = player_data.at[i, 'URL']
    template1.at[i, 'College Name'] = player_data.at[i,'Signed School']
    template1.at[i, 'Recruiting Class'] = 2026
    template1.at[i, 'Player Photo'] = player_data.at[i, 'Player Photo']
    template1.at[i, '247 Key'] = player_data.at[i,'247 Key']
    template1.at[i, 'Industry Rating'] = player_data.at[i,'Comp Rating']
    template1.at[i, 'Industry Star'] = player_data.at[i,'Comp Stars']
    template1.at[i, '247 Star'] = player_data.at[i,'247 Star Rating']
  

template1 = template1.reset_index(drop=True)


template1 = pd.merge(template1, database[['Slug', '247 Key']], on='247 Key', how='left')  

driver.quit()

#Export to a csv with the current date and time
today =date.today()
today = today.strftime("%b-%d-%Y")

template1.to_excel(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\'' + str(today) + '247SigningDayNEW.xlsx', index=False)
