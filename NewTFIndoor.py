# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:15:23 2024

@author: jtsve
"""

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
from selenium.webdriver.chrome.options import Options
import random
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

database = pd.read_excel(r"C:\Users\jtsve\Downloads\TF HS Player Export 1-27-2026.xlsx")

last_day_val = 100

df = pd.DataFrame({'URL':[''],'Name':[''],'School':[''],'Class':[''], 'Event':[''],'State':[''],'Date':[''], 'Result':[''], 'State':[''],
                   'Meet':['']})

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
        

login = 'https://www.milesplit.com/login'

payload = {'email': 'jtn47316@gmail.com',
           'password':'75117987511798',
           'user':'eyJmbG9faWQiOjE4ODYxODE1LCJqd3RfdG9rZW4iOiJleUpoYkdjaU9pSlNVekkxTmlKOS5leUpsZUhBaU9qRTNNVGcyTkRBNU9EVXNJblZ6WlhKZmFXUWlPakU0T0RZeE9ERTFMQ0p6ZFdKRmVIQWlPakUzTWpjek9UQTNNVGNzSW1selJuSmxaU0k2Wm1Gc2MyVXNJbWx6Vlc1cGRtVnljMkZzSWpwMGNuVmxMQ0p6ZFdKelkzSnBjSFJwYjI1ZmMzUmhkSFZ6SWpvaVFXTjBhWFpsSWl3aWFXUWlPakU0T0RZeE9ERTFMQ0p5YjJ4bGN5STZXeUpTVDB4RlgxVlRSVklpWFN3aVpXNTBhWFJzWlcxbGJuUnpJanBiSW5KaGJtdHBibWR6SWl3aWNtRmpaVjkyYVdSbGIzTmZjR2h2ZEc5eklpd2lZWFJvYkdWMFpWOXdjbTltYVd4bGMxOXdjbk1pTENKc2FYWmxYMlYyWlc1MGMxOXRhV3hsYzNCc2FYUWlYU3dpYzJsMFpYTWlPbHN4TTEwc0luVnpaWEp1WVcxbElqb2labXd4TFRVNFl6ZG1ZamRqTFRKbU5XSXRORGd3TmkwNVlXSmpMVEkxTWpGaE16SXlOalV4TXlJc0ltVnRZV2xzSWpvaWFuUnVORGN6TVRaQVoyMWhhV3d1WTI5dElpd2lZMkZ5WkY5aFpHUnlaWE56WDNwcGNDSTZJamd3TlRBMElpd2lhV0YwSWpveE56QTRNamN5T1RnMUxDSnBjMUJ5WlcxcGRXMVRkV0p6WTNKcFltVnlJanAwY25WbExDSndjbTltYVd4bFgzQnBZM1IxY21VaU9pSm9kSFJ3Y3pvdkwzSmxjeTVqYkc5MVpHbHVZWEo1TG1OdmJTOWthWHB1YVdadmJHNHZhVzFoWjJVdmRYQnNiMkZrTDNkZk1UVXdMR2hmTVRVd0wyNTBjRFp4YzNwMGNXbHBiemhrZVdKa2JIazJMbkJ1WnlJc0ltRnVZV3g1ZEdsamMxOWtZWFJoSWpwN0ltRmpZMjkxYm5SZmRIbHdaU0k2SWxCeVpXMXBkVzBpTENKemFYUmxYMmxrSWpveE5Td2lZMkZ0Y0dGcFoyNGlPbTUxYkd3c0ltTnlaV0YwWldSZllYUWlPaUl5TURJekxUQTVMVEkyVkRFMk9qUXhPakV4TGpBd01EQXdNQ3N3TURBd0lpd2laVzFoYVd3aU9pSnFkRzQwTnpNeE5rQm5iV0ZwYkM1amIyMGlMQ0ptWVdObFltOXZhMTlwWkNJNmJuVnNiQ3dpWm1seWMzUmZibUZ0WlNJNmJuVnNiQ3dpYkdGemRGOXVZVzFsSWpwdWRXeHNMQ0p1WVcxbElqcHVkV3hzTENKd2JHRnVYM1I1Y0dVaU9pSlpaV0Z5YkhraUxDSnpkV0p6WTNKcGNIUnBiMjVmWlc1a1gyUmhkR1VpT2lJeU1ESTBMVEE1TFRJMlZESXlPalExT2pFM0xqQXdNREF3TUNzd01EQXdJaXdpYzNWaWMyTnlhWEIwYVc5dVgzTjBZWFIxY3lJNklrRmpkR2wyWlNJc0luVnpaWEp1WVcxbElqb2labXd4TFRVNFl6ZG1ZamRqTFRKbU5XSXRORGd3TmkwNVlXSmpMVEkxTWpGaE16SXlOalV4TXlJc0luVnVhWFpsY25OaGJDSTZkSEoxWlN3aWMzVmljMk55YVdKbGNsOXdiM0owWVd4ZmFXUWlPaUl4TlNKOUxDSmxlSEJsY21sdFpXNTBjeUk2V3lKbWJHOWZNVEl6WDJWNFlXMXdiR1ZmZEdWemRDMHhJbDE5LlZNeld6c2NJQ2hucW5CWDJLcTZNbnV2VXQ1YlFIeWMzWHNIM0VlWGFUTTlTTVhJSzZEaWoxenVPQnpKYXBZekxIZlZoWU05UFdXZnhSZGlZa25LMDZRMmVHYmtNcDItbXRUcHNTbnA1OFBsaFVoZ0FxZFctVWYtbDQ3MXhyanFUODYyMGJzTUVIYXRuZFRIRDhyQkNaRC1EUGdFTklKUmtJVWpPTmVjakJwcEdrMF9PVEVJOHNjc1BUeDhxYWN2NTBVUXE5X3ZUY3h3OEFFbnhvOXpJbE1fSk9SaU5GN0k5dUt4NjI2RUhlWG5fSlV5V2M5TXZUczBQVTZfN05zZ0FmNkNGVnFEbXhKZ3Z0WXdTYjJKaW02NVJfdzBjTTFKWjlMMXpJS2JnSGJ0dThqSzAwNmpwbEdRQ2NldmZDc05wZGF6MlRCY3ZGejVFZ0JjZGJheFd5ajN5M0FfU1dMWTZBRHNFWmtTOHJmUGpTTGZmcWZkdjJPMnlSempIZFlEUFJocGE3c0dyX29mUkZFWFJjc241SGJkNHJfY0MtNk9ubjVTYW9HalNVU3JaUjBzWU1XUy1oTm1QZHB6V0hVVExtNVNIMmRnalJQSWVrSzAzemprWmJ0TEZMQzBveXgzRVdqVGVxSDIzZTB5b0c5SEhmak5PMlJ5U0lSQzZYLVJZeDFlenRhdGVBLUJDNl9CeGFCN0NOMVF1em9uUTJDWUZ1WDExVWtJWE9DRmVXRXBDcXBXTVpuWGVlZnNSNHlrSHJob3VrYzNpNmlVU3g3aGpYM1dtRElTM1pUcklWVjR0TFZHd0hCeDBFTWpRWV82dTN2VjRxS3BYcDBWejVOTGhIYkdrODJ3Z3YzZ2JaUzg2QXVJNkljRzVfRi0yZmh6WG14VWpoSk9NWE9ZIiwiand0X3Rva2VuX2V4cGlyZSI6MTcxODY0MDk4NSwiand0X3JlZnJlc2hfdG9rZW4iOiIzNzllMTNlYzhlYjEzN2Q0MzMyOTI1MzkxOGMxYTg5NDg2ZjA1ZjVhNTE4NzhlMjY2OTdlZTJjYmUzYWU5ZTcwMDA3NzNkNjJlM2JmMzlkNzY3ZmY3OWM1ZTE4ODRkODUxOTczNTUwMWQ5Y2QxZjgzYWYyZjQyMTdjY2ZlNmQzZjI0OGE1ZmNlMWNkZGNiMjQzNzQyMWU0MmMyNzk3NWMzOTZlY2Q2ZWQyZjMzY2RiNGY5MDkiLCJqd3RfcmVmcmVzaF90b2tlbl9leHBpcmUiOjE3MjIwOTY5ODV9'}

payload = {'email': 'jtn47316@gmail.com',
           'password':'75117987511798'}

event_dic = {'55m':'55M', '60m':'60M','55H':'55HH','60H':'60HH','200m':'200M', '300m':'300M', '400m':'400M',
             'S':'Shot Put', 'HJ':'High Jump', 'LJ':'Long Jump', 'TJ':'Triple Jump', 'PV':'Pole Vault'}

grades = ['senior', 'junior','sophomore','freshman']

cks = 'unique_id=029190e9c9ce97770c49d1811f5538e5; osano_consentmanager_uuid=887775a5-d7c2-4eb7-8223-17e94691e0e2; osano_consentmanager=D8RWurlT5FNyaKdKnx0eIzW6N6SYjOmf3W-PcRGdosGQ5cfTfaBg8JEkw8Zr9ozjeoFJeRM8_zlOPU486AIifa-BKRUDnkwx3R11lWLVY9RRTCxfnJVH8nDMCTmpeTB2Rr67aJsf9uwyDOVOShaQDxGExxHD09FjthL3FdeRC6fvDfyqOOjWKI_cfdk8UpUvszZ-_jCoMUYY4YMbxsgsa9d-u2ms5es32b_jW2o5TPO0tswm3rykKW9uLuJgJ9r8b68sVozUmMxFIJOd6JlCLMa2UX1ZnmrqfeRcSQfDG3jn4Dmaf1ZAmoUIU95M0BDqcg3_3mfRaFgm1J3Jzs6ztwXMEjw1HCEH2fSpKoAIEB1QeK5X0DWMwQkyb8KrYe3jmxm0OuBaXOF7Pkmq5TFwqr2ZyuhEX53ftAlxYhkYiFPBS-xTLMb5YMwEIZuVRzcjKu3txgyxa8whCZIEl-F_8YGaMtyKnrFiC2sSLXqkM8O2FOxQKAYCYS9UAWnh13hNtId8_s5elcWMLFJ8N1HyuC_6doRms8Wu7Pn0xaFAMWF855aTTLr7cqHykqyo0oTdNe_fAz5X9UsSXMLOSFQun2FKnv1bgyT87grszFjubRWXjzgYHNZ6VW-Q8gnMR4YpaYZQN7nTYUjlJa6lCTnnRk0_BT9TLE54eQaiQKCUclU0zQZDGN3K7zpG-hWpdeM2djzQb9ggzqf3LGYmT2gGxwpN8OplZSjV3zfEVavoJC1t6Vtud6jJJVEnTYP9GcKqVJfxsD1YzLRzJ2dE-Sr0IqpPG3JbDJ2_iqt7cFcWO7MlwdiljAPuMlRMrpCDzc_iV-lebdG9roGIzJ-KhkGBHHGxS14435qN1GnIBxyT78czWB3IfziGXIeWYEMkDOZCzJx9iMatU2q95iVtar4Cknec2SvOug4HGf11pQC2KBrYVMyKVP2ElTuDHN6fT1AMjMaH1c4q87klYH7GjBIr47M34ONACqAL1Mv5SbOQ55GTEzFU5cNs4KgRxDUpd_UULhaAYkRqeudpmyD9RiI1BnOApKVlNAsuEtk9G8C59vesTIniuhs7Dg0CdY2wBCGmIxMMfpx6WjFnjT3BqWrmhwoeU7SurJ-2HELCDpGv7YPkjNUQ4KLqlJrp60Ul3Au1EyLY1R5hwnGCh2sjsG0SH4Gl7sY1LBmR-RrCW4fTSCwC4YyDyPQaFz_zYCzyogWx181uUr8l4X4Fkk12I7NrmlGeaRVhIAVO1kZRkkVT0jyX8zN3oQvw6VvmCLNa10PBkOAn5UD7T1puCMu0aCWlpCGvQbViEkIOj1nv76XBftE8023k2ERCLgQe6VuPkNI_h6_vJWDHseMUvx8fJhLZl8lNPBGv-QoGU3clfuiScL0SE8NiQSclbT0Wa3fYB5LPpDzuO-8nfXuMjmIt5iTpzlI9YWu72jQdVP4LTUxt5DxoZU0cwJfuJbFDB-XBKOyMiQgpOPF7wPVzqOHVn_4Nt4d9UBNeid0UbBXNjQ-HmOnPdwa2LAmGnGfG93I52E9um5TkMt9a1kbmIdkXN6HdflxHJnwaQKmxIbPDx4mqoCCTHWYv8FTNuNg4p0dmItEJcLppClRepI-z959yvzwI0eBETiPi4i7T9-wln-x9el5-KGMTSGLcbBuKZNQ9EnBZIQIQcyQlssUteOP7emMVQnl8OToXaT-g14scU7cZGuh-5qugU6STSTdSVUAreYtQF7_sxZsGiOanyJl82uaVt2Kw6eIjapWUMjSyNwM8uPZMr7tTG5ZD9iMiXGjcOX579DK7qMeNxCcZF2tDjNxwuB244dX3w3DNDdNihMlC92nMGiLdO9H5f6hT81UKAEqfd1QwGkAIzHTU3adlcXPF-RZ3fJ0jgPTEqC61zF8VPzemRLt60pmpVQ2PmZ0ewMFfLFBflpRKTG28cfQB1E9dYf_qVZtn_bOR0SwvghkgjPvCgosvjQs5F7CKWNx91HpS9BoBjP1V_Ehb6UItK0T8dQ7HlaTb8pRsHaHsMGIg_1stp3hmakWHOd8Nxm6EzehBvc4wY2yRTJW7zYxJQHai1qcCUTtXfzMyzfW7O0yf2DqzmFXj15B3J_NyGlMBU93vQxvBwxNu147IgdmTKl1QmQrPZtG9BOhmqW3UAOojcZ1CZH4vDOSQ_8oUxil6f8tNBm4YL83eiyQhe-36Ohy4jzz8zTwv9qTiwnjbDntp-FY-oh6Rp_95HLqM2n9WtwvVcrYQnn6cV-0DX1mGCp0tJRVgjRA59MKL197Yr9TC6oRmkMdWIm30YQvX0_JDXQSecz7ysYOUiP5vNeXeRTcGhhmVc8cURpL9_Lp5FyLw0S49Y_7bcNXiyUC8r4bkfgtGBPDIL--2y_JIQHe7GJuQPK_Qpwfw3kAUfdNSMdkyO_taQF670bfnt2ARzUyftMSTW4xWMOzKDQVqzSMyFOQyelKz-KJz53zjm6U_PSL7pW9sZFJe93pIaRM_-w-_qzd0x6aTKIQk3QorEDHw6Rb4c4HLSlmf0Grxtpd18WqUBn6XZzfFMNdS--cxbKHYn58SCC4AvmPUO2MeCA_i9H0y1ePo3QtlohBvMRkbJmAe2EfheK0NwTkgRoupHl8EkEwN3QtrwfPxDsMyMYfxt-qjsTDhXU6RaoTj; osano_flo_drawer=1; osano_flo_shown=20221221; ajs_anonymous_id=eb5b12d8-df45-45b7-b3eb-1d12b6ca91a3; _ga=GA1.2.1070843666.1769705735; _gid=GA1.2.594604862.1769705735; _cb=vHNWBeBgIDC-I4Kh; _cb_svref=https%3A%2F%2Fwww.bing.com%2F; __qca=P1-e74b8760-09c9-4b57-b380-014333900940; _chartbeat2=.1769705735453.1769705738347.1.B_ElHsCueY3RDdsvglGIXDOBAdiaJ.2; _chartbeat5=1195|0|%2F|https%3A%2F%2Fwww.milesplit.com%2F%23account|BNLjrgCsqNxGDvPWTx_z2OoBoVNMP||c|BdOk6tCGdeOhWe8i2C9xIjDCGXjEi|milesplit.com||; jwt_token=eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjE3ODAwNzM3NDQsInVzZXJfaWQiOjE4ODYxODE1LCJzdWJFeHAiOjE3OTA3MTM1NDAsImlzRnJlZSI6ZmFsc2UsImlzVW5pdmVyc2FsIjp0cnVlLCJzdWJzY3JpcHRpb25fc3RhdHVzIjoiQWN0aXZlIiwiaWQiOjE4ODYxODE1LCJyb2xlcyI6WyJST0xFX1VTRVIiXSwiZW50aXRsZW1lbnRzIjpbInJhbmtpbmdzIiwicmFjZV92aWRlb3NfcGhvdG9zIiwiYXRobGV0ZV9wcm9maWxlc19wcnMiLCJsaXZlX2V2ZW50c19taWxlc3BsaXQiXSwic2l0ZXMiOlsxM10sInVzZXJuYW1lIjoiZmwxLTU4YzdmYjdjLTJmNWItNDgwNi05YWJjLTI1MjFhMzIyNjUxMyIsImVtYWlsIjoianRuNDczMTZAZ21haWwuY29tIiwiY2FyZF9hZGRyZXNzX3ppcCI6bnVsbCwiaWF0IjoxNzY5NzA1NzQ0LCJpc1ByZW1pdW1TdWJzY3JpYmVyIjp0cnVlLCJwcm9maWxlX3BpY3R1cmUiOiJodHRwczovL3Jlcy5jbG91ZGluYXJ5LmNvbS9kaXpuaWZvbG4vaW1hZ2UvdXBsb2FkL3dfMTUwLGhfMTUwL250cDZxc3p0cWlpbzhkeWJkbHk2LnBuZyIsImFuYWx5dGljc19kYXRhIjp7ImFjY291bnRfdHlwZSI6IlByZW1pdW0iLCJzaXRlX2lkIjoxNSwiY2FtcGFpZ24iOm51bGwsImNyZWF0ZWRfYXQiOiIyMDIzLTA5LTI2VDE2OjQxOjExLjAwMDAwMCswMDAwIiwiZW1haWwiOiJqdG40NzMxNkBnbWFpbC5jb20iLCJmYWNlYm9va19pZCI6bnVsbCwiZmlyc3RfbmFtZSI6bnVsbCwibGFzdF9uYW1lIjpudWxsLCJuYW1lIjpudWxsLCJwbGFuX3R5cGUiOiJZZWFybHkiLCJzdWJzY3JpcHRpb25fZW5kX2RhdGUiOiIyMDI2LTA5LTI5VDIwOjI1OjQwLjAwMDAwMCswMDAwIiwic3Vic2NyaXB0aW9uX3N0YXR1cyI6IkFjdGl2ZSIsInVzZXJuYW1lIjoiZmwxLTU4YzdmYjdjLTJmNWItNDgwNi05YWJjLTI1MjFhMzIyNjUxMyIsInVuaXZlcnNhbCI6dHJ1ZSwic3Vic2NyaWJlcl9wb3J0YWxfaWQiOiIxNSJ9LCJleHBlcmltZW50cyI6WyJmbG9fMTIzX2V4YW1wbGVfdGVzdC0xIl0sImxpdmVyYW1wX2VudmVsb3BlIjoiQW9tOFBoSU81YVpyWG03eGk3UTRiczBpeGFGYVNhV0RmTE5CMlZlZm5vXzBOV2lXdzFZQ2RfNWo1dlpuSXdrV1ppN1hibzZweDlVNWxTQmV0aGxDVGZEMmhzTWlJSkZtS1VtSkdUbk5qQTQzWTZIcThVWk9iYnd3VVMwZE1MYkpIR1A5bnMxdEpvdGVaSnZRVjlnbnBHUFdSdmxNYjJxYlc2a2dHM0JvdWwwQndPZkh1WExpNW9LN0ppaUlaWUQyZ283M3JGYUNhbFJrU3dCQ3pwQncwczVRaVdZWTVhaWs2ZGlpa0V6bG9QS0E4QnFsTWZWYnBPVlNYQjl2NHk5US0yaExyYkFITHB5SU10ZzZtNzVlcmJRUVRJM2o3U0VETGNCYUlVQ1FwTXI4MmJMaTdTMjhkSnloUW5uQ3FJUVBDdnRzMFl2ekNzUnNUdXVJLUlPaHNhXzd5SDRaQ0xNN2JqU2V0NEFkM0JBRm1Td2xxNTNKLWhZR09mWlluYmpmTkNUaDhKXzgxMUw5a1JYMFRIOW5uRGs0ZUFNMENRTXphMWpvcHBOXy1iTVp1dUhfbEhwdW0yeWxoTGZvS3FET2dWTDB2eldzRDctMjVzMC1aQTlheW1TZzYtazY2RzRlckRNQW1qT3Y1Uk5aVjN6LWxZb3ZIV0RnbElDNTlDLVI2LTdLZWdnNkU1QzhkakVqR21kNzZPQ0t3Mk01VXVZMGNCVU1XS2w4QS01U0xOVHZsb3Z3UXVyeTVwOWIyNWxEaF8zWG9ab2oyVWRYTVpTWGhPS3hhZ05ZZUV2MnJ4MG40bmVZcGFCdVJETHdOc2Z5dDl4X25ydDQySWNDbDJXMlZnRDJMTXRsQkdKT014VDU2aGZ1a25vVFA5MzB0WmJieEFzTE43Tm9STUVMSlk2MzhQYXFxUGVkNHVmNm1TZGtmajNfRThtNHEyVGZrLVNCYUZELXJ3RG45ZnFKZVlURzFubW5KZGxHWTFLZDNvVzRPYUtWc3VNMFdzNDF5VlAwdkVZc1ctZm1vUWJoMmpCcDBWYWJMak10MXYwZlZkdXh3VFZoenoxdHBEV2xpRF9pVE9LYmtZQnBMQm9WeWN1UVJPU3U1eGJRejRoNXJvVll3dGxxUnFmTEk4bWJaZ1NmSzNBNE5aNl8iLCJpbXBlcnNvbmF0ZWRfYnkiOm51bGx9.MJwmVZxt-w1LtP_4Fw6YX2znSPsf-W6ZKkT61YN7GR1ispPvvfAnRZRKF3Rof496Lrv3NKEMTtXgOMFnI5re7yJq2A9LeFKig4XAQV8J70d883FYQSxNvZY1Vt7rRoaqsyqpeZXCHA6MRqFf-VA_DEiu5E6BTAYA1b-qkFRjdfQwAa8AI8xWw-wURi-IqwoETmnNMf9q7JEvk3E8pe8lN2Lq1WhkppoJ6hO1cDlBGleZy99hP6QPycIceKzfhlwd7-_zuj8fhVX9MpXVxrY2QlVSvhztNRO6OKCaRPOhbw54fTHwnhSDrAyvUrbMAX24vhBZZGvYN84DKQObVbfIYz58U3NDfHEjR7sO8R2nSOIiI2ArgYVM3XSmZxkM2EQyoyJdx3EMHUuDBSuG9QhzVIqvIIP_bGGU6m9JhVMvz7VuQ5eAAQinWH-xKcXGkJzEWq2Rk4Yj566ahjDywovMi7yX_VNR6_Wmqttc56R79tlvfVVlaG26qif4PE4DqFFwOxbxovER3Obf4DMQhpgdvQ3dJQ6W0F8i8ZWI_S2hJbl-DcbXm7TTwrSEE4EY9jFrreaZZ95LMx7NHgq6YNwlUpIQC0y4unbnmqKsbpt9VqSVHiEjnUNguYdGqw7xDBvW3zQP65J8bshs6gHnzetr2uiASwpTAOwjF-rZjpsB1xE; jwt_refresh_token=1363b848327abd4647fbf4e46054a5c87d24b2105ddedfe4c963011e09275827ff0a60742b50d95d96b5dda751e63e1fee15ad27589132d1adbc0ca1cbbb02b0370eca1034a70c13512c10f978a6d91fd717220d811d3ca603db; sso_token=a715faf311faa74f5799b7ff0972d929; identity=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjI2MTUyNDkiLCJ1c2VyTmFtZSI6ImZsMS01OGM3ZmI3Yy0yZjViLTQ4MDYtOWFiYy0yNTIxYTMyMjY1MTMiLCJlbWFpbCI6Imp0bjQ3MzE2QGdtYWlsLmNvbSIsInBlcm1pc3Npb24iOiIxIiwic3Vic2NyaXB0aW9uRXhwaXJlIjoiMTc5MDcxMzU0MCIsInNzb1Rva2VuIjoiYTcxNWZhZjMxMWZhYTc0ZjU3OTliN2ZmMDk3MmQ5MjkifQ.T4dK3RPEE4iURgwc_40AlKzwIksdpwaPESyl4OYxas8; _chartbeat4=t=CApHp5BMQrLflGa3UBUuzfIBL87XO&E=5&x=0&c=0.13&y=1144&w=860'


def scrape(e):
    df1 = pd.DataFrame({'Milesplit URL':[''],'Name':[''],'School':[''],'Class':[''], 'Event':[''],'Date':[''], 'Result':[''], 'State':[''],
                       'Meet':['']})
    #Scrape Data from rankings
    page = 0
    event = event_dic[e]
    for grade in grades:
        for page in range(1, 21):
            random_number = random.randint(3, 10)
            time.sleep(random_number)
            headers = {'User-Agent': random.choice(header_list), 'cookie':cks}
            proxy = random.choice(proxies)
            url = 'https://www.milesplit.com/rankings/events/high-school-boys/indoor-track-and-field/'+str(e)+'?year=2026&accuracy=fat&grade='+str(grade)+'&ageGroup=&league=0&meet=0&team=0&venue=0&conversion=n&page=' + str(page)
            r = s.get(url,headers=headers,proxies = {'http':proxy, 'https':proxy}) 
            soup = BeautifulSoup(r.content, 'html.parser')
            cards = soup.find_all('tr')
            for card in cards[1:]:
                player_class = None
                state = None
                wind = None
                wind_error = False
                school = None
                result = None
                meet = None
                result = card.find('td', class_='time').text.strip()
                temp = card.find('td', class_='name')
                name = temp.find('div', class_='athlete').text.strip()
                player_url = temp.find('div', class_='athlete').find('a').get('href')
                state = temp.find('div', class_='team').find('span', class_='state').text
                school = temp.find('div', class_='team').find('a').text.strip()
                player_class = card.find('td', class_='year').text.strip()
                temp2 = card.find('td', class_='meet')
                meet = temp2.find('div', class_='meet').find('a').text.strip()
                day = temp2.find('div', class_='date').text.strip()
                try:
                    month = day.split(" ")[0]
                    digit_day = day.split(" ")[1].split(",")[0]
                    day_year = day.split(", ")[1].split(" ")[0]
                    if month == 'Apr':
                        month_num = 4
                    elif month == 'Mar':
                        month_num = 3
                    elif month == 'May':
                        month_num = 5
                    elif month == 'Feb':
                        month_num = 2
                    elif month == 'Jan':
                        month_num = 1
                    elif month == 'Dec':
                        month_num = 12
                    elif month == 'Jun':
                        month_num = 6
                    day = f"{month_num}/{digit_day}/{day_year}"
                except:
                    pass
                if event == "Discus" or event == "Shot Put" or event == "Long Jump" or event == 'Triple Jump' or event == "High Jump" or event == 'Pole Vault' or event == 'Javelin':
                    inches = int(float(result.split('-')[1]))
                    if inches < 10:
                        inches = f"0{inches}"
                    else:
                        inches = str(inches)
                    result = result.split('-')[0] + inches
                    result = float(result)
                else:
                    if event != '800':
                        try:
                            result = float(result)
                        except:
                            pass
                if event == '400M' or event == '300M' or event == '300IH' or event == '400H':
                    try:
                        hour = float(result.split(":")[0]) * 60
                        second = float(result.split(":")[1])
                        result = hour + second
                    except:
                        pass
                if event == 'High Jump':
                    if result < 500:
                        continue
                if event == 'Long Jump':
                    if result < 1500:
                        continue
                try:
                    wind = float(wind)
                    if wind >= 3:
                        wind_error = True
                    meet = f"{meet} ({wind}w)"
                except:
                    pass
                new_row = {'Milesplit URL':player_url,'Name':name,'School':school,'Class':player_class,'Event':event,'Date':day, 'Result':result, 'State':state,
                                   'Meet':meet}
                df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
                
    return(df1)

events = ['55m', '60m','55H','60H','200m', '300m', '400m', 'S', 'HJ', 'LJ', 'TJ', 'PV']

events  = ['300m', '400m', 'S', 'HJ', 'LJ', 'TJ', 'PV']

with requests.session() as s:
    #s.post(login, data=payload)
    for event1 in events:
        df1 = scrape(event1)
        frames= [df,df1]
        df = pd.concat(frames)


df = df.drop_duplicates()
df = df.reset_index(drop=True)
index_names = df[df['URL'] == ''].index

df.drop(index_names, inplace=True)
df = df.reset_index(drop=True)

#df.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\TFTEST1.csv',index=False)

for i in range(0,len(df)):
    date_ = df.at[i, 'Date']
    try:
        month = date_.split("/")[0]
        day = date_.split("/")[1]
        if len(day) == 1:
            day = f"0{day}"
        date_val = int(f"{month}{day}")
        if date_val <= last_day_val:
            df.drop(i, inplace=True)
            continue
    except:
        pass
df = df.reset_index(drop=True)

#df['Slug'] = None

index_names = database[database['Milesplit URL'] != database['Milesplit URL']].index
database.drop(index_names, inplace = True)
database = database.reset_index(drop=True)

#df['Slug'] = df['URL'].map(database.set_index('Milesplit URL')['Slug'])
df = pd.merge(df, database[['Milesplit URL', 'Slug']], on='Milesplit URL',how='left')

template = pd.read_csv(r"C:\Users\jtsve\OneDrive\Desktop\Template Files\ImportTemplate.csv")

for i in range(len(df)):
    template.at[i, 'Milesplit URL'] = df.at[i, 'Milesplit URL']
    try:
       template.at[i, 'First Name'] = df.at[i, 'Name'].split(" ")[0]
       words = df.at[i, 'Name'].split()
       last_name = " ".join(words[1:])
       template.at[i, 'Last Name'] = last_name
    except:
       template.at[i, 'Last Name'] = df.at[i, 'Name']
    #template.at[i,'TF Year'] = 2025
    template.at[i,'TF Meet'] = df.at[i, 'Meet'] + " TF Meet"
    event = df.at[i, 'Event']
    template.at[i, event] = df.at[i, 'Result']
    template.at[i, 'HS Name'] = df.at[i, 'School']
    template.at[i, 'HS State'] = df.at[i, 'State']
    template.at[i, 'HS Class'] = df.at[i, 'Class']
    template.at[i, 'Track'] = 1
    template.at[i, 'TF Date'] = df.at[i, 'Date']
    template.at[i, 'Slug'] = df.at[i, 'Slug']

events_tf = list(event_dic.values())
for event in events_tf:
    temp_df = template.dropna(subset=[event])
    temp_df = temp_df.dropna(subset=['Slug'])
    temp_df['HS Class'] = None
    temp_df['HS State'] = None
    temp_df['HS Name'] = None
    temp_df['Last Name'] = None
    temp_df['First Name'] = None
    temp_df['Milesplit URL'] = None
    temp_df.to_excel(r"C:\Users\jtsve\OneDrive\Documents\m"+event+"Updates"+".xlsx",index=False)

today =date.today()
today = today.strftime("%b-%d-%Y")

#driver.quit()

template.to_csv(r'C:\Users\jtsve\OneDrive\Desktop\Excel Exports\'' + str(today) + 'TFIndoorRankings.csv', index=False)



