"""
Collects all the Stack overflow tags and forms a vocabulary
"""
import os
import sys
import json
import curl
import pycurl
import time
import urllib
import pprint
import cStringIO
import requests
fw = open('tags.txt','w')
prevTime = time.time()
numReq = 0
for num in range(1,1000):
  numReq +=1
  now = time.time()
  if numReq >= 29 and  now - prevTime >= 0.9:
    print "exceeding limit... sleeping- prev: " , prevTime , " curr: ", now
    time.sleep(1)
    prevTime = time.time()
    numReq = 0

  try:
    URL = 'http://api.stackoverflow.com/1.1/tags'
    param = {'page': str(num), 'pagesize':'100'}
    r = requests.get(URL, params=param)
 
    if r.status_code == 503 or r.status_code == 502 or r.status_code == 500 or r.status_code == 406 or r.status_code == 405 or r.status_code == 404 or r.status_code == 403 or r.status_code == 402 or r.status_code == 401 or r.status_code == 400:
      print "status_code : " ,r.status_code, " sleepin..."
      time.sleep(2)
    else: 
      json_data=json.loads(r.text)
      tags = json_data['tags']
      for tag in tags:
        fw.write(tag['name'])
        fw.write(' ')

  except:
    print "connection error: sleeping for 1 sec"
    time.sleep(1)

fw.close()
