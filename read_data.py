#!/bin/python
"""
    Author - Garima Agarwal
    Date - 04/25/2013
    Description - This file defines class which reconstructs project and user data structures 
                  from data files
"""
"""usage python readData dirname"""
import os
import sys
import base64
import fnmatch
import marshal
import pprint as pp


"""
Class which reads data from all the files in a directory and populates the data structure
"""
class DataRetriever():
    """
    init function, takes the directory name which has the data files
    """
    def __init__(self, directory):
        self.directory = directory
        self.project_data = {}
        self.user_data = []
        self.user_dict = {}
        self.user_followers = {}


    """Builds project data structure"""
    def parseProjectData(self):
        for files in os.listdir(self.directory):
            if not fnmatch.fnmatch(files, "project[0-9]*"):
                continue
            filename = os.path.join(self.directory, files)
            print filename
            fh = open(filename,"rb")
            data = marshal.load(fh)
            for project in data:
                new_project = {}
                new_project['full_name'] = project['full_name']
                new_project['owner']  = project['owner']
                new_project['html_url'] = project['html_url']
                new_project['contributors'] = project['contributors']
                new_project['contributors_url'] = project['contributors_url']
                new_project['languages_url'] = project['languages_url']
                new_project['name'] = project['name']
                readme_dict = (project["readme"])
                if readme_dict != []:
                    readme = readme_dict["content"]
                    new_project["readme"] = base64.b64decode(readme) 
                self.project_data[project[u'full_name']] = new_project
            fh.close()
        return self.project_data
        
    """Builds user data structure"""
    def parseUserData(self): 
        for files in os.listdir(self.directory):
            if not fnmatch.fnmatch(files, "user[0-9]*"):
                continue
            filename = os.path.join(self.directory, files)
            fh = open(filename,"rb")
            users = marshal.load(fh)
            self.user_data.extend(users)
            for user in users:
                self.user_followers[user["username"]] = user["followers"]
            fh.close()

    """Builds the followers data structures"""
    def parseUserFollowers(self):
        self.parseUserData()
        for files in os.listdir(self.directory):
            if not fnmatch.fnmatch(files, "user_followers_map*"):
                continue
            filename = os.path.join(self.directory, files)
            fh = open(filename,"rb")
            users_map = marshal.load(fh)
            self.user_dict = dict(self.user_dict.items() + users_map.items())
        return self.user_dict, self.user_followers        
    
if __name__ == '__main__':
    dirname = sys.argv[1]
    obj = DataRetriever(dirname)
    project = obj.parseProjectData()
    pp.pprint(len(project))
