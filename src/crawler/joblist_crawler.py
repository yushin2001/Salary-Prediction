import pandas as pd
import re, time, random, requests
from bs4 import BeautifulSoup
import json
import os

area_url = 'https://static.104.com.tw/category-tool/json/Area.json'
resp = requests.get(area_url)
df1 = []
for i in resp.json()[0]['n']:
    ndf = pd.DataFrame(i['n'])
    ndf['city'] = i['des']
    df1.append(ndf)
df1 = pd.concat(df1, ignore_index=True)
df1 = df1.loc[:,['city','des','no']]
df1 = df1.sort_values('no')

catg_url= 'https://static.104.com.tw/category-tool/json/JobCat.json'
resp = requests.get(catg_url)
df2 = []
for i in resp.json():
    for j in i['n']:
        ndf = pd.DataFrame(j['n'])
        ndf['des1'] = i['des']# 職務大分類
        ndf['des2'] = j['des']# 職務小分類
        df2.append(ndf)
df2 = pd.concat(df2, ignore_index=True)
df2 = df2.loc[:,['des1', 'des2', 'des', 'no']]
df2 = df2.sort_values('no')


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
job_list = []
areacount = 1

for areades, areacode in zip(df1['des'],df1['no']):
    print(f'{areacount} | {areades} | {areacode}')

    for jobdes1, jobdes2, jobdes, jobcode in zip(df2['des1'], df2['des2'], df2['des'], df2['no']):
        page = 1
        # print(areades, ' | ', jobdes1, ' - ', jobdes2, ' - ' ,jobdes)
        # print(areacode, '|', jobcode, '|', page, '|') 

        while page < 150:
            try:
                # 查詢的關鍵字
                my_params = {'ro':'1', # 限定全職的工作為1，不限定則輸入0
                            'jobexp':'1', #經歷要求：1年以下
                            'isnew':'30', # 最近一個月有更新過的職缺
                            'jobcat':str(jobcode),
                            'area':str(areacode),
                            'page':str(page),
                            'mode':'l'} # 清單的瀏覽模式

                response = requests.get('https://www.104.com.tw/jobs/search/?', my_params, headers = headers)
                soup = BeautifulSoup(response.text, features="html.parser")
                soup2 = soup.findAll('article',{'class':'js-job-item'})
                List = [r for r in soup2]
                
                for i in range(len(List)):
                    s1 = str(List[i])
                    s2 = s1[s1.find('data-job-no'):(s1.find('data-job-ro')-1)]
                    s3 = s2[13:-1]
                    job_no = s3

                    sjob = List[i].find_all('a')[0]['href'][21:]
                    qs_index = sjob.find('?')
                    job_id = List[i].find_all('a')[0]['href'][21: (21 + qs_index)]

                    scust = List[i].find_all('a')[1]['href'][25:]
                    qs_index = scust.find('?')
                    cust_id = List[i].find_all('a')[1]['href'][25: (25 + qs_index)]

                    d = {'job_id': job_id, 'job_no': job_no, 'cust_id': cust_id}
                    job_list.append(d)


                page += 1
                
                if len(soup2) < 30:
                    break

            except:
                print(f'Fail: {areades}({areacode}), {jobdes}({jobcode}), page {page}')
    
    print(f'len(job_list): {len(job_list)}')
    areacount += 1
    
print('Finish! ' + str(len(job_list)) + ' jobs in job_list')  

# output the file
with open('./joblist.json', 'w') as outfile:
    json.dump(job_list, outfile, ensure_ascii = False, indent = 4)