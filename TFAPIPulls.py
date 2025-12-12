# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 12:38:01 2024

@author: jtsve
"""

import requests
import json
import pandas as pd
import warnings
import time
import itertools
import requests
import warnings
import random
import datetime
import os
import json

warnings.simplefilter(action='ignore', category=FutureWarning)

today = datetime.date.today()
date_string = today.strftime("%m-%d-%Y")
folder_path = r"C:\Users\jtsve\OneDrive\Desktop\TFAPIJsons"

player_data = pd.read_excel(r"C:\Users\jtsve\Downloads\First college.xlsx")
df = pd.DataFrame({'Slug':[''],'Hand':[''],'3Cone':[''],'Height':[''],'Weight':[''],'40mDash':[''],
              'Shuttle':[''],'Wing':[''],'Arm':[''],'Broad':[''],'Power Toss':[''],'Vertical':[''],'Date':[''],
              'City':[''],'Type':[''],'Rating':[''], 'First College':['']})
for i in range(187235,len(player_data)):
    #time.sleep(2)
    slug = player_data.at[i, 'Slug']
    url_request = 'https://tfb2-api.trackingfootball.com/api/v1/api/player-details?type=slug&value='+slug
    try:
        response = requests.get(url_request, headers={'api-key':'6e0520d5-f63f-47aa-b89e-46c356f48e0a','Connection':'close'})
    except:
        time.sleep(10)
        response = requests.get(url_request, headers={'api-key':'6e0520d5-f63f-47aa-b89e-46c356f48e0a','Connection':'close'})
    r = response.json()
    try:
        filename = f"{slug}({date_string})"
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as json_file:
            json.dump(r, json_file)
    except:
        pass
    combines = r['hsCombines']
    college_list = []
    college_list_str = None
    colleges = r['playerColleges']
    try:
        for college in colleges:
            college_list.append(college['team']['name'])
        college_list_str = ','.join(college_list)
    except:
        pass
    new_row = {'Slug':slug,'First College':college_list_str}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    for combine in combines:
        arm = combine['arm']
        city = combine['city']
        hand = combine['hand']
        type_ = combine['type']
        cone = combine['3Cone']
        height = combine['height']
        weight = combine['weight']
        rating = combine['rating']
        forty = combine['40mDash']
        shuttle = combine['shuttle']
        wing = combine['wingspan']
        broad = combine['broadJump']
        date = combine['combineDate']
        vert = combine['verticalJump']
        power = combine['powerToss']
    
        new_row = {'Slug':slug,'Hand':hand,'3Cone':cone,'Height':height,'Weight':weight,'40mDash':forty,
                      'Shuttle':shuttle,'Wing':wing,'Arm':arm,'Broad':broad,'Power Toss':power,'Vertical':vert,'Date':date,
                      'City':city,'Type':type_,'Rating':rating, 'First College':college_list_str}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\TFAPIResults(11-18).csv",index=False)


df1 = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\CombineAPIResults(9-20).csv")

for i in range(0,len(player_data)):
    college_list = []
    college_list_str = None
    slug = player_data.at[i, 'Slug']
    url_request = 'https://tfb2-api.trackingfootball.com/api/v1/api/player-details?type=slug&value='+slug
    try:
        response = requests.get(url_request, headers={'api-key':'6e0520d5-f63f-47aa-b89e-46c356f48e0a'})
        r = response.json()
    except:
        time.sleep(10)
        i = i-1
        continue
    #time.sleep(.5)
    colleges = r['playerColleges']
    try:
        for college in colleges:
            try:
                college_list.append(college['team']['name'])
            except:
                pass
        college_list_str = ','.join(college_list)
        #df1 = df1.append({'Slug':slug,'Colleges':college_list_str},ignore_index=True)
        player_data.at[i, 'First College'] = college_list_str
    except:
        pass
    8
player_data.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\CombineAPIResults(12-2)-2.csv",index=False)


player_data = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_081825-100225am.xlsx")
df = pd.DataFrame({'Slug':[''],'Hand':[''],'3Cone':[''],'Bench':[''],'Height':[''],'Weight':[''],'10 Split':[''],
                   '20 Split':[''],'40mDash':[''],
              'Shuttle':[''],'Wing':[''],'Arm':[''],'Broad':[''],'Position':[''],'Vertical':[''],'Date':[''],
              'City':[''],'Type':[''],'Combine Score':['']})

for i in range(5882,len(player_data)):
    slug = player_data.at[i, 'Slug']
    url_request = 'https://tfb2-api.trackingfootball.com/api/v1/api/player-details?type=slug&value='+slug
    response = requests.get(url_request, headers={'api-key':'6e0520d5-f63f-47aa-b89e-46c356f48e0a'})
    r = response.json()
    combines = r['nflCombines']
    for combine in combines:
        arm = combine['arm']
        hand = combine['hand']
        type_ = combine['type']
        cone = combine['3Cone']
        bench = combine['bench']
        height = combine['height']
        weight = combine['weight']
        forty = combine['40mDash']
        shuttle = combine['shuttle']
        wing = combine['wingspan']
        broad = combine['broadJump']
        date = combine['combineDate']
        vert = combine['verticalJump']
        try:
            pos = combine['positions'][0]['code']
        except:
            pos = None
        ten = combine['10Split']
        twenty = combine['20Split']
        combine_score = r['nflCombineScore']
        new_row = {'Slug':slug,'Hand':hand,'3Cone':cone,'Bench':bench,'Height':height,'Weight':weight,
                        '10 Split':ten,'20 Split':twenty,'40mDash':forty,
                      'Shuttle':shuttle,'Wing':wing,'Arm':arm,'Broad':broad,'Position':pos,'Vertical':vert,'Date':date
                      ,'Type':type_,'Combine Score':combine_score}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        

df.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\NFLCombineAPIResults(8-18).xlsx",index=False)
len(df)










