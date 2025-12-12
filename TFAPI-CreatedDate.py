# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 08:02:49 2025

@author: jtsve
"""

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

warnings.simplefilter(action='ignore', category=FutureWarning)

player_data = pd.read_excel(r"C:\Users\jtsve\Downloads\Players_TrackingFootball_102125-080844am.xlsx")

player_data['Created Date'] = None

for i in range(0,len(player_data)):
    time.sleep(2)
    slug = player_data.at[i, 'Slug']
    url_request = 'https://tfb2-api.trackingfootball.com/api/v1/api/player-details?type=slug&value='+slug
    response = requests.get(url_request, headers={'api-key':'6e0520d5-f63f-47aa-b89e-46c356f48e0a'})
    r = response.json()
    created = r['createdAt']
    created = created.split("T")[0]
    player_data.at[i, 'Created Date'] = created
    
player_data.to_csv(r"C:\Users\jtsve\Downloads\HSCreatedDateExport(10-21).csv")
