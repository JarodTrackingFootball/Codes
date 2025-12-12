# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 07:49:15 2024

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
import random
import warnings
from datetime import datetime

warnings.simplefilter(action='ignore', category=FutureWarning)

flags = pd.read_excel(r"C:\Users\jtsve\OneDrive\Desktop\TrackFlags(4-24).xlsx")
flag_urls = list(flags['Milesplit URL'])
flags.set_index('Milesplit URL', inplace=True)

player_data = pd.read_excel(r"C:\Users\jtsve\OneDrive\Documents\MStoRun(9-8).xlsx")

index_names = player_data[player_data['Milesplit URL'] != player_data['Milesplit URL']].index

player_data.drop(index_names, inplace=True)
player_data = player_data.reset_index(drop=True)

header_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582']

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
        
login = 'https://www.milesplit.com/login'

payload = {'email': 'jtn47316@gmail.com',
           'password':'75117987511798'}
df = pd.DataFrame({'URL':[''],'Event':[''], 'PR':[''], 'Meet':[''], 'Year':[''],
                     'Wind Error':[''], 'Timing Method':[''], 'Slug':['']})

event_dic = {'55m':'55M','60m':'60M','55H':'55HH','60H':'60HH','100m':'100M', '110H':'110HH','300m':'300M','300H':'300IH','400H':'400H','200m':'200M', 'D':'Discus', '400m':'400M','400M':'400M',
             'S':'Shot Put', 'HJ':'High Jump', 'LJ':'Long Jump', 'TJ':'Triple Jump', 'PV':'Pole Vault', 'J':'Javelin','800m':'800'}

cks = 'unique_id=e765234b297f32ecf75455899c92b05b; osano_consentmanager_uuid=27cab345-39e8-4c37-95ea-8083bb4442a5; osano_consentmanager=14j3cLH-jglZV-VGrVKSVHJiADoe1fxseo7xWVcPxQXqN0-gBM3LQh4RRD9PMC76pLO9JShQ-vwxGALP144xlDt_4HXfXLVV1idhF6OLYraEK7YIqNZ4kyq6YIZBEIAz0SkWbF6e9b_SWnd5owWl1A2jgiO_o5ECnBEu5k6xvEWqb_SlixU9_d_iaQF2Z4bYA0MLUpnfGXfQwm6xeCnmnhNsdQZmJalJmx8lqyvurY9ZW2tngk_WanpQxNYWxKUfhL0bRig5Xz4t9_53423z0kS3t5wq6W7K53MfPJsfXATyHgPMtMM7PtweZM0JBL2MmO6J9PNe80pot9ZApxeqVWRtVx5Mr0FV6ri1mwOXHiN4D6Lk826j4TeHVxa655CX4amLgzQUpr4FnL7ne0r4Q2Zn7kd4JAQqQ9zxrSKtI5Xrgz97F6ZgbnDNqoLQ2PICJRwlLxuxsGDafh676zEYDXRgfz3tVFb0eigccRizNSVbvXXKWwlZ7Pm7H4bGWTL3kNyJ0Jb4pXrxIIyr92WIyyRzPCYNCaKwS6thcNaXweSWDrfxng0jaZv1pNUBmLiqCfnHIFzz4AZwiGy3HjdwKOsOjeh4a8vbSU6zRvrL3n8XVkd6CL51h3fxYXkNG89HR9y6b6oksONDGsZX68i1JtQAxeP3okoLhgKsS2eQwnHi_5bAzh9YhPtFirpALjH-xfaSIKQI3kP_pDVofk0oIV72KWoK_cfvnVKhH8up6Mlcq2nffku5QEWDGvby5WnZ_RBfKBePpzz4YWz8c_-CBN6qgU6jHWq-s_F7pFg6vFKVBl59LlL87e8pblgnBQe0nCxu3QehsS6HkMlmGyj9-_C-qEVDUfwVXG02k75aUi6ic04M8m8aJA5qGsC4h4ArRxCqBPY8NYFRTf2XiQcfb16MNlL495KeQYbCnZzwFJ1F6_h5q0xea4nvR3_VPhtPGb3kpW5RBOZvPBMhgVzx_DpcK_ukjoVdIQ95NbKRs5u-b1jrNogIeQT4Q1emGO84pxYYU1cU95Pu9XCc7xaZTMvpbBr-rRMwflxyQdCMyxqCr-qunmwvcwhZlefQKnI58uNta5UNaMwS1CgB3MexluDwtcz_RZcNL55mP3KRKMWVE9h0-4k85lFcrjACE9adBdMM0uJ99dPuAWtkQpWm0CosCCVwrLv01J07Vsr9ki3U4GJj7axhFHD6EWS7PtCZ4UC7KaCgiAeFdJkevaTjpc8RGWemHNliWzrO9shOfLNs5Q-ZKMZ-2ULbX8xOqPkuZfty0Teon2WSIpHUOGKGmh30BfwYpQpQ5SzE7Vdp7nvRtTcNmWEeMJaCufOkSQeMqcvDyfDv4ox_ptaix8NLWJE3wpZivGwna86_wQBPFlHJOfUn0qwB76Wb6v4bCfMG09AUkRLJlp9mmBTQD9ZIcA4gr7EJQGXmy1yWfUokn7U2-KCpSE_K46WwEpRE94NVN7wEvScqe_k30mJPG4Q9Zqy6OB33iybUGxKDBT9w8G-9F0rigKWFm5D_oXjTnoFm6nF9klV6R5dJT76Okq8BhldaMhrB8pgLJgiZphICO536MSt5ydq7O07Jb8Uje8bvMuAHnuOZeffi67poNGy_FL86BevaH5_xVS6Mv4bIQf_DcxpwOCvm_p6z1LwCRJUD5fwwkWzrzxv2rvkraaD_dt-0kGbGWKo0HvQj_XOkDXYeLXtqst-C7GtZcH1ziiK0v_ljYjNv47Reg28c4IlzRPnqzeGEsQQMA-SPIv45zSFecvuJbRQYiO6toCsvy0U7Hs5_T0-vcmlxeknP-PScrIH89ir5B5t9FknslOJCZiy7ANF4gBdR8kOXvnpoZOZa3ZpP-wLeiiCNTmpRHCAAM4Z_xMfa2vHj1_5b9XaJ76nMHiGmdygNwR1qYfU-TTH8geN_uyZmmQ8pAADjZ3khIIzqxdVDrAP9AXQ5idkGHKtndHwzN1b-DliSXMC7FD1JtaUH7HU0ruVqYIS7DCPpDM60EOZcZcrl5N733xlwHyrVN2-4YjD75FK1QjYT_XC3pLZd6VwToFcaa4p5Sqh0rMV8EPtJ2m7G627JgCwYynKu-8Nm6mdMWtXthQZoXqH98cTRG95nG33H1YA-hnSrwthJM1dpRkF4rKIBjQm-GjpRLbSbb6q7CKXTNi26xGfgOl5FbOpmVT-ptWEwKC41XAx00OhVDH7-1xZGbTTHgp28UHdL3_12aXlKxTODkc4yftUwrGqTFo0_1OjrDBbluCu_4yTAxazpLNvhF8_ixMC_Y9McY0hLFh2b7xeyFvr_0U601o3mlIVIUQuxQmtAt09pJPm32Mva4m4MKS4uway49Z8BPgWw7ark3EsrUw8S2p-GpJDAnV2-dWqHlzh8fo0Zm97tBsVYSzBwbkeQGLIjDGW-R-1PinASrDJ17nczflelEV_lMpuVpEHTiy2qXN4OqvfM3wKa2DF5ZgLzax-qQysbF9RHBdvskASen0JSPLvGtIT5YsKoL062YrPNFg4NrsFJCJ_JlJGNuXkw7Eh1GYxs8nOovcPEueUvLQl1BH9jqaWzp1u8IR-GH1ScLjxRJjyKaMSvDbjL4k6_HJsPQ1m5moFJucXVA_5dHTjAySp7XFNk-hn1VfHIkkNXdpYWVCpkMyCa; osano_flo_drawer=1; osano_flo_shown=20221221; ajs_anonymous_id=adc74027-6454-4f31-833e-94fed04b44c7; _clck=7s2vo%5E2%5Efz7%5E0%5E2079; _cb=CHK_eOCWjBMwDHQ1HU; _cb_svref=external; __qca=P1-8216fad2-2d68-4988-b1d5-fa4c6628e9a3; _bts=542d1a8f-1b3e-4348-8082-2a9c23007321; _ga=GA1.1.1211075359.1757511126; _bti=%7B%22app_id%22%3A%22flosports-ny%22%2C%22bsin%22%3A%22wxnXyK2qzGJp%2Fz1a8c3eUYdA6SY37gpKv%2F6Hvc05nR3uxtA4Yz%2BOHgn%2B0r1MgV7HJfmbtvKEYHdHPE1x27itHQ%3D%3D%22%2C%22is_identified%22%3Afalse%7D; _chartbeat2=.1757511125571.1757511135601.1.CybNzgDF2uAeBFs_TsBiBLb7DC15uM.2; _chartbeat5=; _clsk=e16ac5%5E1757511135828%5E2%5E1%5Ei.clarity.ms%2Fcollect; _li_dcdm_c=.milesplit.com; fhbdb=1; _lc2_fpi=c06ba140db3b--01k4sx7cwy5aqp84f72xra431p; _lc2_fpi_meta=%7B%22w%22%3A1757511136158%7D; _pubcid=84d80324-0658-42f8-b8b9-50754424a8ed; _pubcid_cst=KiweLDosVg%3D%3D; _lr_retry_request=true; _lr_env_src_ats=false; 33acrossIdTp=4OGTSVQnXVcJJc2CDrWzxJCrqjHadipuDM5rGBuAf9A%3D; pbjs-unifiedid=%7B%22TDID%22%3A%228d7e85c1-4891-45dc-896c-1e66501f31d1%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222025-09-10T13%3A32%3A18%22%7D; pbjs-unifiedid_cst=KiweLDosVg%3D%3D; cto_bundle=1g51PF9DQ0NGMm5hYnpqRVMlMkJ4TkJMZTQyR2NPTFAyWENKMk8lMkZ0dXFqSzZ3TVhaU0ppbmx3TjRPczQlMkZtVHdFdXZTT2NJcjV3c1NyTlJFa0xTSjJzWGs3YlFJRGhkWU00NEFDJTJCUHVGJTJGekVXUWY2MGQlMkZDWEtUZEZtNm5sWEVITEowNWdYbg; cto_bidid=gEkns19KU1N2UW5mOEo1cUZDZ21idkhhZFdPJTJGJTJCMEQ4a0xvbzJuR0NXRXFlUkYxeVpNMlI5WXN6JTJCaUZuQkJCeUNqcUZ1UWRJWlR5bW9kMVFSRkNuWno2QUxsUSUzRCUzRA; _cc_id=88499713e6491571b1b322d8987ae83b; panoramaId_expiry=1757597538762; fabrickId=%7B%22fabrickId%22%3A%22E1%3Am_puFpOsQ06D4_wDoLy5QOeOQb4-dr3Gg35ncKHP6V2-PKuoCg2zWyqEpkPb6H1kL8I40yh1qSs287oTgg8Vw_4LS06D5gJtIP09aSWJJME%22%7D; fabrickId_cst=KiweLDosVg%3D%3D; _lr_geo_location=US; FCNEC=%5B%5B%22AKsRol-F-nUEhrPMeXnM-y4ySH4RyCzHKCutpWQZrUyPnP3I-o7n7YqDSy3yx2RZjszBUM2EtW9ypDEcGs-I7WkKadlFpRxnWCGIi-VLgr2Iz5mimzlRgS89uqbe_zW1Taz-wPlHBwm4SsbXInIc7AkH81jK3cO3xw%3D%3D%22%5D%5D; _uetsid=8ae021308e4a11f0a4fed9ac7490f294; _uetvid=8ae059d08e4a11f08faec584f40628ae; jwt_token=eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjE3Njc4NzkxNDksInVzZXJfaWQiOjE4ODYxODE1LCJzdWJFeHAiOjE3MjkxODcxNDcsImlzRnJlZSI6ZmFsc2UsImlzVW5pdmVyc2FsIjpmYWxzZSwic3Vic2NyaXB0aW9uX3N0YXR1cyI6IkV4cGlyZWQiLCJpZCI6MTg4NjE4MTUsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJlbnRpdGxlbWVudHMiOlsicmFua2luZ3MiLCJyYWNlX3ZpZGVvc19waG90b3MiLCJhdGhsZXRlX3Byb2ZpbGVzX3BycyIsImxpdmVfZXZlbnRzX21pbGVzcGxpdCJdLCJzaXRlcyI6W10sInVzZXJuYW1lIjoiZmwxLTU4YzdmYjdjLTJmNWItNDgwNi05YWJjLTI1MjFhMzIyNjUxMyIsImVtYWlsIjoianRuNDczMTZAZ21haWwuY29tIiwiY2FyZF9hZGRyZXNzX3ppcCI6IjgwNTA0IiwiaWF0IjoxNzU3NTExMTQ5LCJpc1ByZW1pdW1TdWJzY3JpYmVyIjpmYWxzZSwicHJvZmlsZV9waWN0dXJlIjoiaHR0cHM6Ly9yZXMuY2xvdWRpbmFyeS5jb20vZGl6bmlmb2xuL2ltYWdlL3VwbG9hZC93XzE1MCxoXzE1MC9udHA2cXN6dHFpaW84ZHliZGx5Ni5wbmciLCJhbmFseXRpY3NfZGF0YSI6eyJhY2NvdW50X3R5cGUiOiJGcmVlIiwic2l0ZV9pZCI6MTUsImNhbXBhaWduIjpudWxsLCJjcmVhdGVkX2F0IjoiMjAyMy0wOS0yNlQxNjo0MToxMS4wMDAwMDArMDAwMCIsImVtYWlsIjoianRuNDczMTZAZ21haWwuY29tIiwiZmFjZWJvb2tfaWQiOm51bGwsImZpcnN0X25hbWUiOm51bGwsImxhc3RfbmFtZSI6bnVsbCwibmFtZSI6bnVsbCwicGxhbl90eXBlIjpudWxsLCJzdWJzY3JpcHRpb25fZW5kX2RhdGUiOm51bGwsInN1YnNjcmlwdGlvbl9zdGF0dXMiOm51bGwsInVzZXJuYW1lIjoiZmwxLTU4YzdmYjdjLTJmNWItNDgwNi05YWJjLTI1MjFhMzIyNjUxMyIsInVuaXZlcnNhbCI6ZmFsc2UsInN1YnNjcmliZXJfcG9ydGFsX2lkIjoiMTUifSwiZXhwZXJpbWVudHMiOlsiZmxvXzEyM19leGFtcGxlX3Rlc3QtMSJdLCJsaXZlcmFtcF9lbnZlbG9wZSI6IkFuQlhXRXZIcVE5VmdzUTkzcmtTRV9pZTVQdWlTU3p2cko1VGtLaEpGZEpKb29sTXc2cmNLMk9KUUYyQ1Y2LVVaVE1KTlZqQlY2M2JpTUJNNEF6a19DZ2pUaUFHdjBDNHFlTjdRY3B0aFN1MkZVS3piNEEzRkZ1N0ZnLUZvZWhMZnM1bVVvWXFuWVYxTFNKd0p2WEtBZlpVODlPNW9fUnc2Mkw1QUE1d3duNjNmRlBaR25yUGVnMUJ3TVdSb1ZaWXctRm5mSkRBVGhCaHJyRFZsZlJvTXlydjRVVjJ6bkJZMlVXeHQ3OU82alhpNV83Vy1wWGcyc1NGNkhJVVYzdnM2M1FXWm9NQlljYXRxNklmbU54RlZhSFRwbGdaUE5sZjBDT2U3Qm1CNnpwSG5UaTZzWjhOVUJ3aTZzaFZMamFrX3FseVlhQjF2Y3FyTmtiRW9lbTFxc3NhYjJJMEJMMW1HeG9Odldsc2FZbEJxOUhaMlBQYjFZQTBQNmJKRmQwajFzREdEdEg1UXRNaUg2SDR2T1NqQUlXaWhHYThmV2xsWWctOUgtN0VsQU5zbThyVHdWenhzR2hFa3p5YU1ZRkVnZHE2ZHVSbDBkb25XUUFRbjBtRzZnN3Q1VEhIRlVJb0RLdzd2UXZDcXpUbDZFcnhKZ1NMWXlQYXFReG9SZUczRWxfdmZJeUtLdDNfa0tYUlNjRVhtdU9JejdZSzdaVEdfTGk2Rl93WURPNmpLWWx0YjBJTUF3VGs3Zm5TalliMG5tSFJtWklMeEtJazlmTXVXY09pYW5kQWVoUXkyclc0bU1aZVR3dzVyU1dFWXR3M3hFeWtlWmxoMzZfdThVM1hjQVBpM0NxbGlyT1hOWmhTVEN0allqdGc2RnM3WndDYlFJeE1SbnRDOTlpemRMSlBDUEFVdmt5LUhMR1pOeHVXTVFmWk5iODYzNENNUllfR1M1OURwY3R2ZDJLYmxOekZ1QzEzUGkxYm5lYlJ0RFhmenhCNUVYN0tHM0k5ZGdPbXc3b2JSbVhvZ1RkNVRudFZtNjVZU252M3ZXeVAtWjZ2Z29ZM2hic092RGJqNHAtWFZac2xwY1BqeVVEU0ttSnhRd2VpOGg5R0wwRmpOV1Z4Q2J2T2FTOUFQZzAzRVM5T0ZsVkNDODh0UUhvS2JZSjhmRXlsSlEwcHhoUEdvR1l1eUtCS0hWa2xtRUpONnowZVVMdlFwWEZOZkNqZlIwMS1wYW1QY0s3Qi1OOEFDUGROSF9FUXVYTl9KbllYdWVvZ2dETGotbDN1T3NtUjVsbURQY0FieEdaUVYzT1UwdTRpUjh2Zmg4RTYyaU13bHQ5aWZ3MTZlWmNHdG5Ka3hUbm1uSThjbk9reUY2RmRySEkzSkx4RUJtUVFlNE1vSHc2aUMxNmZzZXJ3TE9wV3ZVbmJWcGVXQTQxWDgzZjJwbDFOWC1CVmhQRk1Mc3FRemx4Z3hZRjFHZkg4YWdxZHF5azJkT3dKcE1MR0NZbDd1OHNnSUtiTkw1LUdOSWN6Mk9tTlpaamlXNVRLeWtlRjY5TjZQZHRTRlJSaUhLaTRxOXJxODE4eXVnZWZHY01QMFZETXZvQ2VKakRIRjlBVy1tVFdNemRNZjIzMk1kZGRoa2RrRm5HdHRlbHJxTjZDS01xTVhqSkpYbW9zUHpLUE1uNjJLTVJISUFMa2RIOFdrNU95eDRieElscV9yRTl0N2hySmlNV0taMHY1aEl1b2ppOHhWWXljNkZnSTF1ZFNkTGRSZjdyRWlIWC1Gano4Mlk4NldkM2lvQThBNjVITU5nVmNVNGhzVkFRTUpzUnR6Zm5qTE5CTlNvM3lRdW1YODRqRmtTbmt5QnBOMjBxVktrN3VNOExjSkMzN2Z2eVZSeFZpQWN2eHJkWHVZOTI4OEhBSGRkaDZjVWpoRmtnd3p2WC1pLXpFN1FQTlIzME9DSFQxZk9aREFXYnJlOUhXOEw2dnhmUmlpZTZwVUV6QkhRV3gyRVZET1RQSGJPdyJ9.KsRFGRFhhBQjhGp6wUTxLKpoi0_PTgr7Hpe55E8oiWgPU23Nu03IrCKHkIPARurlZodgV3kLKr4r5o9X4xru9-aMduo4XCU5PheaW5j1Ue_v_GI7TSZUkALGY1WMcM43ycYSb5NXSiWd3n4GCALLpNvpBAiSbTwKgodRj9fcpAV01iW41A7lXk5hI1WVHypgy_7Tp_Qx9VTldZs0uS3_hJ6258-GBV3PKqpu0OmMC4Z9DXlghshhskltKr3cv5jh25P61Qkt-0qDbwB4GfbvKLCZKKySew2iYmW0yYlK6HcrmFMZecuVwqWMhUCB0rDBYyVKYT0YusJBOTj5NTOnSKLL9S3HyDqODotMy9NhljPhCMp_xQkQbRS6pzAKVxh3VBrOYZaq31PkesRD1h-NefzzzYIXgqsbHs40e-w_qqNEXeIANFt6nFhqUfLkyvifFnc6FsNvHMTTbozgDuC3sLgXLDHyimSudriMrIj63LlM4Z18Y2AFT_yKjFFUZtZ6Z4Fbb_0Bow3P6wn34YKom5QBByiclguXiJf0oAfyIcmRMHMSyTFNev-XRZPaKDznbZ_7j91glbbw5lwihlAAjFf-fsV-u76cjAHglT4RrEuewWDFpGRkRe9R2CcuqcQTcfLzI-47Zd7z_ziOgpFOlpY5BT46_4TAxCyyQVdTo-k; jwt_refresh_token=1363b848327abd4647fbf4e46054a5c87d24b2105ddedfe4c963011e09275827ff0a60742b50d95d96b5dda751e63e1fee15ad27589132d1adbc0ca1cbbb02b0370eca1034a70c13512c10f978a6d91fd717220d811d3ca603db; identity=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjI2MTUyNDkiLCJ1c2VyTmFtZSI6ImZsMS01OGM3ZmI3Yy0yZjViLTQ4MDYtOWFiYy0yNTIxYTMyMjY1MTMiLCJlbWFpbCI6Imp0bjQ3MzE2QGdtYWlsLmNvbSIsInBlcm1pc3Npb24iOiIxIiwic3Vic2NyaXB0aW9uRXhwaXJlIjoiMTc1ODkyNjcxNyIsInNzb1Rva2VuIjoiYjMyZjExYTY0ZDlmMTNjMTIzMTgwOGU0ZDVmMmFlNzYiLCJmbG9Kd3RSZWZyZXNoVGltZXN0YW1wIjoxNzU3NTE0NzUyfQ.bCgWiRJ6tRj6VTBUlm5RVUvmQp8v8erkXcRs8K4Llzc; sso_token=b32f11a64d9f13c1231808e4d5f2ae76; personalization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdGhsZXRlcyI6eyIxNjE5NjEyMSI6eyJjb3VudCI6MiwidGltZXN0YW1wIjoxNzU3NTExMTUyfX19.6sRN09BcJ287ljuM6yp_4D9-Amf8GKGYei3rS_SsAM0; _chartbeat4=t=BpkjBMdi4ABD069ovCVeZv5C0Ha8f&E=10&x=0&c=0.79&y=1144&w=852; _ga_WH18KX2QXN=GS2.1.s1757511125$o1$g1$t1757511182$j3$l0$h0'
#df = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\MSRun(7-2).csv")

s = requests.Session()
for r in range(372,len(player_data)):
    headers = {'User-Agent': random.choice(header_list), 'cookie':cks}
    proxy = random.choice(proxies)
    s.headers.update(headers)
    s.proxies.update({'http':proxy, 'https':proxy})
    if player_data.at[r, 'Milesplit URL'] != player_data.at[r, 'Milesplit URL']:
        continue
    if "milesplit" not in player_data.at[r, 'Milesplit URL']:
        continue
    df1 = pd.DataFrame({'URL':[''],'Event':[''], 'PR':[''], 'Meet':[''], 'Year':[''],'Date':[''],'Slug':['']})
    df2 = pd.DataFrame({'URL':[''],'Event':[''], 'PR':[''], 'Meet':[''], 'Year':[''],'Date':[''],'Slug':['']})
    df3 = pd.DataFrame({'URL':[''],'Event':[''], 'PR':[''], 'Meet':[''], 'Year':[''],'Date':[''],'Slug':['']})
    slug = player_data.at[r, 'Slug']
    url = player_data.at[r, 'Milesplit URL']
    hs_class = player_data.at[r, 'HS Class']
    player_id = url.split('athletes/')[1].split('-')[0]
    player_state = url.split('//')[1].split('.')[0]
    get_url = 'https://'+player_state+'.milesplit.com/api/v1/athletes/'+player_id+'/performances'
    #headers = {'User-Agent': random.choice(header_list), 'cookie':cks}
    #proxy = random.choice(proxies)
    try:
        r5 = s.get(get_url,headers=headers,proxies = {'http':proxy, 'https':proxy}, timeout = 150)
        r1 = r5.json()
    except:
        time.sleep(150)
        #headers = {'User-Agent': random.choice(header_list), 'cookie':cks}
        #proxy = random.choice(proxies)
        r5 = s.get(get_url,headers=headers,proxies = {'http':proxy, 'https':proxy}, timeout = 150)
        r1 = r5.json()
    try:
        cards = r1['data']
    except:
        continue
    
    for card in cards:
        flagged = False
        e = None
        event = None
        wind = None
        year = None
        meet_name = None
        meet_date = None
        text= None
        r3 = None
        r2 = None
        inches = None
        ft = None
        
        e = card['eventCode']
        if e in event_dic.keys():
            event = event_dic[e]
        if event == '800':
            flagged = True
        event_id = card['id']
        if card['isHandTimed'] == '1':
            continue
        meet_name = card['meetName']
        
        event_url = 'https://va.milesplit.com/api/v1/performances/'+event_id+'?detailed=true&m=GET'
        #time.sleep(2)
        #headers = {'User-Agent': random.choice(header_list), 'cookie':cks}
        #proxy = random.choice(proxies)
        try:
            r2 = s.get(event_url, headers=headers,proxies = {'http':proxy, 'https':proxy}, timeout = 150)
        except:
            time.sleep(150)
            #headers = {'User-Agent': random.choice(header_list), 'cookie':cks}
            #proxy = random.choice(proxies)
            r2 = s.get(event_url,headers=headers,proxies = {'http':proxy, 'https':proxy}, timeout = 150)
        r3 = r2.json()
        wind = r3['data']['windReading']
        if wind == '' or wind == 'Not Recorded':
            pass
        else:
            try:
                wind_f = float(wind)
                if wind_f > 2.9:
                    continue
                else:
                    meet_name = f"{meet_name} ({wind}w)"
            except:
                pass
        if 'Meet' in meet_name:
            meet_name = meet_name.replace('Meet','TF Meet')
        else:
            meet_name = meet_name + " TF Meet"   
        temp_date = r3['data']['meetStartDate'] 
        date_obj = datetime.strptime(temp_date, '%Y-%m-%d')
        meet_date = date_obj.strftime('%m/%d/%Y')
        year = date_obj.year
        text = card['mark']
        if event == "Discus" or event == "Shot Put" or event == "Long Jump" or event == 'Triple Jump' or event == "High Jump" or event == 'Javelin' or event == 'Pole Vault':
            try:
                if "(" in text:
                    text = text.split("(")[0]
            except:
                pass
            try:
                inches = int(float(text.split('-')[1]))
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                text = text.split('-')[0] + inches
            except:
                pass
        try:
            if 'w' in str(text):
                text = str(text).replace('w', '')
        except:
            pass
        try:
            if 'm' in str(text):
                text = float(str(text).split('m')[0])
                inches = text*39.3700787
                ft = int(inches/12)
                inches = inches - (ft*12)
                if inches < 10:
                    inches = f"0{inches}"
                else:
                    inches = str(inches)
                text = f"{ft}{inches}"
                text = float(text)
                text = int(text)
                text = str(text)
        except:
            pass
        if event == 'High Jump':
            if int(text) < 500:
                continue
        if event == '400M' or event == '300M' or event == '400H' or event == '300IH':
            try:
                hour = float(text.split(":")[0]) * 60
                second = float(text.split(":")[1])
                text = hour + second
                text = str(text)
            except:
                pass
        if text == 15:
            continue
        if event != '800':
            try:
                temp = float(text)
            except:
                continue
        if event == "Discus" or event == "Shot Put" or event == "Long Jump" or event == 'Triple Jump' or event == "High Jump" or event == 'Javelin' or event == 'Pole Vault':
            new_row = {'URL':url,'Event':event, 'PR':text, 'Meet':meet_name, 'Year':year,'Date':meet_date, 
                             'Slug':slug, 'Class':hs_class}
            df2 = pd.concat([df2, pd.DataFrame([new_row])], ignore_index=True)
        elif event == '800':
            new_row = {'URL':url,'Event':event, 'PR':text, 'Meet':meet_name, 'Year':year,'Date':meet_date, 
                             'Slug':slug, 'Class':hs_class}
            df3 = pd.concat([df3, pd.DataFrame([new_row])], ignore_index=True)
        else:
            new_row = {'URL':url,'Event':event, 'PR':text, 'Meet':meet_name, 'Year':year,'Date':meet_date, 
                             'Slug':slug, 'Class':hs_class}
            df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
            
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
    index_names = df2[df2['URL'] == ''].index
    df2.drop(index_names, inplace=True)
    df2 = df2.reset_index(drop=True)
    df1 = df1.reset_index(drop=True)
    df2['PR'] = df2['PR'].astype(int)
    df1['PR'] = df1['PR'].astype(float)
    
    
    df1 = df1.sort_values('PR')
    df1 = df1.drop_duplicates(subset='Event', keep='first')
    frames= [df,df1]
    df = pd.concat(frames)
    
    
    df2 = df2.sort_values('PR', ascending=False)
    df2 = df2.drop_duplicates(subset='Event', keep='first')
    frames= [df,df2]
    df = pd.concat(frames)
    
    if flagged == True:
        index_names = df3[df3['URL'] == ''].index
        df3.drop(index_names, inplace=True)
        df3 = df3.reset_index(drop=True)
        df3 = df3.sort_values('PR')
        df3 = df3.drop_duplicates(subset='Event', keep='first')
        frames= [df,df3]
        df = pd.concat(frames)
s.close()
       
df = df.drop_duplicates() 
df = df.reset_index(drop=True)

template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv") 

for i in range(0,len(df)):

    try:
        if df.at[i, 'Class'] - df.at[i, 'Year'] > 3:
            continue
    except:
        pass
    try:
        event = df.at[i, 'Event']
        template.at[i, event] = df.at[i, 'PR']
    except:
        continue
    template.at[i, 'TF Date'] = df.at[i, 'Date']
    template.at[i, 'Milesplit URL'] = df.at[i, 'URL']
    #template.at[i,'TF Year'] = df.at[i, 'Year']
    template.at[i,'TF Meet'] = df.at[i, 'Meet'].strip()
    template.at[i, 'Slug'] = df.at[i, 'Slug']
    template.at[i, 'Track'] = 1

writer = pd.ExcelWriter('FullTrackPull-M(8-9).xlsx')
template.to_excel(writer, index=False)

writer.close()

df.to_csv(r"C:\Users\jtsve\OneDrive\Desktop\Excel Exports\MSRun(8-9).csv",index=False)
           
events_tf = ['55M', '60M','55HH', '60HH', '100M', '110HH', '200M', '300M', '300IH','400M','400H',
             '800','Shot Put','Discus', 'Javelin','High Jump',
             'Long Jump', 'Triple Jump', 'Pole Vault']

for event in events_tf:
    temp_df = template.dropna(subset=[event])
    #temp_df = temp_df.dropna(subset=['Slug'])
    temp_df['HS Class'] = None
    temp_df['HS State'] = None
    temp_df['HS Name'] = None
    temp_df['Last Name'] = None
    temp_df['First Name'] = None
    temp_df['Milesplit URL'] = None
    temp_df['TF Year'] = None
    temp_df.to_excel(r"C:\Users\jtsve\OneDrive\Documents\/"+event+"UpdatesM"+"-FULL2.xlsx",index=False)

            