"""
Collects all the Lines of code [LOC] and dumps it in file as 

{project ID: {lang: LOC} }

Author : Ashwath Rajendran
"""
import os
import sys
import json
import time
import pprint
import requests
from collections import defaultdict
from read_data import *
import curl
import pycurl
import urllib
import marshal
import cStringIO

pp = pprint.PrettyPrinter(depth = 4)

class getLOC():
  def getAllLOCandDump(self):
    #fw = open('LOC.txt','w')
    obj = createRequest()
    obj.get_auth_token()
    projectLOC = defaultdict()
    prevTime = time.time()
    numReq = 0
    projectDataObject = getData('./github_data')
    projectList = projectDataObject.parseProjectData()
    for project in projectList:
      URL = project[u'languages_url']
      projectFullName = project[u'full_name']
      """
      numReq +=1
      now = time.time()
      if numReq >= 5000 and  now - prevTime >= 3600:
        print "exceeding limit... sleeping- prev: " , prevTime , " curr: ", now
        time.sleep(1)
        prevTime = time.time()
        numReq = 0
      """
      #try:
      r = obj.auth_curl_cmd(str(URL))
      language_loc=json.loads(r)
      projectLOC[projectFullName] = language_loc
      pp.pprint(projectLOC)
      """
      languages = defaultdict()
      for lang in language_loc:
        languages[lang] = language_loc[lang]
      """
      #  fw.write(tag['name'])
      #  fw.write(' ')
      """
      except:
        print "connection error: sleeping for 1 sec"
        time.sleep(1)
     """
   
   
   
   
   
from subprocess import Popen, PIPE
class createRequest():
   def __init__(self):
       self.user_id = self.git_config_get('user.name')
       self.pwd = self.git_config_get('user.password')
       self.start_page = 1
       #self.parser = processUserData("/home/ash/code/IR/gitbook/github_data")

       if self.user_id == None or self.pwd == None:
           print "Error getting username or password"
           return

       self.token = None
       self.users = []

   def git_config_get(self, key):
       pipe = Popen(['git', 'config', '--get', key], stdout=PIPE)
       return pipe.communicate()[0].strip()

   def auth_curl_cmd(self, url):
       params = ["Authorization: token " + str(self.token)]
       return self.curl_cmd(url, params)

   def curl_cmd(self, url, header_params = None, post_params=None):
       while True:
           write_buf = cStringIO.StringIO()
           c = pycurl.Curl()
           c.setopt(pycurl.URL, url)
           c.setopt(pycurl.USERPWD, "%s:%s" %(self.user_id, self.pwd))
           c.setopt(c.WRITEFUNCTION, write_buf.write)

           if header_params != None:
               c.setopt(pycurl.HTTPHEADER, header_params)


           if post_params != None:
               c.setopt(pycurl.POSTFIELDS, post_params)

           c.perform()
           buf = write_buf.getvalue()
           http_code = c.getinfo(pycurl.HTTP_CODE)
           if http_code == 500 or http_code == 501 or http_code == 502 or http_code == 503 or http_code == 504:
               time.sleep(60)
           else:
               break

       if http_code != 200 and http_code != 201:
           print http_code
           print "Error in the curl request. %s" %(buf)
           return None

       write_buf.close()
       return buf

   def get_auth_token(self):
       auth_url = "https://api.github.com/authorizations"
       params = "{\"scopes\":[\"repo\"]}"
       print "Getting auth"
       data = self.curl_cmd(auth_url, None, params)
       print "Got auth"
       if data == None:    return

       self.token = json.loads(data)['token']

   def get_commits(self, data):
       commits = []
       data = json.loads(data)
       for commit in data:
           cm = commit["commit"]["author"]["date"]
           commits.append(cm)
       return commits

   def get_repos(self, users):
       repo_base_url = "https://api.github.com/users/"
       repos = []
       for user in users:
           repo_url = repo_base_url + str(user) + "/repos"
           print "url is ", repo_url
           params = ["Authorization: token " + str(self.token)]
           repos = self.curl_cmd(repo_url, params)
           if repos == None:
               continue
           repos = json.loads(repos)
           new_repos = []
           for repo in repos:
               contributors_url = str(repo['contributors_url'])
               contributors = self.auth_curl_cmd(contributors_url)
               if contributors == None:
                   continue
               repo['contributors'] = json.loads(contributors)
               languages_url = str(repo['languages_url'])
               languages = self.auth_curl_cmd(contributors_url)
               repo['languages'] = json.loads(languages)
               commit_url = "https://api.github.com/repos/" + str(user) + "/" + str(repo['name']) + "/commits"
               commits = self.auth_curl_cmd(commit_url)
               if commits == None:
                   continue

               commits = self.get_commits(commits)
               repo['commits'] = commits

               readme_url = "https://api.github.com/repos/" + str(user) + "/" + str(repo['name']) + "/readme"
               print "readme url is", readme_url
               readme = self.auth_curl_cmd(readme_url)
               if readme != None:
                   repo['readme'] = json.loads(readme)
               else:
                   repo['readme'] = []
               new_repos.append(repo)
           self.parser.parse_repo_data(new_repos)

   def get_top_users_with_followers(self, number_users, follower_count_cap):
       followers_count = self.parser.read_info_file()
       if followers_count != None:
           follower_count_cap = followers_count
       MAX_COUNT = 1000
       user_count = 1
       count = 1
       if self.token == None:
           print "Take authentication token first"
           return
       try:
           while(user_count < number_users):
               user_url = 'https://api.github.com/legacy/user/search/followers:<' + str(follower_count_cap) + '?sort=followers&start_page=' + str(self.start_page)
               self.start_page += 1
               print "Calling api"
               users = self.auth_curl_cmd(user_url)
               users, min_follower_count = self.parser.parse_user_data(users)
               self.users.extend(users)
               count += len(users)
               user_count += len(users)
               self.get_repos(users)
               if count >= 1000:
                   count = 0
                   follower_count_cap = min_follower_count
                   self.start_page = 1
       except:
           self.parser.dump_all_data(follower_count_cap)

if __name__ == '__main__':
    #obj = createRequest()
    #obj.get_auth_token()
    #obj.get_top_users_with_followers(6000, 20000)  
    locObj = getLOC()
    locObj.getAllLOCandDump()
