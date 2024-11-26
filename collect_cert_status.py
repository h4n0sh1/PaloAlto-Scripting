#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    This script queries a list of Palo Alto firewall IPs from the file "pa_est.csv", for any system log containing the key word "extended".
    It then returns the list of Palo Alto firewalls with their matching log entry in the file "query.csv"
    
    Author: h4n0sh1
    Created: 04/04/2024
    License: GPL
"""

import requests
import xml.etree.ElementTree as ET
import csv
import threading


body = { 
		'user': 'xxxx',
		'password': 'xxxx'
		}

def request_task(url):
    requests.post(url, verify=False)

def fire_and_forget(url):
    threading.Thread(target=request_task, args=(url,)).start()

def get_api_key(url,data):
	r = requests.post(url,data=data, verify=False)
	api_key = ET.fromstring(r.text).find("result").find("key").text
	return api_key

error_pa = open("list_error_collect.csv", "bw")
error_pa.close()

ret_map = {}
with open("pa_est.csv", newline='') as list_pa, open("list_error.csv", "a") as error_pa:
	buffer = csv.reader(list_pa, delimiter=' ')
	for row in buffer: 
		try:
			url = "https://" + row[0] + "/api/?type=keygen"
			api_key = get_api_key(url,body)
			query_url = "https://" + row[0] + "/api?type=log&log-type=system&query=(description contains 'extended')&key=" + api_key
			r = requests.post(query_url, verify=False)
			#print(f"{r.text}")
			job_number = ET.fromstring(r.text).find("result").find("job").text
			job_url = "https://" + row[0] + "/api?type=log&action=get&job-id="+ job_number +"&key=" + api_key
			r = requests.post(job_url, verify=False)
			fw_name = ET.fromstring(r.text).find("result").find("log").find("logs").find("entry").find("device_name").text
			desc = ET.fromstring(r.text).find("result").find("log").find("logs").find("entry").find("opaque").text
			print(f"Rendering xTended query content -> {r.text}")
			ret_map[fw_name] = desc 
		except:
			print(f"Error for PA - {row[0]}")
			error_pa.write(row[0])

with open('query.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in ret_map.items():
       writer.writerow([key, value])

			
