# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:43:00 2025

@author: jtsve
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:26:23 2024

@author: jtsve
"""

import pandas as pd

df = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\TFAPIResults(11-18).csv")

result = df.groupby('Slug').agg({
    '3Cone': 'min',  # Maximum value in column B
    'Height': 'max',  # Maximum value in column C
    'Weight': 'max',  # Minimum value in column D
    'Shuttle': 'min',
    'Broad': 'max',
    'Vertical':'max',
    '40mDash':'min',
    'Wing':'max',
    'Arm':'max',
    'Power Toss':'max',
    'Rating':'max'
}).reset_index()

result.to_excel(r"C:\Users\jtsve\Downloads\TFCombineDataCombined(12-2)-2.xlsx",index=False)

result = pd.read_excel(r"C:\Users\jtsve\Downloads\TFCombineDataCombined(12-2).xlsx")
result1 = result[result['SUM'] != 0]
