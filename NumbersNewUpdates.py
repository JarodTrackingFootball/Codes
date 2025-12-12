# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 09:23:02 2024

@author: jtsve
"""

import pandas as pd
import numpy as np

#Import Files to compare
db = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_070725-103428am.xlsx")
df = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\NumbersRun(7-28).csv")

index_names = db[db['247 Key'] != db['247 Key']].index

db.drop(index_names, inplace=True)
db = db.reset_index(drop=True)

db['247 Key'] = db['247 Key'].astype(int)

df['High School'] = df['High School'].str.strip()

df = pd.merge(df, db[['Slug','HS Class','HS State', 'HS Name', 'Player Photo', 'Industry Rating', 'Industry Star','247 Star', 'Committed School', '247 Key',
                      'Baseball','Basketball','Golf',"Hockey",'Lacrosse', 'Powerlifting',
                      'Rugby', 'Soccer','Swimming',  'Tennis','Volleyball', 
                      'Wrestling','Track', 'About']], on='247 Key', how='left')


index_names = df[df['Slug'] != df['Slug']].index

df.drop(index_names, inplace=True)
df = df.reset_index(drop=True)

for i in range(len(df)):
    if df.at[i, 'State'] == df.at[i, 'HS State']:
        df.at[i, 'State'] = None
    if df.at[i, 'High School'] == df.at[i, 'HS Name']:
        df.at[i, 'High School'] = None
    if df.at[i, 'Year'] == df.at[i, 'HS Class']:
        df.at[i, 'Year'] = None
    if df.at[i, 'Player Photo_x'] == df.at[i, 'Player Photo_y']:
        df.at[i, 'Player Photo_x'] = None
    if df.at[i, 'Industry Rating_x'] == df.at[i, 'Industry Rating_y']:
        df.at[i, 'Industry Rating_x'] = None
    if df.at[i, 'Industry Stars'] == df.at[i, 'Industry Stars']:
        df.at[i, 'Industry Stars'] = None
    if df.at[i, '247 Star Rating'] == df.at[i, '247 Star']:
        df.at[i, '247 Star Rating'] = None
    if df.at[i, 'Status'] == 'Decommit':
        if df.at[i, 'Committed School_y'] == df.at[i, 'Committed School_y']:
            df.at[i, 'Committed School_x'] = 'uncommitted'
            
template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")
bad_index = []

for j in range(len(df)):
    status = 0
    template.at[j, 'Slug'] = df.at[j, 'Slug']
    if df.at[j, 'State'] != None and df.at[j, 'State'] == df.at[j, 'State']:
        template.at[j, 'HS State'] = df.at[j, 'State']
        status = 1
    if df.at[j, 'Year'] != None and df.at[j, 'Year'] == df.at[j, 'Year']:
        template.at[j, 'HS Class'] = df.at[j, 'Year']
        status = 1
    if df.at[j, 'High School'] != None and df.at[j, 'High School'] == df.at[j, 'High School']:
        template.at[j, 'HS Name'] = df.at[j, 'High School']
        """
        if df.at[j, 'About'] != df.at[j, 'About']:
            template.at[j, 'About'] = "Previously Attended " + df.at[j, 'HS Name']
        else:
            template.at[j, 'About'] = df.at[j, 'About'] + "; Previously Attended " + df.at[j, 'HS Name']
        status = 1
        """
    if df.at[j, 'Player Photo_x'] != None and df.at[j, 'Player Photo_x'] == df.at[j, 'Player Photo_x']:
        template.at[j, 'Player Photo'] = df.at[j, 'Player Photo_x']
        status = 1
    if df.at[j, 'Industry Rating_x'] != None and df.at[j, 'Industry Rating_x'] == df.at[j, 'Industry Rating_x']:
        template.at[j, 'Industry Rating'] = df.at[j, 'Industry Rating_x']
        status = 1
    if df.at[j, 'Industry Stars'] != None and df.at[j, 'Industry Stars'] == df.at[j, 'Industry Stars']:
        template.at[j, 'Industry Stars'] = df.at[j, 'Industry Stars']
        status = 1
    if df.at[j, '247 Star Rating'] != None and df.at[j, '247 Star Rating'] == df.at[j, '247 Star Rating']:
        template.at[j, '247 Star'] = df.at[j, '247 Star Rating']
        status = 1
    if df.at[j, 'Committed School_x'] == 'uncommitted':
        template.at[j, 'Committed School'] = 'uncommitted'
        status = 1
    if df.at[j, 'Baseball_x'] == 1 and df.at[0, 'Baseball_y'] != df.at[0, 'Baseball_y']:
        template.at[j, 'Baseball'] = 1
        status = 1
    if df.at[j, 'Basketball_x'] == 1 and df.at[0, 'Basketball_y'] != df.at[0, 'Basketball_y']:
        template.at[j, 'Basketball'] = 1
        status = 1
    if df.at[j, 'Golf_x'] == 1 and df.at[0, 'Golf_y'] != df.at[0, 'Golf_y']:
        template.at[j, 'Golf'] = 1
        status = 1
    if df.at[j, 'Hockey_x'] == 1 and df.at[0, 'Hockey_y'] != df.at[0, 'Hockey_y']:
        template.at[j, 'Hockey'] = 1
        status = 1
    if df.at[j, 'Lacrosse_x'] == 1 and df.at[0, 'Lacrosse_y'] != df.at[0, 'Lacrosse_y']:
        template.at[j, 'Lacrosse'] = 1
        status = 1
    if df.at[j, 'Powerlifting_x'] == 1 and df.at[0, 'Powerlifting_y'] != df.at[0, 'Powerlifting_y']:
        template.at[j, 'Powerlifting'] = 1
        status = 1
    if df.at[j, 'Rugby_x'] == 1 and df.at[0, 'Rugby_y'] != df.at[0, 'Rugby_y']:
        template.at[j, 'Rugby'] = 1
        status = 1
    if df.at[j, 'Soccer_x'] == 1 and df.at[0, 'Soccer_y'] != df.at[0, 'Soccer_y']:
        template.at[j, 'Soccer'] = 1
        status = 1
    if df.at[j, 'Swimming_x'] == 1 and df.at[0, 'Swimming_y'] != df.at[0, 'Swimming_y']:
        template.at[j, 'Swimming'] = 1
        status = 1
    if df.at[j, 'Tennis_x'] == 1 and df.at[0, 'Tennis_y'] != df.at[0, 'Tennis_y']:
        template.at[j, 'Tennis'] = 1
        status = 1
    if df.at[j, 'Volleyball_x'] == 1 and df.at[0, 'Volleyball_y'] != df.at[0, 'Volleyball_y']:
        template.at[j, 'Volleyball'] = 1
        status = 1
    if df.at[j, 'Wrestling_x'] == 1 and df.at[0, 'Wrestling_y'] != df.at[0, 'Wrestling_y']:
        template.at[j, 'Wrestling'] = 1
        status = 1
    if df.at[j, 'Track_x'] == 1 and df.at[0, 'Track_y'] != df.at[0, 'Track_y']:
        template.at[j, 'Track'] = 1
        status = 1
    if status == 0:
        bad_index.append(j)
        
      

template.drop(bad_index, inplace=True)
template = template.reset_index(drop=True) 
        
        
template.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\NumbersUpdates(8-5).xlsx",index=False)        
        
        
        
        
        
        
        
        