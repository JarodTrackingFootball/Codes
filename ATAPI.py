# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 08:24:49 2023

@author: jtsve
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 13:53:55 2023

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
from selenium.webdriver.common.action_chains import ActionChains
import itertools
import requests
import warnings
import random
import datetime
import os
import json

flags = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\TrackFlags(4-24).xlsx")
flag_urls = list(flags['Athletic URL'])
flags.set_index('Athletic URL', inplace=True)

warnings.simplefilter(action='ignore', category=FutureWarning)

today = datetime.date.today()
date_string = today.strftime("%m-%d-%Y")
folder_path = r"C:\Users\jtsve\OneDrive\Desktop\ATHJson"

player_data = pd.read_excel(r"C:\Users\jtsve\OneDrive\Documents\ATHtoRun(9-8).xlsx")


index_names = player_data[player_data['Athletic URL'] != player_data['Athletic URL']].index

player_data.drop(index_names, inplace=True)
player_data = player_data.reset_index(drop=True)

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



df = pd.DataFrame({'Slug':[''],'URL':[''],'Class':[''],'Event':[''], 'PR':[''], 'Meet':[''], 'Meet_ID':[''], 'Year':[''], 'Date':['']})

for r in range(0,len(player_data)):
    #random_number = random.randint(3, 10)
    #time.sleep(random_number)
    slug = player_data.at[r, 'Slug']
    url = player_data.at[r, 'Athletic URL']
    class_ = player_data.at[r, 'HS Class']
    headers = {'User-Agent': random.choice(header_list)}
    proxy = random.choice(proxies)
    
    if "AID=" in url:
        playerid = url.split("AID=")[1]
    else:
        try:
            playerid = url.split("athlete/")[1].split("/")[0]
        except:
            continue
    player_page = 'https://www.athletic.net/api/v1/AthleteBio/GetAthleteBioData?athleteId='+str(playerid)+'&sport=tf&level=0'
    try:
        response1 = requests.get(player_page, headers=headers,proxies = {'http':proxy, 'https':proxy})
        r1 = response1.json()
    except:
        r = r-1
        continue
    try:
        filename = f"{playerid}({date_string})"
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as json_file:
            json.dump(r1, json_file)
    except:
        pass
    
    df1 = pd.DataFrame({'Slug':[''],'URL':[''],'Class':[''],'Event':[''], 'PR':[''], 'Meet':[''], 'Meet_ID':[''], 'Year':[''], 'Date':['']})
    df2 = pd.DataFrame({'Slug':[''],'URL':[''],'Class':[''],'Event':[''], 'PR':[''], 'Meet':[''], 'Meet_ID':[''], 'Year':[''], 'Date':['']})
    
    try:
        results = r1['resultsTF']
        meets = r1['meets']
    except:
        continue
    for result in results:
        date = None
        year = None
        converted = False
        meet= None
        if result['PersonalBest'] == 0:
            continue
        try:
            if "h" in result['Result']:
                continue
        except:
            pass
        try:
            if "?" in result['Result']:
                continue
        except:
            pass
        if result['EventID'] == 7:
            event_name = '400R'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            try:
                hour = float(str(pr.split(":")[0])) * 60
                second = float(str(pr.split(":")[1]))
                pr = str(hour + second)
            except:
                pass
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 50:
            event_name = '800R'
            try:
                if result['Wind'] >= 3:
                    continue
            except:
                pass
            try:
                if result['FAT'] != 1:
                    continue
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 8:
            event_name = '1600R'
            try:
                if result['Wind'] >= 3:
                    continue
            except:
                pass
            try:
                if result['FAT'] != 1:
                    continue
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 39:
            event_name = '3200R'
            try:
                if result['Wind'] >= 3:
                    continue
            except:
                pass
            try:
                if result['FAT'] != 1:
                    continue
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 4:
            event_name = '800'
            try:
                if result['Wind'] >= 3:
                    continue
            except:
                pass
            try:
                if result['FAT'] != 1:
                    continue
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 1:
            event_name = '100M'
            if result['EventTypeID'] == 98:
                continue
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0:1] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            if event_name == 'High Jump':
                if result < 500:
                    continue
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 2:
            event_name = '200M'
            if result['EventTypeID'] == 98:
                continue
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0:1] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    wind = str(result['Wind'])
                    meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 41:
            event_name = '55M'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0:1] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 42:
            event_name = '60M'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0:1] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 43:
            event_name = '55HH'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0:1] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 44:
            event_name = '60HH'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass

            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 10:
            event_name = '110HH'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 45:
            event_name = '400H'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            try:
                hour = float(pr.split(":")[0]) * 60
                second = float(pr.split(":")[1])
                pr = str(hour + second)
            except:
                pass
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 105:
            event_name = '300M'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            try:
                hour = float(pr.split(":")[0]) * 60
                second = float(pr.split(":")[1])
                pr = str(hour + second)
            except:
                pass
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 3:
            event_name = '400M'
            if result['EventTypeID'] == 98:
                continue
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            try:
                hour = float(pr.split(":")[0]) * 60
                second = float(pr.split(":")[1])
                pr = str(hour + second)
            except:
                pass
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 11:
            event_name = '300IH'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            try:
                if result['FAT'] != 1:
                    continue
            except:
                pass
            if result['SortInt'] != result['SortIntRaw']:
                try:
                    pr = str(result['SortInt'])
                    if len(pr) == 4:
                        pr = str(pr[0] + "." + pr[1:3])
                    elif len(pr) == 5:
                        pr = str(pr[0:2] + "." + pr[2:4])
                    converted = True
                except:
                    pass
            else:
                pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            try:
                hour = float(pr.split(":")[0]) * 60
                second = float(pr.split(":")[1])
                pr = str(hour + second)
            except:
                pass
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            if converted == True:
                meet = meet + " (Converted time)"
            try:
               if str(result['Wind']) != 'None':
                   if result['Wind'] != 0:
                       wind = str(result['Wind'])
                       meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 12:
            event_name = 'Shot Put'
            if result['EventTypeID'] == 10:
                continue
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            try:
                if result['Description'] != '12lb':
                    continue
            except:
                pass
            if 'm' not in pr:
                try:
                    if "\"" in pr:
                        pr = pr.replace("\"","")
                    if "-" in pr:
                        inches = int(float(pr.split("-")[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split("-")[0]+inches
                    elif "\' " in pr:
                        inches = int(float(pr.split('\' ')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\' ')[0] + inches
                    else:
                        inches = int(float(pr.split('\'')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\'')[0] + inches
                except:
                    pass
            if 'm' in pr:
                text = float(str(pr).split('m')[0])
                inches = text*39.3700787
                ft = int(inches/12)
                inches = inches - (ft*12)
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                pr = f"{ft}{inches}"
                pr = float(pr)
                pr = int(pr)
                pr = str(pr)
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 17:
            event_name = 'Long Jump'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            if 'm' not in pr:
                try:
                    if "\"" in pr:
                        pr = pr.replace("\"","")
                    if "-" in pr:
                        inches = int(float(pr.split("-")[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split("-")[0]+inches
                    elif "\' " in pr:
                        inches = int(float(pr.split('\' ')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\' ')[0] + inches
                    else:
                        inches = int(float(pr.split('\'')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\'')[0] + inches
                except:
                    pass
            if 'm' in pr:
                text = float(str(pr).split('m')[0])
                inches = text*39.3700787
                ft = int(inches/12)
                inches = inches - (ft*12)
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                pr = f"{ft}{inches}"
                pr = float(pr)
                pr = int(pr)
                pr = str(pr)
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
               if str(result['Wind']) != 'None':
                   if result['Wind'] != 0:
                       wind = str(result['Wind'])
                       meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                if int(pr) < 1500:
                    continue
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 18:
            event_name = 'Triple Jump'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            if 'm' not in pr:
                try:
                    if "\"" in pr:
                        pr = pr.replace("\"","")
                    if "-" in pr:
                        inches = int(float(pr.split("-")[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split("-")[0]+inches
                    elif "\' " in pr:
                        inches = int(float(pr.split('\' ')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\' ')[0] + inches
                    else:
                        inches = int(float(pr.split('\'')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\'')[0] + inches
                except:
                    pass
            if 'm' in pr:
                text = float(str(pr).split('m')[0])
                inches = text*39.3700787
                ft = int(inches/12)
                inches = inches - (ft*12)
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                pr = f"{ft}{inches}"
                pr = float(pr)
                pr = int(pr)
                pr = str(pr)
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
               if str(result['Wind']) != 'None':
                   if result['Wind'] != 0:
                       wind = str(result['Wind'])
                       meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 13:
            event_name = 'Discus'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            try:
                if result['Description'] != '1.6kg':
                    continue
            except:
                pass
            if 'm' not in pr:
                try:
                    if "\"" in pr:
                        pr = pr.replace("\"","")
                    if "-" in pr:
                        inches = int(float(pr.split("-")[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split("-")[0]+inches
                    elif "\' " in pr:
                        inches = int(float(pr.split('\' ')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\' ')[0] + inches
                    else:
                        inches = int(float(pr.split('\'')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\'')[0] + inches
                except:
                    pass
            if 'm' in pr:
                text = float(str(pr).split('m')[0])
                inches = text*39.3700787
                ft = int(inches/12)
                inches = inches - (ft*12)
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                pr = f"{ft}{inches}"
                pr = float(pr)
                pr = int(pr)
                pr = str(pr)
                
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:    
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 14:
            event_name = 'Javelin'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            try:
                if result['Description'] != '800g':
                    continue
            except:
                pass
            if 'm' not in pr:
                try:
                    if "\"" in pr:
                        pr = pr.replace("\"","")
                    if "-" in pr:
                        inches = int(float(pr.split("-")[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split("-")[0]+inches
                    elif "\' " in pr:
                        inches = int(float(pr.split('\' ')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\' ')[0] + inches
                    else:
                        inches = int(float(pr.split('\'')[1]))
                        if inches < 10:
                            inches = f"0{inches}"
                        else:
                            inches = str(inches)
                        pr = pr.split('\'')[0] + inches
                except:
                    pass
            if 'm' in pr:
                text = float(str(pr).split('m')[0])
                inches = text*39.3700787
                ft = int(inches/12)
                inches = inches - (ft*12)
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                pr = f"{ft}{inches}"
                pr = float(pr)
                pr = int(pr)
                pr = str(pr)
                
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 9:
            event_name = 'High Jump'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            if 'm' not in pr:
               try:
                   if "\"" in pr:
                       pr = pr.replace("\"","")
                   if "-" in pr:
                       inches = int(float(pr.split("-")[1]))
                       if inches < 10:
                           inches = f"0{inches}"
                       else:
                           inches = str(inches)
                       pr = pr.split("-")[0]+inches
                   elif "\' " in pr:
                       inches = int(float(pr.split('\' ')[1]))
                       if inches < 10:
                           inches = f"0{inches}"
                       else:
                           inches = str(inches)
                       pr = pr.split('\' ')[0] + inches
                   else:
                       inches = int(float(pr.split('\'')[1]))
                       if inches < 10:
                           inches = f"0{inches}"
                       else:
                           inches = str(inches)
                       pr = pr.split('\'')[0] + inches
               except:
                   pass
            if 'm' in pr:
                text = float(str(pr).split('m')[0])
                inches = text*39.3700787
                ft = int(inches/12)
                inches = inches - (ft*12)
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                pr = f"{ft}{inches}"
                pr = float(pr)
                pr = int(pr)
                pr = str(pr)
                
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                if int(pr) < 500:
                    continue
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
            continue
        elif result['EventID'] == 16:
            event_name = 'Pole Vault'
            try:
                if result['Wind'] >= 3:
                    continue
                    
            except:
                pass
            pr = result['Result']
            try:
                pr = pr.replace("a","")
            except:
                continue
            if 'm' not in pr:
               try:
                   if "\"" in pr:
                       pr = pr.replace("\"","")
                   if "-" in pr:
                       inches = int(float(pr.split("-")[1]))
                       if inches < 10:
                           inches = f"0{inches}"
                       else:
                           inches = str(inches)
                       pr = pr.split("-")[0]+inches
                   elif "\' " in pr:
                       inches = int(float(pr.split('\' ')[1]))
                       if inches < 10:
                           inches = f"0{inches}"
                       else:
                           inches = str(inches)
                       pr = pr.split('\' ')[0] + inches
                   else:
                       inches = int(float(pr.split('\'')[1]))
                       if inches < 10:
                           inches = f"0{inches}"
                       else:
                           inches = str(inches)
                       pr = pr.split('\'')[0] + inches
               except:
                   pass
            if 'm' in pr:
                text = float(str(pr).split('m')[0])
                inches = text*39.3700787
                ft = int(inches/12)
                inches = inches - (ft*12)
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                pr = f"{ft}{inches}"
                pr = float(pr)
                pr = int(pr)
                pr = str(pr)
                
            year = result['SeasonID']
            meet_id = result['MeetID']
            try:
                meet = meets[str(meet_id)]['MeetName']
            except:
                pass
            try:
                if str(result['Wind']) != 'None':
                    if result['Wind'] != 0:
                        wind = str(result['Wind'])
                        meet = f"{meet} ({wind}w)"
            except:
                pass
            try:
                date = meets[str(meet_id)]['EndDate'].split("T")[0]
                month = date.split("-")[1]
                year = date.split("-")[0]
                day = date.split("-")[2]
                date = f"{month}/{day}/{year}"
            except:
                pass
            new_row = {'Slug':slug,'URL':url,'Class':class_,'Event':event_name, 'PR':pr, 'Meet':meet, 'Meet_ID':meet_id, 'Year':year, "Date":date}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
            
            continue
        
    if url in flag_urls:
        for t in range(len(df1)):
            try:
                if str(df1.at[t, 'PR']) == str(flags.loc[url, df1.at[t, 'Event']]):
                    df1.drop(t, inplace = True)
            except:
                pass
        for l in range(len(df2)):
            try:
                if str(df2.at[l, 'PR']) == str(flags.loc[url, df2.at[l, 'Event']]):
                    df2.drop(t, inplace = True)
            except:
                pass
            
    index_names = df1[df1['URL'] == ''].index
    df1.drop(index_names, inplace=True)
    df1 = df1.reset_index(drop=True)
    df1 = df1.sort_values('PR')
    df1 = df1.drop_duplicates(subset='Event', keep='first')
    frames= [df,df1]
    df = pd.concat(frames)
    
    index_names = df2[df2['URL'] == ''].index
    df2.drop(index_names, inplace=True)
    df2 = df2.reset_index(drop=True)
    df2 = df2.sort_values('PR', ascending=False)
    df2 = df2.drop_duplicates(subset='Event', keep='first')
    frames= [df,df2]
    df = pd.concat(frames)
    
df = df.drop_duplicates() 
df = df.reset_index(drop=True)

template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")

errors = ['DNF', 'DQ', 'DNS', 'NT', 'SCR', 'FS']

for i in range(0,len(df)):
    if df.at[i, 'PR'] in errors:
        continue
    try:
        if abs(df.at[i, 'Class'] - df.at[i, 'Year']) > 3:
            continue
    except:
        pass
    try:
        event = df.at[i, 'Event']
        template.at[i, event] = df.at[i, 'PR']
    except:
        continue
    template.at[i, 'TF Date'] = df.at[i, 'Date']
    template.at[i, 'Athletic URL'] = df.at[i, 'URL']
    template.at[i,'TF Year'] = df.at[i, 'Year']
    try:
        template.at[i,'TF Meet'] = (df.at[i, 'Meet'] + " TF Meet").strip()
    except:
        pass
    template.at[i, 'Slug'] = df.at[i, 'Slug']
    template.at[i, 'Track'] = 1

writer = pd.ExcelWriter('FullTrackPull(9-8).xlsx')
template.to_excel(writer, index=False)
#writer.save()
writer.close()

events_tf = ['55M', '60M','55HH', '60HH', '100M', '110HH', '200M', '300M', '300IH','400M','400H',
             '800','400R','800R','1600R','3200R','Shot Put','Discus', 'Javelin','High Jump',
             'Long Jump', 'Triple Jump', 'Pole Vault']

for event in events_tf:
    temp_df = template.dropna(subset=[event])
    #temp_df = temp_df.dropna(subset=['Slug'])
    temp_df['HS Class'] = None
    temp_df['HS State'] = None
    temp_df['HS Name'] = None
    temp_df['Last Name'] = None
    temp_df['First Name'] = None
    temp_df['Athletic URL'] = None
    temp_df['TF Year'] = None
    temp_df.to_excel(r"C:\Users\jtsve\OneDrive\Documents\/"+event+"Updates-FULL"+".xlsx",index=False)

template.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\ATRun(9-8).csv",index=False)

