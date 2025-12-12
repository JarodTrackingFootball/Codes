import requests
import json
import pandas as pd
import warnings
import time
import aiohttp
import asyncio
warnings.simplefilter(action='ignore', category=FutureWarning)

player_data = pd.read_excel(r"C:\Users\jtsve\Downloads\TF Full export 11.13.25.xlsx")
df = pd.DataFrame({'Slug':[''],'Hand':[''],'3Cone':[''],'Height':[''],'Weight':[''],'40mDash':[''],
              'Shuttle':[''],'Wing':[''],'Arm':[''],'Broad':[''],'Power Toss':[''],'Vertical':[''],'Date':[''],
              'City':[''],'Type':[''],'Rating':[''], 'First College':['']})

slugs = list(player_data['Slug'])  # you already had thi

semaphore = asyncio.Semaphore(20)  # limit concurrent requests
async def fetch_slug(session, slug):
    url = f"https://tfb2-api.trackingfootball.com/api/v1/api/player-details?type=slug&value={slug}"
    headers = {"api-key": "6e0520d5-f63f-47aa-b89e-46c356f48e0a"}
    async with semaphore:
        async with session.get(url, headers=headers) as resp:
            return await resp.json()
async def run(slugs):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_slug(session, slug) for slug in slugs]
        return await asyncio.gather(*tasks)
data = await run(slugs)
