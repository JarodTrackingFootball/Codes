
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 11:53:38 2022

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
import re
from selenium.webdriver.chrome.options import Options


def extract_height(input_string):
    # Define the regular expression pattern to search for the height format
    pattern = r'\d{1,2}\'\d{1,2}'
    pattern2 = r'\d{1,2}\'\d{1,2}\"'
    
    # Use re.findall() to find all occurrences of the pattern in the input string
    heights = re.findall(pattern, input_string)
    if heights == None:
        heights = re.findall(pattern2, input_string)
    
    # Return the list of matched heights
    return heights

def extract_email(input_string):
    # Define a regular expression pattern to match email addresses
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    
    # Use re.search() to find the first email address in the input string
    match = re.search(pattern, input_string)
    
    # If a match is found, return the email address; otherwise, return None
    if match:
        return match.group()
    else:
        return None
    
def extract_first_three_digit_number(input_string):
    # Define a regular expression pattern to match a 3-digit number at the start of the string
    pattern = r'^\d{3}'
    
    # Use re.search() to find the first occurrence of the pattern in the input string
    match = re.search(pattern, input_string)
    
    # If a match is found, return the matched 3-digit number; otherwise, return None
    if match:
        return match.group()
    else:
        return None

player_data = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_081225-010053pm.xlsx")
#Open the driver 
options = Options()
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)


index_names = player_data[player_data['Twitter URL'] != player_data['Twitter URL']].index

player_data.drop(index_names, inplace=True)
#player_data = player_data[player_data['HS Class'] == 2026 | player_data['HS Class'] == 2027]

player_data = player_data.reset_index(drop=True)


data = pd.DataFrame({'Slug':[''], 'URL':[''],'GPA':[''],'ACT':[''],'SAT':[''],'Height':[''],'Weight':[''],'Phone Number':[''], 
                     'Email':[''],'NCAA ID':[''], 'High School':[''], 'Committed':[''], 'Committed School':[''],
                     'Baseball':[''],'Basketball':[''],'Golf':[''],"Hockey":[''],'Lacrosse':[''], 'Powerlifting':[''],
                     'Rugby':[''], 'Soccer':[''],'Swimming':[''],  'Tennis':[''],'Volleyball':[''], 
                     'Wrestling':[''],'Track':[''],'Notes':['']})

#conversions = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\CFBTeamTwitterLinks.csv")
#school_dic = conversions.set_index('Lower Case Handle')['TF New Name'].to_dict()
#school_twitters = conversions.set_index('Lower Case Handle')['TF New Name'].to_dict()
#driver = webdriver.Chrome(r"C:\Users\jtsve\OneDrive\Desktop\chromedriver")
for i in range(22396, len(player_data)):
    if type(player_data.at[i, 'Twitter URL']) == float:
        continue
    slug = player_data.at[i, 'Slug']
    basketball= 0
    baseball= 0
    golf= 0
    hockey= 0
    lacrosse= 0
    powerlifting= 0
    rugby= 0
    soccer= 0
    tennis= 0
    volleyball= 0
    wrestling= 0
    swimming = 0
    track = 0
    notes = None
    ncaa_id = None
    weight = None
    height = None
    url = player_data.at[i, 'Twitter URL']
    phone_number = email = high_school = committed_school = None
    committed = 0
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #bio = driver.find_element(By.CLASS_NAME, 'css-1dbjc4n').text
    if soup.find('div', {'data-testid':'UserDescription'}) or soup.find('span', {'data-testid':'UserJoinDate'}):
        pass
    else:
        new_row = {'Slug':slug,'URL':url,'Notes':'DNE'}
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        continue
    try:
        bio = soup.find('div', {'data-testid':'UserDescription'}).text
    except:
        bio = ""
        notes = "DNE"
    bio = bio.lower()
    gpa = None
    sat = None
    act = None
    #Get the gpa if it's in the bio
    if "gpa" in bio.lower() or 'g.p.a' in bio.lower() or 'g.p.a.' in bio.lower():
        if 'gpa' in bio:
            num = bio.lower().split('gpa')[0][-5:]
            num1 = bio.lower().split('gpa')[1][0:5]
        elif 'g.p.a' in bio:
            num = bio.lower().split('g.p.a')[0][-5:]
            num1 = bio.lower().split('g.p.a')[1][0:5]
        elif 'cumalative gpa' in bio:
            num = bio.split(" cumalative gpa")[0].split(" ")[-1]
            num1 = ""
        else:
            num = bio.lower().split('g.p.a.')[0][-5:]
            num1 = bio.lower().split('g.p.a.')[1][0:5]
        if 'gpa: ' in bio:
            num = bio.split('gpa: ')[1][0:3]
            gpa = [float(n) for n in re.findall(r'-?\d+\.?\d*', num)]
        if "\"" in num and "\'" in num:
            num = ""
        if "\"" in num1 and "\'" in num1:
            num1 = ""
        gpa = [float(n) for n in re.findall(r'-?\d+\.?\d*', num + num1)]
        if type(gpa) != float:
            for i in range(len(gpa)):
                if gpa[i] > 2 and gpa[i] < 5:
                    gpa = gpa[i]
                    break

    #Get the ACT score if its there
    
    if 'act' in bio and 'contact' not in bio:
        num = bio.lower().split('act')[0][-3:]
        num1 = bio.lower().split('act')[1][0:4]
        act = [float(n) for n in re.findall(r'-?\d+\.?\d*', num + num1)]
        if type(act) != float:
            for i in range(len(act)):
                if act[i] > 10 and act[i] < 37:
                    act = int(act[i])
                    break
    #Get the SAT score if its there
    if 'sat' in bio:
        num = bio.lower().split('sat')[0][-5:]
        num1 = bio.lower().split('sat')[1][0:6]
        sat = [float(n) for n in re.findall(r'-?\d+\.?\d*', num + num1)]
        if type(sat) != float:
            for i in range(len(sat)):
                if sat[i] > 600 and sat[i] < 1601:
                    sat = int(sat[i])
                    break

    if 'ncaa' in bio:
        if len(bio.split("ncaa")[1]) > 16:
            num = bio.split("ncaa")[1][0:17]
        else:
            num =  bio.split("ncaa")[1]
        ncaa = [float(n) for n in re.findall(r'-?\d+\.?\d*', num)]
        if type(ncaa) != float:
            for i in range(len(ncaa)):
                if ncaa[i] > 999999999:
                    ncaa_id = int(ncaa[i])
    if " lbs" in bio:
        weight = bio.split(" lbs")[0][-3:]
    elif "lbs" in bio:
        weight = bio.split("lbs")[0][-3:]
    try:    
        heights = extract_height(bio)
    except:
        pass
    try:
        height = heights[0]
    except:
        pass
    if weight == None and height != None:
        try:
            weight = extract_first_three_digit_number(bio.split(height)[1]) 
        except:
            pass
    if height != None:
        try:
            height = int(height.split("'")[0])*12 + int(height.split("'")[1])
        except:
            pass
    #Check fo text of other sports
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
    if 'state champ' in bio or 'state champion' in bio:
        notes = "State Champ"
    
    #Check for emoji's of sports:
    try:
        info = soup.find('div', {'data-testid':'UserDescription'})
        cards = info.find_all('img')
        for card in cards:
            card = card.get('src')
        #Basketball emoji's
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3c0.svg' in card:
                basketball = 1
        #Baseball emoji's
            if 'https://abs-0.twimg.com/emoji/v2/svg/26be.svg' in card:
                baseball = 1
        #golf emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/26f3.svg' in card:
                golf = 1
            elif 'https://abs-0.twimg.com/emoji/v2/svg/1f3cc.svg' in card:
                golf = 1
        #powerlifting emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3cb-1f3fb-200d-2642-fe0f.svg' in card:
                powerlifting = 1
        #hockey emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3d2.svg' in card:
                hockey = 1
        #lacrosse emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f94d.svg' in card:
                lacrosse = 1
        #rugby emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3c9.svg' in card:
                rugby = 1
        #soccer emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/26bd.svg' in card:
                soccer = 1
        #tennis emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3be.svg' in card:
                tennis = 1
        #wrestling emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f93c-200d-2642-fe0f.svg' in card:
                wrestling = 1
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f93c-200d-2640-fe0f.svg' in card:
                wrestling = 1
        #volleyball emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3d0.svg' in card:
                volleyball = 1
        #track emojis
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3c3-200d-2642-fe0f.svg' in card:
                track = 1
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3bd.svg' in card:
                track = 1
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3c3-1f3fe-200d-2642-fe0f.svg' in card:
                track = 1
            if 'https://abs-0.twimg.com/emoji/v2/svg/1f3c3-1f3fe.svg' in card:
                track = 1
    except:
        pass
    #Get the committed school
    if type(player_data.at[i, 'Committed School']) == str:
        pass
    

    else:
        """
        try:
            temps = bio.split('@')
            for temp in temps:
                possible = temp.split(" ")[0].lower()
                if possible in school_twitters:
                    committed_school = school_twitters[possible]
                    break
            for t in school_twitters:
                if str(t) in bio.lower():
                    if committed_school == "":
                        committed_school = school_twitters[t]
                        last_len = len(school_twitters[t])
                    elif school_twitters[t] in committed_school:
                        pass
                    else:
                        if len(school_twitters[t]) == last_len:
                            committed_school = committed_school + "/" + school_twitters[t]
                        elif len(school_twitters[t]) > last_len:
                            committed_school = school_twitters[t]
                        else:
                            pass
        except:
            pass
        """
        if "committed" in bio or "commit" in bio and "uncommitted" not in bio:
            committed = 1
            
            
            if " commit" in bio:
                if "uncommitted" in bio:
                    pass
                else:
                    committed_school = bio.split(" commit")[0]
                    if "university of " in committed_school:
                        committed_school = committed_school.split("university of ")[1]
                        try:
                            committed_school = committed_school.split(" commit")[0]
                        except:
                            pass
                    if "state" in bio:
                        try:
                            committed_school = bio.split(" state")[0].split(" ")[-2] + bio.split(" state")[0].split(" ")[-1]
                        except:
                            committed_school = bio.split(" state")[0].split(" ")[-1]
                        committed_school = committed_school + " State"
                            
                    elif " university" in bio:
                        try:
                            committed_school = bio.split(" university")[0].split(" ")[-2] + bio.split(" university")[0].split(" ")[-1]
                        except:
                            committed_school = bio.split(" university")[0].split(" ")[-1]
                    elif " football commit" in bio:
                        try:
                            committed_school = bio.split(" football commit")[0].split(" ")[-2] + bio.split(" football commit")[0].split(" ")[-1]
                        except:
                            committed_school = bio.split(" football commit")[0].split(" ")[-1]
                    
                    elif "committed to " in bio:
                        committed_school = bio.split("committed to ")[1]
                if type(committed_school) == str:
                    """
                    if "@" in committed_school:
                        committed_school = committed_school.replace('@', "")
                    try:
                        committed_school = school_dic[committed_school]
                    except:
                        pass
                    """
                    if committed_school.lower() == "second air force":
                        committed_school = "Air Force"
                    elif committed_school.lower() == "gvsu":
                        committed_school = "Grand Valley State"
                    elif committed_school.lower() == "west point":
                        committed_school = "Army"
                    elif committed_school.lower() == 'great lakes navy':
                        committed_school = 'Navy'
                    elif committed_school.lower() == "football":
                        committed_school = bio.split("football")[0].split(" ")[-1]
                    elif "state" in committed_school:
                        committed_school = committed_school.split(" state")[0] + " State"
                    elif "eastern " in committed_school or "western " in committed_school or "northern " in committed_school or "southern " in committed_school:
                        committed_school = committed_school.split(" ")[0] + " " + committed_school.split(" ")[1]
                    elif "east " in committed_school or "west " in committed_school or "north " in committed_school or "south " in committed_school:
                        committed_school = committed_school.split(" ")[0] + " " +committed_school.split(" ")[1]
                    elif "university" in committed_school:
                        committed_school = committed_school.split(" university")[0]
                    committed_school = committed_school.capitalize()

    #Get the Phone# and Email
    try:
        email = extract_email(bio)
    except:
        pass
    """
    if 'email: ' in bio:
        email = bio.split('email: ')[1]
        if len(email.split(" ")) > 1:
            email = email.split(" ")[0]
    elif 'email:' in bio:
        email = bio.split('email:')[1]
        if len(email.split(" ")) > 1:
            email = email.split(" ")[0]
    elif 'email- ' in bio:
        email = bio.split('email- ')[1]
        if len(email.split(" ")) > 1:
            email = email.split(" ")[0]
    elif 'email-' in bio:
        email = bio.split('email-')[1]
        if len(email.split(" ")) > 1:
            email = email.split(" ")[0]
        if "," in email:
            email = email.replace(",", "")
        if "|" in email:
            email = email.replace("|", "")
    elif '@gmail.com' in bio:
        email = bio.split('@gmail.com')[0].split(" ")[-1] + "@gmail.com"
    elif '@yahoo.com' in bio:
        email = bio.split('@yahoo.com')[0].split(" ")[-1] + "@yahoo.com"
    if type(email) == str and len(email) > 2:
        if '.com' in email:
           email = email.split('.com')[0] + ".com"
        elif '.org' in email:
           email = email.split('.org')[0] + '.org'
        if email[0] == '@' or email[0] == '|':
            email = email[1:]
        if email[-1] == ',' or  email[-1] == '.' or  email[-1] == '|':   
            email = email[:-1]
        if "|" in email:
            email = email.split("|")[-1]
        if "/" in email:
            email = email.split("/")[-1]
    """  
    try:
        phone_number = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', bio)[0]
        if "ncaa" in bio or "ncsa" in bio or "id" in bio:
            phone_number = ""
        if "." in phone_number:
            phone_number = ""
        phone_number = phone_number.replace('-',"")
        phone_number = phone_number.replace('(',"")
        phone_number = phone_number.replace(')',"")
        phone_number = phone_number.replace(' ',"")
    except:
        pass
    if ("head coach" in bio or "hc" in bio) and phone_number != None:
        phone_number = "Coach Check"
    #Get the High School Name(don't know if i should get 1 or 2 before)
    if 'high school' in bio:
        front = bio.split(' high school')[0]
        if len(front.split(" ")) == 1:
            high_school = front
        elif len(front.split(" ")) > 1:
            high_school = front.split(" ")[-2] + " " +  front.split(" ")[-1]
            if '|' in high_school or '/' in high_school:
                high_school = high_school.split(" ")[-1]
            try:
                matches = re.findall('[0-9]', high_school)
                if len(matches) > 0:
                    high_school = high_school.split(" ")[-1]
            except:
                pass
        elif 'hs' in bio:
            front = bio.split(' hs')[0]
            if len(front.split(" ")) == 1:
                high_school = front
            elif len(front.split(" ")) > 1:
                high_school = front.split(" ")[-2] + " " +  front.split(" ")[-1]
                if '|' in high_school or '/' in high_school:
                    high_school = high_school.split(" ")[-1]
                try:
                    matches = re.findall('[0-9]', high_school)
                    if len(matches) > 0:
                        high_school = high_school.split(" ")[-1]
                except:
                    pass
        if type(high_school) == str:
            if "gpa " in high_school:
                high_school = high_school.replace('gpa ', '')
            if "@" in high_school:
                high_school = high_school.replace('@','')
            high_school = high_school.title()
            high_school = high_school.strip()
        try:
            email = email.strip()
        except:
            pass
        try:
            committed_school = committed_school.strip()
            committed_school = committed_school.title()
        except:
            pass
        
    new_row = {'Slug':slug,'URL':url, 'GPA':gpa,'ACT':act,'SAT':sat,'Height':height,'Weight':weight, 'Phone Number':phone_number, 
                         'Email':email, 'NCAA ID':ncaa_id,'High School':high_school, 'Committed':committed, 'Committed School':committed_school,
                         'Basketball':basketball, 'Baseball':baseball,
                         'Track':track,'Wrestling':wrestling,"Hockey":hockey, 'Soccer':soccer,'Swimming':swimming,
                         'Volleyball':volleyball, 'Powerlifting':powerlifting, 'Rugby':rugby,
                         'Golf':golf,
                         'Lacrosse':lacrosse, 'Tennis':tennis, 'Notes':notes}
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

for i in range(len(data)):
    if type(data.at[i, 'ACT']) == list:
        data.at[i, 'ACT'] = None
    if type(data.at[i, 'GPA']) == list:
            data.at[i, 'GPA'] = None
    if type(data.at[i, 'SAT']) == list:
            data.at[i, 'SAT'] = None
            
data.drop(index=data.index[0], 
        axis=0, 
        inplace=True)  

driver.quit()

data.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\Bios_8-18-25.xlsx", index=False) 



