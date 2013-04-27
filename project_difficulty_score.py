"""
calculates the project's difficulty score based on the number of lines of code 
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
import pickle
import cStringIO

pp = pprint.PrettyPrinter(depth = 4)

class ProjectDifficultyCalculator():
  """
  takes in the {project ID: {lang1: LOC, lang2:LOC} } data structure and assigns a project difficulty score for each language to the project.
  If a project has multiple languages, then a cumulative difficult will be assigned as the overall difficulty of the project

  """
  def readDataAndDump(self):
    pp = pprint.PrettyPrinter(depth = 4)
    allProjects = defaultdict()
    with open('LOC.txt','rb') as f:
      print "loading the dict from pickle file.. please wait.. "
      while 1:
        try:
          allProjects.update(pickle.load(f))
        except EOFError:
          print 'parsing done!'
          break # no more data in the file
    #pp.pprint(projectDataObject)
    print 'there are ',len(allProjects), 'projects in total in the pickle file'

    allProjLang = defaultdict()   #just stores the sum of squares of all LOC for normalising
    difficultyScore = defaultdict() # the final that stores { project: score }  final DS to dump with pickle

    for proj in allProjects:
      languages = allProjects[proj]
      for lang in languages:
        if lang in allProjLang:
          allProjLang += languages[lang]*languages[lang]
        else:
          allProjLang = languages[lang]*languages[lang]
    # substitute the LOC to a normalized LOC
    for proj in allProjects:
      languages = allProjects[proj]
      for lang in languages:
        languages[lang] = float(languages[lang]/float(allProjLang[lang]))
    # scale it all from 0 to 1 --> 1 is the max project's score. divide every lang's score by that max score

        





if __name__ == '__main__':
    #obj = createRequest()
    #obj.get_auth_token()
    #obj.get_top_users_with_followers(6000, 20000)  
    locObj =ProjectDifficultyCalculator()
    locObj.readDataAndDump()

