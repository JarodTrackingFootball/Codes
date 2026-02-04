# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 08:27:06 2025

@author: jtsve
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 10:30:18 2023

@author: jtsve
"""

import pandas as pd

conversions = pd.read_csv(r'C:\Users\jtsve\OneDrive\Desktop\Template Files\ScrapingConversion.csv')
school_dic = conversions.set_index('R')['T'].to_dict()

contact = pd.read_excel(r"C:\Users\jtsve\OneDrive\Documents\PrepAboutData1-2026.xlsx")
results = pd.read_excel(r"C:\Users\jtsve\OneDrive\Documents\PrepData1-2026.xlsx")



#contact['Class'] = contact['Class'].astype(str)




df = pd.merge(contact, results, on='Match', how='outer')
df['Offers'] = None


for i in range(len(df)):
 
    offer_list = []
    offers = None
    offer_count = 0
    try:
        if "@" in df.at[i, 'Player X Handle']:
            df.at[i, 'Player X Handle'] = df.at[i, 'Player X Handle'].replace("@","")
            if "X.com" in df.at[i, 'Player X Handle']:
                df.at[i, 'Player X Handle'] = df.at[i, 'Player X Handle'].split('X.com/')[1]
    except:
        pass
    try:
        if "@" in df.at[i, 'Player Instagram Handle']:
            df.at[i, 'Player Instagram Handle'] = df.at[i, 'Player Instagram Handle'].replace("@","")
        if "instagram.com" in df.at[i, 'Player Instagram Handle']:
            df.at[i, 'Player Instagram Handle'] = df.at[i, 'Player Instagram Handle'].split('instagram.com/')[1]
    except:
        pass
    try:
        if df.at[i, 'SAT Score'] in ['N/A',"Didn’t take yet", "Didn’t take this", "Na","N/a","None","?",'-']:
            df.at[i, 'SAT Score'] = None
    except:
        pass
    try:
        if df.at[i, 'ACT Score'] in ['N/A',"Didn’t take yet", "Didn’t take this", "Na","N/a","None","?",'-']:
            df.at[i, 'ACT Score'] = None
    except:
        pass
    try:
        if df.at[i, 'Current Offers'] in ['N/A',"None", "no"]:
            df.at[i, 'Current Offers'] = None
    except:
        pass
    try:
        if df.at[i, 'Current Offers'] == df.at[i, 'Current Offers']:
            offer_list = df.at[i, 'Current Offers'].split(",")
            offer_list = map(str.strip, offer_list)
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
            df.at[i, 'Offers'] = offers
    except:
        pass
    done = False
    temp_height = None
    temp_hand = None
    temp_wing = None
    temp_broad1 = None
    temp_broad2 = None
    height = None
    ft= None
    inches = None
    try:
        temp_height = df.at[i, 'Height']
        try:
            if float(temp_height.split("''")[0]) > 10:
                height = float(temp_height.split("''")[0])
                df.at[i, 'Height'] = height
                done = True
        except:
            pass
        if done == False:
            try:
                if float(temp_height.split("\"")[0]) > 10:
                    height = float(temp_height.split("\"")[0])
                    df.at[i, 'Height'] = height
                    done = True
            except:
                pass
        if done == False:
            try:
                ft = int(temp_height.split("'")[0])
            except:
                  ft = int(temp_height.split("\"")[0]) 
            try:
                inches = float(temp_height.split("'")[1].split("\"")[0])
            except:
                try:
                    inches = float(temp_height.split("\"")[1])
                except:
                    inches = 0
            df.at[i, 'Height'] = (ft*12)+inches
    except:
        pass
    
    try:
        temp_wing = df.at[i, 'Wingspan']
        try:
            if float(temp_wing.split("''")[0]) > 10:
                wing = float(temp_wing.split("''")[0])
                df.at[i, 'Wingspan'] = wing
                done = True
        except:
            pass
        if done == False:
            try:
                if float(temp_wing.split("\"")[0]) > 10:
                    wing = float(temp_wing.split("\"")[0])
                    df.at[i, 'Wingspan'] = wing
                    done = True
            except:
                pass
        if done == False:
            try:
                ft = int(temp_wing.split("'")[0])
            except:
                  ft = int(temp_wing.split("\"")[0]) 
            try:
                inches = float(temp_wing.split("'")[1].split("\"")[0])
            except:
                try:
                    inches = float(temp_wing.split("\"")[1])
                except:
                    inches = 0
            df.at[i, 'Wingspan'] = (ft*12)+inches
    except:
        pass
    
    try:
        temp_hand = df.at[i, 'Hand Size']
        try:
            if float(temp_hand.split("''")[0]) > 10:
                hand = float(temp_hand.split("''")[0])
                df.at[i, 'Hand Size'] = hand
                done = True
        except:
            pass
        if done == False:
            try:
                if float(temp_hand.split("\"")[0]) > 10:
                    hand = float(temp_hand.split("\"")[0])
                    df.at[i, 'Hand Size'] = hand
                    done = True
            except:
                pass
        if done == False:
            try:
                ft = int(temp_hand.split("'")[0])
            except:
                  ft = int(temp_hand.split("\"")[0]) 
            try:
                inches = float(temp_hand.split("'")[1].split("\"")[0])
            except:
                try:
                    inches = float(temp_hand.split("\"")[1])
                except:
                    inches = 0
            df.at[i, 'Hand Size'] = (ft*12)+inches
    except:
        pass
    
    try:
        temp_broad1 = df.at[i, 'Broad Jump #1']
        try:
            ft = int(temp_broad1.split("'")[0])
        except:
            ft = int(temp_broad1.split("\"")[0])
        try:
            inches = float(temp_broad1.split("'")[1].split("\"")[0])
        except:
            try:
                inches = float(temp_broad1.split("\"")[1])
            except:
                inches = 0
        if inches > 12:
            df.at[i, 'Broad Jump #1'] = "ERROR"
        df.at[i, 'Broad Jump #1'] = (ft*12)+inches
    except:
        pass
    
    try:
        temp_broad2 = df.at[i, 'Broad Jump #2']
        try:
            ft = int(temp_broad2.split("'")[0])
        except:
            ft = int(temp_broad2.split("\"")[0])
        try:
            inches = float(temp_broad2.split("'")[1].split("\"")[0])
        except:
            try:
                inches = float(temp_broad2.split("\"")[1])
            except:
                inches = 0
        if inches > 12:
            df.at[i, 'Broad Jump #2'] = "ERROR"
        df.at[i, 'Broad Jump #2'] = (ft*12)+inches
    except:
        pass
    try:
        if "'" in df.at[i, 'L-Drill #1']:
            df.at[i, 'L-Drill #1'] = df.at[i, 'L-Drill #1'].replace("'",".")
        elif "," in df.at[i, 'L-Drill #1']:
            df.at[i, 'L-Drill #1'] = df.at[i, 'L-Drill #1'].replace(",",".")
    except:
        pass
    try:
        if "'" in df.at[i, 'L-Drill #2']:
            df.at[i, 'L-Drill #2'] = float(df.at[i, 'L-Drill #2'].replace("'","."))
        elif "," in df.at[i, 'L-Drill #2']:
            df.at[i, 'L-Drill #2'] = float(df.at[i, 'L-Drill #2'].replace(",","."))
    except:
        pass
df['Broad Jump #1'] = pd.to_numeric(df['Broad Jump #1'], errors='coerce')  
df['Broad Jump #2'] = pd.to_numeric(df['Broad Jump #2'], errors='coerce') 
df['Shuttle #1'] = pd.to_numeric(df['Shuttle #1'], errors='coerce')  
df['Shuttle #2'] = pd.to_numeric(df['Shuttle #2'], errors='coerce') 
try:
    df['Vertical #1'] = pd.to_numeric(df['Vertical #1'], errors='coerce')  
    df['Vertical #2'] = pd.to_numeric(df['Vertcial #2'], errors='coerce') 
except:
    pass
df['40 Yd Dash #1'] = pd.to_numeric(df['40 Yd Dash #1'], errors='coerce')  
df['40 Yd Dash #2'] = pd.to_numeric(df['40 Yd Dash #2'], errors='coerce') 
   
df['L-Drill #1'] = pd.to_numeric(df['L-Drill #1'], errors='coerce')  
df['L-Drill #2'] = pd.to_numeric(df['L-Drill #2'], errors='coerce')  


df['Broad Jump'] = df[['Broad Jump #1','Broad Jump #2']].max(axis=1)
df['40 Dash'] = df[['40 Yd Dash #1','40 Yd Dash #2']].min(axis=1)
df['L Drill'] = df[['L-Drill #1','L-Drill #2']].min(axis=1)
df['Shuttle'] = df[['Shuttle #1','Shuttle #2']].min(axis=1)
try:
    df['Vertical'] = df[['Vertical #1','Vertical #2']].max(axis=1)
except:
    pass

template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")

for i in range(len(df)):
    template.at[i, 'HS Combine Event'] = 'Prep Redzone'
    if df.at[i, 'Location_x'] == df.at[i, 'Location_x']:
        template.at[i, 'HS Combine Location'] = df.at[i, 'Location_x'] + " (Hand timed)"
    else:
        template.at[i, 'HS Combine Location'] = df.at[i, 'Location_y']+ " (Hand timed)"
    try:
        template.at[i, 'HS Combine Date'] = df.at[i, 'Date'].strftime('%m/%d/%Y')
    except:
        pass
    template.at[i, 'HS Class'] = df.at[i, 'Grad Class_x']
    try:
        template.at[i, 'Last Name'] = df.at[i, 'Last Name_x'].title()
    except:
        try:
            template.at[i, 'Last Name'] = df.at[i, 'Last Name_y'].title()
        except:
            continue
    try:
        template.at[i, 'First Name'] = df.at[i, 'First Name_x'].title()
    except:
        try:
            template.at[i, 'First Name'] = df.at[i, 'First Name_y'].title()
        except:
            pass
    template.at[i, 'HS Primary Pos'] = df.at[i, 'Position_y']
    template.at[i, 'Combine Height'] = df.at[i, 'Height']
    template.at[i, 'Combine Weight'] = df.at[i, 'Weight']
    template.at[i, '40 Dash'] = df.at[i, '40 Dash']
    template.at[i, '3-Cone'] = df.at[i, 'L Drill']
    template.at[i, 'Shuttle'] = df.at[i, 'Shuttle']
    template.at[i, 'Broad'] = df.at[i, 'Broad Jump']
    try:
        template.at[i, 'Vertical'] = df.at[i, 'Vertical']
    except:
        pass
    try:
        template.at[i, 'Wingspan'] = df.at[i, 'Wingspan']
    except:
        pass
    try:
        template.at[i, 'Hand'] = df.at[i, 'Hand Size']
    except:
        pass
    template.at[i, 'Email'] = df.at[i, 'Email']
    template.at[i, 'Phone'] = df.at[i, 'Player Phone']
    template.at[i, 'HS Name'] = df.at[i, 'High School']
    template.at[i, 'HS State'] = df.at[i, 'Home State']
    template.at[i, 'GPA'] = df.at[i, 'GPA']
    template.at[i, 'ACT'] = df.at[i, 'ACT Score']
    template.at[i, 'SAT'] = df.at[i, 'SAT Score']
    template.at[i, 'Offer Schools'] = df.at[i, 'Offers']
    if df.at[i, 'Player X Handle'] == df.at[i, 'Player X Handle']:
        template.at[i, 'X URL'] = 'https://x.com/'+df.at[i, 'Player X Handle']
    if df.at[i, 'Player Instagram Handle'] == df.at[i, 'Player Instagram Handle']:
        template.at[i, 'Instagram URL'] = 'https://www.instagram.com/'+df.at[i, 'Player Instagram Handle']
    try:
        template.at[i, 'Parent Name'] = df.at[i, 'Guardian First Name'] + " " + df.at[i, 'Guardian Last Name']
    except:
        pass
    try:
        pemail = df.at[i, 'Guardian Email']
        pphone = df.at[i, 'Guardian Phone']
        template.at[i, 'Parent Contact'] = f"Email: {pemail}, Phone: {pphone}"
    except:
        pass
template.to_excel(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\PrepRedzoneData1-2026.xlsx",index=False)    