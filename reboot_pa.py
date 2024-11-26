#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    This script reboots a list of Palo Alto firewalls (tested on PA-220) contained in the file "pa_est.csv"
    The .csv is contains a list of IP as in : 
    172.23.0.57
    172.85.65.254
    172.99.17.252
    172.88.154.252


    Author: h4n0sh1
    Created: 03/04/2024
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

error_pa = open("list_error.csv", "w")
error_pa.close()

with open("pa_est.csv", newline='') as list_pa, open("list_error.csv", "a") as error_pa:
	buffer = csv.reader(list_pa, delimiter=' ')
	for row in buffer: 
		try:
			url = "https://" + row[0] + "/api/?type=keygen"
			api_key = get_api_key(url,body)
			reboot_url = "https://" + row[0] + "/api?type=op&cmd=<request><restart><system></system></restart></request>&key=" + api_key
			print(f"Rebooting PA - {row[0]}")
			fire_and_forget(reboot_url)
		except:
			print(f"Error for PA - {row[0]}")
			error_pa.write(row[0])

		
		

