import pandas as pd
import re, time, random, requests
from bs4 import BeautifulSoup
import json
import os

# open the file with job_id, job_no and cust_id
# with open('./joblist.json') as f:
#     job_list = json.load(f)

# open the raw data
with open('./raw.json') as f:
    job_list = json.load(f)

# open the list of jobs without apply data
with open('./applyFail.json') as f:
    fail = json.load(f)

# User Agent
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

# get each company's data
def get_custData (cid):
    url_cust = f'https://www.104.com.tw/company/ajax/content/{cid}'
    headers_cust = {
        'User-Agent': user_agent,
        'Referer': f'https://www.104.com.tw/company/{cid}'
    }

    res_cust = requests.get(url_cust, headers = headers_cust)
    json_cust = res_cust.json()
    cust_data = json_cust['data']
    cust_dict = {'empNo': cust_data['empNo'], 'capital':cust_data['capital']}

    return cust_dict


# get each job's data
def get_jobData (jid):
    url_job = f'https://www.104.com.tw/job/ajax/content/{jid}'
    headers_job = {
        'User-Agent': user_agent,
        'Referer': f'https://www.104.com.tw/job/{jid}'
    }
    res_job = requests.get(url_job, headers = headers_job)
    json_job = res_job.json()

    return json_job


# data of apply analysis
def get_applyData (jno):
    url_apply = f'https://www.104.com.tw/jb/104i/applyAnalysisToJob/all?job_no={jno}'
    headers_apply = {
        'User-Agent': user_agent
    }
    res_apply = requests.get(url_apply, headers = headers_apply)
    json_apply = res_apply.json()
    
    return json_apply


# List of failure
# jobFail = []
# custFail = []
applyFail = []

print(f'len(job_list) = {len(job_list)}')

for i in fail:
# for i in range(len(job_list)):
#     if i % 1000 == 0:
#         print(f'i = {i}')

    job = job_list[i]
    job_id = job['job_id']
    job_no = job['job_no']
    cust_id = job['cust_id']

    # try:
    #     job_list[i]['custData'] = get_custData(cust_id)
    # except:
    #     time.sleep(1.5)
    #     try:
    #         job_list[i]['custData'] = get_custData(cust_id)
    #     except:
    #         custFail.append(i)
    #         print(f'Fail to get cust data (i = {i})')
    
    # try:
    #     job_list[i]['jobData'] = get_jobData(job_id)
    # except:
    #     time.sleep(1.5)
    #     try:
    #         job_list[i]['jobData'] = get_jobData(job_id)
    #     except:
    #         jobFail.append(i)
    #         print(f'Fail to get job data (i = {i})')
    time.sleep(1)
    try:
        job_list[i]['applyData'] = get_applyData(job_no)
    except:
        time.sleep(2)
        try:
            job_list[i]['applyData'] = get_applyData(job_no)
        except:
            time.sleep(2)
            try:
                job_list[i]['applyData'] = get_applyData(job_no)
            except:
                # applyFail.append(i)
                print(f'i = {i}: Fail to get apply data ({job_no})')

# print(f'len of custFail: {len(custFail)}')
# print(f'len of jobFail: {len(jobFail)}')
# print(f'len of applyFail: {len(applyFail)}')

# output the file
with open('./raw2.json', 'w') as outfile:
    json.dump(job_list, outfile, ensure_ascii = False, indent = 4)

# if len(custFail) > 0:
#     with open('./custFail.json', 'w') as outfile1:
#         json.dump(custFail, outfile1, ensure_ascii = False, indent = 4)

# if len(jobFail) > 0:
#     with open('./jobFail.json', 'w') as outfile2:
#         json.dump(jobFail, outfile2, ensure_ascii = False, indent = 4)

with open('./applyFail2.json', 'w') as outfile3:
    json.dump(applyFail, outfile3, ensure_ascii = False, indent = 4)