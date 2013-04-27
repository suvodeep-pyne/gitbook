"""
Author - Garima Agarwal
"""
import os
import sys
import json
import curl
import pycurl
import time
import urllib
import pprint
import marshal
import cStringIO

from subprocess import Popen, PIPE

pp = pprint.PrettyPrinter(depth = 6)

class ProcessUserData():
    def __init__(self, directory, user_filename="user", project_filename="project", users_per_file=1000):
        self.user_filename_base = user_filename
        self.project_filename_base = project_filename
        self.current_user_filename = user_filename + "0"
        self.current_project_filename = project_filename + "0"
        self.directory = directory
        self.users_per_file = users_per_file
        self.count_users = 0
        self.count_project = 0
        self.user_file_count = 1
        self.project_file_count = 1
        self.user_data = []
        self.project_data = []


    def read_info_file(self):
        filename = os.path.join(self.directory, "info")
        try:
            file_h = open(filename)
            data = file_h.read()
            fields = data.split(" ")
            self.user_file_count = fields[0]
            self.project_file_count = fields[1]
            followers = fields[2]
            print self.user_file_count, self.project_file_count, followers
            return followers
        except IOError:
            return None

    def dump_all_data(self, followers):
        self.dump_data(self.user_data, self.current_user_filename)
        self.dump_data(self.project_data, self.current_project_filename)
        info_file = os.path.join(self.directory, "info" )
        fh = open(info_file, "w")
        fh.write(("" + str(self.user_file_count+1) + " " + str(self.project_file_count+1) + " " + str(followers)))
        fh.close()


    def dump_data(self, data, filename):
        filename = os.path.join(self.directory , filename)
        file_handle = open(filename, "wb")
        marshal.dump(data, file_handle)
        file_handle.close()

    def parse_repo_data(self, data):
        print "Parsing repo data"
        self.count_project += len(data)
        self.project_data.extend(data)

        if self.count_project > self.users_per_file:
            print "Dumping project data"
            self.dump_data(self.project_data, self.current_project_filename)
            self.project_data = []
            self.current_project_filename = self.project_filename_base + str(self.project_file_count)
            self.project_file_count += 1
            self.count_project = 0

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

        if self.count_users > self.users_per_file:
            self.dump_data(self.user_data, self.current_user_filename)
            self.user_data = []
            self.count_users = 0
            self.current_user_filename = self.user_filename_base + str(self.user_file_count)
            self.user_file_count += 1
        return users, follower_count



class CreateRequest():
    def __init__(self):
        self.user_id = self.git_config_get('user.name')
        self.pwd = self.git_config_get('user.password')
        self.start_page = 1
        self.parser = ProcessUserData("user")
        self.user_follower_map = {}

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

    def get_followers(self, users):
        for user in users:
            followers_url = "https://api.github.com/users/" + str(user) + "/followers"
            params = ["Authorization: token " + str(self.token)]
            followers = self.curl_cmd(followers_url, params)
            if followers == None:
                continue
            followers = json.loads(followers)
            followers_list = []
            for follower in followers:
                followers_list.append(follower["login"])
            self.user_follower_map[user] = followers_list
    
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

    def get_top_users_with_followers(self, number_users, follower_count_cap, get_followers = False):
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
                if get_followers:
                    self.get_followers(users)
                    self.parser.dump_data(self.user_follower_map, "user_follower_map")
                else:
                    self.get_repos(users)
                if count >= 1000:
                    count = 0
                    follower_count_cap = min_follower_count
                    self.start_page = 1
        except:
            self.parser.dump_all_data(follower_count_cap)
            self.parser.dump_data(self.user_follower_map, "user_follower_map")

if __name__ == '__main__':
    obj = CreateRequest()
    obj.get_auth_token()
    if len(sys.argv) > 1:
        print "Getting followers"
        obj.get_top_users_with_followers(60000, 20000, True)
    else:
        obj.get_top_users_with_followers(6000, 20000)
