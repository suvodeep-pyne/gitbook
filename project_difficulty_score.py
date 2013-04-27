"""
calculates the project's difficulty score based on the number of lines of code 
"""
import pprint 
import time
import requests
from read_data import *
import json
projectDataObject = getData('./github_data')
projectList = projectDataObject.parseProjectData()
for project in projectList:
  pp = pprint.PrettyPrinter(indent=4)
  URL = project[u'languages_url']
  projectFullName = project[u'full_name']
  r = requests.get(URL)
  
  if r.status_code == 503 or r.status_code == 502 or r.status_code == 500 or r.status_code == 406 or r.status_code == 405 or r.status_code == 404 or r.status_code == 403 or r.status_code == 402 or r.status_code == 401 or r.status_code == 400:
        print "status_code : " ,r.status_code, " ERROR!!"
  else: 
    language_loc=json.loads(r.text)
    for lang in language_loc:
      print lang, " has " , language_loc[lang], "lines of code"


