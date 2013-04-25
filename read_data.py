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

class getData():
    def __init__(self, directory):
        self.directory = directory
        self.project_data = []
        self.user_data = []
        self.user_dict = {}
        self.user_followers = {}


    def parseProjectData(self):
        for files in os.listdir(self.directory):
            if not fnmatch.fnmatch(files, "project[0-9]*"):
                continue
            filename = os.path.join(self.directory, files)
            fh = open(filename,"rb")
            data = marshal.load(fh)
            for project in data:
                readme_dict = (project["readme"])
                if readme_dict != []:
                    readme = readme_dict["content"]
                    project["readme"] = base64.b64decode(readme) 
                self.project_data.append(project)
        return self.project_data
        
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
    obj = getData(dirname)
    project = obj.parseProjectData()
