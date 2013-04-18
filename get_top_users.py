import os
import sys
import json
import curl
import pycurl
import urllib
import pprint
import marshal
import cStringIO

from subprocess import Popen, PIPE

pp = pprint.PrettyPrinter(depth = 6)

class processUserData():
    def __init__(self, directory, user_filename="user", project_filename="project", users_per_file=5000):
        self.user_filename_base = user_filename
        self.project_filename_base = project_filename
        self.current_user_filename = user_filename + "0"
        self.current_project_filename = project_filename + "0"
        self.directory = directory
        self.users_per_file = users_per_file
        self.count_users = 0
        self.count_project = 0
        self.user_data = []
        self.project_data = []
        

    def dump_data(self, data, filename):
        filename = os.path.join(self.directory , filename)
        file_handle = open(filename, "wb")
        marshal.dump(data, file_handle)
        file_handle.close()
        
    def parse_repo_data(self, data):
        self.count_project += len(data)
        self.project_data.extend(data)

        if self.count_project % self.users_per_file == 0:
            self.dump_data(self.project_data, self.current_project_filename)
            self.current_project_filename = self.project_filename_base + str(self.count_project / self.users_per_file)
        
    """
    Parses user data and dump the data to a file
    """
    def parse_user_data(self, data):
        users = []
        decoded_data = json.loads(data)["users"]
        self.user_data.extend(decoded_data)
        follower_count = 0
        for user in decoded_data:
            users.append(user["login"])
            self.count_users += 1
            follower_count = user["followers_count"]
        
        if self.count_users % self.users_per_file == 0:
            self.dump_data(self.user_data, self.current_user_filename)
            self.current_user_filename = self.user_filename_base + str(self.count_users / self.users_per_file)
        return users, follower_count
        


class createRequest():
    def __init__(self):
        self.user_id = self.git_config_get('user.name')
        self.pwd = self.git_config_get('user.password')
        self.start_page = 1
        self.parser = processUserData("/home/garima/IR/project/gitbook/data")

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

        if http_code != 200 and http_code != 201:
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
            repos = json.loads(repos)
            new_repos = []
            for repo in repos:
                contributors_url = str(repo['contributors_url'])
                contributors = self.auth_curl_cmd(contributors_url)
                repo['contributors'] = json.loads(contributors)
                languages_url = str(repo['languages_url'])
                languages = self.auth_curl_cmd(contributors_url)
                repo['languages'] = json.loads(languages)
                commit_url = "https://api.github.com/repos/" + str(user) + "/" + str(repo['name']) + "/commits"
                commits = self.auth_curl_cmd(commit_url)
                commits = self.get_commits(commits)
                repo['commits'] = commits
                new_repos.append(repo)
            repos.extend(new_repos)
        self.parser.parse_repo_data(repos)

    def get_top_users_with_followers(self, number_users, follower_count_cap):
        MAX_COUNT = 1000
        user_count = 1
        count = 1
        if self.token == None:
            print "Take authentication token first"
            return
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
        print self.users

if __name__ == '__main__':
    obj = createRequest()
    obj.get_auth_token()
    obj.get_top_users_with_followers(6000, 20000)
